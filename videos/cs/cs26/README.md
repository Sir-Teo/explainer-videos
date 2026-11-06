# Computer Science, Built — Part 26: P versus NP

Part 26 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act V, *Limits and Secrets*. In 1956 Gödel asked von Neumann whether
finding a proof could be as easy as checking one. This part makes the question precise, proves the theorems that are
known, builds the Cook–Levin formula and the classic reductions and runs them, and explains why the question has
resisted fifty years of attack.

The instrument is `explainer/cs/algo/complexity.py`. It holds:
* a CDCL SAT solver (two watched literals, 1-UIP learning, VSIDS, phase saving, Luby restarts) and plain DPLL;
* SAT to 3-SAT; 3-SAT to independent set, clique and vertex cover; Karp's 3-colouring gadgets with k-colouring as CNF;
  Sipser's subset-sum digits, with maps from satisfying assignments to solutions of each;
* the Cook–Levin tableau for a small nondeterministic Turing machine: legal 2 × 3 windows generated from the machine,
  Tseitin-encoded, and decoded back from a model;
* Savitch's CANYIELD, TQBF evaluation and generalized geography;
* Pratt certificates; Schur and Pythagorean-triple colourings as CNF.

It is tested in `tests/test_cs26_complexity.py`. CDCL and DPLL agree with brute force on 300 random formulas. Every
reduction preserves satisfiability, and the mapped-back answers are checked. The tableau is satisfiable exactly when the
machine accepts. Savitch, TQBF, geography, the Pratt certificates and S(3) = 13 are checked too.

* **Finding against checking.** Hook.
  - Gödel's letter of 20 March 1956.
  - A 3-colourable graph of 60 vertices and 112 edges: a colouring is checked in 5 µs, found by our solver in about a
    millisecond; brute force would take 7 × 10¹⁵ years.
* **1. What counts as efficient.**
  - n², n³, 2ⁿ and n! at a microsecond a step.
  - Edmonds and Cobham (1965); robustness of P; the extended Church–Turing thesis.
* **2. More time, more problems.**
  - The time hierarchy theorem by a clocked diagonal (proved); the nested classes.
  - Savitch's theorem (proved), run on paths of 4, 8 and 16 nodes: depth 3, 4 and 5, with 20, 443 and 47,038 calls.
* **3. NP.**
  - Verifiers and certificates; the equivalence with nondeterministic machines.
  - Examples; Babai's quasi-polynomial graph isomorphism; AKS.
* **4. Reductions and completeness.**
  - Polynomial reductions, NP-hardness and completeness.
  - Search reduces to decision: five yes/no questions find a satisfying assignment.
* **5. Cook–Levin.**
  - The tableau of our NTM on 0010, with sliding 2 × 3 windows (408 legal windows).
  - The four-part formula and why it is polynomial.
  - The formulas built and solved for inputs of length 2 to 8: 3,416 to 23,324 variables, solved in under a second.
    The input 0000 is proved unsatisfiable.
* **6. The web of reductions.**
  - One 5-clause formula through independent set (15 vertices, 29 edges), clique and vertex cover.
  - Through 3-colouring: 41 vertices and 75 edges, as 123 variables and 389 clauses for the solver. The colouring maps
    back to a satisfying assignment, and an unsatisfiable formula's graph is not 3-colourable.
  - Through subset sum: 18 nine-digit numbers and the target 111133333, hit by the mapped subset.
  - Karp's 21 problems as a family tree.
* **7. NP-completeness everywhere.**
  - Tetris, Minesweeper, Sudoku, protein folding.
  - At work: scheduling, packing, dependency resolution, register allocation.
* **8. Strong and weak hardness.**
  - Subset-sum DP on 30 numbers: each extra digit costs ten times more (0.008 ms at 2 digits to 11.5 ms at 6).
    Meet in the middle at 12 digits: 50 ms.
  - Strong NP-hardness; Ibarra–Kim's approximation scheme.
* **9. coNP and the polynomial hierarchy.**
  - Tautology; NP ∩ coNP and factoring.
  - A Pratt certificate for 2⁶¹ − 1 (60 checks); the hierarchy and its collapses.
