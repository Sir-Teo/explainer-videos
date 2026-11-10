# Computer Science, Built — Part 15: Runtimes

Part 15 closes Act III of the sixty-one-part course ([plan](../README.md), [syllabus](../SYLLABUS.md)).
Build the machinery beneath functions: environments and closures, continuations, bytecode dispatch,
allocation and collection. Then compare selected mechanisms with real runtimes on the current host.
The instruments live in `explainer/cs/runtime/`; `compute.py` records the data and versions, and
`measurements.py` defines auditable observation and benchmark protocols.

- **Opening:** the Job allocates temporary lists and pairs. Its displayed live peak is a collection sample,
  not an every-instruction liveness maximum.
- **1. Interpreters:** eval/apply, environments and a metacircular evaluator. Fibonacci timings are
  best-of-three process-internal measurements, not a ranking of languages.
- **2. Closures:** lexical versus dynamic scope, escaping captures and closure conversion. Heap allocation
  is our implementation choice; scope and storage are distinct.
- **3. Continuations:** direct, CPS and accumulator factorials. Counts are logical reference-VM slots and
  exclude Python big-integer storage/time. Proper tail calls bound a tail-call chain; the Job's non-tail
  `bump` recursion still grows with vocabulary. `call/cc` changes control without undoing arbitrary effects.
- **4. Bytecode:** the stack instruction set, compiled `bump`, opcode mix, and stack versus register VMs.
  Pebble has 32-bit tagged words with a signed 31-bit integer payload; the Python VM uses unbounded integers.
- **5. Pebble VM:** actual source, tested in-range cosimulation, dispatch order and native C dispatch timing.
  Agreement on the examples supports finite implementation checks, not universal equivalence.
- **6. Reference counting:** reachability, zero-count cascades, cycles, and instrumented pointer-update traffic.
  A cascade can pause; Rust `Rc` is non-atomic whereas `Arc` supports sharing with atomics.
- **7. Tracing:** mark–sweep, fragmentation, compaction and four collectors with equal reserved capacity.
  Work columns use the stated model's word operations, which need not cost equal native time.
- **8. Cheney:** copying, actual forwarding locations, updated roots/fields and scan/free pointers.
  The approximation `L/(S-L)` counts copying, excluding root scans, bookkeeping and finite-run boundaries.
- **9. Generations:** last-observed-live ages and end censoring, an unobserved-but-live result witness,
  nursery sizes and actual promoted-word/consumed-word ratios. A major already empties the nursery.
- **10. Concurrent collection:** the same pointer moves under no, insertion and deletion barriers;
  root/allocation policies; randomized checks. JVM and Go pause logs use explicit, different heap policies.
- **11. JITs:** version-specific tiers, inline-cache measurements with an explicit logarithmic axis,
  hidden classes and actual deoptimization trace excerpts. An enabled tier need not improve a short run.
- **12. Dispatch/exceptions:** vtables and interface/multiple dispatch. The native benchmark uses defined
  unsigned arithmetic, checked results, opaque boundaries, disabled devirtualization and an assembly witness.
  Table-driven exceptions move costs off handler entry; they do not remove all metadata/optimization costs.
- **13. Other machines:** a hand-assembled WebAssembly module and actual validation failure. Branching to a
  block exits; branching to a loop restarts its header. Specification verification is separate from engine
  verification; isolation also needs runtime bounds checks and host policy. Prolog, actors and dataflow follow.
- **14. The Job:** exact emulator counts for six passages, sampled IPC and projected ledger row 6.
  Collector instruction share is not automatically the same fraction of wall time or cycles.
- **15. Frontier:** scoped historical memory/time results, established real-time bounds and precise extensions,
  fixed-program specialization, meta-tracing, warmup evidence and integration of verified runtime components.

## Build

```bash
python -m videos.cs.cs15.compute           # every number in the part (about ten minutes; the ledger item is most of it)
python tools/build.py cs15 -q l            # a 480p preview
python tools/build.py cs15                 # 1080p
```

