# Computer Science, Built — Part 8: Out of Order

Part 8 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act II, *Making It Fast*. Part 7's pipeline starts its instructions
in program order, so when one waits, all wait. This part lets instructions run as soon as their operands are ready:
the dataflow limit that bounds any such machine, register renaming, the CDC 6600's scoreboard and Tomasulo's
algorithm, the reorder buffer that keeps exceptions precise, speculation, memory disambiguation, and the price of
guessing: Spectre, run on our own machine. The out-of-order core is a cycle-by-cycle simulator
(`explainer/cs/pebble/ooo.py`), checked against the emulator in every configuration (`tests/test_cs8_ooo.py`); the
limit study's oracle scheduler is `explainer/cs/pebble/limits.py`; the attack is `programs.spectre`. Every number is
computed in `compute.py`.

* **Waiting in line.** One cache miss on an in-order machine (81 cycles for 16 instructions) and out of order (70,
  the independent work hidden under the miss); the Job's first chapter on Part 7's pipeline (IPC 0.83), on our core
  in order (0.78) and out of order (1.89, 2.42 times fewer cycles); the reorder buffer's occupancy: 128 entries, 10.7
  in use on average, never full.
* **1. The dataflow limit.** The scan loop; four trips as a dataflow graph; the critical path (6 cycles, through
  `addi t0, t0, 12`) against the pipeline's 28; schedules at widths 1, 2, 4, 8 (24, 12, 7, 6 cycles); work and span,
  max(N/W, L) ≤ T_W ≤ N/W + L (Graham, 1966); in a loop the chain sets a rate: 6 instructions a cycle at best.
* **2. False dependences, and renaming.** RAW, WAR and WAW; on the Job, 981,268 true dependences against 915,048
  false ones; the register alias table and physical registers; the oracle with and without renaming: IPC 2,399
  against 3.68.
* **3. The scoreboard.** The CDC 6600 (1964; Cray and Thornton), its ten units, Watson's memo; issue, read
  operands, execute, write result, with WAW, RAW and WAR checked at each; Hennessy and Patterson's example, cycle by
  cycle, reproduced exactly (62 cycles; the add waits from 16 to 22 for the divide to read `a1`).
* **4. Tomasulo's algorithm.** The IBM 360/91 (1967) and its four floating-point registers; reservation stations,
  tags, the common data bus; the same example, station by station: 56 cycles, the add broadcast in cycle 10; the
  catch: results reach the registers out of order, so exceptions are imprecise.
* **5. The reorder buffer.** Smith and Pleszkun (1985): in order, out of order, in order; the ring, filled at the
  tail and emptied at the head, recorded from the core in the scan loop (with a wrong path dropped); a precise divide
  by zero; the modern pipeline; result-in-ROB (Pentium Pro) against a merged physical register file (R10000, 21264).
* **6. Wider, and the ILP wall.** Wall's 1991 study repeated on the Job: the oracle 2,399, no renaming 3.68,
  conservative memory 62.3, a real predictor 3.41, no speculation 0.47; width and window: with real branches the
  window does not matter (3.4 at any size), with perfect branches 8.3 (window 128) and 30 (2,048); our core 0.86, 1.24,
  1.89, 1.97 at widths 1 to 8, flat in ROB size; 3.16 and 3.53 with perfect prediction.
* **7. Speculation.** Predict, run ahead, keep the receipts; a misprediction recorded (11 wrong-path instructions,
  the next right-path fetch 8 cycles after the branch's); four predictors on the Job (always taken 0.69, 2-bit 1.87,
  tournament 1.89, perfect 3.16); 22,296 mispredictions throw away 253,764 instructions (31% extra work) and run
  28,905 wrong-path loads; one wrong guess per 37 instructions; CPI = CPI_perfect + rate × P gives P ≈ 7.9 cycles.
* **8. Loads, stores, and their order.** Memory dependences are hidden behind address arithmetic; load and store
  queues and store-to-load forwarding; conservative, speculative and wait-table disambiguation (the Alpha 21264); a
  memory-order violation recorded (the load reads 0, is squashed, reads 77); counting 1,500 cache-missing samples:
  97,740 cycles conservative, 7,652 speculative (23 violations), 7,408 with the wait table, 13 times faster; on the
  Job no difference (154,835 loads, 5,270 stores).
