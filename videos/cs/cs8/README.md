# Computer Science, Built — Part 8: Out of Order

Part 8 of the sixty-one-part course ([series plan](../README.md), [syllabus](../SYLLABUS.md)) studies dependency
scheduling, register renaming, retirement, speculation and memory ordering using an executable teaching model.
The functional core is `explainer/cs/pebble/ooo.py`; the offline trace scheduler is
`explainer/cs/pebble/limits.py`. These implement different scheduling models. `compute.py` produces the chapter's
numerical data, and `tests/test_cs8_ooo.py` checks selected configurations against the emulator.

## Chapter guide

- **Hook.** A one-entry issue queue forces in-order starts; increasing it to 64 exposes overlap and increases
  queue capacity together. The short cold-load example takes 81 versus 70 modeled cycles. On chapter 1, retired
  IPC is 0.78 versus 1.89; Part 7's 0.83 comes from a separate pipeline. Whole-run mean ROB occupancy is 10.7 of
  128 entries; the plot shows a 600-cycle sample, not a complete execution.
- **1. Dataflow.** Four scan trips have N = 24 instructions, weighted latency work A = 28 and span L = 6.
  The unlimited-unit scheduler limits new starts per cycle: widths 1, 2, 4, 8 take 24, 12, 7, 6 cycles.
  Its lower bound is max(⌈N/W⌉, L). Graham's nonpreemptive W-processor bound is separately
  T_G ≤ A/W + (1 − 1/W)L, using occupied processor time rather than start slots.
- **2. Renaming.** Source-operand uses and name-reuse events have explicit counting conventions. Distinct live
  versions remove register WAR/WAW hazards; physical registers are later reclaimed safely. The offline oracle's
  2,399 versus 3.68 IPC uses future paths, trace-supplied inputs and memory word addresses, unlimited resources,
  and omitted realistic device/I/O ordering. It is not a feasible hardware speedup or an algorithmic lower bound.
- **3–4. Scoreboard and Tomasulo.** Stage-specific hazards, reservation-station tags and broadcasts are animated
  through a textbook example (62 versus 56 cycles). In-order dispatch and finite station pressure still matter.
  Renaming alone does not provide precise architectural exceptions.
- **5. Reorder buffer.** The retirement ring and exception timeline separate architectural commit from physical
  execution/cache effects. Pebble deliberately faults on divide by zero; this differs from RISC-V M. The model's
  width W applies to fetch, rename and retirement, with up to W ALUs and two memory ports, W+2 total issue slots.
- **6. ILP limits.** Sensitivity bars and start-distance curves describe the offline scheduler. Its `window`
  constrains start times by instruction-index distance, not by the oldest unfinished instruction or a physical
  ROB. Functional-core width/capacity sweeps are a separate experiment; retired IPC is not slot utilization.
- **7. Speculation.** A recorded wrong path is squashed and fetched again. The chapter-1 tournament run counts
  22,296 redirects and 253,764 squashed renamed entries, including some wrong-path redirects; entries are not
  execution starts. The fitted effective penalty, about 7.9 cycles, is counterfactual configuration accounting.
  The 37 retired instructions per counted redirect do not determine ROB occupancy or a lookahead ceiling.
- **8. Memory ordering.** Byte-range overlap, youngest older stores, forwarding and late-address replay are
  distinguished. A fixed 1,500-sample histogram takes 97,740 / 7,652 / 7,408 cycles under conservative,
  speculative and wait-table policies; the speculative run has 23 dynamic violations. All three take 437,580
  cycles on chapter 1, with 154,835 loads and 5,270 stores covering counts, metadata and copied letters.
- **9. Spectre.** The simulated byte array places secret bytes outside a policy bound, without hardware permission
  isolation. The experiment flushes probes, trains six times (warming line 0), evicts the bound, executes a custom
  timer barrier, attacks, then times lines 1–255. Hit/miss intervals are 5/63 cycles; six rounds decode PEBBLE in
  109,424 cycles. The decoder excludes zero. Barrier, mask and control-shadow variants give all-63 tested probe
  intervals. This finite gadget result is not a proof against every channel. Barriers are ISA-specific; masking
  needs unsigned comparisons, a nonempty valid fallback and preserved dependencies.
- **10. VLIW.** Bundles and colored software-pipelined iterations illustrate resource/data schedules on a fixed
  path. They are not an executable control-flow translation: same-bundle operand versions, guards, exits and
  branches need ISA rules. Variable latency, interlocks and compatibility costs depend on the implementation.
