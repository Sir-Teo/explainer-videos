# Computer Science, Built — Part 7: Pipelines

Part 7 of the sixty-one-part course ([plan](../README.md), [syllabus](../SYLLABUS.md)) opens Act II,
*Making It Fast*. A functional cycle-by-cycle Pebble model overlaps instructions through five stages.
Finite tests compare selected programs/configurations with the instruction emulator. It is not a physical gate
pipeline: memory delays, mux/control estimates and register overhead define an **assumed teaching clock budget**.
The M-extension latencies are modeled, motivated by earlier arithmetic circuits.

- **Performance accounting:** time = instructions × CPI × clock period. The same Job chapter uses 827,576
  instructions; measured model CPI and assumed periods give its projected speedup. MIPS alone can mislead.
- **Throughput versus latency:** equal stages give speedup `(t+o)/(t/k+o)` with limit **1+t/o**.
  Register overhead increases instruction latency. The assumed five-stage period is 1,130 ps versus 2,630 ps
  single-cycle. The depth optimum assumes equal splittable work, fixed miss fraction and `k−1` penalty;
  compare feasible integer depths near the continuous optimum. Historical Pentium 4 depths do not validate it.
- **Structural and data hazards:** one coherent byte array has two ideal logical access ports. Division occupies
  EX for 16 modeled cycles. Forwarding prioritizes the newest producer, ignores zero-register writes and cannot
  forward unavailable load data. A load produces at end-MEM while the next consumer needs start-EX in the same
  cycle; these are different instants. Write-back-before-decode is a simulator policy.
- **Branches and targets:** counter startup, aliasing, gshare, our bimodal/gshare tournament, simplified TAGE,
  and indexed perceptron weights. A counter's failure does not test all local-history models. Classic MIPS delay
  slots were removed in Release 6. Warm correct BTB hits and balanced recognized calls explain modeled benefits;
  neither guarantees free branches or perfect returns.
- **Precise exceptions:** committed architectural state has a precise boundary; cache/predictor effects are separate.
  Pebble stops and reports a fault PC, with no OS resume implementation. Its divide-zero fault differs from
  RISC-V M's defined result. `fence.i` orders same-hart instruction fetch; multicore/migration requires the
  specified wider protocol. The deliberate stale-code example has no instruction-fence implementation.
- **The Job:** six instructions/seven cycles describes the mismatched-length fast path with warm correct
  prediction. Full search includes letter comparisons. The corpus row is a **fitted extrapolation** from 24
  passages, checked on one 16,000-character heldout text (16,019 encoded bytes); that check supplies no full-corpus error bound. Projected
  runtime also assumes the teaching clock.
- **Power and Amdahl:** dynamic `αCV²f` excludes leakage. Lower VDD slows circuits; lower threshold to retain
  speed raises leakage. Fixed-work Amdahl fractions are baseline **time** fractions. Search is 99.7% of single-cycle
  instructions; deleting it at no replacement cost gives a roughly 350× ceiling only in that uniform-cost model,
  not a measured pipeline bound. Pipeline speedup is clock ratio divided by CPI ratio.
- **Sorted arrays:** fixed-seed irregular and sorted orders preserve the sum. Host bars read current cached
  five-run medians; no historical Xeon timings are narrated. Sorting/generation are excluded; 300 passes reuse
  the same array. Compiler options, output observability and machine dependence are recorded. Timing alone
  does not isolate branch prediction. Branchless masking uses `(x<128)-1` in the word model and can do more work.
- **Frontier:** report empirical one-trace curves and nominal packed table payload, excluding history, validity
  and implementation overhead. PPM-style context tables grow over configured lengths up to 64. Its algorithm
  differs from TAGE, so the gap does not isolate storage or establish an impossibility bound. Hindsight majority
  is an offline oracle for a chosen feature class. Compression relates probabilities/log loss to code length,
  not directly to an accuracy ceiling. XOR has no perfect fixed affine separator of its two input bits, but a
  fixed line can classify 3/4 of uniform cases; this run's 49% is not a theorem. Piecewise-linear and
  multiperspective predictors use different feature constructions. TAGE-SC-L combines components; BranchNet
  evaluates offline convolutional training on unseen inputs. Research exercises specify heldout evaluation.

## Build

```bash
python -m videos.cs.cs7.compute            # every number in the part (about ten minutes; the Job's fit is the slow step)
python tools/build.py cs7 -q l             # a 480p preview
python tools/build.py cs7                  # 1080p
```