* **10. Space.**
  - TQBF by recursion (1,029 nodes at 16 variables against 131,071 in the full tree); Stockmeyer–Meyer.
  - Generalized geography on a 9-vertex graph (11 positions).
  - Hex, Go, chess and checkers; L, NL, NL = coNL, Reingold.
* **11. Time in square-root space.**
  - Hopcroft–Paul–Valiant; tree evaluation and Cook–Mertz; Williams 2025. At a trillion steps the bound drops from
    about 2.5 × 10¹⁰ to 6.3 × 10⁶ cells.
* **12. Between P and NP-complete.**
  - Ladner's theorem (sketch); the suspects; the CSP dichotomy (Bulatov; Zhuk).
* **13. SAT in practice.**
  - CDCL step by step; DPLL against CDCL at the threshold.
  - The phase transition for n = 50, 100 and 150 (40 or 20 formulas per point). The fraction satisfiable falls through
    ½ near 4.3, where the median conflicts peak: 2,259 at n = 150.
  - Schur numbers S(3) = 13 and S(4) = 44 by our solver; S(5) = 160 (Heule 2017); the Boolean Pythagorean triples
    (7,825; Heule, Kullmann and Marek 2016).
* **14. Why it is hard.**
  - Relativization (Baker–Gill–Solovay); natural proofs (Razborov–Rudich); algebrization (Aaronson–Wigderson).
  - Williams's ACC⁰ lower bound.
* **15. Five possible worlds.**
  - Impagliazzo's worlds; what P = NP would mean; Gasarch's poll.
  - Could the question be independent of set theory?
* **16. Frontier: complexity about complexity.**
  - Exact De Morgan formula sizes of all 256 three-input functions: majority 5 leaves, parity 10, against
    Khrapchenko's 9. Shannon's counting argument.
  - The state of lower bounds (3.1n for circuits; n³ for formulas; ACC⁰); geometric complexity theory.
  - Meta-complexity: MCSP, Hirahara (2022), Liu–Pass (2020).
  - Open problems. Outro.

## Build

```bash
python -m videos.cs.cs26.compute           # every number in the part (the famous-instance item takes the longest)
python tools/build.py cs26 -q l            # a 480p preview
python tools/build.py cs26                 # 1080p
```

## Problems, with solutions

1. **P, NP and coNP.** Prove that if P = NP then NP = coNP, and that an NP-complete problem in coNP implies
   NP = coNP.

   *Solution.* P is closed under complement (flip the answer of a polynomial-time decider). If P = NP then
   coNP = co-P = P = NP. For the second claim, let L be NP-complete with L ∈ coNP, and take any A ∈ NP. Then A ≤ₚ L
   by some f, and the same f reduces the complement of A to the complement of L, which is in NP. So the complement of
   A is in NP, that is, A ∈ coNP; hence NP ⊆ coNP. Conversely, if B ∈ coNP then its complement is in NP ⊆ coNP, so B
   ∈ NP. The classes are equal.

2. **2-SAT is easy.** Show that 2-SAT is in P, and explain where the 3-SAT gadgets fail.

   *Solution.* Each clause (a ∨ b) is equivalent to the implications ¬a → b and ¬b → a. Build the implication graph
   on the 2n literals. If some variable x and ¬x lie in the same strongly connected component, then x → ¬x → x, so
   the formula is unsatisfiable. Otherwise, take the components in reverse topological order (Part 18). Set each
   literal true when its component comes after its negation's; no implication then leads from true to false
   (Aspvall, Plass and Tarjan, 1979). Linear time. A 3-clause (a ∨ b ∨ c) is (¬a ∧ ¬b) → c: an implication with a
   conjunction on the left, which no graph of single-literal edges can express. Every NP-completeness reduction has
   to manufacture exactly such an "and".

3. **Hamiltonian path.** Reduce 3-SAT to Hamiltonian path.

   *Solution* (Sipser, Theorem 7.46). For each variable xᵢ build a "diamond": a top and a bottom vertex joined by a
   horizontal row of vertices that can be traversed left-to-right (xᵢ true) or right-to-left (xᵢ false). Stack the
   diamonds so that the bottom of one is the top of the next; the path runs from the first top to the last bottom.
   For each clause cⱼ add a single vertex. If xᵢ occurs in cⱼ, add a detour from a pair of adjacent row vertices in
   diamond i to cⱼ and back, oriented so it can be taken only when traversing left-to-right; for ¬xᵢ, right-to-left.
   Separator vertices between the pairs stop the path from leaving one diamond and re-entering another. A satisfying
   assignment gives a path: traverse each row in its truth direction and visit each clause vertex once by a detour
   from one true literal. Conversely, a Hamiltonian path must return from each detour to the same row, so it fixes a
   direction per row, an assignment, and visits each clause through a true literal.