* **9. Spectre.** Flush+Reload (Yarom and Falkner, 2014); the bounds-check gadget; the attack on our core (train, flush
  the bound, call out of bounds, time the probe): one line at 5 cycles among 254 at 63; the secret "PEBBLE" in 109,424
  cycles; a speculation barrier (12.1 cycles a call against 4.0) and an index mask (5.0) both stop it; Spectre and
  Meltdown (2018), and the fixes in kernels, compilers, browsers and chips.
* **10. The compiler's alternative: VLIW.** The cost of scheduling hardware; the scan loop in four-wide bundles (3
  cycles a trip, 6 of 12 slots `nop`); software pipelining, II ≥ max(⌈6/4⌉, 1) = 2; why VLIW lost the desktop (unknown
  latencies, data-dependent branches, binary compatibility, Itanium's history); DSPs and accelerators.
* **11. RISC and CISC.** The iron law's two sides; the VAX, Cocke's 801, Berkeley RISC, Stanford MIPS (1980–1981);
  the Job's instruction mix; 59% of its loads feed one instruction and die, so x86 would need 11% fewer instructions;
  micro-ops since the Pentium Pro, fusion, the decoder's cost; x86, Arm, RISC-V; the 2017 Turing Award.
* **12. Simultaneous multithreading.** Empty issue slots; Tullsen, Eggers and Levy (1995); what is per thread and
  what is shared; in the limit study, two threads give +40% at 4 wide and +80% at 8 wide; Hyper-Threading, POWER5,
  POWER8; the price, including timing channels between threads.
* **13. Modern cores in numbers.** Reorder-buffer sizes from the Pentium Pro (40) to Golden Cove (512), Zen 5 (448)
  and Apple's M1 (about 630, measured); why so big (DRAM latency, prediction quality); decode widths 3 to 8; reading
  real cores (manuals, Agner Fog, uops.info, independent measurement, `perf`).
* **14. The Job out of order.** CPI 0.529 taken apart: 0.25 width, 0.067 dependences and front end, 0.212 wrong
  guesses (40% of the time); 24 passages fitted, checked on 16 KB of *Moby-Dick* (−0.09%); thirty novels: IPC 2.11,
  5.07 × 10¹⁰ cycles, 57 seconds at Part 7's 885 MHz; ledger row 2, 2.52 times faster.
* **15. Frontier: past the dataflow limit, safely.** Value prediction (Lipasti, Wilkerson and Shen, 1996) in the limit
  study: perfect prediction of every load would give +19% (3.34 → 3.98), a stride predictor loses at every confidence
  threshold (its confident guesses are 60–90% right); Perais and Seznec (2014). Secure speculation: our rule (a load
  in the shadow of an unresolved branch keeps its value until every older branch has executed, in the spirit of STT
  and NDA, 2019) blocks the gadget and costs 3.5% on the Job; open questions: proofs (speculative non-interference),
  the cost floor, other channels, and the parallelism still unused.
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs8.compute            # every number in the part (about half an hour on four cores: the sweep and the Job's fit are slow)
python tools/build.py cs8 -q l             # a 480p preview
python tools/build.py cs8                  # 1080p
```

The core runs about 35,000 instructions a second, so the corpus is projected, as in Part 7, from passages. Ledger
rows 0 to 2 are written to `.cache/cs8/ledger.json`. The ledger keeps Part 7's clock; a real out-of-order core needs
more pipeline stages to hold it, which the scenes say.

## Problems, with solutions

1. **Work and span.** Draw the dataflow graph of `lw a0, 0(s0)`; `lw a1, 4(s0)`; `add a2, a0, a1`; `mul a3, a2, a2`;
   `add a4, a0, a3` (load 2 cycles, multiply 3, add 1). Find L, and check max(N/W, L) ≤ T_W ≤ N/W + L for W = 1, 2.

   *Solution.* Edges: both loads → `add a2`; `add a2` → `mul`; `mul` → `add a4`; the first load → `add a4`. Earliest
   starts: loads 0, `add a2` 2, `mul` 3, `add a4` 6, finishing at 7, so **L = 7**, through either load, the add and the
   multiply. N = 5. W = 1: the loads at 0 and 1, the add at 3, the multiply at 4, the last add at 7: **T₁ = 8**, and
   max(5, 7) = 7 ≤ 8 ≤ 12. W = 2: both loads at 0, then as the critical path: **T₂ = 7**, and 7 ≤ 7 ≤ 9.5. The
   multiply dominates: more width cannot help.

2. **Renaming the textbook example.** Rename the example of chapters 3 and 4 into physical registers `p10`, `p11`, ….
   Which dependences survive?

   *Solution.* `lw p10, 0(s0)`; `lw p11, 4(s1)`; `mul p12, p11, a3`; `sub p13, p10, p11`; `div p14, p12, p10`;
   `add p15, p13, p11` (with a1 → p15 in the alias table at the end). Only the true dependences remain: the second
   load to the multiply, the subtract and the add; the first load to the subtract and the divide; the multiply to the
   divide; the subtract to the add. The write-after-read between the divide (reading the old `a1`) and the add
   (writing the new one) is gone, because they now name `p10` and `p15`. This is why Tomasulo's add broadcast in cycle
   10 and the scoreboard's waited until 22.

3. **Mispredictions and the window.** A core mispredicts once every 40 instructions, has CPI 0.3 with perfect
   prediction and a 15-cycle penalty. What is its CPI? About how much of a 512-entry window does it use?

   *Solution.* CPI = 0.3 + (1/40) × 15 = **0.675**: wrong guesses take 56% of the time. Between two wrong guesses the
   core runs about 40 right-path instructions, so the useful part of the window is of that order, **under a tenth of
   512**; the rest fills with wrong-path work or stays empty. The window pays only during long-latency misses, which
   is exactly why real cores are built so large (chapter 13); otherwise prediction matters more. Our core on the Job:
   one per 37, P ≈ 7.9, CPI 0.317 + 0.212.

4. **Why the mask works.** Why does the index mask stop Spectre although the bounds check is still mispredicted? For
   an array of size 2ᵏ, why is `x & (size - 1)` not a complete fix?

   *Solution.* The mask is computed from x and the bound by `sltu`, `sub` and `and`: arithmetic, with a data
   dependence on the bound, not a control dependence. The core speculates on branches, not on data, so on the wrong
   path the masked index is the true result of the comparison: 0 whenever x ≥ size. The secret is never loaded. (A
   core with value prediction could break this, which is one reason value prediction worries security researchers.)
   `x & (size - 1)` keeps every index inside an array of exactly 2ᵏ bytes, so it is safe there; but if the array is
   shorter than the power of two it occupies (size 10 in a 16-byte block), indices 10 to 15 still reach whatever lies
   after it. And an optimizing compiler that can prove x < size on the architectural path may delete the mask
   altogether, which is why Linux's `array_index_nospec` is written so that the compiler cannot see through it.

5. **Build: Part 7's fix, out of order.** Part 7's problem 5 moved the load in the scan loop above the end-of-table
   test, hiding the load-use bubble and saving 4.4% on the pipeline. Make the same change and run chapter 1 on our
   out-of-order core. What does it save now, and why?

   *Solution.* In `JOB_V0`, swap `beq a2, s1, insert` and `lw t1, 4(t0)` at `scan` (the load may now run one entry
   past the end of the table, which is harmless: the slot is empty memory). On the core: **437,580 → 437,072 cycles,
   0.1%**, for 331 more instructions; the output is unchanged. The out-of-order core already starts the load as soon
   as `t0` is known, whatever its place in the code, so a compiler's static reordering buys almost nothing: the
   scheduling the compiler did by hand for the pipeline, the hardware does for itself. What limits the core is the
   length test's mispredictions, which no reordering removes.

6. **★ Research: how cheap can safe speculation be?** Our secure rule blocks the gadget for 3.5% on the Job. Does it
   block every speculative leak through the cache in our model? Find a program where it costs more than 30%, and a
   rule that blocks the same leaks for less.

   *What is known, and where to start.* This is open in general. The rule is `OutOfOrder(..., secure=True)`; the
   gadget is `programs.spectre`, and `compute._spectre(secret, secure=True)` returns the probe times. Two observations
   to begin with. (a) The rule delays loads' *values*, not loads: a speculative load still fills the cache with the
   line it reads. That is safe only if the load's *address* cannot depend on speculatively loaded data, which the rule
   guarantees because the address's producers are held back; a proof would show that every cache fill on a wrong path
   is at an address computed from non-speculative values (the "speculative non-interference" of Guarnieri et al.,
   S&P 2020, makes this precise for programs). (b) The rule is expensive where loads feed loads under hard branches:
   a pointer chase whose loop body branches on each node's value costs **23%** under the rule (19,378 → 23,919 cycles,
   3,000 nodes). Longer chains and less predictable branches push it higher. Cheaper rules from the literature:
   Speculative Taint Tracking (Yu et al., MICRO 2019) releases a value as soon as the *loads that produced it* are
   non-speculative, not every older branch; NDA (Weisse et al., MICRO 2019) offers a family of such policies;
   InvisiSpec (Yan et al., MICRO 2018) lets speculative loads run but hides their cache fills until they are safe;
   Speculative Privacy Tracking (Choudhary et al., MICRO 2021) lets values flow when the program would have leaked
   them anyway. A careful answer implements one of these in `ooo.py`, shows the gadget still blocked, and reports
   the cost on the Job, the pointer chase and the histogram of chapter 8.

## 习题与解答

1. **工作量与跨度。** 画出 `lw a0, 0(s0)`、`lw a1, 4(s0)`、`add a2, a0, a1`、`mul a3, a2, a2`、`add a4, a0, a3` 的数据流图（取数
   2 个周期，乘法 3 个，加法 1 个）。求 L，并对 W = 1、2 验证 max(N/W, L) ≤ T_W ≤ N/W + L。

   *解答。* 边：两条取数 → `add a2`；`add a2` → `mul`；`mul` → `add a4`；第一条取数 → `add a4`。最早开始时间：取数 0，`add a2` 2，
   `mul` 3，`add a4` 6，在 7 结束，所以 **L = 7**。N = 5。W = 1：两条取数在 0 和 1，加法在 3，乘法在 4，最后的加法在 7，
   **T₁ = 8**，且 max(5, 7) = 7 ≤ 8 ≤ 12。W = 2：两条取数都在 0，然后沿关键路径走：**T₂ = 7**，且 7 ≤ 7 ≤ 9.5。乘法占了主导：再宽
   也没用。

2. **给教科书的例子重命名。** 把第 3、4 章的例子重命名到物理寄存器 `p10`、`p11`……哪些依赖还在？

   *解答。* `lw p10, 0(s0)`；`lw p11, 4(s1)`；`mul p12, p11, a3`；`sub p13, p10, p11`；`div p14, p12, p10`；`add p15, p13, p11`。
   只剩真依赖：第二条取数到乘法、减法和加法；第一条取数到减法和除法；乘法到除法；减法到加法。除法（读旧的 `a1`）和加法（写新的
   `a1`）之间的读后写消失了，因为它们现在分别叫 `p10` 和 `p15`。这就是为什么托马苏洛算法里加法在第 10 周期广播，而记分牌要等到第
   22 周期。

3. **预测错误与窗口。** 一个核每 40 条指令猜错一次，完美预测时 CPI 为 0.3，代价 15 个周期。它的 CPI 是多少？512 项的窗口大约用了
   多少？

   *解答。* CPI = 0.3 + (1/40) × 15 = **0.675**：猜错占了 56% 的时间。两次猜错之间，核大约执行 40 条正确路径上的指令，所以窗口中
   有用的部分就是这个量级，**不到 512 的十分之一**；其余的装着错误路径上的工作，或者空着。窗口只在长延迟的缺失期间才划算，这正是
   真实的核做得这么大的原因（第 13 章）；除此之外，预测更重要。我们的核跑任务：每 37 条一次，P ≈ 7.9，CPI 0.317 + 0.212。

4. **掩码为什么有效。** 边界检查仍然被猜错，为什么下标掩码能挡住幽灵攻击？对大小为 2ᵏ 的数组，为什么 `x & (size - 1)` 不是完整的
   修复？

   *解答。* 掩码由 x 和边界通过 `sltu`、`sub`、`and` 算出：这是算术，对边界是数据依赖，而不是控制依赖。核对分支做推测，对数据不做，
   所以在错误路径上，掩码后的下标就是比较的真实结果：只要 x ≥ size 就是 0。秘密从不会被读出。（有数值预测的核可能打破这一点，这也是
   安全研究者担心数值预测的一个原因。）`x & (size - 1)` 把每个下标都限制在恰好 2ᵏ 字节的数组之内，所以在那里是安全的；但如果数组比它
   所占的二的幂短（16 字节块里只有 10 字节），下标 10 到 15 仍然能碰到数组后面的东西。而且优化编译器如果能证明在体系结构路径上
   x < size，可能把掩码整个删掉，所以 Linux 的 `array_index_nospec` 写得让编译器看不穿。

5. **动手：第 7 部分的修复，放到乱序核上。** 第 7 部分的第 5 题把扫描循环里的取数移到"表结束了吗"的检查之前，藏起取数—使用气泡，在
   流水线上省下 4.4%。做同样的改动，在乱序核上运行第 1 章。现在省下多少？为什么？

   *解答。* 在 `JOB_V0` 里，把 `scan` 处的 `beq a2, s1, insert` 和 `lw t1, 4(t0)` 对调（取数现在可能越过表尾一个条目，这无害：那个
   位置是空内存）。在核上：**437,580 → 437,072 个周期，0.1%**，多执行 331 条指令；输出不变。乱序核一旦知道 `t0` 就会发出这条取数，
   不管它在代码里排在哪里，所以编译器的静态重排几乎什么也换不来：编译器替流水线手工做的调度，硬件自己就做了。限制这个核的是长度检查的
   预测错误，任何重排都去不掉。

6. **★ 研究题：安全的推测能有多便宜？** 我们的安全规则以任务上 3.5% 的代价挡住了这个攻击片段。在我们的模型里，它能挡住所有通过
   缓存的推测泄露吗？找一个让它的代价超过 30% 的程序，再找一条代价更低、挡住同样泄露的规则。

   *已知什么，从哪里入手。* 一般情况下这是开放问题。规则是 `OutOfOrder(..., secure=True)`；攻击片段是 `programs.spectre`，
   `compute._spectre(secret, secure=True)` 返回探测时间。先看两点。（a）这条规则推迟的是取数的*值*，不是取数本身：推测执行的取数仍然
   会把它读的那一行装进缓存。这只有在取数的*地址*不可能依赖推测读出的数据时才安全，而规则保证了这一点，因为地址的生产者被扣住了；
   证明需要说明错误路径上的每一次缓存填充都发生在由非推测值算出的地址上（Guarnieri 等人在 S&P 2020 提出的"推测非干涉"对程序给出了
   精确的表述）。（b）在难预测的分支下、取数喂取数的地方，这条规则很贵：一个循环体按每个节点的值分支的指针追逐，在规则下代价 **23%**
   （19,378 → 23,919 个周期，3,000 个节点）。更长的链、更难预测的分支会让它更高。文献中更便宜的规则：推测污点追踪（Yu 等，MICRO 2019）
   在*产生该值的取数*不再是推测的时候就放行，而不是等所有更早的分支；NDA（Weisse 等，MICRO 2019）给出了一族这样的策略；InvisiSpec
   （Yan 等，MICRO 2018）让推测的取数执行，但把它们的缓存填充藏起来，直到安全；推测隐私追踪（Choudhary 等，MICRO 2021）在程序本来就会
   泄露这些值时让它们流动。一个认真的回答应当在 `ooo.py` 里实现其中之一，证明攻击片段仍被挡住，并报告在任务、指针追逐和第 8 章计数
   程序上的代价。

## Glossary additions

乱序执行 out-of-order execution · 数据流图 dataflow graph · 关键路径 critical path · 工作量与跨度 work and span · 指令级并行
instruction-level parallelism (ILP) · 真依赖 true dependence · 反依赖 anti-dependence (WAR) · 输出依赖 output dependence (WAW) ·
寄存器重命名 register renaming · 寄存器别名表 register alias table (RAT) · 物理寄存器 physical register · 空闲列表 free list ·
记分牌 scoreboard · 保留站 reservation station · 公共数据总线 common data bus · 标签 tag · 托马苏洛算法 Tomasulo's algorithm ·
重排序缓冲区 reorder buffer (ROB) · 提交 / 退休 commit / retire · 不精确异常 imprecise exception · 发射队列 issue queue · 唤醒与选择
wakeup and select · 超标量 superscalar · 指令窗口 instruction window · 极限研究 limit study · 推测执行 speculative execution ·
错误路径 wrong path · 预测错误代价 misprediction penalty · 取数队列 / 存数队列 load queue / store queue · 存数到取数转发 store-to-load
forwarding · 内存消歧 memory disambiguation · 内存顺序违例 memory-order violation · 等待表 wait table · 存储集 store sets · 机器清除
machine clear · 侧信道 side channel · 冲刷+重载 Flush+Reload · 幽灵 Spectre · 熔断 Meltdown · 推测屏障 speculation barrier · 下标掩码
index masking · 超长指令字 VLIW · 显式并行指令计算 EPIC · 软件流水 software pipelining · 启动间隔 initiation interval · 精简指令集
RISC · 复杂指令集 CISC · 微操作 micro-op · 宏融合 macro-fusion · 同时多线程 simultaneous multithreading (SMT) · 超线程
Hyper-Threading · 数值预测 value prediction · 安全推测 secure speculation · 推测污点追踪 speculative taint tracking · 推测非干涉
speculative non-interference · 超前执行 runahead execution

## Sources

The reading list is split, as the research tier asks (videos/cs/SYLLABUS.md §1.1), into the qualifying-exam canon and
recent work.

*Canon.* Books: Hennessy & Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed., ch. 3 (the scoreboard
example and its latencies, Tomasulo's algorithm, the reorder buffer, multiple issue, limits of ILP, SMT); Shen &
Lipasti, *Modern Processor Design*, ch. 4–9; Thornton, *Design of a Computer: The Control Data 6600* (1970); Fog, *The
microarchitecture of Intel, AMD and VIA CPUs* (updated yearly).

Papers: Graham, "Bounds for certain multiprocessing anomalies", Bell System Technical Journal (1966); Tomasulo, "An
efficient algorithm for exploiting multiple arithmetic units", IBM J. R&D (1967); Riseman & Foster, "The inhibition of
potential parallelism by conditional jumps", IEEE Trans. Computers (1972); Keller, "Look-ahead processors", Computing
Surveys (1975); Patterson & Ditzel, "The case for the reduced instruction set computer", Computer Architecture News
(1980); Fisher, "Trace scheduling: a technique for global microcode compaction", IEEE Trans. Computers (1981); Rau &
Glaeser, "Some scheduling techniques and an easily schedulable horizontal architecture", MICRO (1981); Smith &
Pleszkun, "Implementation of precise interrupts in pipelined processors", ISCA (1985); Lam, "Software pipelining",
PLDI (1988); Wall, "Limits of instruction-level parallelism", ASPLOS (1991); Tullsen, Eggers & Levy, "Simultaneous
multithreading: maximizing on-chip parallelism", ISCA (1995); Lipasti, Wilkerson & Shen, "Value locality and load
value prediction", ASPLOS (1996); Yeager, "The MIPS R10000 superscalar microprocessor", IEEE Micro (1996); Moshovos,
Breach, Vijaykumar & Sohi, "Dynamic speculation and synchronization of data dependences", ISCA (1997); Chrysos & Emer,
"Memory dependence prediction using store sets", ISCA (1998); Kessler, "The Alpha 21264 microprocessor", IEEE Micro
(1999).

*Recent.* Mutlu, Stark, Wilkerson & Patt, "Runahead execution", HPCA (2003); Yarom & Falkner, "FLUSH+RELOAD", USENIX
Security (2014); Perais & Seznec, "Practical data value speculation for future high-end processors", HPCA (2014);
Kocher et al., "Spectre attacks: exploiting speculative execution", IEEE S&P (2019); Lipp et al., "Meltdown: reading
kernel memory from user space", USENIX Security (2018); Yan et al., "InvisiSpec", MICRO (2018); Yu et al.,
"Speculative taint tracking (STT)", MICRO (2019); Weisse et al., "NDA: preventing speculative execution attacks at
their source", MICRO (2019); Guarnieri et al., "Spectector: principled detection of speculative information flows",
IEEE S&P (2020); Choudhary et al., "Speculative privacy tracking (SPT)", MICRO (2021).

Core data (chapter 13): Intel and AMD disclosures as reported in their optimization manuals and at Hot Chips; the
Apple M1's window is not published and is quoted from Dougall Johnson's measurements and AnandTech's analysis.