The sorted-array timings are measured by compiling a small C program with the system compiler (`-O1` with
if-conversion and vectorization turned off, so the branch survives) and are machine-specific; the scene reads the CPU
name from `/proc/cpuinfo`. Ledger rows 0 and 1 are written to `.cache/cs7/ledger.json`.

## Problems, with solutions

1. **A load-use chart.** Draw the pipeline chart for `lw t0, 0(a0)`; `add t1, t0, t0`; `sw t1, 4(a0)` with
   forwarding. Where is the bubble, and which paths carry values?

   *Solution.*

   ```
                  1    2    3    4    5    6    7    8
   lw  t0, 0(a0)  IF   ID   EX   MEM  WB
   add t1, t0, t0      IF   ID   ID   EX   MEM  WB
   sw  t1, 4(a0)            IF   IF   ID   EX   MEM  WB
   ```

   The add is held in ID for one cycle (cycle 4), and a bubble enters EX behind the load: its value exists only at
   the end of MEM. In cycle 5 the **MEM/WB → EX** path carries t0 into the add, and in cycle 6 the **EX/MEM → EX**
   path carries t1 into the store's data operand. Three instructions take 3 + 4 + 1 = **8 cycles**.

2. **The cost of branches.** 20% of instructions are branches, 60% of them taken. Predict-not-taken costs 2 cycles per
   taken branch; a predictor that is 95% right costs 2 per mistake. What CPI does each give?

   *Solution.* CPI = 1 + branch fraction × miss rate × penalty. Predict-not-taken misses every taken branch:
   1 + 0.2 × 0.6 × 2 = **1.24**. The predictor: 1 + 0.2 × 0.05 × 2 = **1.02** (assuming the target buffer supplies the
   target of every correctly predicted taken branch). A 20-stage machine with a 15-cycle penalty would give
   1 + 0.2 × 0.6 × 15 = 2.8 against 1 + 0.2 × 0.05 × 15 = 1.15: the deeper the pipeline, the more a predictor is worth.

3. **The best depth.** Minimize T(k) = (t/k + o)(1 + b(k − 1)) to show k* = √(t(1 − b)/(b·o)). With t = 2560 ps and
   o = 70 ps, what is k* for b = 0.01 and for b = 0.1?

   *Solution.* Multiply out: T = t/k + o + bt − bt/k + bok − bo = t(1 − b)/k + bok + (o + bt − bo). The constant does
   not depend on k, so dT/dk = −t(1 − b)/k² + bo, which is zero at **k* = √(t(1 − b)/(b·o))**; the second derivative
   2t(1 − b)/k³ is positive, so it is a minimum. For b = 0.01: √(2560 × 0.99 / 0.7) ≈ **60 stages**; for b = 0.1:
   √(2560 × 0.9 / 7) ≈ **18 stages**. For small b the depth scales approximately as 1/√b; the exact expression also contains √(1−b). The Job's
   measured b = 0.0265 gives 37.

4. **Amdahl and Gustafson.** 80% of a program can run in parallel. What speedup do 4, 16 and infinitely many
   processors give? What if the problem grows so the serial time stays fixed (Gustafson)?

   *Solution.* Amdahl: S(n) = 1 / (0.2 + 0.8/n): **2.5** for 4 processors, **4.0** for 16, and **5** at most, however
   many. Gustafson measures the fractions on the parallel machine: if the serial part stays 20% of the run time there
   and the parallel work grows with n, the same work would take 0.2 + 0.8n on one processor, so the scaled speedup is
   **3.4** for 4 and **13.0** for 16, growing without limit. Both are right; they answer different questions (a
   fixed problem, or a fixed time).

5. **Build: hide the bubble.** In the Job's scan loop, move one instruction so the load-use bubble disappears. Run
   chapter 1 on the pipeline: how many cycles do you save, and what is the new CPI?

   *Solution.* The loop reads an entry's length and tests it at once:

   ```
   scan:   beq  a2, s1, insert
           lw   t1, 4(t0)       # same length?
           bne  t1, a1, next    # needs t1 now: one bubble per entry
   ```

   For this byte-array model, first prove that `t0+4` is aligned, remains in allocated readable memory even at the insertion slot, and has no MMIO side effects. Then swap the first two instructions so the test fills the slot. Hoisting a potentially faulting or out-of-bounds load is not generally valid:

   ```
   scan:   lw   t1, 4(t0)       # read early only after proving address safety
           beq  a2, s1, insert
           bne  t1, a1, next
   ```

   On chapter 1 with the ledger's pipeline (forwarding, a BTB, a tournament predictor and a return stack) the load-use
   stalls fall from 124,112 to 28,699, the cycles from 995,654 to **952,210 (43,444 saved, 4.4%)**, and the CPI from
   1.203 to **1.150**, at the price of 331 more instructions (one extra load each time a word is added to the table).
   The output is unchanged. Part 13's compiler finds moves like this one by itself: instruction scheduling.

