# Computer Science, Built — Part 3: Logic from Switches

Part 3 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the first step of act one: building a computer from switches. Boole turns logic
into algebra; a 21-year-old Shannon notices that relay circuits obey it; the transistor makes the switch fast and
small; one gate, NAND, turns out to be enough for everything; and yet almost every function needs an astronomically
large circuit, and nobody can name one that does. Every circuit here is a netlist in this series' hardware library
(`explainer/cs/pebble/hdl.py`), simulated bit-parallel and checked on every input (`compute.py`).

* **A thesis about switches.** Shannon's 1937 master's thesis; switches in series compute AND, in parallel OR; relays
  let circuits drive circuits; objectives.
* **1. Boole's algebra.** *The Laws of Thought* (1854); syllogisms as equations; the laws in dual pairs; or distributes
  over and, shown with Venn regions; simplifying by the laws (absorption as a circuit that collapses to a wire).
* **2. Circuits are expressions.** Shannon's dictionary; the staircase light as XOR; seven contacts reduced to one by
  algebra; the consensus theorem by analysing a circuit.
* **3. The transistor.** Relays, tubes, transistors (1947), the MOSFET (1959), the integrated circuit (1958–59); nMOS
  and pMOS as switches; the CMOS inverter; its transfer curve computed from square-law transistors (threshold
  0.50 V_DD, gain ≈ 170, noise margins ≈ 0.40 V_DD); a chain of inverters restoring a sloppy zero.
* **4. CMOS gates.** NAND and NOR as dual series–parallel networks, run on all inputs; an and-or-invert gate in six
  transistors; transistors per gate and why chips are mostly NAND; power only while switching, P ≈ αCV²f.
* **5. One gate is enough.** NOT, AND, OR from NAND; the fewest NANDs for each of the sixteen two-input functions, by
  exhaustive search (XOR 4, XNOR 5); the four-NAND XOR; completeness via the disjunctive normal form; Post's five
  traps (1941), computed for every two-input gate: only NAND and NOR are complete alone.
* **6. Normal forms and maps.** The Boolean cube and implicants as edges and faces; Karnaugh maps as the unfolded
  4-cube on a torus, with Quine–McCluskey's prime implicants and a minimal cover (computed); parity's DNF of 2ⁿ⁻¹
  terms against a tree of n − 1 XORs; minimization is NP-hard (Masek) and Σ₂ᵖ-complete (Umans).
* **7. Choosing with gates.** The 2-to-1 multiplexer; a multiplexer with constants is complete; Shannon expansion; a
  tree of multiplexers reads a truth table, and a lookup table reprogrammed from majority to parity is how an FPGA
  works; the 3-to-8 decoder.
* **8. Decision diagrams.** From a decision tree to a reduced ordered BDD (majority: 15 nodes to 6); variable order
  matters exponentially (x₁x₂ + x₃x₄ + ⋯: 2k + 2 against 2ᵏ⁺¹ nodes, computed up to 14 variables); canonical forms make
  equivalence a pointer comparison; multiplication defeats every order (Bryant, 1991).
* **9. How many gates?** Size and depth (parity as a chain and as a tree); Shannon's counting argument (1949) and the
  computed curves; Lupanov's matching upper bound (1958); formulas against circuits (Khrapchenko's n²); the
  explicit-function gap (≈ 3.1n, Li & Yang 2022), P versus NP, and Håstad's constant-depth bound.
* **10. Gates take time.** Propagation delay and the critical path; a static hazard simulated with unit delays and
  removed by the consensus term; RC delay, fan-out and buffers; the clock budget.
* **11. The blocks Pebble needs.** Comparator, priority encoder, barrel shifter (log₂ n stages), and a table of every
  block with gates, depth, NAND counts and the inputs checked.
* **12. Our hardware layer.** Netlists as topologically ordered lists; bit-parallel simulation (64 tests per word);
  the NAND rewrite, re-verified; exhaustive checking and where it stops.
* **13. Machines of switches.** Stibitz, Zuse's Z1 and Z3, Atanasoff–Berry, Colossus, ENIAC and its first
  programmers; Moore's law on landmark chips from the 4004 to 2024's GPUs.