`interp`, `vm`, `rc`, `pauses`, `jit`, `dispatch` and `wasm` run gcc, g++, java, go, node and CPython on this machine;
their timings belong to the computer that runs them. Pebble instruction counts are exact for the executed
examples; sampled IPC and whole-corpus runtime projections retain their stated assumptions. Native subprocess
failures propagate rather than becoming cached timing text. Preserve or regenerate current schemas with
`--force cps tracing gen pauses dispatch jit` after this correction.

## Problems, with solutions

1. **Closure conversion.** Closure-convert `let twice f = let g = fun x -> f (f x) in g` by hand: find the free
   variables, and write the `CLOSURE` and `FREE` code our compiler would emit.

   *Solution.* `twice` has one parameter, f (slot 0). The inner function's only free variable is f, so `twice`
   pushes it and builds a closure with one captured value: `LOCAL 0; CLOSURE g, 1 free; SETLOCAL 1; LOCAL 1;
   RET`. Inside g (parameter x in slot 0), each use of f reads the closure: `FREE 0` (the outer f), `FREE 0`,
   `LOCAL 0`, `CALL 1` (the inner `f x`), then `TAILCALL 1` for the outer call, which is in tail position. f is
   not a known function, so each call passes one argument. Our compiler emits exactly this (`p.listing("twice")`),
   and `twice (fun y -> y + 1) 5` gives 7.

2. **Three sums.** Rewrite `sum` over a list in CPS and with an accumulator; give each version's stack depth and
   heap use for n elements.

   *Solution.* Direct `sum (h :: t) = h + sum t` keeps Θ(n) pending frames. CPS
   `sum_k (h :: t) k = sum_k t (fun s -> k (h + s))` uses tail calls and O(1) stack, but
   allocates n continuation closures. In this VM each captures h and k: a header, code slot and
   two captures, so 4n words plus constant setup. `sum_a (h :: t) acc = sum_a t (acc + h)`
   uses O(1) stack and no extra heap objects beyond input/setup. “No extra heap” excludes the already
   built input, startup closures and host big-integer storage. The reported 4,002-word example is
   4n + 2, not exactly 4n. Reassociation is valid in the exact-integer model; floating point or
   checked-overflow semantics require separate justification. CPS makes pending work explicit
   without requiring an associative operator.

3. **Cheney by hand.** From-space holds, in address order, a pair p = (c1, 7); cells c1 = 1 :: c2, d1 = 9 :: d2,
   c2 = 2 :: c3, d2 = 8 :: [], c3 = 3 :: []; and a closure k capturing d1. The roots point at p and c2. Run Cheney's
   algorithm, giving the to-space order and every forwarding address.

   *Solution.* Roots first, in order: p is copied to to-space address 0 (every object here is 3 words: a header and
   two fields), c2 to 3; forwarding addresses are written into their old copies. Scan p: its field c1 is not yet
   copied, so c1 goes to 6. Scan c2: c3 goes to 9. Scan c1: its tail c2 is already forwarded (to 3), so the field
   is just updated. Scan c3: nothing. Scan meets free at 12: done. To-space order p, c2, c1, c3; forwarding
   addresses p → 0, c2 → 3, c1 → 6, c3 → 9. d1, d2 and k are never touched. (`cheney_trace` in `compute.py`
   reproduces this.)

4. **Two cost models.** Derive the work per allocated word of a copying collector and of mark–sweep, with live data
   L in the same total memory M; compare at M = 2L, 4L and 8L.

   *Solution.* Copying uses two semispaces of M/2. Each collection copies L words and frees M/2 − L for
   allocation: L / (M/2 − L). Mark–sweep marks L words and sweeps all M, then frees M − L: (L + M) / (M − L)
   (taking marking and sweeping a word as equal). At M = 2L, copying cannot run at all (M/2 = L), while mark–sweep
   costs 3. At 4L: copying 1, mark–sweep 5/3. At 8L: copying 1/3, mark–sweep 9/7. Copying wins once memory is
   plentiful, because it never touches garbage; mark–sweep works in tight memory and never moves an object. The
   Job's measurements (`cost`) follow the copying curve.

