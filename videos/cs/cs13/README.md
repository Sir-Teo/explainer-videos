# Computer Science, Built — Part 13: The Compiler

Part 13 of the [sixty-one-part course](../README.md), in Act III, *Speaking to the Machine*.
Part 12 built the reader for Pebble; this part builds the compiler, follows its intermediate representations,
and tests whether the generated machine code preserves the program's behavior.

The compiler is in `explainer/cs/lang/compiler/`: name/type checking and layout, CFG lowering, an IR interpreter,
dominators and SSA, optimization passes, instruction selection, register allocation, scheduling, differential
fuzzing and bounded enumerative search with separate SMT validation. The chapter uses actual traces and graphs
from these implementations. Tests live in `tests/test_cs13_compiler.py`.

The seventeen scenes cover the scan-loop hook; compiler history and pipeline; semantic checking; IR and CFGs;
dominators; SSA; dataflow fixed points; optimization; loops; inlining and aliasing; instruction selection;
register allocation; scheduling; the compiled Job; correctness; the research frontier; and worked problems.

## Measurements and interpretation

These are the repaired local data, not universal compiler performance claims.

| Quantity | Recorded result | Scope |
| --- | ---: | --- |
| First-chapter array scan, hand written | 827,576 instructions | Pebble physical execution |
| Same scan, compiled `-O0` | 4,466,758 instructions | Same workload |
| Same scan, compiled `-O2` / `-O3` | 853,694 instructions | About 3.2% above hand written |
| List Job, compiled `-O2` / `-O3` | 768,386 / 739,791 instructions | First chapter |
| Pipeline input | 2,285 characters; 651 tokens; 371 AST nodes | List Job |
| Lowered / final IR | 207 instructions in 61 blocks / 311 instructions | Final count includes the compiler pipeline's transformations |
| Emitted code | 238 instruction words; 952 bytes | Physical 32-bit words before `_brk`, including runtime code; 234 indented listing lines is a different statistic |
| Liveness trace | 14 visits; 12 updates | The displayed `total` CFG |
| Allocation example | 17 vertices; 41 edges; clique and coloring size 5 | The displayed interference graph |
| LICM example | 2 pure IR operations hoisted | No conditional load is speculated |
| Register sweep, 13 → 4 registers | 768,386 → 1,156,277 instructions | Current list-Job run |
| Six-passage out-of-order core comparison | Compiled cycles / hand cycles = 1.0666 | Aggregate cycle counts, not mean passage ratios |
| Ledger projection | 61.18 seconds compiled; 57.4 seconds hand written | Scaled from simulated cycles; not a measured production wall time |
| Host GCC 14.2.0 C Job | 220.5 / 127.5 / 145.1 / 116.5 ms | `-O0`…`-O3`, recorded local best of three |
| LLVM 19.1.7 | 3 `mem2reg` φs; 90 parsed pipeline names, 61 distinct | Printed `opt -O2` pipeline text; not executed per-function pass counts |
| Differential sample | 240 generated; 190 compared at four levels; 50 excluded; 0 mismatches | Exclusions hit the reference step limit; no correctness proof |

Instruction counts, pipeline cycles, projected ledger time, host timings and code size measure different things.
The compiled program can execute more instructions and still exhibit a different pipeline cost. The six measured
passages are the comparison population; the ledger extrapolation assumes that their relative cycle cost transfers.

The search chapter displays eight candidates of lengths 1, 1, 2, 2, 3, 3, 3 and 4. Finite test observations prune
the search; this pruning is incomplete. Each displayed candidate is separately validated under its SMT word model.
The approximately 310-second search-plus-proof total belongs to the recorded host. These are validated candidates,
not proofs of shortest code. Absolute value at `INT_MIN` follows Pebble's wrap-around definition.

## Semantic boundaries

* Dominance refers to reachable CFG nodes. A dominance frontier requires that the node does **not strictly dominate**
  the destination, so a loop header can belong to its own frontier. Renaming walks the actual dominator tree;
  instruction order and φ-edge uses still matter.
* Monotone does not mean inflationary. Bottom initialization, a fair worklist and finite lattice height establish
  convergence here. Equality with meet-over-paths needs the stated distributivity assumptions and concerns syntactic
  CFG paths, including infeasible ones.
* Strict SSA interference is chordal under the uniform-register model. Coloring an explicit chordal graph and
  solving spilling, coalescing, instruction constraints or full allocation have different complexity bounds.
* Greedy maximal munch is a heuristic with arbitrary tile costs. Tree dynamic programming is optimal only for its
  specified tree/tile cost model; the general DAG problem has additional sharing choices.
* Memory transformations require both memory and control/trap safety. Different access widths can overlap. The
  repaired LICM keeps conditional loads guarded and only moves a header load under conservative effect checks.
  C's character alias exception, `restrict` contracts and Rust references require their own language rules.
* Rice/halting arguments concern unbounded program models. They are not undecidability proofs for a fixed finite
  machine. CompCert's proved translation begins at its specified AST and ends at assembly, with an explicit trusted
  boundary. The fuzzer's bounded sample and historical Csmith/Alive results are evidence with separate scopes.