- **11. RISC/CISC.** Runtime depends on instruction count, CPI and clock. `lw` plus a combined compare/branch can
  correspond to `cmp [mem]` plus `jne`: two instructions on each side. The 90,726 heuristic load-use/name-liveness
  candidates do not establish legal translations or instruction savings. Internal micro-ops are implementation
  operations, and load-operation micro-fusion differs from compare/branch macro-fusion.
- **12. SMT.** An offline two-trace start-slot schedule illustrates aggregate throughput (+40% at four slots,
  +80% at eight in the selected study). It is not a functional SMT core or a per-thread latency/fairness guarantee.
- **13. Core measurements.** A 1995–2024 historical selection uses differing counted units. Firestorm's estimated
  coalesced groups and rename-retire entries are shown separately. Widths at different stages, workload-dependent
  branch accuracy, physical memory delays and measurement definitions must be distinguished.
- **14. Job projection.** CPI components compare configurations rather than partition unique causes. A fit to 24
  passages uses encoded-byte features. The heldout 16,000-character passage is 16,019 bytes: 3,290,777 measured
  cycles versus 3,287,720 predicted (−0.09%). The corpus row projects 50,727,519,299 cycles, 57.32 seconds at an
  assumed 884.96 MHz, 2.52 times faster than the pipeline projection. No full-corpus run, error bound or physical
  out-of-order clock validation is supplied.
- **15. Frontier.** Value prediction needs accuracy, coverage, availability and recovery. Perfect load guesses
  improve the selected eight-slot oracle schedule by 19%; the stride heuristic loses at the shown thresholds.
  There is no universal 99% threshold. The control-shadow rule blocks this decoder at a 3.55% chapter-1 cost;
  STT, NDA, Dolma and ProSpeCT have distinct mechanisms, policies and proof scopes.
- **Outro.** Animated recap, course connections, practical tools, exercises and the next part's illustrative memory
  hierarchy. Matrix-multiplication data-movement bounds depend on the computation model and memory assumptions.

## Build and verification

```bash
python -m videos.cs.cs8.compute
python -m videos.cs.cs8.compute --force spectre  # refresh the corrected timer-site parser
python -m unittest discover -s tests -p test_cs8_ooo.py -q
python tools/build.py cs8 -q l
python tools/build.py cs8
```

The corpus is projected from passages. Ledger rows 0–2 live in `.cache/cs8/ledger.json`; the clock is an assumed
teaching budget inherited from Part 7. Host simulation throughput is not a silicon timing measurement.

The [9 November 2026 QA packet](../../../docs/qa/evidence/cs8-polish-20261109/README.md) binds the source/preview
checkpoint to bilingual captures, numerical witnesses, English speech signals, actual cue requests and selected
native/narrated clips. The Spectre parser now identifies the two timed probe instruction PCs: extra timer reads
inserted by fenced training previously shifted fixed-size chunks. Only `mitigations.fence.fast[0]` changes, 2 → 1;
simulated execution and all other numerical fields are unchanged. Continuous narrated listening, Chinese speech,
whole-video native review and production runtime approval remain open.

## Problems, with solutions

1. **Work and span.** Use `lw a0, 0(s0)`; `lw a1, 4(s0)`; `add a2, a0, a1`; `mul a3, a2, a2`;
   `add a4, a0, a3`, with load/multiply/add latencies 2/3/1. Find N, A and L, then distinguish the two width models.

   *Solution.* N = 5, A = 9, L = 7. Both loads feed the first add, then multiply, then final add; the first load
   also feeds the final add. With W new starts per cycle and otherwise unlimited resources, T₁ = 8 and T₂ = 7;
   each satisfies max(⌈N/W⌉, L) ≤ T_W. For W nonpreemptive processors occupied for the operation's full latency,
   greedy T_G is 9 at W = 1 and 7 at W = 2, within Graham's bounds 9 and 8 respectively.

2. **Renaming.** Rename the textbook example with p10, p11, ….

   *Solution.* `lw p10, 0(s0)`; `lw p11, 4(s1)`; `mul p12, p11, a3`; `sub p13, p10, p11`;
   `div p14, p12, p10`; `add p15, p13, p11`. True value dependencies survive. The divide reads the older p10
   while the add writes p15, removing the architectural-name WAR hazard. Reclaim names only when safe.