4. **Search from decision.** Show that if SAT can be decided in polynomial time, a satisfying assignment can be found
   in polynomial time.

   *Solution.* First ask whether φ is satisfiable; if not, stop. Then for i = 1, …, n ask whether φ with x₁, …, xᵢ₋₁
   fixed as chosen and xᵢ = 1 is satisfiable. If yes, fix xᵢ = 1; otherwise xᵢ = 0 must extend to a satisfying
   assignment, because the formula with the previous choices was satisfiable. That is n + 1 calls to the decider on
   formulas no larger than φ, so polynomial time. Chapter 4 ran it: five calls for four variables.

5. **Build: Sudoku.** Reduce Sudoku to SAT, solve a hard puzzle with this part's CDCL solver, and count its conflicts.

   *Solution.* Variables x(r, c, v) for row, column and value, 729 in all. Each cell gets at least one value (81
   clauses of 9 literals) and at most one (81 × 36 binary clauses). Each value appears at least once in every row,
   column and box (243 clauses) and at most once (243 × 36). That is 324 long clauses and 11,664 binary ones, plus a
   unit clause for each given digit. Number the variables 81(r − 1) + 9(c − 1) + v. Run `complexity.cdcl(729,
   clauses)`, decode the true variables back into a grid, and check every row, column and box. Arto Inkala's 2012
   "world's hardest Sudoku" (21 givens, 12,009 clauses) takes our solver 111 conflicts and about 0.1 s; most of the
   work is unit propagation. Puzzles designed to defeat human techniques are not especially hard for clause
   learning.

6. ★ **Research: the threshold at small n.** For random 3-SAT, locate the threshold for n ≤ 300 with our solver,
   estimate its width as a power of n, and compare the peak cost with the satisfiability threshold.

   *Where to start.* Friedgut (1999) proved that a sharp threshold exists, possibly depending on n. The cavity method
   predicts its limit at about 4.267 (Mézard, Parisi and Zecchina, 2002; Mertens, Mézard and Zecchina, 2006). Ding,
   Sly and Sun (2015) proved the analogous prediction for large k. Kirkpatrick and Selman (1994) observed finite-size
   scaling: the curves for different n collapse when plotted against (m/n − α_c) n^{1/ν}. Repeat that experiment with
   enough formulas per point (thousands, not our twenty to forty) to put error bars on α_c(n) and ν. Then ask whether
   the peak of the median conflicts sits at the same ratio as the 50% point, or drifts as n grows; our data put the
   peak slightly above the crossing at n = 100 and at it for n = 150. Measure, fit, and compare the fitted trend of α_c(n) with
   4.267.

## 习题与解答

1. **P、NP 与 coNP。** 证明若 P = NP 则 NP = coNP；并证明若某个 NP 完全问题属于 coNP，则 NP = coNP。

   *解答。* P 对补运算封闭（把多项式时间判定器的答案翻转即可）。若 P = NP，则 coNP = co-P = P = NP。对第二个结论，设 L 是 NP 完全的且
   L ∈ coNP，任取 A ∈ NP。则有某个 f 使 A ≤ₚ L，同一个 f 也把 A 的补归约到 L 的补，而后者属于 NP。所以 A 的补属于 NP，即 A ∈ coNP；
   于是 NP ⊆ coNP。反过来，若 B ∈ coNP，则它的补属于 NP ⊆ coNP，所以 B ∈ NP。两个类相等。