## Build and cache provenance

```bash
python -m videos.cs.cs13.compute
python tools/build.py cs13 -q l
python tools/build.py cs13
python -m unittest tests.test_cs13_compiler
```

Fourteen compiler-dependent data caches carry a revision hash over `compute.py` and the compiler source. Normal
loads regenerate stale entries; cached-only QA rejects them before mutation. Host GCC, LLVM and superoptimization
records retain their recorded tools and timing context. Re-measure those deliberately with, for example,
`python -m videos.cs.cs13.compute --force gcc`. Computation requires the relevant local tools and Z3.
A cached numeric artifact is not by itself evidence that a changed compiler was re-executed.

## Problems, with solutions

1. **Dominators and φs.** Use edges E→H, H→B/X, B→T/F, T→R/J, F→J, J→H; R and X return.
   Compute the dominator tree and frontiers. Initialize `v` in E, assign it in T/F and use it in X.

   *Solution.* Immediate-dominator edges are E→H, H→B/X, B→T/F/J, T→R.
   DF(T)=DF(F)={J}; DF(J)=DF(B)=DF(H)={H}; DF(E)=DF(R)=DF(X)=∅.
   Iterated-frontier placement puts φs at J and H. With the stated use at X, `v` is live at H, so pruning keeps
   the header φ. If that incoming value is never used before redefinition, a suitably changed example can prune it.
   R has one predecessor and adds no merge. The two outgoing T edges are CFG edges, not sequential execution.

2. **Least liveness solution.** B1 initializes `s=0; i=0`; B2 tests `i<n`, goes to B3 or X;
   B3 executes `s=s+i; i=i+1` then returns to B2; X uses `s` and returns. Solve backward liveness.

   *Solution.* IN(X)={s}, OUT(X)=∅, IN(B2)=IN(B3)={s,i,n}, IN(B1)={n}.
   OUT(B1)=OUT(B2)=OUT(B3)={s,i,n}. Starting at bottom and applying the monotone equations reaches these sets.
   Every use reachable without a redefinition forces its variable into the corresponding set; induction on
   iterations shows that the result lies below every fixed point. To exhibit a larger fixed point, include an
   unused parameter `t` in the universe and add it to IN and OUT of B1/B2/B3 only. The back edge sustains it, while
   the exit boundary stays OUT(X)=∅ and IN(X)={s}. Adding it to every set would violate that boundary.

3. **Word arithmetic.** For which nonzero signed 32-bit constants c is `(x*c)/c = x` valid for every word x?

   *Solution.* Under Pebble's wrapping multiply and division toward zero, including wrapping `INT_MIN/-1`,
   exactly c=1 and c=−1 work. For |c|≥2, any wrapped product has magnitude at most 2³¹; division cannot reach
   x=2³¹−1. For c=3 and x=2³¹−1, the product wraps to 2³¹−3, and the quotient is 715,827,881.
   Mathematical integer multiplication followed by exact division does cancel. C signed-overflow and division
   undefined behavior permit different transformations on defined executions; unsigned modular arithmetic also
   does not justify this cancellation. State the language model before proving a rewrite.

4. **Simplification and optimistic coloring.** Prove the degree-<k removal rule and analyze a 4-cycle for k=2.

   *Solution.* Restore removed vertices in reverse order. Each has fewer than k already-colored neighbors, so a
   color remains. A 4-cycle has degree k everywhere, so conservative simplification stalls and a basic spill
   decision may choose a value even though the graph is bipartite. Optimistically pushing one vertex permits the
   rest to simplify and succeeds on this graph. This example does not make optimistic coloring optimal on arbitrary
   graphs or with architectural register constraints.

5. **Build: load value numbering.** Design a safe first implementation, then explain what changes across blocks.

   *Solution.* Within one block, key a load by width, address value and memory version. Reuse a dominating earlier
   load only if no intervening store may overlap it and no call or relevant I/O/effect invalidates the observation.
   A conservative implementation invalidates on **every** store, regardless of width, and resets at each block
   boundary. This version does not remove a load in a different block. To reuse the body load inside its dominated
   then block, track sound memory versions through edges and joins (or use a memory-SSA/alias analysis), as well as
   control and trap legality. A join is not handled by merely incrementing a traversal-local counter.
   Test byte-store/word-load overlap, word-store/byte-load overlap, calls, joins, zero-trip loops and conditional
   invalid pointers, then compare interpreter and physical execution. The current regression suite includes the
   LICM overlap and guarded-null failures; finite fuzzing supplements these tests without proving the new pass.