6. **★ Research: close the gap.** On the Job's chapter-1 branches our TAGE gets 94.3% in 9 KB and the unlimited PPM
   predictor 97.5%. How much of that gap can a 64 KB predictor close? Which branches stay wrong, and could anything but
   branch history predict them?

   *What is known, and where to start.* This is a heldout generalization problem. The known 254,436 outcomes need only 31,805 bytes plus an index to replay perfectly, within 64 KiB; predict-before-update alone does not prevent encoded future labels. Choose separate training, tuning and untouched test chapters, prohibit future-label encoding in code or initial state, and count all tables, histories, tags, validity, weights and metadata in the budget. Start from `explainer/cs/pebble/predict.py` and the trace from `videos/cs/cs7/compute.py`
   (`trace_of(*benchmarks()["the Job, chapter 1"])`); `PR.accuracy` scores any object with `predict(pc)` and
   `update(pc, taken)`. Count mispredictions per static branch first. On this trace **68% of our TAGE's misses come
   from one branch**, the scan loop's length test `bne t1, a1, next` (9,846 of 14,412); the letter comparison in `cmp`
   gives 15% and the letter-or-separator test 9%. The unlimited PPM predictor cuts the scan branch's misses to 2,120,
   because between insertions the table's sequence of lengths is fixed, so a long enough history pins down where the
   scan is.

   Three directions, each from the literature. (1) *Better use of history*: the full TAGE of Seznec's TAGE-SC-L (more
   tables, longer tags, alternate-prediction logic, a statistical corrector and a loop predictor) is the standard
   64 KB baseline in the Championship Branch Prediction. (2) *Path and position*: the scan branch's outcome is a
   function of the loop counter `a2` and the current word's length `a1`, which is not in the branch history at all.
   A predictor indexed by data values (Heil, Smith and Smith, "Improving branch predictors by correlating on data
   values", MICRO 1999) could predict it almost perfectly; the question is what such a predictor costs in hardware
   and whether it generalizes beyond this program. (3) *Offline learning*: train a small model per hard branch on
   one chapter and test it on another (Zangeneh et al., BranchNet, MICRO 2020). A careful answer reports accuracy on
   a *different* chapter from the one used for design, the storage in bits counted as the championship counts it,
   and which misses remain.

## 习题与解答

1. **取数—使用的流水线图。** 在有转发的情况下，画出 `lw t0, 0(a0)`、`add t1, t0, t0`、`sw t1, 4(a0)` 的流水线图。气泡在哪里？
   哪些通路传送数值？

   *解答。* 流水线图见上文英文部分。add 在 ID 级多停一个周期（第 4 周期），一个气泡跟在取数指令后面进入 EX：它的值要到 MEM
   结束才有。第 5 周期，**MEM/WB → EX** 通路把 t0 送进 add；第 6 周期，**EX/MEM → EX** 通路把 t1 送进存数指令的数据操作数。
   三条指令共用 3 + 4 + 1 = **8 个周期**。

2. **分支的代价。** 20% 的指令是分支，其中 60% 跳转。"预测不跳转"每遇到一次跳转损失 2 个周期；一个正确率 95% 的预测器每次猜错
   损失 2 个周期。两者的 CPI 各是多少？

   *解答。* CPI = 1 + 分支比例 × 猜错率 × 代价。"预测不跳转"错在每一条跳转的分支：1 + 0.2 × 0.6 × 2 = **1.24**。预测器：
   1 + 0.2 × 0.05 × 2 = **1.02**（假设分支目标缓冲器为每条预测正确的跳转分支提供目标地址）。一台代价为 15 个周期的 20 级流水线
   机器则是 1 + 0.2 × 0.6 × 15 = 2.8 对 1 + 0.2 × 0.05 × 15 = 1.15：流水线越深，预测器越值钱。

3. **最佳深度。** 求 T(k) = (t/k + o)(1 + b(k − 1)) 的最小值，证明 k* = √(t(1 − b)/(b·o))。取 t = 2560 ps，o = 70 ps，b = 0.01
   和 b = 0.1 时 k* 各是多少？

   *解答。* 展开：T = t(1 − b)/k + bok + (o + bt − bo)，常数项与 k 无关，所以 dT/dk = −t(1 − b)/k² + bo，在
   **k* = √(t(1 − b)/(b·o))** 处为零；二阶导数 2t(1 − b)/k³ 为正，所以是最小值。b = 0.01 时约 **60 级**；b = 0.1 时约
   **18 级**。当 b 很小时，深度近似与 √b 成反比；精确式还含 √(1−b)。用任务实测的 b = 0.0265 得到 37。

4. **阿姆达尔与古斯塔夫森。** 一个程序 80% 可以并行。4 个、16 个、无穷多个处理器各带来多少加速？如果问题随之变大、使串行时间保持
   不变（古斯塔夫森），又如何？

   *解答。* 阿姆达尔：S(n) = 1 / (0.2 + 0.8/n)：4 个处理器 **2.5**，16 个 **4.0**，无论多少个最多 **5**。古斯塔夫森在并行机器上
   度量比例：如果串行部分在那里始终占运行时间的 20%，而并行工作随 n 增长，同样的工作在单处理器上要 0.2 + 0.8n，于是按规模放大的
   加速是 4 个 **3.4**、16 个 **13.0**，没有上限。两者都对，回答的是不同的问题（问题固定，还是时间固定）。

5. **动手：藏起气泡。** 在任务的扫描循环里移动一条指令，让取数—使用气泡消失。在流水线上运行第 1 章：省下多少周期？新的 CPI
   是多少？

   *解答。* 循环读出条目的长度后立刻检查它（代码见上文英文部分）。先证明 `t0+4` 对齐、即使到插入位置仍在已分配可读内存中，且没有设备访问副作用。只有在这些条件下才能把前两条指令对调，让取数在"表结束了吗"的检查之前发出，由这个
   检查填补空档。在第 1 章上，用账本所用的流水线（转发、分支目标缓冲器、锦标赛预测器和返回地址栈），取数—使用停顿从 124,112 次
   降到 28,699 次，周期从 995,654 降到 **952,210（省下 43,444，4.4%）**，CPI 从 1.203 降到 **1.150**，代价是多执行 331 条指令
   （每往表里加一个词就多一次取数）。输出不变。第 13 部分的编译器会自己找到这样的移动：指令调度。

6. **★ 研究题：缩小差距。** 在任务第 1 章的分支上，我们的 TAGE 用 9 KB 达到 94.3%，不限存储的 PPM 预测器达到 97.5%。一个 64 KB
   的预测器能把这个差距缩小多少？哪些分支仍然猜错？除了分支历史，还有什么能预测它们？

   *已知什么，从哪里入手。* 这是留出泛化问题。已知的254,436次结果只需31,805字节加索引，就能在64二进制千字节内完美重放；先预测再更新本身不能阻止编码未来标签。必须分开训练、调参与未使用测试章节，禁止代码或初值编码未来测试结果，并把表、历史、标记、有效位、权重与元数据全计入预算。从 `explainer/cs/pebble/predict.py` 和
   `videos/cs/cs7/compute.py` 里的轨迹入手（`trace_of(*benchmarks()["the Job, chapter 1"])`）；`PR.accuracy` 可以给任何带
   `predict(pc)` 和 `update(pc, taken)` 的对象打分。先按静态分支统计预测错误。在这条轨迹上，**我们的 TAGE 有 68% 的错误来自同一条
   分支**，即扫描循环里的长度检查 `bne t1, a1, next`（14,412 次中的 9,846 次）；`cmp` 里的字母比较占 15%，字母还是分隔符的检查占
   9%。不限存储的 PPM 把扫描分支的错误降到 2,120 次，因为在两次插入之间表里的长度序列是固定的，足够长的历史就能确定扫描进行到了哪里。

   文献中有三个方向。（1）*更好地利用历史*：塞兹内克 TAGE-SC-L 的完整 TAGE（更多的表、更长的标签、备选预测逻辑、统计校正器和循环
   预测器）是分支预测锦标赛 64 KB 赛道的标准基线。（2）*路径与位置*：扫描分支的结果是循环计数器 `a2` 和当前单词长度 `a1` 的函数，
   而它们根本不在分支历史里。按数据值索引的预测器（Heil、Smith 和 Smith，《通过与数据值相关来改进分支预测器》，MICRO 1999）可以提供有用特征；问题在于这样的预测器在硬件上要花多少，以及它能否推广到这个程序之外。（3）*离线学习*：在一章上为每条难预测的分支训练
   一个小模型，在另一章上测试（Zangeneh 等，BranchNet，MICRO 2020）。一个认真的回答应当报告在设计时*没有*用过的另一章上的准确率、按锦标赛
   规则以比特计算的存储，以及还剩下哪些错误。

## Glossary additions

极限研究 limit study · 部分匹配预测 prediction by partial matching (PPM) · 线性可分 linearly separable · 熵率 entropy rate ·
统计校正器 statistical corrector · 难预测的分支 hard-to-predict branch · 前端瓶颈 front-end bottleneck ·
流水线 pipeline · 流水级 pipeline stage · 流水线寄存器 pipeline register · 吞吐量 throughput · 延迟 latency · 取指 / 译码 /
执行 / 访存 / 写回 IF / ID / EX / MEM / WB · 流水线图 pipeline chart · 冒险 hazard · 结构冒险 structural hazard · 数据冒险 data
hazard · 控制冒险 control hazard · 写后读 RAW · 停顿 stall · 气泡 bubble · 转发 forwarding · 取数—使用冒险 load-use hazard · 冲刷
flush · 延迟槽 delay slot · 分支预测 branch prediction · 静态预测 static prediction · 饱和计数器 saturating counter · 全局历史
global history · 锦标赛预测器 tournament predictor · 感知机预测器 perceptron predictor · 分支目标缓冲器 branch target buffer (BTB) ·
返回地址栈 return-address stack · 精确异常 precise exception · 每秒百万条指令 MIPS · 功耗墙 power wall · 登纳德缩放 Dennard
scaling · 阿姆达尔定律 Amdahl's law · 古斯塔夫森定律 Gustafson's law · 无分支代码 branch-free code · 条件传送 conditional move

## Sources

The reading list is split, as the research tier asks (videos/cs/SYLLABUS.md §1.1), into the qualifying-exam canon and
recent work.

*Canon.* Books: Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed., ch. 1 and 3 and Appendix C;
Patterson & Hennessy, *Computer Organization and Design, RISC-V Edition*, ch. 1 and 4; Shen & Lipasti, *Modern
Processor Design*, ch. 2 and 9; Harris & Harris, *Digital Design and Computer Architecture*, ch. 7; Fog, *The
microarchitecture of Intel, AMD and VIA CPUs* (updated yearly).

Papers: Amdahl, "Validity of the single processor approach to achieving large scale computing capabilities", AFIPS
(1967); Dennard et al., "Design of ion-implanted MOSFETs with very small physical dimensions", IEEE JSSC (1974);
Smith, "A study of branch prediction strategies", ISCA (1981); Gustafson, "Reevaluating Amdahl's law", CACM (1988);
Yeh & Patt, "Two-level adaptive training branch prediction", MICRO (1991); McFarling, "Combining branch predictors",
DEC WRL TN-36 (1993); Jiménez & Lin, "Dynamic branch prediction with perceptrons", HPCA (2001); Hrishikesh et al., "The
optimal logic depth per pipeline stage is 6 to 8 FO4 inverter delays", ISCA (2002); Seznec & Michaud, "A case for
(partially) tagged geometric history length branch prediction", JILP (2006); Wall, "Limits of instruction-level
parallelism", ASPLOS (1991); Cleary & Witten, "Data compression using adaptive coding and partial string matching",
IEEE Trans. Comm. (1984); Chen, Coffey & Mudge, "Analysis of branch prediction via data compression", ASPLOS (1996);
Minsky & Papert, *Perceptrons* (1969).

*Recent work.* Jiménez, "Piecewise linear branch prediction", ISCA (2005); Heil, Smith & Smith, "Improving branch
predictors by correlating on data values", MICRO (1999); Kanev et al., "Profiling a warehouse-scale computer", ISCA
(2015); Seznec, "TAGE-SC-L branch predictors again" and Jiménez, "Multiperspective perceptron predictor", 5th
Championship Branch Prediction (2016); Zangeneh, Pruett, Lym & Patt, "BranchNet: a convolutional neural network to
predict hard-to-predict branches", MICRO (2020).
