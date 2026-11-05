# Computer Science, Built — Part 13: The Compiler

Part 13 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, *Speaking to the Machine*. Part 12 taught the machine to read the Pebble
language; this part teaches it to write Pebble machine code. The compiler lives in `explainer/cs/lang/compiler/`:
`check.py` (names, scopes, types, struct layout), `lower.py` and `ir.py` (three-address code and control-flow
graphs), `interp.py` (the reference interpreter), `ssa.py` (dominators, frontiers, SSA construction and
destruction), `opt.py` (copy propagation, SCCP, DCE, GVN, natural loops, LICM, induction-variable strength reduction,
algebra, inlining), `codegen.py` (maximal-munch selection with compare-and-branch fusion, liveness, Chaitin–Briggs
colouring with coalescing and rematerialization, spilling, jump threading, emission), `driver.py` (levels `-O0` …
`-O3`), `analysis.py` (Kildall's solver with traces, chordality, a list scheduler), `fuzz.py` (random programs,
differential testing) and `superopt.py` (an enumerative superoptimizer and a rule checker, both backed by z3). About
2,500 lines, tested in `tests/test_cs13_compiler.py` against the interpreter, the reference word count, the
definition of dominance and the fuzzer. Every number is computed in `compute.py`.

* **A program that writes programs.** The Job's scan loop by hand (Part 6), in the Pebble language (Part 12), and as
  our compiler writes it: 827,576 instructions by hand on the first chapter, 4,466,758 unoptimized, 730,195 optimized
  (12% fewer than by hand).
* **1. FORTRAN, and the shape of a compiler.** Hopper's A-0 (1952); Backus's team, the IBM 704, April 1957, about 18
  person-years, and the quotation about "half as fast"; front, middle and back ends; M + N instead of M × N (UNCOL
  1958, GCC, LLVM); the list Job through every stage: 2,285 characters, 651 tokens, 371 nodes, 207 IR instructions in
  61 blocks, 20 φs, 315 after `-O3`, 235 machine instructions, 956 bytes.
* **2. Names, scopes and types.** The symbol table as a stack of scopes; typing rules as inference rules; four
  programs our checker rejects, with its messages; `Node` is 16 bytes and `Entry` 12; globals, virtual registers and
  address-taken locals.
* **3. Three-address code and the control-flow graph.** `s = s + a[i]` lowered; `total` as seven blocks; leaders,
  basic blocks, Frances Allen's CFG; clang's LLVM IR for the same function.
* **4. Dominators.** The definition, tested against "delete d, is n still reachable?"; the fixed-point equations
  solved in 2 passes (every function of the Job also takes 2); the dominator tree; dominance frontiers.
* **5. Static single assignment.** Renaming; φ at joins and loop headers; placement at the iterated dominance
  frontier (Cytron et al. 1991), pruned; renaming down the dominator tree; clang's `mem2reg` puts the same 3 φs in
  the same places.
* **6. Dataflow analysis and fixed points.** Liveness equations; the iteration on `total` (14 visits, 12 updates);
  reaching definitions and available expressions; the lattice of 16 subsets, height 4; Knaster–Tarski and Kleene;
  meet-over-paths and Kam & Ullman.
* **7. Optimizations on SSA.** The constant lattice; SCCP folds a function to `x + 32` and deletes a branch; dead code
  as mark and sweep; value numbering (−20% on the array Job); algebra and its traps; phase ordering, and clang
  `-O2`'s 88 pass runs of 60 passes.