2. **2-SAT 很容易。** 证明 2-SAT 属于 P，并说明 3-SAT 的小部件在哪里失效。

   *解答。* 每个子句 (a ∨ b) 等价于蕴涵 ¬a → b 与 ¬b → a。在 2n 个文字上建蕴涵图。若某个变量 x 与 ¬x 在同一个强连通分量里，则
   x → ¬x → x，公式不可满足。否则按逆拓扑序处理各分量（第 18 部分）：若一个文字所在分量排在其否定所在分量之后，就令它为真；这样就不会有
   蕴涵从真导向假（Aspvall、Plass 与 Tarjan，1979）。线性时间。三文字子句 (a ∨ b ∨ c) 是 (¬a ∧ ¬b) → c：左边是一个合取，单文字边构成的图
   表达不了。每个 NP 完全性归约都必须制造出这样一个“与”。

3. **哈密顿路径。** 把 3-SAT 归约到哈密顿路径。

   *解答*（Sipser，定理 7.46）。为每个变量 xᵢ 建一个“菱形”：顶点和底点之间连着一排水平顶点，可以从左到右（xᵢ 为真）或从右到左（xᵢ 为假）
   走过。把菱形上下叠起，一个的底点就是下一个的顶点；路径从第一个顶点走到最后一个底点。为每个子句 cⱼ 加一个顶点。若 xᵢ 出现在 cⱼ 中，就从
   菱形 i 那排里一对相邻顶点出发，绕到 cⱼ 再回来，方向设成只有从左到右走时才能绕；对 ¬xᵢ 则是从右到左。各对之间的分隔顶点阻止路径离开一个
   菱形再进入另一个。满足赋值给出一条路径：每排按真值方向走，每个子句顶点通过一个真文字绕行访问一次。反过来，哈密顿路径从每次绕行必须回到
   同一排，所以每排确定一个方向，即一个赋值，并且通过某个真文字访问每个子句。

4. **由判定得到搜索。** 证明若 SAT 能在多项式时间内判定，则满足赋值也能在多项式时间内找到。

   *解答。* 先问 φ 是否可满足；若否，停止。然后对 i = 1, …, n，问：在已选定 x₁, …, xᵢ₋₁ 并令 xᵢ = 1 时 φ 是否可满足。若是，就定 xᵢ = 1；
   否则 xᵢ = 0 必定能扩展成满足赋值，因为带着之前选择的公式是可满足的。总共 n + 1 次调用判定器，每次的公式都不比 φ 大，所以是多项式时间。
   第 4 章运行过它：四个变量用了五次调用。

5. **动手：数独。** 把数独归约到 SAT，用本部分的 CDCL 求解器解一道难题，并统计冲突次数。

   *解答。* 变量 x(r, c, v) 表示行、列、数值，共 729 个。每格至少一个值（81 个 9 文字子句），至多一个（81 × 36 个二元子句）；每个数值在每行、
   每列、每宫至少出现一次（243 个子句），至多一次（243 × 36 个）。共 324 个长子句和 11,664 个二元子句，再为每个已给数字加一个单元子句。
   把变量编号为 81(r − 1) + 9(c − 1) + v，运行 `complexity.cdcl(729, clauses)`，把为真的变量解码回网格，再检查每行、每列、每宫。
   Arto Inkala 2012 年的“世界最难数独”（21 个提示数，12,009 个子句）只花了我们的求解器 111 次冲突、约 0.1 秒，大部分工作是单元传播；
   专为难倒人类技巧而设计的题目，对子句学习并不特别难。

6. ★ **研究：小 n 时的阈值。** 用我们的求解器在 n ≤ 300 时定位随机 3-SAT 的阈值，估计其宽度作为 n 的幂，并比较代价峰值与可满足性阈值的位置。

   *从哪里入手。* Friedgut（1999）证明存在一个尖锐阈值（可能依赖于 n）。空腔方法预测其极限约为 4.267（Mézard、Parisi 与 Zecchina，2002；
   Mertens、Mézard 与 Zecchina，2006），而 Ding、Sly 与 Sun（2015）对大 k 证明了相应的预测。Kirkpatrick 与 Selman（1994）观察到有限尺寸
   标度：把不同 n 的曲线对 (m/n − α_c) n^{1/ν} 作图会重合。用足够多的公式（每点几千个，而不是我们的二十到四十个）重做这个实验，给 α_c(n) 和
   ν 加上误差棒；再问冲突中位数的峰值是否与 50% 点在同一比值，还是随 n 漂移（我们的数据中，n = 100 与 150 时峰值略高于交叉点）。测量、拟合，
   并把 α_c(n) 的拟合趋势与 4.267 比较。

## Glossary additions

