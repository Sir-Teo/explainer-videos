# Computer Science, Built — Part 15: Runtimes

Part 15 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), closing Act III, *Speaking to the Machine*. A language needs somewhere to live:
environments make closures, continuations turn the stack into data, a bytecode machine runs the program, and a
garbage collector takes away what it no longer needs, while the program keeps running. The instruments are in
`explainer/cs/runtime/`: `bytecode.py` (the λ-core of Part 14 closure-converted and compiled to a 36-instruction stack
bytecode with flat closures, known-arity calls, partial applications and proper tail calls), `vm.py` (the reference
VM in Python, with tagged words and four collectors: Cheney's copying, mark–sweep, mark–compact and generational),
`pvm.py` (the same VM and Cheney's collector written in the Pebble language, compiled by Part 13's compiler and run
on the Pebble emulator, agreeing with the reference count for count), `tricolor.py` (incremental marking under a
hostile mutator, with and without write barriers), `cek.py` (a CEK machine with `callcc`) and `prolog.py` (resolution
and unification), tested in `tests/test_cs15_runtime.py`. Every number is computed in `compute.py`; chapters 1, 10,
11, 12 and 13 time real runtimes on this machine (CPython, V8, HotSpot, Go, gcc) and record their versions.

* **A program needs a place to live.** The Job allocates 369,855 words on Part 7's chapter (79 per byte) with at
  most 27,465 live at once; the heap fills and empties eight times.
* **1. Interpreters: eval and apply.** The eval/apply cycle; McCarthy's eval and Russell's interpreter; the
  metacircular evaluator; 357,894 applications for the Job; `fib(32)` on seven runtimes, from 2.9 ms (gcc) to
  165 ms (CPython).
* **2. Environments and closures.** Lexical against dynamic scope (1 against 10, both computed); the funarg problem;
  closures on the heap; closure conversion, `CLOSURE` and `FREE`; flat against linked closures.
* **3. Continuations and tail calls.** CPS factorial on our VM (5 words of stack and 1,004 closures, against 5,004
  words); the Job with and without tail calls (2,996 against 68,371 words of stack); `call/cc` as an early exit on
  a CEK machine (0 multiplications against 12); Peirce's law.
* **4. A bytecode virtual machine.** The instruction set; tagged words; `bump` compiled (37 instructions); the
  opcode mix (`LOCAL` and `SETLOCAL` are 53%); CPython's `dis`; stack against register machines.
* **5. The VM, on Pebble.** The VM in the Pebble language; co-simulation with the reference; 47 Pebble instructions
  per bytecode; dispatch order (47, 60, 100); switch against threaded code in C on this machine.
* **6. Why collect, and counting references.** Reachability; reference counting and its cascade; cycles, and
  CPython's cycle collector (199,998 objects found); what counting would cost the Job (about 11 updates per object).
* **7. Tracing: mark–sweep and mark–compact.** Marking and sweeping animated; fragmentation; compaction; four
  collectors on the Job in the same memory.
* **8. Cheney's copying collector, and what it costs.** The two-pointer algorithm, traced; work against heap size,
  measured and modelled by L/(S − L).
* **9. Generations.** 87% of the Job's objects never survive a collection; nurseries of six sizes; two thirds of
  Cheney's work in the same memory; the write barrier, and why the λ-core never needs it.
* **10. Collecting while the program runs.** The tri-color abstraction; a live object lost, move by move; strong and
  weak invariants, Dijkstra's and Yuasa's barriers (735 of 2,000 cycles lose an object without one, none with
  either); pauses of the JVM's four collectors and Go's on this machine (155 ms to 20 µs).
* **11. Just-in-time compilers.** V8's four tiers (148 ms to 18 ms); inline caches against the number of shapes
  (6× slower at 32); hidden classes; a deoptimization traced; tracing JITs.
* **12. Dynamic dispatch and exceptions.** Vtables (0.5 ns direct, 1.0 ns virtual); interfaces and multiple
  dispatch; zero-cost exceptions (`try` free, `throw` about 900 ns) against `setjmp`.
* **13. WebAssembly, and other machines.** A 55-byte module assembled by hand and run by node; validation as type
  checking, and node's error; Prolog's `append` run backwards; actors and dataflow.
* **14. The Job, collected.** Ledger row 6: the λ-core on the Pebble VM, priced on Part 8's core, about 2.4 hours
  for the thirty novels, 149× row 5; the collector's share under 4%.
* **15. Frontier: the limits of runtimes.** Memory against time (our curve; Hertz and Berger's 5×, 3×, 2×);
  minimum mutator utilization and Metronome; the Futamura projections, PyPy and Truffle; warmup (Barrett et al.);
  verified runtimes; open problems. Outro.

## Build

```bash
python -m videos.cs.cs15.compute           # every number in the part (about ten minutes; the ledger item is most of it)
python tools/build.py cs15 -q l            # a 480p preview
python tools/build.py cs15                 # 1080p
```

`interp`, `vm`, `rc`, `pauses`, `jit`, `dispatch` and `wasm` run gcc, g++, java, go, node and CPython on this machine;
their timings belong to the computer that runs them. Everything run on Pebble is exact.

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

   *Solution.* Direct: `sum (h :: t) = h + sum t` keeps one frame per element: Θ(n) stack (8,007 words for n =
   1,000 on our VM) and no heap. CPS: `sum_k (h :: t) k = sum_k t (fun s -> k (h + s))` is all tail calls, so
   O(1) stack (8 words), but builds one continuation per element, each holding h and k: 4 words each, 4n in all
   (4,002 words). Accumulator: `sum_a (h :: t) acc = sum_a t (acc + h)`: O(1) stack and no heap. The accumulator
   is possible because + is associative: the pending work can be done early. CPS needs no such insight; it works
   for any function, which is why compilers use it.

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

   *Solution sketch.* Split the heap into a nursery and two old semispaces. Allocate in the nursery; when it fills,
   run Cheney with the stack and globals as roots, copying survivors into the current old semispace and treating
   any pointer outside the nursery as already done; when the old space cannot take a nursery's worth, run a full
   Cheney over both. The λ-core needs no write barrier because every heap object is written once, when it is
   created, and its fields can only point at objects that already exist, which are older: no old object can ever
   point at a younger one. The Python `Generational` collector predicts the result: about a third less copying
   (127,215 against 195,726 words on Part 7's chapter). But the collector is under 4% of the Pebble VM's time, so
   the whole Job speeds up by at most about 1%: Amdahl's law (Part 10), again.

6. **★ Research: the collector trilemma.** Find a collector with bounded pauses, constant memory overhead and
   constant work per word allocated, or prove that no collector can have all three.

   *Where to start.* Upper bounds: Blelloch and Cheng (1999) bound time and space for a real-time parallel copying
   collector; Metronome (Bacon, Cheng and Rajan 2003) bounds utilization given the allocation rate. Lower bounds:
   Robson (1971, 1974) for allocators that never move objects; Bendersky and Petrank (2011) and Cohen and Petrank
   (2013) for collectors that may compact only part of the heap. Open: (a) an adversarial mutator showing that any
   collector with pauses below p and memory below cL must do superconstant work per word, or a collector that
   escapes it; (b) the same question for immutable heaps like the λ-core's, where no barrier is needed and the
   lower-bound constructions do not apply; (c) measurements on the Pebble VM, whose collector is short enough to
   modify and whose costs are exact.

## 习题与解答

1. **闭包转换。** 手工对 `let twice f = let g = fun x -> f (f x) in g` 做闭包转换：找出自由变量，写出我们的编译器会生成的
   `CLOSURE` 与 `FREE` 代码。

   *解答。* `twice` 有一个参数 f（槽 0）。内层函数唯一的自由变量是 f，所以 `twice` 先把它压栈，再建一个捕获一个值的闭包：
   `LOCAL 0; CLOSURE g, 1 free; SETLOCAL 1; LOCAL 1; RET`。在 g 内部（参数 x 在槽 0），每次用到 f 都从闭包里读：
   `FREE 0`（外层的 f）、`FREE 0`、`LOCAL 0`、`CALL 1`（内层的 `f x`），然后外层调用处于尾位置，用 `TAILCALL 1`。
   f 不是已知函数，所以每次调用只传一个参数。我们的编译器生成的正是这些（`p.listing("twice")`），
   `twice (fun y -> y + 1) 5` 得 7。

2. **三种求和。** 把列表上的 `sum` 改写成 CPS 形式和带累加器的形式；给出每个版本对 n 个元素的栈深度和堆用量。

   *解答。* 直接形式：`sum (h :: t) = h + sum t` 每个元素占一个栈帧：Θ(n) 的栈（在我们的虚拟机上 n = 1,000 时为
   8,007 个字），不用堆。CPS：`sum_k (h :: t) k = sum_k t (fun s -> k (h + s))` 全是尾调用，所以栈是 O(1)（8 个字），
   但每个元素建一个续延，各保存 h 和 k：每个 4 个字，共 4n（4,002 个字）。累加器：`sum_a (h :: t) acc = sum_a t
   (acc + h)`：O(1) 的栈，不用堆。能用累加器是因为 + 满足结合律：待做的工作可以提前做。CPS 不需要这种洞察，
   对任何函数都适用，所以编译器用它。

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

   *解答要点。* 把堆分成新生代和两个老年代半空间。在新生代中分配；新生代满时，以栈和全局变量为根运行切尼算法，
   把存活对象复制到当前的老年代半空间，凡是指向新生代之外的指针都视为已处理；当老年代容纳不下一个新生代的量时，
   对两者做一次完整的切尼收集。λ 核心不需要写屏障，因为每个堆对象只在创建时写入一次，它的字段只能指向已经存在的、
   也就是更老的对象：老对象永远不可能指向更年轻的对象。Python 的 `Generational` 收集器预言了结果：复制量少约三分之一
   （在第7部分的那一章上是 127,215 对 195,726 个字）。但收集器只占 Pebble 虚拟机时间的 4% 不到，所以整个作业最多只快约
   1%：又是阿姆达尔定律（第10部分）。

6. **★ 研究：收集器的三难困境。** 找出一个停顿有界、内存开销为常数倍、每分配一个字的工作量为常数的收集器，
   或者证明没有收集器能三者兼得。

   *从哪里开始。* 上界：布莱洛赫与程（1999）为实时并行复制收集器给出了时间和空间的界；Metronome（培根、程与拉詹，
   2003）在已知分配速率时给出利用率的界。下界：罗布森（1971、1974）针对从不移动对象的分配器；本德斯基与彼得兰克
   （2011）以及科恩与彼得兰克（2013）针对只能压缩部分堆的收集器。尚未解决的：（a）构造一个对抗性的变异器，
   证明任何停顿低于 p、内存低于 cL 的收集器每个字都必须做超常数的工作，或者找到一个能逃脱它的收集器；
   （b）对像 λ 核心这样不可变的堆提出同样的问题，那里不需要屏障，已有的下界构造也不适用；（c）在 Pebble 虚拟机上
   测量，它的收集器短到可以修改，代价也是精确的。

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
