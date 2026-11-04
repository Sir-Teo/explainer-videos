# Computer Science, Built — Part 9: The Memory Hierarchy

Part 9 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act II, *Making It Fast*. Processors got fast and memory didn't; the
answer is a hierarchy of caches that works because programs have locality. This part builds caches from nothing
(`explainer/cs/pebble/cache.py`: set-associative caches with LRU, tree pseudo-LRU, FIFO and random replacement,
write-back and write-through, a multi-level hierarchy with stride prefetching, memory traces, LRU stack distances,
Belady's optimum and the three Cs, each checked against brute force in `tests/test_cs9_cache.py`), measures the
memory of the computer that made the video, proves a lower bound on the data any matrix multiply must move, and gives
the Job real memory. Every number is computed in `compute.py`; the machine's are measured by small C programs.

* **A second for every cycle.** This machine's latencies at one second per clock cycle: L1 4.4 s, L2 12 s, the next
  level 1.2 minutes, DRAM 6.5 minutes (15 with a TLB miss), an SSD about 3 days, a disk about 5 months. The Job's
  table: 678 KB, 2.8 billion line reads, 88% of them missing a 32 KB cache; and yet the Job slows by 0.05%.
* **1. The memory wall.** Processors +25% then +52% a year, DRAM latency about +7% (Hennessy and Patterson); Wulf and
  McKee (1995); the wall as a ratio: DRAM is 166 cycles from Pebble's 885 MHz core and 525 from this machine's.
* **2. Locality.** Every access of the Job's first chapter as an address-against-time scatter (the table's scans as
  diagonal strokes, the letters scattered); Denning's working set (1968); reuse distance (Mattson et al. 1970); miss
  curves: the chapter's 92 lines against the corpus's 678 KB table, and the cliff where the working set fits.
* **3. A direct-mapped cache.** Tag, index and offset; a toy cache of eight lines and nine accesses, with a conflict;
  the Job's table and letters both start at multiples of the cache size and collide (14,948 misses at 8 KB
  direct-mapped against 92 with two ways).
* **4. Associativity and replacement.** Sets and ways; LRU, tree pseudo-LRU, FIFO, random, Belady (1966); on the first
  chapter in 4 KB, 8 ways: 3.9%, 3.6%, 3.8%, 2.0%, 0.74% — random beats LRU on scans longer than the cache; write-back,
  write-through, write-allocate.
* **5. Three kinds of miss.** Hill's compulsory, capacity and conflict (1987), measured by size and associativity; a
  negative conflict count (set-associative LRU beating fully associative LRU).
* **6. Average memory access time.** AMAT = t_hit + m × t_penalty, nested across levels; with this machine's
  latencies and typical miss rates, about 3.4 ns, though DRAM is 90 times slower than L1.
* **7. This machine's staircase.** Pointer chasing through a random cycle: 1.6 ns to 32 KB, 4.4 ns to 1 MB, 25 ns at
  2 MB, 140 ns from 4 MB, 326 ns at 512 MB (page-table walks); lscpu reports 33 MB of L3 that this virtual machine
  falls off near 4 MB; bandwidth about 60, 30 and 9 GB/s, and why 9 GB/s means twenty lines in flight.
* **8. Programming for caches.** Loop order (column walks and power-of-two conflicts); measured in C from n = 256 to
  2048: i-j-k 1.9 → 0.5 GFLOP/s, i-k-j 3.9 → 1.7, tiled flat near 2.4–3.0, numpy's BLAS 89; tiling; structs of
  arrays.
* **9. Cache-oblivious algorithms.** The ideal-cache model (Frigo, Leiserson, Prokop and Ramachandran 1999); a 256 ×
  256 transpose: row by row 0.56 lines per element until 32 KB, blocked for 16 KB optimal only from 4 KB, recursive
  optimal (0.125) from 1 KB; the van Emde Boas layout.
* **10. The red-blue pebble game.** Hong and Kung (1981); the proof idea with Loomis–Whitney; Q ≥ 2n³/√M − 2M (Smith
  et al. 2019); our multiplies at n = 64, M = 1024 words: the bound 14,336 words, untiled 270,336 (19 times), tiled
  T = 16 42,240 (2.9 times).