3. **Penalty accounting.** A defined model has perfect-prediction CPI 0.3, one miss per 40 retired instructions
   and an additive 15-cycle effective penalty. Determine CPI. Can these values determine ROB occupancy?

   *Solution.* CPI = 0.3 + 15/40 = 0.675. The additive term is 55.6% of this accounting total. It does not determine
   occupancy: dependency chains, unresolved-operation duration, fetch/issue/retire widths, recovery and memory
   behavior also matter. An average inter-miss instruction count is not a hard lookahead bound.

4. **Masking.** Compare a bound-dependent mask with `x & (size - 1)` for unsigned x and a nonempty 2ᵏ-byte array.

   *Solution.* In this model, `sltu`, `sub`, `and` make the dependent access wait for the bound comparison's value;
   invalid x maps to the valid fallback index 0. Modulo masking also stays inside that exact power-of-two array,
   but wraps invalid requests rather than validating them. For a shorter logical array it may expose invalid
   logical elements. Either mechanism needs the intended policy, valid fallback and compiler/ISA dependency
   guarantees. This model does not implement value prediction; general side-channel security needs a threat model.

5. **Hoist the scan load.** Repeat Part 7's transformation on chapter 1 after checking address/exception safety.

   *Solution.* The stored experiment takes 437,580 → 437,072 cycles (about 0.12%), with 331 extra retired
   instructions and unchanged output. The specified extra read stays in allocated model memory. Out-of-order
   scheduling already overlaps much of this load's latency; this result is conditional on the program, inputs,
   memory and prediction policy, and does not authorize arbitrary speculative loads.

6. **Research.** Define protected/public inputs, permitted observations and a non-speculative baseline. Search for
   a leak or a workload costing over 30% under `secure=True`, then compare a more selective rule.

   *Starting point.* The rule withholds completed load values while an older branch is unresolved; cache fills
   still occur. The supplied gadget's decoder fails, and a 3,000-node pointer chase costs 19,378 → 23,919 cycles
   (23.4%). Neither observation proves security, guarantees a larger slowdown on longer chains, nor predicts the
   cost of a literature design. Test counterexamples and overhead separately; a general proof needs the defined
   observation/threat model and full microarchitectural behavior.

## 习题与解答

1. **工作量与跨度。** 上述五条指令有 N = 5、A = 9、L = 7。每周期限制新启动数、其余资源无限时，T₁ = 8、T₂ = 7，
   满足 max(⌈N/W⌉, L) ≤ T_W。若 W 个处理器在指令整个延迟内被占用，则贪心调度分别为 9 和 7，Graham 上界分别为 9 和 8。
2. **重命名。** 依次使用 p10–p15，得到上面的指令序列。真实值依赖仍在；除法读取旧版本 p10，加法写入 p15，名称反依赖消失。
   物理名称只能在安全时回收。
3. **预测代价。** 指定加法记账模型给出 CPI = 0.3 + 15/40 = 0.675，附加项占总量 55.6%。这些平均数不能确定 ROB 占用；
   依赖、未完成操作、宽度、恢复和内存行为同样重要。
4. **掩码。** 无符号、非空且大小恰为 2ᵏ 字节时，两种掩码都把下标限制在数组内。依赖比较的掩码把无效请求映射到合法的零下标；
   模数掩码会回绕，并不验证原请求。较短逻辑数组仍可能暴露无效元素；还须保持编译器与 ISA 要求的数据依赖。
5. **提前取数。** 先证明指定额外读的地址与异常安全。该实验周期为 437,580 → 437,072，约省 0.12%，多退休 331 条指令，输出相同。
   乱序调度已重叠大部分延迟；结论受程序、输入、内存与预测策略约束。
6. **研究题。** 明确秘密、公开输入、可见观察与非推测基线，再寻找泄露反例或超过 30% 的开销。规则扣住取数值，却仍会填充缓存；
   指定攻击解码失败与一次指针追逐的 23.4% 开销都不是一般安全证明，也不能预测文献方案的成本。

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

Core data (chapter 13) are a historical selection, not a current-core survey. Counted operation units vary.
Apple Firestorm is separate: Dougall Johnson's reverse-engineered notes distinguish about 330 coalesced retire
groups from about 623 rename-retire entries. See [his notes](https://dougallj.github.io/applecpu/firestorm.html).

Additional research: Loughlin et al., *Dolma: Securing speculation with the principle of transient
non-observability*, USENIX Security (2021); Daniel et al., *ProSpeCT: Provably secure speculation for the
constant-time policy*, USENIX Security (2023). These are distinct mechanisms and threat models; this chapter's
control-shadow experiment reproduces neither complete design. The QA packet records exactly which primary
excerpts were inspected.