6. **★ Research: precisely scoped spilling.** Reproduce a known fixed-k algorithm before defining an extension.

   *Solution and starting point.* For weighted spill-everywhere **without holes** on a chordal interference graph,
   a clique-tree dynamic program is polynomial for each fixed register count k. At each clique, retain a subset of
   at most k vertices; require agreement on the parent separator, combine compatible child states, and charge each
   retained vertex's weight exactly once, at its highest containing clique. Running intersection makes those local
   choices consistent. Maximizing retained weight gives exact minimum spill cost W−retained weight. The number of
   states grows like a power with exponent k, so this is not a polynomial bound when k is input.
   Holes, mandatory short ranges, reload placement, coalescing and machine constraints change the problem; consult
   the relevant theorem before transferring a bound. A retained-weight approximation does not transfer its ratio
   to spill cost: W=100, optimum retained=99 gives spill=1, whereas retained=50 gives spill=50 despite retaining
   more than half the optimum. Implement the known DP, compare it on small exhaustively solved instances, then
   specify one extension and review its literature before calling it open.

## 习题与解答

1. **支配树与 φ。** 边为 E→H，H→B/X，B→T/F，T→R/J，F→J，J→H；R、X 返回。
   E 初始化 v，T/F 赋值，X 使用。直接支配树为 E→H，H→B/X，B→T/F/J，T→R。
   DF(T)=DF(F)={J}，DF(J)=DF(B)=DF(H)={H}，其余为空。迭代支配边界在 J、H 放 φ；由于 X 使用 v，
   v 在 H 活跃，剪枝仍保留循环头 φ。R 只有一个前驱，不增加合流。T 的两条出边表示分支，并非顺序执行。

2. **最小活跃性解。** B1 初始化 s、i；B2 测试 i<n，进入 B3 或 X；B3 累加并递增后回 B2；X 使用 s。
   IN(X)={s}、OUT(X)=∅、IN(B2)=IN(B3)={s,i,n}、IN(B1)={n}；三个非出口块的 OUT 均为 {s,i,n}。
   从空集开始的单调迭代得到最小不动点。若全集包含未使用参数 t，只把它加入三个非出口块的 IN/OUT，回边可以
   维持这个更大的不动点；X 的边界不变。给所有集合都加 t 会破坏出口方程。

3. **机器字运算。** 在 Pebble 的 32 位回绕乘法、向零截断除法和 INT_MIN/−1 回绕规则下，
   对所有 x 都有 (x*c)/c=x 的非零常量只有 ±1。|c|≥2 时，回绕乘积的绝对值最多为 2³¹，商不可能达到
   x=2³¹−1。c=3 时乘积为 2³¹−3，商为 715,827,881。数学整数、C 的有符号未定义行为、无符号模运算
   属于不同模型，不能混用证明。

4. **化简与乐观着色。** 逆序放回度数小于 k 时移走的结点，总有空闲颜色。k=2 的四圈所有度数都等于 k，
   保守化简无法开始，可能选择溢出；但图本身可二着色。乐观压栈一个点后，其余点可化简，本例无需溢出。
   这不证明乐观算法在任意图或带机器约束时最优。

5. **动手：读取的值编号。** 同一基本块内，用读取宽度、地址值和内存版本作键。只有更早读取支配当前读取，
   且其间没有可能重叠的写入、调用或相关副作用，才可复用。保守版本遇到任何宽度的写入都失效，并在块边界重置；
   它不会消除跨块读取。跨块需要沿边和合流传播可靠的内存版本，配合支配、别名及控制/陷阱条件；遍历时随意增加
   一个计数器并不足够。测试不同宽度重叠、调用、合流、零次循环和条件保护的无效指针，再比较解释器与机器执行。
   有限模糊测试只能补充证据，不能证明新优化正确。

6. **★ 研究：精确定义溢出问题。** 对弦图上有权、无空洞的处处溢出，固定 k 的团树动态规划已经是已知结果。
   每个团保留至多 k 个点，父子分隔集上的选择必须一致，每个点的权重只在最高包含团计一次。最大保留权重给出
   精确溢出代价 W−保留权重；状态数的指数依赖 k，不能据此声称 k 作为输入时也为多项式。
   空洞、必须保留的短活跃段、重载位置、合并和机器约束会改变问题。保留权重的近似比不等于溢出代价近似比：
   W=100、最优保留99时只溢出1，保留50却溢出50。先实现已知算法并对小图穷举验证，再定义扩展、查阅文献，
   判断是否仍为开放问题。

## Primary checks for the scoped claims

* [Strict SSA and register allocation](https://homepages.dcc.ufmg.br/~fernando/publications/papers/FOSSACS06.pdf)
* [Spill-everywhere complexity and fixed-k cases](https://arxiv.org/abs/0710.3642)
* [CompCert proof and trusted boundary](https://compcert.org/man/manual001.html)
* [LLVM parameter attributes and dereferenceability](https://llvm.org/docs/LangRef.html#parameter-attributes)
* [MLGO's documented objectives](https://llvm.org/docs/MLGO.html)
* [Csmith's historical study](https://www.flux.utah.edu/paper/yang-pldi11)
* [Alive's historical study](https://people.cs.rutgers.edu/~sn349/papers/alive-pldi15.pdf)
* [AlphaDev's task and deployment scope](https://pmc.ncbi.nlm.nih.gov/articles/PMC10247365/)

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