多项式时间 polynomial time · 时间层级定理 time hierarchy theorem · 空间层级 space hierarchy · Savitch 定理 Savitch's theorem ·
验证器 verifier · 证书 certificate · 非确定性 nondeterminism · 多项式时间归约 polynomial-time reduction · NP 难 NP-hard ·
NP 完全 NP-complete · Cook–Levin 定理 Cook–Levin theorem · 表格 tableau · 合法窗口 legal window · 独立集 independent set ·
团 clique · 顶点覆盖 vertex cover · 三着色 3-colouring · 子集和 subset sum · 自归约 self-reducibility · 伪多项式 pseudo-polynomial ·
强 NP 难 strongly NP-hard · 完全多项式时间近似方案 FPTAS · coNP · Pratt 证书 Pratt certificate · 多项式层级 polynomial hierarchy ·
量化布尔公式 TQBF · 广义地理游戏 generalized geography · 对数空间 logarithmic space · 树求值 tree evaluation · Ladner 定理 Ladner's theorem ·
二分定理 dichotomy theorem · 冲突驱动子句学习 CDCL · 单元传播 unit propagation · 相变 phase transition · 相对化 relativization ·
自然证明 natural proofs · 代数化 algebrization · 单向函数 one-way function · 最小电路规模问题 MCSP · 元复杂性 meta-complexity

## Sources

*Canon.* Books:
- Sipser, *Introduction to the Theory of Computation* (3rd ed., 2012), ch. 7–8;
- Arora & Barak, *Computational Complexity: A Modern Approach* (2009), ch. 1–6;
- Papadimitriou, *Computational Complexity* (1994);
- Garey & Johnson, *Computers and Intractability* (1979);
- Moore & Mertens, *The Nature of Computation* (2011), ch. 4–6;
- Goldreich, *P, NP, and NP-Completeness* (2010);
- Fortnow, *The Golden Ticket* (2013); Biere, Heule, van Maaren & Walsh (eds.), *Handbook of Satisfiability* (2nd ed.,
  2021).

Papers:
- Foundations: Gödel's letter to von Neumann (1956); Edmonds (1965); Cobham (1965); Hartmanis & Stearns (1965);
  Savitch (1970); Cook (1971); Karp (1972); Levin (1973); Meyer & Stockmeyer (1972); Stockmeyer & Meyer (1973);
  Ladner (1975); Pratt (1975).
- Hardness everywhere: Kaye (2000); Demaine, Hohenberger & Liben-Nowell (2003); Yato & Seta (2003); Berger &
  Leighton (1998); Mancinelli et al. (2006); Schaefer (1978); Lichtenstein & Sipser (1980); Robson (1983, 1984);
  Fraenkel & Lichtenstein (1981); Reisch (1981); Ibarra & Kim (1975); Garey & Johnson (1978).
- Space: Immerman (1988); Szelepcsényi (1987); Reingold (2005); Hopcroft, Paul & Valiant (1977); Cook, McKenzie,
  Wehr, Braverman & Santhanam (2012); Cook & Mertz (2024); Williams, "Simulating time with square-root space" (2025).
- NP and coNP: Babai (2015); Agrawal, Kayal & Saxena (2002); Karp & Lipton (1980); Bulatov (2017); Zhuk (2017).
- SAT: Davis, Logemann & Loveland (1962); Marques-Silva & Sakallah (1996); Moskewicz et al., "Chaff" (2001); Friedgut
  (1999); Kirkpatrick & Selman (1994); Ding, Sly & Sun (2015); Heule, Kullmann & Marek (2016); Heule (2017).
- Barriers and frontier: Baker, Gill & Solovay (1975); Razborov & Rudich (1994); Aaronson & Wigderson (2008);
  Williams (2011); Murray & Williams (2018); Shannon (1949); Khrapchenko (1971); Håstad (1986, 1998); Tal (2014);
  Li & Yang (2022); Mulmuley & Sohoni (2001); Bürgisser, Ikenmeyer & Panova (2016); Liu & Pass (2020); Hirahara
  (2022); Impagliazzo, "A personal view of average-case complexity" (1995); Hartmanis & Hopcroft (1976); Aaronson,
  "P =? NP" (2016); Gasarch, "The third P =? NP poll" (2019).