* **8. Loops.** Back edges and natural loops (the array Job's `word`: an outer loop of 10 blocks, an inner of 3);
  loop inversion (−6.5% array, −12.5% list); LICM, 4 instructions hoisted (−10.6%); induction-variable strength
  reduction (−36%), which rediscovers Part 6's pointer; unrolling, vectorization, the polyhedral model.
* **9. Inlining and aliasing.** `same` copied into `lookup` (−3.7% on the list Job, nothing to inline in the array
  Job); the call graph and summaries; type-based, address-taken and points-to alias analysis; Rice's theorem and why
  every analysis is conservative.
* **10. Instruction selection.** Tiles; maximal munch; Aho–Johnson dynamic programming and iburg; DAGs are NP-hard;
  `same` selected, with compare-and-branch fusion.
* **11. Register allocation.** Interference; `total`'s graph (17 nodes, 41 edges, ω = 5, coloured with 5);
  Chaitin's simplify, spill, select; Briggs and George coalescing; rematerialization; NP-hard in general; SSA graphs
  are chordal (Hack, Grund & Goos 2006), checked on every function of the Job, and four of five stop being chordal
  after out-of-SSA (a 4-hole in `same`); the register sweep (13 → 4 registers: 767,276 → 1,148,719 instructions);
  linear scan.
* **12. Scheduling and the pipeline.** The dependence DAG of the inner loop and a false WAR dependence; list
  scheduling; on Part 7's pipeline the compiled Job runs 12% fewer instructions and 12% more cycles when branches are
  predicted not taken, and 9% fewer cycles with a two-bit predictor; software pipelining.
* **13. The Job, compiled.** Every pass in turn; `-O0` … `-O3` against the hand-written programs of Parts 6 and 11;
  on Part 8's out-of-order core, 11% fewer instructions and about the same cycles (+1.5%); ledger row 5: 58 s on one
  core (4.2 min unoptimized); gcc on the C Job of Part 10: 215 ms at `-O0`, 115 ms at `-O1`, nothing more at
  `-O2`/`-O3`.
* **14. Is the compiler right?** Csmith (325+ bugs in gcc and LLVM; none in CompCert's proved parts); our fuzzer: 240
  programs, 190 compared at four levels, 0 mismatches, and the two bugs it found during development; z3 on five
  rewrite rules (three false, with counterexamples); Alive; translation validation; CompCert.
* **15. Frontier: searching for the best program.** The full employment theorem; Massalin's superoptimizer rebuilt:
  shortest proved Pebble programs for eight functions (|x| in 3, min in 4 after 4 minutes); STOKE, Souper, AlphaDev;
  equality saturation and e-graphs (egg, Cranelift); MLGO; open problems.
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs13.compute           # every number in the part (about 20 minutes: superopt and fuzz dominate)
python tools/build.py cs13 -q l            # a 480p preview
python tools/build.py cs13                 # 1080p
```

The `gcc`, `llvm` and `superopt` timings belong to the computer that runs them (the clang and gcc versions are
recorded); instruction and cycle counts come from the Pebble emulator, Part 7's pipeline and Part 8's core, and are
exact.

## Problems, with solutions

1. **Dominators and φs by hand.** Compute the dominator tree and dominance frontiers of a `while` loop containing an
   `if` with an early `return`, and place the φs for a variable assigned in both branches.

   *Solution.* Blocks: `entry → head`; `head → body | exit`; `body → then | else`; `then → ret` (the early return)
   and `then → join`; `else → join`; `join → head`. The dominator tree is entry → head → {exit, body}, body → {then,
   else, join}, then → ret. Frontiers: DF(then) = DF(else) = {join} (each reaches join, which the other also
   reaches); DF(join) = DF(body) = {head} (the back edge); DF(head) = {head}; DF(ret) = DF(exit) = ∅. A variable
   assigned in both branches gets a φ at join (the frontier of the assignments) and then, because that φ is itself
   an assignment, a φ at head (the frontier of join); if the variable is not live at head, pruned SSA drops the
   second φ. The early return adds no φ: `ret` has a single predecessor.

2. **Liveness by hand.** Run liveness on a three-block loop and show that the result is the least solution.

   *Solution.* Take `B1: s = 0; i = 0` → `B2: if i < n` → `B3: s = s + i; i = i + 1` → B2, and B2 → exit using `s`. use/def:
   B1 defines s, i; B2 uses i, n; B3 uses s, i and defines s, i; exit uses s. Starting from empty sets and visiting
   backward: IN(exit) = {s}; IN(B3) = {s, i}; IN(B2) = {i, n, s}; then OUT(B3) = IN(B2) adds n to IN(B3) =
   {s, i, n}; IN(B1) = {n}: only the parameter. A second sweep changes nothing. Any solution must contain these sets: each element is
   forced by a use reachable without an intervening definition, by induction on the number of iterations (Kleene's
   chain F^k(⊥) is below every fixed point, since F is monotone and ⊥ is below everything). So the iteration's
   answer is the least fixed point; adding, say, `t` to every set gives a larger solution that is still consistent
   but useless.

3. **x·c / c.** Show that `x * 3 / 3 → x` is false on 32-bit integers, and find for which c the rule is sound.

   *Solution.* With x = −1,859,365,541 (the solver's counterexample), 3x wraps around 2³² and the division no longer
   undoes it. In general the rule fails as soon as c·x can overflow, which happens for some x whenever |c| ≥ 2. For
   c = 1 it is trivial; for c = −1 it holds too, under the machine's wrap-around semantics, because −(−x) = x even at
   x = −2³¹ (where −x = x and x / −1 = x). Checked with z3 for every c from −8 to 8 and for ±2³¹: only ±1 survive.
   The rule *is* sound on mathematical integers, which is exactly why compilers for C may use it on signed values
   (signed overflow is undefined) but not on unsigned ones, and why a solver, not intuition, should decide.

4. **Simplification.** Prove that if simplification removes every node, each with fewer than k neighbours when
   removed, the graph is k-colourable; then show that Chaitin's method spills on a 4-cycle with k = 2.

   *Solution.* Induction on the number of nodes, in reverse order of removal: when a node is put back, it has fewer
   than k neighbours among the nodes already coloured, so at least one of the k colours is free. On a 4-cycle every
   node has degree 2 = k, so simplification cannot start and Chaitin's method must spill, although the cycle is
   bipartite and needs only 2 colours. Briggs's *optimistic* colouring fixes this: push the node anyway, and spill
   only if, when it is popped, no colour is actually free. On the 4-cycle, opposite nodes then share colours and
   nothing spills.

5. **Build: loads in value numbering.** Our GVN never merges two loads of the same address (`total`'s `%t10` and
   `%t14` both load `[%iv2]`). Add it, safely, using the type-based rule of chapter 9, and test it.

   *Solution.* Give each load the key (load, size, address value, memory version), where the memory version is a
   counter bumped by every store of the same size and by every call (and by `getc`/`putc`), within one basic block;
   across blocks, walk the dominator tree and bump the version on entry to any block that is a join point with a
   store on some incoming path (or, simplest and still useful, reset at every block boundary). Two loads with equal
   keys are the same value. In `total`, the then-block's load is dominated by the body's load of the same address
   with no store between, so it becomes a use of `%t10`, saving one load per positive element. Run
   `tests/test_cs13_compiler.py`, which checks the Job at every level against the reference count, and
   `python -m videos.cs.cs13.compute --force fuzz`: any mismatch is a bug in the new rule (the most likely one is
   forgetting that a byte store and a word load may overlap when the word is being built from bytes, which the
   size rule excludes only because the Pebble language has no casts).

6. **★ Research: spilling on SSA.** On SSA programs colouring is easy but optimal spilling is NP-hard. Find a
   polynomial algorithm with a proven approximation ratio, or show that none exists.

   *Where to start.* What is known: SSA interference graphs are chordal and colour optimally in linear time (Hack,
   Grund & Goos 2006; Bouchez, Darte & Rastello; Brisk et al.); deciding the cheapest set of values to spill
   ("spill everywhere") is NP-hard even on SSA programs (Bouchez, Darte & Rastello, "On the complexity of spill
   everywhere under SSA form", 2007), and so is optimal coalescing. Spill-everywhere is a maximum-weight
   k-colourable subgraph problem: polynomial on interval graphs (straight-line code), hard on chordal graphs when k
   is part of the input (Yannakakis & Gavril 1987). Local allocation with load costs is NP-hard but has
   approximation algorithms (Farach-Colton & Liberatore 2000). (a) Reproduce the NP-hardness reduction for spill
   everywhere on chordal graphs. (b) For fixed k, design a dynamic program over a clique tree of the interference
   graph and measure it on the Job's functions with `regalloc`'s sweep as a benchmark. (c) Ask whether a constant
   ratio is possible when costs are weighted by loop depth, the case compilers actually face.

## 习题与解答

1. **手算支配者与 φ。** 对一个内含带提前 `return` 的 `if` 的 `while` 循环，计算支配树和支配边界，并为一个在两个分支中
   都被赋值的变量放置 φ。

   *解答。* 基本块：`entry → head`；`head → body | exit`；`body → then | else`；`then → ret`（提前返回）和
   `then → join`；`else → join`；`join → head`。支配树为 entry → head → {exit, body}，body → {then, else, join}，
   then → ret。支配边界：DF(then) = DF(else) = {join}（两者都能到达 join，而另一条路径也能到达它）；DF(join) =
   DF(body) = {head}（回边）；DF(head) = {head}；DF(ret) = DF(exit) = ∅。在两个分支中都被赋值的变量，在 join 处得到
   一个 φ（赋值所在块的边界）；由于这个 φ 本身也是一次赋值，head 处还要一个 φ（join 的边界）；若该变量在 head 处
   不活跃，剪枝 SSA 会去掉第二个 φ。提前返回不增加 φ：`ret` 只有一个前驱。

2. **手算活跃性。** 在一个三块循环上运行活跃性分析，并说明结果是最小解。

   *解答。* 取 `B1: s = 0; i = 0` → `B2: if i < n` → `B3: s = s + i; i = i + 1` → B2，以及 B2 → exit（使用 `s`）。
   use/def：B1 定义 s、i；B2 使用 i、n；B3 使用 s、i 并定义 s、i；exit 使用 s。从空集出发、逆向访问：IN(exit) = {s}；
   IN(B3) = {s, i}；IN(B2) = {i, n, s}；随后 OUT(B3) = IN(B2) 使 IN(B3) 增加 n，成为 {s, i, n}；IN(B1) = {n}：只剩参数。
   再扫一遍没有变化。任何解都必须包含这些集合：每个元素都由一条不经过重新定义就能到达的使用所强制，对迭代次数归纳
   即得（因为 F 单调、⊥ 在一切之下，Kleene 链 F^k(⊥) 位于每个不动点之下）。所以迭代的结果是最小不动点；比如给每个
   集合都加上 `t`，得到的解更大，仍然自洽，却毫无用处。

3. **x·c / c。** 证明 `x * 3 / 3 → x` 在 32 位整数上不成立，并找出使该规则成立的 c。

   *解答。* 取 x = −1,859,365,541（求解器给出的反例），3x 在 2³² 上回绕，除法就无法还原。一般地，只要 c·x 可能溢出，
   规则就失效，而 |c| ≥ 2 时总有这样的 x。c = 1 显然成立；c = −1 在机器的回绕语义下也成立，因为即使 x = −2³¹ 时
   −(−x) = x（此时 −x = x，x / −1 = x）。用 z3 对 −8 到 8 的每个 c 以及 ±2³¹ 检验：只有 ±1 通过。该规则在数学整数上
   *是*成立的，这正是 C 编译器可以在有符号值上使用它（有符号溢出是未定义行为）、却不能在无符号值上使用它的原因，也
   说明应该由求解器而不是直觉来裁决。

4. **化简。** 证明：如果化简能移走所有结点，且每个结点被移走时邻居都少于 k 个，那么图是 k 可着色的；再说明 k = 2 时
   Chaitin 方法在一个 4 圈上会溢出。

   *解答。* 按移走的逆序对结点数归纳：一个结点放回时，在已着色的结点中它的邻居少于 k 个，所以 k 种颜色中至少有一种
   空闲。在 4 圈上每个结点的度都是 2 = k，化简无从开始，Chaitin 方法只能溢出，尽管这个圈是二部图、只需 2 种颜色。
   Briggs 的*乐观*着色解决了这个问题：照样把结点压栈，只有在弹出时确实没有空闲颜色才溢出。在 4 圈上，相对的两个结点
   于是共用颜色，什么都不溢出。

5. **动手：值编号中的读内存。** 我们的 GVN 从不合并两次读同一地址（`total` 的 `%t10` 和 `%t14` 都读 `[%iv2]`）。
   用第 9 章基于类型的规则安全地加上这一功能，并测试它。

   *解答。* 给每次读内存一个键（load、宽度、地址的值、内存版本），其中内存版本是一个计数器，在同一基本块内每遇到一次
   同宽度的写内存、每次调用（以及 `getc`/`putc`）就加一；跨基本块时沿支配树行走，进入任何某条入边上有写内存的汇合块时
   增加版本（或者最简单而仍然有用的做法：在每个块边界重置）。键相同的两次读内存是同一个值。在 `total` 中，then 块的读
   被 body 块对同一地址的读所支配，其间没有写，于是它变成对 `%t10` 的使用，每个正元素省一次读。运行
   `tests/test_cs13_compiler.py`（它在每个级别上对照参考计数检查 Job）和
   `python -m videos.cs.cs13.compute --force fuzz`：任何不一致都是新规则的错误（最可能的是忘了：当一个字由字节拼成
   时，写字节和读字可能重叠；宽度规则之所以能排除它，只是因为 Pebble 语言没有类型转换）。

6. **★ 研究：SSA 上的溢出。** 在 SSA 程序上，着色容易，但最优溢出是 NP 难的。找出一个有可证近似比的多项式算法，或者
   证明不存在。

   *从哪里开始。* 已知：SSA 冲突图是弦图，可在线性时间内最优着色（Hack、Grund 与 Goos 2006；Bouchez、Darte 与
   Rastello；Brisk 等）；决定溢出哪些值代价最小（“处处溢出”）即使在 SSA 程序上也是 NP 难的（Bouchez、Darte 与
   Rastello，《On the complexity of spill everywhere under SSA form》，2007），最优合并也是。处处溢出是一个最大权
   k 可着色子图问题：在区间图（直线代码）上是多项式的，在弦图上当 k 作为输入时是困难的（Yannakakis 与 Gavril
   1987）。带读内存代价的局部分配是 NP 难的，但有近似算法（Farach-Colton 与 Liberatore 2000）。（a）重现弦图上处处
   溢出的 NP 难归约。（b）对固定的 k，在冲突图的团树上设计一个动态规划，并以 `regalloc` 的寄存器扫描为基准在 Job 的
   函数上测量。（c）问：当代价按循环深度加权（编译器实际面对的情形）时，能否达到常数近似比？

## Glossary additions

编译器 compiler · 前端 / 中端 / 后端 front end / middle end / back end · 中间表示 intermediate representation (IR) ·
符号表 symbol table · 作用域 scope · 遮蔽 shadowing · 类型规则 typing rule · 对齐 alignment · 布局 layout · 取地址
address taken · 三地址码 three-address code · 临时变量 temporary · 基本块 basic block · 首指令 leader · 控制流图
control-flow graph · 支配 dominate · 直接支配者 immediate dominator · 支配树 dominator tree · 支配边界 dominance
frontier · 逆后序 reverse postorder · 静态单赋值 static single assignment (SSA) · φ 函数 φ-function · 剪枝 SSA pruned
SSA · 数据流分析 dataflow analysis · 活跃 live · 到达定义 reaching definitions · 可用表达式 available expressions ·
格 lattice · 单调 monotone · 不动点 fixed point · 稀疏条件常量传播 sparse conditional constant propagation · 复写传播
copy propagation · 死代码消除 dead-code elimination · 值编号 value numbering · 强度削弱 strength reduction · 阶段顺序
phase ordering · 回边 back edge · 自然循环 natural loop · 循环头 loop header · 前置块 preheader · 循环反转 loop
inversion · 循环不变代码外提 loop-invariant code motion · 归纳变量 induction variable · 循环展开 unrolling · 内联
inlining · 调用图 call graph · 别名分析 alias analysis · 指令选择 instruction selection · 铺砖 tiling · 最大吞噬
maximal munch · 寄存器分配 register allocation · 冲突图 interference graph · 着色 colouring · 溢出 spill · 合并
coalescing · 再物化 rematerialization · 弦图 chordal graph · 线性扫描 linear scan · 指令调度 instruction scheduling ·
依赖图 dependence graph · 列表调度 list scheduling · 软件流水 software pipelining · 差分测试 differential testing ·
模糊测试 fuzzing · 翻译确认 translation validation · 超级优化 superoptimization · 等式饱和 equality saturation ·
e 图 e-graph

## Sources

*Canon.* Books: Aho, Lam, Sethi & Ullman, *Compilers: Principles, Techniques, and Tools* (the Dragon Book), ch. 6–10;
Cooper & Torczon, *Engineering a Compiler*; Appel, *Modern Compiler Implementation in ML*; Muchnick, *Advanced
Compiler Design and Implementation*; Rastello & Bouchez Tichadou (eds.), *SSA-based Compiler Design*; Nielson,
Nielson & Hankin, *Principles of Program Analysis*.

Papers: Backus et al., "The FORTRAN automatic coding system" (1957); Backus, "The history of FORTRAN I, II, and III"
(1978); Strong et al., "The problem of programming communication with changing machines" (UNCOL, 1958); Rice,
"Classes of recursively enumerable sets and their decision problems" (1953); Allen, "Control flow analysis" (1970);
Allen & Cocke, "A catalogue of optimizing transformations" (1971); Kildall, "A unified approach to global program
optimization" (1973); Kam & Ullman, "Monotone data flow analysis frameworks" (1977); Aho & Johnson, "Optimal code
generation for expression trees" (1976); Lengauer & Tarjan, "A fast algorithm for finding dominators in a flowgraph"
(1979); Rau & Glaeser, "Some scheduling techniques and an easily schedulable horizontal architecture" (1981); Chaitin
et al., "Register allocation via coloring" (1981) and Chaitin, "Register allocation and spilling via graph coloring"
(1982); Gavril, "The intersection graphs of subtrees in trees are exactly the chordal graphs" (1974); Massalin,
"Superoptimizer: a look at the smallest program" (1987); Lam, "Software pipelining" (1988); Cytron, Ferrante, Rosen,
Wegman & Zadeck, "Efficiently computing static single assignment form and the control dependence graph" (1991);
Wegman & Zadeck, "Constant propagation with conditional branches" (1991); Fraser, Hanson & Proebsting, "Engineering
a simple, efficient code-generator generator" (iburg, 1992); Briggs, Cooper & Torczon, "Improvements to graph
coloring register allocation" (1994); George & Appel, "Iterated register coalescing" (1996); Andersen, *Program
analysis and specialization for the C programming language* (1994); Steensgaard, "Points-to analysis in almost
linear time" (1996); Landi, "Undecidability of static analysis" (1992); Ramalingam, "The undecidability of aliasing"
(1994); Pnueli, Siegel & Singerman, "Translation validation" (1998); Poletto & Sarkar, "Linear scan register
allocation" (1999); Necula, "Translation validation for an optimizing compiler" (2000); Cooper, Harvey & Kennedy, "A
simple, fast dominance algorithm" (2001); Lattner & Adve, "LLVM: a compilation framework for lifelong program
analysis and transformation" (2004).

*Recent.* Hack, Grund & Goos, "Register allocation for programs in SSA-form" (2006); Bouchez, Darte & Rastello, "On
the complexity of spill everywhere under SSA form" (2007); Leroy, "Formal verification of a realistic compiler"
(2009); Tate, Stepp, Tatlock & Lerner, "Equality saturation: a new approach to optimization" (2009); Yang, Chen, Eide
& Regehr, "Finding and understanding bugs in C compilers" (2011); Schkufza, Sharma & Aiken, "Stochastic
superoptimization" (2013); Lopes, Menendez, Nagarakatte & Regehr, "Provably correct peephole optimizations with
Alive" (2015); Sasnauskas et al., "Souper: a synthesizing superoptimizer" (2017); Willsey et al., "egg: fast and
extensible equality saturation" (2021); Trofin et al., "MLGO: a machine learning guided compiler optimizations
framework" (2021); Mankowitz et al., "Faster sorting algorithms discovered using deep reinforcement learning" (2023).