* **14. Gates that forget nothing.** Landauer's bound; the Toffoli gate (reversible and universal); Fredkin's gate;
  why quantum computing (Part 53) needs them.
* **15. Frontier: the smallest circuit.** Exact minimum circuits: every 3-input function solved by breadth-first
  search over circuits (30, 843, 21,778 and 569,780 distinct circuits of 1–4 gates; costs 0–4 for 5, 30, 117, 80 and
  24 functions; parity 2, the multiplexer 3, majority 4). The census beyond: 4 inputs, at most 7 gates (Knuth,
  2005); 5 inputs, at most 12 (the last cases settled by computer in 2019); 6 inputs unknown, at the limit of SAT
  solvers. Gate elimination, the method behind every linear lower bound: fix an input, remove at least three gates,
  induct (Blum's 3n, 1984; (3 + 1/86)n, 2016; 3.1n, Li and Yang, 2022, for affine dispersers). The Minimum Circuit
  Size Problem: in NP, NP-completeness open (Levin; Kabanets and Cai, 2000); partial MCSP
  NP-hard (Hirahara, 2022); one-way functions and time-bounded Kolmogorov complexity (Liu and Pass, 2020);
  meta-complexity.
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs3.compute            # every number in the part (about ten seconds)
python tools/build.py cs3 -q l             # a 480p preview
python tools/build.py cs3                  # 1080p
```

## Problems, with solutions

1. **NOR is complete.** Build NOT, OR and AND from NOR.

   *Solution.* NOT x = x NOR x (1 gate). x OR y = NOT(x NOR y) (2 gates). x AND y = (NOT x) NOR (NOT y), by De Morgan
   (3 gates). Since {AND, OR, NOT} is complete (the DNF), so is NOR. These counts are the mirror images of NAND's.

2. **Post's test.** Show {XOR, AND} is not complete but {XOR, AND, 1} is.

   *Solution.* XOR and AND both map 0, 0 to 0, so every circuit of them outputs 0 on the all-zero input: the set is
   trapped in the 0-preserving class and cannot make NOT. Adding the constant 1 escapes that trap; the other four are
   escaped already (AND is not affine and not self-dual, XOR is not monotone and does not preserve 1). Concretely,
   NOT x = x XOR 1, and with NOT and AND we have everything.

3. **A Karnaugh map.** Minimize f = Σm(1, 3, 4, 5, 9, 11, 12, 13).

   *Solution.* With the variables ABCD, the ones form two groups of four: B'D (minterms 1, 3, 9, 11) and BC' (4, 5, 12,
   13). So **f = B'D + BC'**, two terms of two literals, against eight terms of four in the normal form.

4. **Counting functions.** How many Boolean functions of 3 inputs are there, and how many are monotone?

   *Solution.* 2^(2³) = **256** functions. The monotone ones, counted by brute force over all 256 truth tables, number
   **20** (the Dedekind number M(3)): the constants, the three variables, and the and/or combinations of them such as
   majority.

5. **A hazard.** f = xy' + yz with x = z = 1.

   *Solution.* Then f = y' + y = 1 always, but when y changes the term being switched off can fall before the other
   rises (the y' term waits for an inverter), so f glitches to 0 when **y falls** from 1 to 0: yz drops at once and
   xy' rises one inverter delay late. The consensus term of
   xy' and yz is **xz**; adding it holds f at 1 while y changes: f = xy' + yz + xz.

6. **Build: a 4-to-1 multiplexer in NANDs.**

   *Solution.* A 2-to-1 mux in NANDs is NAND(NAND(a, s'), NAND(b, s)) with s' = NAND(s, s): four gates. Three of them
   make a 4-to-1 mux, and the two first-level muxes share one inverter of s₀: **11 NANDs**. The library's mechanical
   `mux_n(2).to_nand()` gives **24** (it rewrites each AND, OR and NOT separately, without sharing or simplifying),
   with depth 9 against the hand design's 5. Both pass the exhaustive check on all 64 inputs.

7. **★ Research: four inputs, and MCSP.** Extend `compute_census` (in `videos/cs/cs3/compute.py`) to all 65,536
   functions of four inputs and recover Knuth's result that the hardest need 7 gates. Open: is the Minimum Circuit
   Size Problem NP-complete?

   *What is known, and where to start.* The breadth-first search over sets of wires that settles three inputs in
   six seconds explodes at four: the number of distinct circuits grows roughly thirtyfold per gate, and seven gates
   are needed. Three ideas make it tractable. (1) *Symmetry*: permuting and negating inputs and negating the output
   (the NPN group, of order 2⁴·4!·2 = 768) preserves cost, so only the 222 NPN classes of 4-input functions need a
   search. (2) *Meet in the middle*: the cost of f is at most the cost of g and h plus one when f = g ∘ h, so costs
   can be built up from small ones without storing circuits (Knuth's "footprint" method, TAOCP 7.1.2). (3) *SAT*:
   encode "a circuit of r gates computes f" as a formula and ask a solver; this is how the last 5-input cases were
   closed (Haaswijk, Soeken, Mishchenko and De Micheli; Kulikov and others). A correct answer is checked by
   exhibiting, for each class, a circuit of the claimed size and an exhaustive proof that none is smaller. On MCSP:
   it is in NP; it is not known to be NP-hard under the usual reductions, and there are results showing that
   proving it NP-hard by certain natural kinds of reduction would itself imply new circuit lower bounds (Murray and
   Williams, 2015). Hirahara (2022) proved NP-hardness for partial truth tables. The full question is open.

## 习题与解答

1. **NOR 是完备的。** 用 NOR 搭出 NOT、OR 和 AND。

   *解答。* NOT x = x NOR x（1 个门）。x OR y = NOT(x NOR y)（2 个门）。x AND y = (NOT x) NOR (NOT y)，由德摩根律（3 个门）。既然
   {AND, OR, NOT} 是完备的（析取范式），NOR 也是。这些门数正是 NAND 的镜像。

2. **波斯特判据。** 证明 {XOR, AND} 不完备，而 {XOR, AND, 1} 完备。

   *解答。* XOR 和 AND 都把 0, 0 映到 0，所以它们组成的任何电路在全零输入上都输出 0：这个集合被困在“保 0”类里，造不出 NOT。加上常数
   1 就逃出了这个陷阱；另外四个陷阱已经逃出（AND 不是仿射的、也不是自对偶的，XOR 不是单调的、也不保 1）。具体地，NOT x = x XOR 1，
   有了 NOT 和 AND 就有了一切。

3. **卡诺图。** 化简 f = Σm(1, 3, 4, 5, 9, 11, 12, 13)。

   *解答。* 变量为 ABCD 时，这些 1 组成两个四格的组：B'D（最小项 1, 3, 9, 11）和 BC'（4, 5, 12, 13）。所以 **f = B'D + BC'**，两项、
   每项两个文字，而范式需要八项、每项四个文字。

4. **数函数。** 3 个输入的布尔函数有多少个？其中单调的有多少个？

   *解答。* 共 2^(2³) = **256** 个。对全部 256 张真值表穷举，单调函数有 **20** 个（戴德金数 M(3)）：两个常数、三个变量，以及它们的
   与、或组合，例如多数函数。

5. **险象。** f = xy' + yz，其中 x = z = 1。

   *解答。* 此时 f = y' + y = 1 恒成立，但当 y 变化时，被关掉的那一项可能先于另一项变高（y' 那一项要等反相器），所以在 **y 从 1 变
   为 0** 时 f 会毛刺到 0：yz 立刻变低，而 xy' 要晚一个反相器延迟才变高。xy' 与 yz 的共识项是 **xz**；加上它，在 y 变化期间 f 保持为 1：f = xy' + yz + xz。

6. **动手：用 NAND 搭 4 选 1 多路选择器。**

   *解答。* 用 NAND 搭的 2 选 1 多路选择器是 NAND(NAND(a, s'), NAND(b, s))，其中 s' = NAND(s, s)：四个门。三个这样的选择器组成 4 选
   1，第一级的两个共享同一个 s₀ 的反相器：**11 个 NAND**。库中机械的 `mux_n(2).to_nand()` 给出 **24** 个（它把每个 AND、OR、NOT 分
   别改写，不共享也不化简），深度 9，而手工设计是 5。两者都通过了全部 64 个输入的穷举检查。

7. **★ 研究题：四个输入，以及 MCSP。** 把 `compute_census`（在 `videos/cs/cs3/compute.py` 里）推广到四个输入的全部 65,536
   个函数，重新得到高德纳的结论：最难的需要 7 个门。未解：最小电路规模问题（MCSP）是 NP 完全的吗？

   *已知什么，从哪里入手。* 对导线集合做广度优先搜索，六秒就能解决三个输入，到四个输入就爆炸了：不同电路的数目每加一个门大约增长
   三十倍，而需要七个门。三个想法让它变得可行。（1）*对称性*：置换、取反输入以及对输出取反（NPN 群，阶为 2⁴·4!·2 = 768）不改变
   代价，所以只需搜索四输入函数的 222 个 NPN 等价类。（2）*中间相遇*：当 f = g ∘ h 时，f 的代价至多是 g 与 h 的代价之和加一，于是
   可以不存储电路、由小代价逐步建立大代价（高德纳的“足迹”方法，TAOCP 7.1.2）。（3）*SAT*：把“r 个门的电路计算 f”编码成公式交给
   求解器；最后几个五输入情形就是这样解决的（Haaswijk、Soeken、Mishchenko 与 De Micheli；Kulikov 等）。正确的答案要这样检验：对每个
   等价类，给出一个达到所称规模的电路，并穷举证明不存在更小的。关于 MCSP：它属于 NP；在通常的归约下还不知道它是 NP 难的，而且有
   结果表明，用某些自然的归约证明它 NP 难，本身就会推出新的电路下界（Murray 与 Williams，2015）。Hirahara（2022）对部分真值表证明了
   NP 难。完整的问题仍然悬而未决。

## Glossary additions

开关 switch · 继电器 relay · 串联 / 并联 series / parallel · 晶体管 transistor · 互补金属氧化物半导体 CMOS · 上拉 / 下拉网络
pull-up / pull-down network · 传输特性曲线 transfer curve · 噪声容限 noise margin · 与非门 / 或非门 NAND / NOR · 完备的
(functionally) complete · 析取范式 / 合取范式 DNF / CNF · 卡诺图 Karnaugh map · 质蕴涵项 prime implicant · 多路选择器
multiplexer · 译码器 / 编码器 decoder / encoder · 查找表 lookup table (LUT) · 现场可编程门阵列 FPGA · 二元决策图 binary decision
diagram (BDD) · 香农展开 Shannon expansion · 电路规模 / 深度 circuit size / depth · 关键路径 critical path · 传播延迟 propagation
delay · 险象 / 毛刺 hazard / glitch · 共识项 consensus term · 扇出 fan-out · 桶形移位器 barrel shifter · 优先编码器 priority encoder
· 可逆门 reversible gate · 托福利门 Toffoli gate

## Sources

Books: Harris & Harris, *Digital Design and Computer Architecture*, ch. 1–2; Nisan & Schocken, *The Elements of
Computing Systems*, ch. 1; Petzold, *Code*; Weste & Harris, *CMOS VLSI Design*, ch. 1; Wegener, *The Complexity of
Boolean Functions*; Jukna, *Boolean Function Complexity*; Knuth, *TAOCP* vol. 4A §7.1.

Papers: Boole (1854); Shannon, "A symbolic analysis of relay and switching circuits" (1938) and "The synthesis of
two-terminal switching circuits" (1949); Post (1941); Karnaugh (1953); Lupanov (1958); Landauer (1961); Moore,
"Cramming more components onto integrated circuits" (1965); Khrapchenko (1971); Bennett (1973); Masek (1979);
Toffoli (1980); Fredkin & Toffoli (1982); Bryant (1986, 1991); Håstad (1986); Rojas (1998); Umans (2001); Li & Yang,
"3.1n − o(n) circuit lower bounds for explicit functions" (2022).