5. **Build: a nursery for the Pebble VM.** Give the Pebble VM a nursery, in the Pebble language, and measure the Job.
   Why does the λ-core need no write barrier?

   *Solution sketch.* Reserve a nursery plus two old semispaces. A minor copies nursery survivors
   into old space; a major copies both reachable regions and already empties the nursery. Do not count a
   second zero-work minor afterward. Under this core's complete-initialization, immutable-field and
   promotion rules there are no old-to-young mutation edges. Adding mutable fields requires a remembered
   set/barrier; lazy or runtime updates need their own treatment. Compare equal total capacity, and report
   promoted **words / actually consumed nursery words**, not an object fraction.

   Measure the implemented Pebble nursery rather than turning reference-collector word savings into a
   guaranteed native speedup. If an instruction-cost model has fraction f attributable to collection and
   a measured new collector instruction ratio r, its conditional Amdahl speedup is `1/(1-f+f*r)`.
   Neither f nor r is automatically a wall-time fraction.

6. **★ Research: extend a known real-time collector bound.** State a machine, mutator, root, object-size,
   allocation-rate and liveness model. Choose an established result and formulate one precise improvement
   or a matching lower-bound question under those assumptions.

   *Where to start.* The [Blelloch–Cheng 1999 author abstract](https://www.cs.cmu.edu/~scandal/papers/pldi99.html)
   already reports space `2(R(1+2/k)+N+5PD)` and stops proportional to k nonblocking machine instructions:
   R is maximum reachable space, N maximum reachable object count, D maximum object depth, P processors,
   and k copying work per allocated location. These quantities matter; “bounded pause, constant-factor
   space, constant work” without a model is not one established unsolved theorem. Read the full construction
   before attempting a proof extension. Possible projects include measuring constants on a specified
   immutable-core collector, investigating a different root policy or scheduler, or proving a bound for
   a clearly delimited object/machine model. Distinguish experiments, conjectures and proven results.

## 习题与解答

1. **闭包转换。** 手工对 `let twice f = let g = fun x -> f (f x) in g` 做闭包转换：找出自由变量，写出我们的编译器会生成的
   `CLOSURE` 与 `FREE` 代码。

   *解答。* `twice` 有一个参数 f（槽 0）。内层函数唯一的自由变量是 f，所以 `twice` 先把它压栈，再建一个捕获一个值的闭包：
   `LOCAL 0; CLOSURE g, 1 free; SETLOCAL 1; LOCAL 1; RET`。在 g 内部（参数 x 在槽 0），每次用到 f 都从闭包里读：
   `FREE 0`（外层的 f）、`FREE 0`、`LOCAL 0`、`CALL 1`（内层的 `f x`），然后外层调用处于尾位置，用 `TAILCALL 1`。
   f 不是已知函数，所以每次调用只传一个参数。我们的编译器生成的正是这些（`p.listing("twice")`），
   `twice (fun y -> y + 1) 5` 得 7。

2. **三种求和。** 把列表上的 `sum` 改写成 CPS 形式和带累加器的形式；给出每个版本对 n 个元素的栈深度和堆用量。

   *解答。* 直接形式每个元素保留一个待做加法的帧，栈为 Θ(n)。CPS 用尾调用，栈为 O(1)，但创建 n 个续延闭包；
   在本虚拟机中，每个闭包有头、代码槽以及 h 和 k 两项捕获，共 4 个字，因此是 4n 加常数启动量。累加器版本使用 O(1) 栈，
   除输入和启动对象外不再创建堆对象。“不再分配”不包含已有输入、启动闭包及宿主大整数存储。4,002 个字的例子是 4n + 2，
   不恰好是 4n。精确整数模型允许加法重结合；浮点或检查溢出语义需要另外论证。CPS 显式保存待做工作，无须运算满足结合律。

3. **手算切尼算法。** 来源空间按地址顺序存放：序对 p = (c1, 7)；单元 c1 = 1 :: c2、d1 = 9 :: d2、c2 = 2 :: c3、
   d2 = 8 :: []、c3 = 3 :: []；以及捕获 d1 的闭包 k。根指向 p 和 c2。运行切尼算法，给出目标空间的顺序和每个转发地址。

   *解答。* 先按顺序处理根：p 复制到目标空间地址 0（这里每个对象 3 个字：一个头和两个字段），c2 复制到 3；
   旧副本中写入转发地址。扫描 p：字段 c1 尚未复制，于是 c1 复制到 6。扫描 c2：c3 复制到 9。扫描 c1：它的尾 c2
   已经转发（到 3），只需更新字段。扫描 c3：什么也没有。scan 追上 free（12）：完成。目标空间顺序为 p、c2、c1、c3；
   转发地址 p → 0、c2 → 3、c1 → 6、c3 → 9。d1、d2 和 k 从未被碰过。（`compute.py` 中的 `cheney_trace` 复现了这一过程。）

4. **两个代价模型。** 设活数据为 L，总内存同为 M，推导复制收集器与标记–清除每分配一个字的工作量；比较 M = 2L、
   4L、8L 时的情形。

   *解答。* 复制收集器用两个 M/2 的半空间。每次收集复制 L 个字，并为分配腾出 M/2 − L：L / (M/2 − L)。标记–清除标记 L
   个字，清扫全部 M，腾出 M − L：(L + M) / (M − L)（把标记一个字和清扫一个字看作同价）。M = 2L 时复制收集器根本
   无法运行（M/2 = L），而标记–清除的代价是 3。4L 时：复制 1，标记–清除 5/3。8L 时：复制 1/3，标记–清除 9/7。
   内存充裕时复制收集器胜出，因为它从不碰垃圾；标记–清除能在紧张的内存里工作，而且从不移动对象。作业的实测数据
   （`cost`）符合复制收集器的曲线。

5. **动手：给 Pebble 虚拟机加一个新生代。** 用 Pebble 语言给 Pebble 虚拟机加一个新生代（nursery），并测量作业。
   为什么 λ 核心不需要写屏障？

   *解答要点。* 预留新生代和两个老年代半空间。次收集把新生代存活对象复制到老年代；主收集复制两区中的可达对象，
   已经清空新生代，不应再记录一次零工作的次收集。在这里的完整初始化、不可变字段和晋升规则下，没有老对象写入年轻指针的边。
   增加可变字段时，需要记忆集和屏障；惰性及运行时更新也要单独处理。比较相等总容量，报告“晋升字数 / 实际消耗的新生代字数”，
   不要把它称为对象比例。应当测量实际 Pebble 实现，不能把参考模型节省的字数直接当成保证的本机加速。
   若指令代价模型中收集占比为 f，新收集器的实测指令比例为 r，则条件性的阿姆达尔加速为 `1/(1-f+f*r)`；两者都不自动等于墙钟比例。

6. **★ 研究：扩展一项已知实时收集器界。** 说明机器、变异器、根、对象大小、分配速率和活数据模型，选择已有结果，
   在这些假设下提出一项精确改进或匹配下界问题。

   *从哪里开始。* [布莱洛赫与程一九九九年的作者摘要](https://www.cs.cmu.edu/~scandal/papers/pldi99.html)
   已给出空间界 `2(R(1+2/k)+N+5PD)`，以及与 k 成正比的非阻塞机器指令停顿界。R 是最大可达空间，N 是最大可达对象数，
   D 是最大对象深度，P 是处理器数，k 是每分配一个位置所做的复制工作。这些量不能省略；没有模型的三项目标不是一个已确立的
   未解决定理。尝试扩展证明前先阅读完整构造。可以测量指定不可变核心收集器的常数，研究不同的根策略或调度，或为明确限定的
   对象和机器模型证明界。清楚区分实验、猜想和已经证明的结果。

## Glossary additions

运行时 runtime · 解释器 interpreter · 求值 / 应用 eval / apply · 元循环求值器 metacircular evaluator · 环境
environment · 词法作用域 / 动态作用域 lexical / dynamic scope · 闭包 closure · funarg 问题 funarg problem · 闭包转换
closure conversion · 扁平闭包 / 链式闭包 flat / linked closure · 续延 continuation · 续延传递风格 continuation-passing
style (CPS) · 尾调用 tail call · call/cc · CEK 机 CEK machine · 字节码 bytecode · 虚拟机 virtual machine · 栈式机 /
寄存器机 stack / register machine · 分派 dispatch · 线索代码 threaded code · 标签字 tagged word · 部分应用 partial
application · 垃圾回收 garbage collection · 根 root · 可达 reachable · 引用计数 reference counting · 延迟引用计数
deferred reference counting · 标记–清除 mark–sweep · 标记–压缩 mark–compact · 碎片 fragmentation · 复制收集器 copying
collector · 半空间 semispace · 转发地址 forwarding address · 代际假说 generational hypothesis · 新生代 nursery · 晋升
promotion · 写屏障 write barrier · 记忆集 remembered set · 卡表 card marking · 三色标记 tri-color marking · 强 / 弱三色不变式
strong / weak tri-color invariant · 增量更新 incremental update · 起始快照 snapshot at the beginning · 浮动垃圾 floating
garbage · 停顿 pause · 最小变异器利用率 minimum mutator utilization · 即时编译 just-in-time compilation · 分层编译
tiered compilation · 内联缓存 inline cache · 多态内联缓存 polymorphic inline cache · 隐藏类 hidden class · 推测
speculation · 去优化 deoptimization · 追踪 JIT tracing JIT · 虚函数表 vtable · 多分派 multiple dispatch · 零开销异常
zero-cost exceptions · WebAssembly · 验证 validation · 消解 resolution · 参与者 actor · 数据流 dataflow · 二村映射
Futamura projections · 预热 warmup

## Sources

*Canon.* Books: Abelson & Sussman, *Structure and Interpretation of Computer Programs*, chapters 4–5; Friedman &
Wand, *Essentials of Programming Languages*; Appel, *Compiling with Continuations* (1992); Jones, Hosking & Moss,
*The Garbage Collection Handbook*; Smith & Nair, *Virtual Machines*; Nystrom, *Crafting Interpreters*.

Papers: McCarthy, "Recursive functions of symbolic expressions and their computation by machine" (1960); Collins,
"A method for overlapping and erasure of lists" (1960); Landin, "The mechanical evaluation of expressions" (1964);
Moses, "The function of FUNCTION in LISP" (1970); Cheney, "A nonrecursive list compacting algorithm" (1970); Bell,
"Threaded code" (1973); Deutsch & Bobrow (1976); Steele, "Debunking the 'expensive procedure call' myth" (1977);
Dijkstra, Lamport, Martin, Scholten & Steffens, "On-the-fly garbage collection: an exercise in cooperation" (1978);
Lieberman & Hewitt, "A real-time garbage collector based on the lifetimes of objects" (1983); Ungar, "Generation
scavenging" (1984); Deutsch & Schiffman, "Efficient implementation of the Smalltalk-80 system" (1984); Felleisen &
Friedman, "Control operators, the SECD-machine, and the λ-calculus" (1986); Yuasa, "Real-time garbage collection on
general-purpose machines" (1990); Hölzle, Chambers & Ungar, "Optimizing dynamically-typed object-oriented languages
with polymorphic inline caches" (1991) and "Debugging optimized code with dynamic deoptimization" (1992); Shao &
Appel, "Space-efficient closure representations" (1994); Ertl & Gregg, "The structure and performance of efficient
interpreters" (2003); Ierusalimschy, de Figueiredo & Celes, "The implementation of Lua 5.0" (2005); Shi, Casey, Ertl
& Gregg, "Virtual machine showdown: stack versus registers" (2008); Rohou, Swamy & Seznec, "Branch prediction and the
performance of interpreters: don't trust folklore" (2015); Haas et al., "Bringing the web up to speed with
WebAssembly" (2017); Watt, "Mechanising and verifying the WebAssembly specification" (2018).

*Frontier.* Hertz & Berger, "Quantifying the performance of garbage collection vs. explicit memory management"
(2005); Bacon, Cheng & Rajan, "A real-time garbage collector with low overhead and consistent utilization" (2003);
Blelloch & Cheng, "On bounding time and space for multiprocessor garbage collection" (1999); Bendersky & Petrank,
"Space overhead bounds for dynamic memory management with partial compaction" (2011); Cohen & Petrank (2013);
Futamura, "Partial evaluation of computation process" (1971); Bolz, Cuni, Fijałkowski & Rigo, "Tracing the
meta-level: PyPy's tracing JIT compiler" (2009); Würthinger et al., "Practical partial evaluation for
high-performance dynamic language runtimes" (2017); Barrett, Bolz-Tereick, Killick, Mount & Tratt, "Virtual machine
warmup blows hot and cold" (2017); the CakeML project's verified garbage collector.