* **11. External memory and B-trees.** Aggarwal and Vitter (1988): scanning, searching, the sorting bound
  (N/B) log_{M/B}(N/B); B-trees (Bayer and McCreight 1972).
* **12. Prefetching.** Next-line, stride, software; the Job's scan loop on Part 8's core with the table beyond L2:
  3.09 cycles per entry with perfect memory, 3.10 with real memory and the prefetcher, 3.54 without; the cold pass
  3.37 against 8.29.
* **13. Inside DRAM.** Banks, rows, the row buffer; activate, read, precharge (about 14 ns each); refresh; row-buffer
  hits: sequential 99%, every 4 KB 50%, random 0%; DDR5, HBM, the TLB (Part 32).
* **14. The Job meets memory.** The exact LRU misses of all 4.6 million scans (a line hits iff the last scan to reach
  it was shorter than the cache): 88% at 32 KB, 48% at 256 KB, compulsory only at 1 MB; priced on Part 8's core in
  steady state and weighted by the sampled miss fractions (91% of table reads, 57% of letter reads miss L1): +0.05% at
  885 MHz, +2% without a prefetcher, +14% at 2.8 GHz; ledger row 3: 57.35 s.
* **15. Frontier: learning to replace.** On the Job's scans, scaled down: LRU 63%, random 55%, bimodal insertion
  (Qureshi et al. 2007) 47%, Belady 33%; Hawkeye (Jain and Lin 2016), Glider (Shi et al. 2019); open questions:
  online policies against Belady, pebble bounds beyond matrix multiply, disaggregated memory, processing in memory.
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs9.compute            # every number in the part (about fifteen minutes; the C measurements and the core's microbenchmarks are the slow steps)
python tools/build.py cs9 -q l             # a 480p preview
python tools/build.py cs9                  # 1080p
```

The measurements (`machine`, `staircase`, `bandwidth`, `matmul`) belong to whatever computer runs them; the scenes
print its CPU name. The ledger's row 3 converts this machine's measured latencies to cycles of Pebble's 885 MHz clock,
so it changes a little from machine to machine. Ledger rows 0 to 3 are written to `.cache/cs9/ledger.json`.

## Problems, with solutions

1. **Address bits.** A 32 KB, 8-way cache with 64-byte lines and 48-bit addresses: how many bits of tag, index and
   offset? Which set does address `0x7f3a12345678` use?

   *Solution.* 32 KB / 64 B = 512 lines; 512 / 8 ways = 64 sets. Offset: log₂ 64 = **6 bits**; index: log₂ 64 = **6
   bits**; tag: 48 − 12 = **36 bits**. The low 12 bits of the address are `0x678` = 0110 0111 1000: offset `111000` =
   56, index `011001` = **set 25**; the tag is `0x7f3a12345`.

2. **AMAT.** L1: 4 cycles, 5% misses; L2: 12 cycles, 20% of those miss; DRAM: 200 cycles. What is the AMAT? What miss
   rate in L1 would double it?

   *Solution.* AMAT = 4 + 0.05 × (12 + 0.2 × 200) = 4 + 0.05 × 52 = **6.6 cycles**. Doubling to 13.2 needs
   4 + m × 52 = 13.2, so m = **17.7%**: the L1 miss rate need only rise from 5% to under 18% to halve the speed of
   memory.

3. **Random beats LRU.** Explain why random replacement beats LRU on a loop over C + 1 lines in a cache of C lines.
   What does Belady's policy do?

   *Solution.* After the first pass, the line LRU evicts on each miss is always the least recently used one — which
   is exactly the next line the loop will ask for. So **every access misses**, forever. Random replacement evicts a
   random one of the C lines; the line needed next survives each miss with probability 1 − 1/C, so most accesses hit:
   simulated, about **3% for C = 64** (22% for C = 8, roughly 2/C as C grows). Belady keeps C − 1 lines permanently and lets one slot rotate: **one miss per pass of C + 1 accesses**,
   the least possible. This is the Job's situation at scale (chapter 14).

4. **Tiling and the bound.** Show that a tiled multiply with 3T² ≤ M moves O(n³/T) words. How close to the pebble bound
   2n³/√M can the best T come?

   *Solution.* There are (n/T)³ triples of blocks, and each multiply-accumulate of blocks reads three T × T blocks:
   3T² words per triple, 3n³/T in all (writes of C are a lower-order term if the C block stays resident across the k
   loop: then 2n³/T + n²). With 3T² = M, T = √(M/3) and the traffic is 3√3 · n³/√M ≈ 5.2 n³/√M: within **2.6 times**
   of the bound. Keeping C's block resident and streaming A and B gives 2n³/T with T² close to M, which approaches
   **2n³/√M**: the bound is tight, and this schedule is how the tight constant was shown achievable. Our simulated
   T = 16 came within 2.9 times with an ordinary LRU cache.

5. **Build: insertion policies.** Add bimodal insertion to `cache.py` and run the Job's scaled scans: do you reproduce
   47%? What insertion probability is best?

   *Solution.* In `SetAssoc.access`, after a miss inserts the line at the most-recently-used end, move it to the
   least-recently-used end unless a random draw below ε says otherwise. On the first 6,000 words of the corpus with a
   128-line fully associative cache (`compute_frontier`): ε = 1 (plain LRU) **63.5%**, ε = 1/4 56.6%, 1/8 50.6%,
   1/16 47.8%, **1/32 46.6%** (the reproduction), 1/64 45.6%, 1/256 44.9%, and **ε = 0 43.2%**, the best here: always
   inserting at the LRU end (Qureshi's LIP). On this workload the table only grows, so no new line ever deserves to
   displace the front of the table; BIP's small ε exists for workloads whose working set changes, which is why DIP
   chooses between policies at run time. Belady's optimum is 32.7%.

6. **★ Research: Belady on the Job's scans.** On the full scans, keeping the table's front misses 70% at 32 KB against
   LRU's 88%. What is Belady's miss rate there, and how close can an online policy get?

   *What is known, and where to start.* Open as posed. The sequence is 2.8 billion line reads (`compute_scans`; the
   ends of all 4.6 million scans are `scan_ends(...)` in `compute.py`), too long for a direct simulation of Belady in
   Python, but highly structured: every scan is a prefix of the table. (a) The "keep the front" count is an *upper
   bound* on Belady's misses (it is one particular offline policy). (b) For a single cyclic scan longer than the
   cache, Belady keeps a fixed subset and misses once per pass per extra line; prefix scans of varying lengths mix
   these regimes, so a dynamic program over scan lengths may give Belady's count exactly, as the stack trick gave
   LRU's. (c) Online: LIP/BIP and DIP (Qureshi et al. 2007), RRIP (Jaleel et al. 2010), and Hawkeye (Jain and Lin
   2016), which learns from Belady on a sampled past; on this trace every table read comes from one instruction, so
   Hawkeye's per-instruction predictor sees nothing to separate — a careful answer explains what feature would. Report
   misses at 32 KB, 256 KB and 512 KB against the bound from (a) or the exact value from (b).

## 习题与解答

1. **地址位。** 一个 32 KB、8 路、64 字节行、48 位地址的缓存：标签、索引和偏移各几位？地址 `0x7f3a12345678` 落在哪一组？

   *解答。* 32 KB / 64 B = 512 行；512 / 8 路 = 64 组。偏移 log₂ 64 = **6 位**；索引 log₂ 64 = **6 位**；标签 48 − 12 = **36 位**。
   地址低 12 位是 `0x678` = 0110 0111 1000：偏移 `111000` = 56，索引 `011001` = **第 25 组**；标签是 `0x7f3a12345`。

2. **平均访存时间。** L1：4 个周期，5% 缺失；L2：12 个周期，其中 20% 缺失；DRAM：200 个周期。平均访存时间是多少？L1 缺失率
   到多少会让它翻倍？

   *解答。* AMAT = 4 + 0.05 × (12 + 0.2 × 200) = 4 + 0.05 × 52 = **6.6 个周期**。翻倍到 13.2 需要 4 + m × 52 = 13.2，即
   m = **17.7%**：L1 缺失率只要从 5% 升到不到 18%，存储器的速度就减半。

3. **随机胜过 LRU。** 为什么在一个 C 行的缓存上循环访问 C + 1 行时，随机替换胜过 LRU？Belady 的策略怎么做？

   *解答。* 第一遍之后，LRU 每次缺失淘汰的总是最久未用的那一行——恰恰是循环下一个要用的行。所以**每次访问都缺失**，永远如此。
   随机替换淘汰 C 行中随机的一行；下一个要用的行每次缺失都以 1 − 1/C 的概率留下来，所以大多数访问命中：模拟得到 **C = 64 时
   约 3%**（C = 8 时 22%，C 增大时约为 2/C）。Belady 让 C − 1 行
   永久留下，只让一个位置轮转：**每遍 C + 1 次访问只缺失一次**，这是最少的。这正是任务在大尺度上的处境（第 14 章）。

4. **分块与下界。** 证明满足 3T² ≤ M 的分块乘法搬动 O(n³/T) 个字。最好的 T 能离卵石下界 2n³/√M 多近？

   *解答。* 共有 (n/T)³ 组分块三元组，每组的乘加读三个 T × T 块：每组 3T² 个字，总共 3n³/T（如果 C 的块在 k 循环中一直留在
   缓存里，C 的写回只是低阶项：2n³/T + n²）。取 3T² = M，T = √(M/3)，流量是 3√3 · n³/√M ≈ 5.2 n³/√M：在下界的 **2.6 倍**
   以内。让 C 的块常驻、A 和 B 流过，得到 2n³/T，T² 接近 M 时趋近 **2n³/√M**：下界是紧的，这个调度正是常数可达的证明方式。
   我们模拟的 T = 16 用普通 LRU 缓存也在 2.9 倍以内。

5. **动手：插入策略。** 在 `cache.py` 里加入双峰插入，在任务的缩小版扫描上运行：能复现 47% 吗？什么插入概率最好？

   *解答。* 在 `SetAssoc.access` 中，缺失后新行先插在最近使用端，然后除非一次随机抽取小于 ε，否则把它移到最久未用端。在语料前
   6,000 个词、128 行全相联缓存上（`compute_frontier`）：ε = 1（普通 LRU）**63.5%**，1/4 为 56.6%，1/8 为 50.6%，1/16 为
   47.8%，**1/32 为 46.6%**（即复现值），1/64 为 45.6%，1/256 为 44.9%，**ε = 0 为 43.2%**，在这里最好：总是插在最久未用端
   （Qureshi 的 LIP）。在这个负载上表只增不减，所以没有哪个新行值得挤走表的前部；BIP 的小 ε 是为工作集会变化的负载准备的，
   这也是 DIP 在运行时于两种策略间选择的原因。Belady 最优为 32.7%。

6. **★ 研究题：任务扫描上的 Belady。** 在完整的扫描上，保留表的前部在 32 KB 时缺失 70%，LRU 为 88%。Belady 的缺失率是多少？
   在线策略能离它多近？

   *已知什么，从哪里入手。* 按题目所问，这是开放的。序列有 28 亿次行读取（`compute_scans`；全部 460 万次扫描的终点是
   `compute.py` 里的 `scan_ends(...)`），用 Python 直接模拟 Belady 太长，但结构很强：每次扫描都是表的前缀。（a）"保留前部"的计数
   是 Belady 缺失数的*上界*（它是一种特定的离线策略）。（b）对单个比缓存长的循环扫描，Belady 保留固定子集，每遍每多出一行缺失
   一次；长度各异的前缀扫描混合了这些情形，所以对扫描长度做动态规划也许能精确给出 Belady 的计数，正如栈的技巧精确给出了 LRU 的。
   （c）在线策略：LIP/BIP 和 DIP（Qureshi 等，2007），RRIP（Jaleel 等，2010），以及从抽样的过去中向 Belady 学习的 Hawkeye（Jain 与
   Lin，2016）；在这条轨迹上每次读表都来自同一条指令，所以 Hawkeye 按指令的预测器无从区分——一个认真的回答要说明什么特征才能区分。
   报告 32 KB、256 KB 和 512 KB 下的缺失，并与（a）的上界或（b）的精确值对比。

## Glossary additions

存储层次 memory hierarchy · 存储墙 memory wall · 局部性 locality · 时间局部性 temporal locality · 空间局部性 spatial locality ·
工作集 working set · 重用距离 reuse distance · 栈距离 stack distance · 缺失率曲线 miss-ratio curve · 缓存行 cache line ·
直接映射 direct-mapped · 组相联 set-associative · 全相联 fully associative · 路 way · 组 set · 标签 tag · 索引 index ·
偏移 offset · 替换策略 replacement policy · 最近最少使用 LRU · 伪 LRU pseudo-LRU · 先进先出 FIFO · 最优替换 Belady's optimal
policy · 写回 write-back · 写直达 write-through · 写分配 write-allocate · 强制缺失 compulsory miss · 容量缺失 capacity miss ·
冲突缺失 conflict miss · 平均访存时间 average memory access time (AMAT) · 指针追逐 pointer chasing · 延迟阶梯 latency staircase ·
带宽 bandwidth · 分块 tiling · 循环交换 loop interchange · 结构体数组 / 数组结构体 array of structs / struct of arrays ·
缓存无关算法 cache-oblivious algorithm · 理想缓存模型 ideal-cache model · van Emde Boas 布局 van Emde Boas layout · 红蓝卵石游戏
red-blue pebble game · 外存模型 external-memory model · B 树 B-tree · 预取 prefetching · 步长预取器 stride prefetcher · 行缓冲
row buffer · 激活 / 读 / 预充电 activate / read / precharge · 刷新 refresh · 高带宽存储器 HBM · 快表 TLB · 插入策略 insertion
policy · 双峰插入 bimodal insertion · 解耦内存 disaggregated memory

## Sources

The reading list is split, as the research tier asks (videos/cs/SYLLABUS.md §1.1), into the qualifying-exam canon and
recent work.

*Canon.* Books: Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed., ch. 2 and Appendix B
(the processor–memory gap and its growth rates); Bryant & O'Hallaron, *Computer Systems: A Programmer's Perspective*,
ch. 6; Jacob, Ng & Wang, *Memory Systems: Cache, DRAM, Disk* (2008); Drepper, "What every programmer should know
about memory" (2007).

Papers: Wilkes, "Slave memories and dynamic storage allocation" (1965); Belady, "A study of replacement algorithms for a
virtual-storage computer", IBM Systems Journal (1966); Denning, "The working set model for program behavior", CACM
(1968); Mattson, Gecsei, Slutz & Traiger, "Evaluation techniques for storage hierarchies", IBM Systems Journal (1970);
Bayer & McCreight, "Organization and maintenance of large ordered indices" (1972); Hong & Kung, "I/O complexity: the
red-blue pebble game", STOC (1981); Hill, "Aspects of cache memory and instruction buffer performance", PhD thesis,
Berkeley (1987); Aggarwal & Vitter, "The input/output complexity of sorting and related problems", CACM (1988); Wulf &
McKee, "Hitting the memory wall: implications of the obvious" (1995); Frigo, Leiserson, Prokop & Ramachandran,
"Cache-oblivious algorithms", FOCS (1999).

*Recent.* Qureshi, Jaleel, Patt, Steely & Emer, "Adaptive insertion policies for high performance caching", ISCA
(2007); Jaleel, Theobald, Steely & Emer, "High performance cache replacement using re-reference interval prediction
(RRIP)", ISCA (2010); Jain & Lin, "Back to the future: leveraging Belady's algorithm for improved cache replacement",
ISCA (2016); Smith, Lowery, Langou & van de Geijn, "A tight I/O lower bound for matrix multiplication" (2019); Shi,
Huang, Jain & Lin, "Applying deep learning to the cache replacement problem", MICRO (2019).
