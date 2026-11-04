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
