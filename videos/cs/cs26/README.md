# Computer Science, Built — Part 26: P versus NP

Part 26 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act V, *Limits and Secrets*. In 1956 Gödel asked von Neumann whether
finding a proof could be as easy as checking one. This part makes the question precise, develops scoped proof sketches, builds a bounded Cook–Levin encoding and concrete reductions, and distinguishes finite experiments from asymptotic theorems. New numerical payloads retain full inputs, models, certificates and cutoffs.

The instrument is `explainer/cs/algo/complexity.py`. It holds:
* a CDCL SAT solver (two watched literals, 1-UIP learning, VSIDS, phase saving, Luby restarts) and plain DPLL;
* SAT to 3-SAT; 3-SAT to independent set, clique and vertex cover; Karp's 3-colouring gadgets with k-colouring as CNF;
  Sipser's subset-sum digits, with maps from satisfying assignments to solutions of each;
* the Cook–Levin tableau for a small nondeterministic Turing machine: legal 2 × 3 windows generated from the machine,
  Tseitin-encoded, and decoded back from a model;
* Savitch's CANYIELD, TQBF evaluation and generalized geography;
* Pratt certificates; Schur and Pythagorean-triple colourings as CNF.

It is tested in `tests/test_cs26_complexity.py`: 19 tests include 300 random solver comparisons against an independent truth-table evaluator, all eight projected inputs of the colouring gadget, duplicate/empty clauses, integer domains, budgets, zero-step reachability, quantified-variable scope, malformed Pratt trees and false RUP proofs. These are finite implementation checks.

Numerical items use schema 2. Each payload binds the complete numerical source signature and the bytes of its artifacts. All 1,393 actual CDCL queries are retained: 719 SAT, 673 UNSAT and one UNKNOWN. Resolved answers have native Glucose 4.2 cross-checks; every positive model is evaluated directly. One Schur refutation has an independently checked RUP trace. Other native UNSAT results are cross-checks, not claims that their proof traces were checked. A conflict-budget cutoff is never inferred to be UNSAT from a `None` model.

The teaching APIs reject literal zero, out-of-range variables, nonpositive restart/conflict budgets, invalid quantifiers and oversized clauses in the at-most-three-literal reductions. DPLL handles empty clauses. Duplicate literals are normalized consistently. An empty 3-colouring clause produces a K4 obstruction. Savitch uses equality at zero steps and integer half-budgets. Geography maps arbitrary hashable vertex labels to dense internal bits; its winner is the initial placer, with the second player moving next. Memoization may use exponential space. Pratt construction accepts primes below 2⁶⁴ and uses trial division of p−1; malformed/cyclic checker inputs fail without looping. The checker certifies the order criterion independently of the constructor's primality screen.

* **Finding against checking.** Hook.
  - Gödel's letter of 20 March 1956.
  - A planted 3-colourable graph of 60 vertices and 112 edges. Full edge lists and both planted/solved colourings are retained. The displayed enumeration scenario multiplies 3⁶⁰ by the measured average full valid-colouring check; it is neither a measured search nor a lower bound.
* **1. What counts as efficient.**
  - n², n³, 2ⁿ and n! at a microsecond a step.
  - Edmonds and Cobham (1965); robustness of P; the extended Church–Turing thesis.
* **2. More time, more problems.**
  - The time hierarchy theorem: constructible f,g ≥ n and f log f = o(g) imply DTIME(f) ⊊ DTIME(g). Padded descriptions absorb fixed machine constants and finite exceptions. The screen is a proof sketch, not the false unqualified TIME(f) ⊊ TIME(f log f) claim.
  - Savitch for s ≥ log n; runs on paths of 4, 8 and 16 nodes have depths 3, 4 and 5, with 20, 443 and 47,038 calls. The illustrative three-configuration-slot count excludes the stored input graph, iterators and Python overhead. Whole configuration graphs have 2^{O(s)} vertices under the stated read-only-input convention.
* **3. NP.**
  - Verifiers and certificates; the equivalence with nondeterministic machines.
  - Examples; Babai's quasi-polynomial graph isomorphism; AKS.
* **4. Reductions and completeness.**
  - Polynomial reductions, NP-hardness and completeness.
  - Search reduces to decision: five yes/no questions find a satisfying assignment.
* **5. Cook–Levin.**
  - The NTM on 0010 has T = 6 rows and at most five transitions. Acceptance is absorbing and required in the final row. Its 408 legal local windows are specific to this fixed machine. All decoded traces are checked against whole-machine transitions and separate reachable-configuration layers.
  - The four-part formula and why it is polynomial.
  - The formulas built and solved for inputs of length 2 to 8: 3,416 to 23,324 variables. Full formulas and models are retained; host durations are illustrative. The bounded 0000 instance is UNSAT, also confirmed by direct configuration exploration.
* **6. The web of reductions.**
  - One 5-clause formula through independent set (15 vertices, 29 edges), clique and vertex cover.
  - Through 3-colouring: 41 vertices and 75 edges, as 123 variables and 389 clauses for the solver. The colouring maps
    back to a satisfying assignment, and an unsatisfiable formula's graph is not 3-colourable.
  - Through subset sum: 18 nine-digit numbers and the target 111133333, hit by the mapped subset.
  - Karp's 21 problems as a family tree.
* **7. NP-completeness everywhere.**
  - Specified generalized decision versions of offline Tetris, Minesweeper consistency, Sudoku completion and lattice hydrophobic-polar folding. Fixed boards and physical protein behaviour require separate models.
  - At work: scheduling, packing, dependency resolution, register allocation.
* **8. Strong and weak hardness.**
  - Subset-sum bitsets on 30 numbers retain sums 0..W inclusive, with all weights, target, full final bitset and explicit witness. Independent meet-in-the-middle witnesses confirm each target. Integer bit costs remain relevant; decimal digit growth is a numeric-range illustration, not an exact timing law.
  - Strong numerical hardness; the positive-profit 0–1 knapsack FPTAS. Weak hardness alone does not guarantee an FPTAS. A strong-hardness obstruction to FPTAS needs polynomially bounded integer objectives on the hard restricted instances. Asymptotic bin-packing schemes have a different guarantee.
* **9. coNP and the polynomial hierarchy.**
  - Tautology; NP ∩ coNP and factoring.
  - The complete Pratt tree for 2⁶¹ − 1 has 60 certificate nodes; a separate arithmetic checker performs 89 modular powers. Full trees for both factors of the displayed N are also retained. The decision language asks for a divisor 2 ≤ d ≤ k < N. NP and coNP are duals at PH level 1; quantified strings have polynomial bit length.
* **10. Space.**
  - TQBF by recursion (1,029 nodes at 16 variables against 131,071 in the full tree); Stockmeyer–Meyer.
  - Generalized geography on a 9-vertex graph (11 positions).
  - Hex, Go, chess and checkers; L, NL, NL = coNL, Reingold.
* **11. Time in square-root space.**
  - Hopcroft–Paul–Valiant; Cook–Mertz tree evaluation; Williams 2025: deterministic multitape TIME(t) ⊆ SPACE(√(t log t)) for t ≥ n. The table evaluates asymptotic functions with constants omitted, not measured/guaranteed memory cells. For constructible s ≥ n and fixed ε > 0, SPACE(s) is not contained in TIME(s^{2−ε}). Tree evaluation in L, or outside NL, is not settled by Cook–Mertz.
* **12. Between P and NP-complete.**
  - Ladner's theorem (sketch); the suspects; the CSP dichotomy for each fixed finite constraint language on a finite domain (Bulatov; Zhuk).
* **13. SAT in practice.**
  - CDCL step by step; DPLL against CDCL at the threshold.
  - Finite random 3-SAT samples for n = 50, 100 and 150 (40, 40 and 20 trials per point), with every formula and status retained and Wilson 95% binomial intervals. A coarse finite plot neither identifies the limiting constant nor establishes a scaling exponent. See the dated 2026 update below.
  - Local Schur 13/3 and 44/4 positive colourings are fully checked; the Schur 14/3 native proof has 92 checked RUP additions. The 45/4 teaching run exhausts 30,000 conflicts and remains UNKNOWN. Complete local Pythagorean colourings are checked; the 7,825 triple encoding is independently matched to Euclid parametrization. Published S(5) = 160 and the 7,825 boundary are separate results, whose huge proofs are not rerun here.
* **14. Why it is hard.**
  - Relativization (Baker–Gill–Solovay); natural proofs (Razborov–Rudich); algebrization (Aaronson–Wigderson).
  - Williams's ACC⁰ lower bound.
* **15. Five possible worlds.**
  - Impagliazzo's worlds; what P = NP would mean; Gasarch's poll.
  - Could the question be independent of set theory?
* **16. Frontier: complexity about complexity.**
  - Exact De Morgan formula sizes of all 256 three-input functions: majority 5 leaves, parity 10, against
    Khrapchenko's 9. Shannon's counting argument.
  - Dated lower-bound examples: B₂ fan-in-two gate circuits differ from literal-leaf formulas. Li–Yang 2022 is a 3.1n−o(n) example, not a verified current-record survey. Superpolynomial SAT circuits would prove NP ⊄ P/poly, a sufficient stronger route to P ≠ NP, not a necessary equivalence. Five n is linear, not superlinear; geometric occurrence-obstruction limits do not reject all of GCT.
  - Meta-complexity: ordinary MCSP versus partial MCSP. Hirahara 2022 proves randomized polynomial-time reduction hardness. Liu–Pass 2020 uses mild average hardness of exact Kᵗ on uniformly random strings for suitable polynomial t ≥ (1+ε)n; it is not an equivalence with public-key encryption.
  - Open problems. Outro.

## Build

```bash
python -m videos.cs.cs26.compute           # validate source/artifact signatures; recompute stale items
python -m unittest tests.test_cs26_complexity
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

2. **2-SAT is easy.** Prove 2-SAT is in P, then explain why a direct implication-graph encoding does not represent a general 3-clause.

   *Solution.* Turn (a ∨ b) into ¬a → b and ¬b → a, including repeated literals for units. An empty clause is immediately UNSAT. If x and ¬x share an SCC, the formula is UNSAT; otherwise an SCC topological ordering gives a satisfying assignment, in linear time. For the obstruction, every 2-CNF relation is closed under coordinate-wise majority: if a two-literal clause were false at the majority of three satisfying assignments, each literal would be false in at least two assignments, so some assignment would falsify both. Existential projection preserves this closure. But 3-OR contains 100, 010 and 001 and excludes their majority 000. Thus no existential 2-CNF gadget represents 3-OR exactly. This is a specific expressibility argument, not a claim that every NP-completeness reduction must manufacture a particular AND gadget.

3. **Hamiltonian path.** Reduce 3-SAT to directed Hamiltonian path, specifying the variable/clause ports and why cross-row detours fail.

   *Solution.* For n variables and m clauses, introduce connectors b₀,…,bₙ. Variable row i has vertices vᵢ,₀,…,vᵢ,₃ₘ₊₂ and both directed edges between every consecutive pair. Add bᵢ₋₁ → each row endpoint, and each row endpoint → bᵢ. For clause j = 1,…,m, create cⱼ and dedicate the pair Lᵢⱼ = vᵢ,₃ⱼ₋₁, Rᵢⱼ = vᵢ,₃ⱼ in every row. A positive occurrence adds Lᵢⱼ → cⱼ → Rᵢⱼ; a negative occurrence reverses those two ports. Keep the direct row edges. Non-port spacer vertices separate successive pairs and occur before/after the first/last pair. The graph has O(nm+n+m) vertices and edges. Source b₀ has indegree zero and sink bₙ has outdegree zero, forcing the endpoints of any spanning directed path.

   Every spacer has only its two row neighbours, so an internal spanning path must use both of those incidences. Each port therefore already uses one row-side incidence and has only one remaining path incidence: either its paired port or cⱼ. If a path enters cⱼ from one pair and exits into another pair, the unused mate of the entering port cannot obtain its remaining incidence: its partner and cⱼ have already used theirs. Thus each clause detour returns to the same pair. Each row is traversed in one consistent direction; interpret left-to-right as true. All clause vertices must be visited through an occurrence compatible with that direction, giving a satisfying assignment. Conversely, a satisfying assignment fixes each row direction; choose one true occurrence per clause and replace that pair's direct edge with the two-edge detour. This visits every vertex exactly once. The zero-clause case reduces to rows without clause detours. The retained finite audit compares independent truth-table SAT with exhaustive Hamiltonian-path search on 128 complete graphs, including an UNSAT full eight-clause three-variable example; that audit supports the implementation of this recipe, while the paired-port argument proves its general correctness.

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
   clauses)`, decode the true variables back into a grid, and check every row, column and box.

   The retained 21-clue exercise puzzle is:

   ```text
   800000000
   003600000
   070090200
   050007000
   000045700
   000100030
   001000068
   008500010
   090000400
   ```

   Run `python -m videos.cs.cs26.compute sudoku`. The current retained run has 111 teaching-solver conflicts; host time is in the schema-2 payload. All 12,009 clauses, the full SAT model and the decoded grid are retained, with independent row, column, box and given-clue checks. A puzzle's human difficulty is not a solver complexity guarantee.

6. ★ **Research: finite-size crossings and widths.** Estimate the 50% crossing and the 10%–90% window for n ≤ 300, including binomial uncertainty and solver cutoffs. Use independent formulas at each point. Report UNKNOWN separately; do not count timeouts as UNSAT. Compare the location of the median-conflict peak with the finite crossing. Increase sample size and ratio resolution before fitting, propagate crossing uncertainty, and test sensitivity to the chosen size range. A power-law fit over a few small n values does not prove an asymptotic exponent.

   *Starting evidence.* Our 1,300 formulas use proper random 3-clauses: three distinct uniformly sampled variables, independent fair signs, and clauses sampled with replacement. There are 40 trials per ratio for n = 50 and 100 and 20 for n = 150. Schema-2 payloads retain Wilson 95% intervals and all conflict counts. Friedgut's sharpness theorem concerns a shrinking transition window; Ding–Sly–Sun 2015 identifies the limiting prediction for sufficiently large k. Consult the dated 2026 reports below for newer existence/computability and upper-bound claims. None is established by this finite exercise.

## 习题与解答

1. **P、NP 与 coNP。** 证明若 P = NP 则 NP = coNP；并证明若某个 NP 完全问题属于 coNP，则 NP = coNP。

   *解答。* P 对补运算封闭（把多项式时间判定器的答案翻转即可）。若 P = NP，则 coNP = co-P = P = NP。对第二个结论，设 L 是 NP 完全的且
   L ∈ coNP，任取 A ∈ NP。则有某个 f 使 A ≤ₚ L，同一个 f 也把 A 的补归约到 L 的补，而后者属于 NP。所以 A 的补属于 NP，即 A ∈ coNP；
   于是 NP ⊆ coNP。反过来，若 B ∈ coNP，则它的补属于 NP ⊆ coNP，所以 B ∈ NP。两个类相等。

2. **2-SAT 很容易。** 每个 (a ∨ b) 产生 ¬a → b 与 ¬b → a；单文字可重复成二文字，空子句直接不可满足。若变量与其否定位于同一强连通分量，公式不可满足，否则利用分量拓扑序得到赋值，耗时线性。精确表达能力的障碍如下：任何 2-CNF 关系对逐坐标多数运算封闭，因为若一个二文字子句在三个满足赋值的多数值上为假，两文字各至少在两个赋值上为假，必有一个赋值使二者全假。存在量词投影也保持这种封闭性。但 3-OR 包含 100、010、001，不包含它们的多数值 000，因此不存在精确表达 3-OR 的存在量化 2-CNF 小部件。这不是对所有 NP 完全性归约的统一 AND 部件断言。

3. **哈密顿路径。** 把 3-SAT 归约到有向哈密顿路径，并明确阻止跨行绕行的机制。

   *解答。* n 个变量、m 个子句使用连接点 b₀,…,bₙ。第 i 行有 vᵢ,₀,…,vᵢ,₃ₘ₊₂，相邻点双向相连；bᵢ₋₁ 指向该行两端，两端都指向 bᵢ。子句 j 的专用端口为 Lᵢⱼ = vᵢ,₃ⱼ₋₁、Rᵢⱼ = vᵢ,₃ⱼ。正出现增加 Lᵢⱼ → cⱼ → Rᵢⱼ，负出现则反向；原行内直接边保留。相邻端口对之间、首尾端口对与行端点之间，都有非端口分隔点。规模为 O(nm+n+m)，任何覆盖全图的有向路径都必须从入度零的 b₀ 到出度零的 bₙ。

   分隔点只有两个行内邻点，因此路径必须使用两侧关联边。每个端口已经使用一侧行边，剩余一次关联只能给配对端口或 cⱼ。若从一对进入 cⱼ 却从另一对离开，进入端口的未用配偶就无法补齐剩余关联，因为它的配偶与 cⱼ 都已占满；所以绕行必回到同一对。每行因此方向一致，左到右代表真。每个子句点都通过方向相容的文字被访问，得到满足赋值。反过来，按满足赋值选择各行方向，每个子句挑一个真出现，用两条绕行边代替对应直接边，即得到访问全部顶点一次的路径。无子句时只剩变量行。证据包对128个完整图做了独立真值表 SAT 与穷尽哈密顿搜索对照，包括三变量全部八个三文字子句的不可满足例子；有限核验支持实现，一般正确性来自上述配对端口论证。

4. **由判定得到搜索。** 证明若 SAT 能在多项式时间内判定，则满足赋值也能在多项式时间内找到。

   *解答。* 先问 φ 是否可满足；若否，停止。然后对 i = 1, …, n，问：在已选定 x₁, …, xᵢ₋₁ 并令 xᵢ = 1 时 φ 是否可满足。若是，就定 xᵢ = 1；
   否则 xᵢ = 0 必定能扩展成满足赋值，因为带着之前选择的公式是可满足的。总共 n + 1 次调用判定器，每次的公式都不比 φ 大，所以是多项式时间。
   第 4 章运行过它：四个变量用了五次调用。

5. **动手：数独。** 把数独归约到 SAT，用本部分的 CDCL 求解器解一道难题，并统计冲突次数。

   *解答。* 变量 x(r, c, v) 表示行、列、数值，共 729 个。每格至少一个值（81 个 9 文字子句），至多一个（81 × 36 个二元子句）；每个数值在每行、
   每列、每宫至少出现一次（243 个子句），至多一次（243 × 36 个）。共 324 个长子句和 11,664 个二元子句，再为每个已给数字加一个单元子句。
   把变量编号为 81(r − 1) + 9(c − 1) + v，运行 `complexity.cdcl(729, clauses)`，把为真的变量解码回网格，再检查每行、每列、每宫。
   上面的英文解答给出了完整21提示题盘。运行 `python -m videos.cs.cs26.compute sudoku`；保留运行的教学求解器冲突数为111，本机耗时见带来源签名的载荷。完整12,009个子句、SAT模型及解码网格全部保存，并独立检查每行、每列、每宫及已给数字。人类解题难度不是求解器复杂度保证。

6. ★ **研究：有限尺寸交叉点与宽度。** 对 n ≤ 300 估计50%交叉点与10%–90%窗口，报告二项抽样不确定性与求解截断。每点独立生成公式，未知状态单列，超时不能算作不可满足。比较冲突中位数峰值与有限交叉点，增加样本量、加密比值网格，并传播交叉点误差。少数小规模上的幂律拟合不能证明渐近指数。

   *起点。* 1,300个实例采用三个不同变量、独立公平正负号，子句有放回抽样。n 为50、100时每点40次，为150时每点20次；载荷保留 Wilson 95%区间及全部冲突计数。Friedgut 的尖锐性针对缩窄窗口；Ding–Sly–Sun 2015对足够大的 k 识别极限预测。较新的存在性、可计算性和上界报告见下方2026年日期更新；本有限习题不证明这些结果。

## Glossary additions

多项式时间 polynomial time · 时间层级定理 time hierarchy theorem · 空间层级 space hierarchy · Savitch 定理 Savitch's theorem ·
验证器 verifier · 证书 certificate · 非确定性 nondeterminism · 多项式时间归约 polynomial-time reduction · NP 难 NP-hard ·
NP 完全 NP-complete · Cook–Levin 定理 Cook–Levin theorem · 表格 tableau · 合法窗口 legal window · 独立集 independent set ·
团 clique · 顶点覆盖 vertex cover · 三着色 3-colouring · 子集和 subset sum · 自归约 self-reducibility · 伪多项式 pseudo-polynomial ·
强 NP 难 strongly NP-hard · 完全多项式时间近似方案 FPTAS · coNP · Pratt 证书 Pratt certificate · 多项式层级 polynomial hierarchy ·
量化布尔公式 TQBF · 广义地理游戏 generalized geography · 对数空间 logarithmic space · 树求值 tree evaluation · Ladner 定理 Ladner's theorem ·
二分定理 dichotomy theorem · 冲突驱动子句学习 CDCL · 单元传播 unit propagation · 相变 phase transition · 相对化 relativization ·
自然证明 natural proofs · 代数化 algebrization · 单向函数 one-way function · 最小电路规模问题 MCSP · 元复杂性 meta-complexity

## Dated research update: inspected 11 November 2026

- [Carenini, ECCC TR26-229](https://eccc.weizmann.ac.il/report/2026/229/) reports an O(n^{1/2+1/k}) clause-count window and existence of a limiting threshold for every fixed k ≥ 3. The abstract and Theorem 1.1/Corollary 1.2 were inspected through the primary PDF viewer; direct file retrieval returned 503 and is recorded.
- [OpenAI, *Computing the Random 3-SAT Threshold*, release dated 27 September 2026](https://github.com/openai/math/tree/main/preprints/Computing-the-Random-3-SAT-Threshold-September-27-2026) credits Carenini for existence and reports a single finite algorithm approximating α₃ to arbitrary precision. Theorem 1.1 supplies no efficiency bound and does not evaluate or identify α₃ with 4.267.
- [Vorobyev, arXiv:2610.10599v1, 6 October 2026](https://arxiv.org/abs/2610.10599) reports UNSAT with high probability at density 4.268, with a rational certificate and Lean formalization. The inspected introduction still describes convergence as open; this versioned statement differs from the existence reports above.

These are dated preprint claims. The exact statements were read; their complete proofs/formalizations were not reproduced in this episode. The older “existence remains open” wording therefore cannot serve as an undated current-status summary. Our local plots establish neither these claims nor an exact limiting value. / 这些是注明版本的预印本报告；本部分查阅了精确命题，没有重做完整证明或形式化。旧版“存在性仍开放”不能不加日期地充当当前状态；本地图像也没有证明这些主张或精确极限值。

## Model and source distinctions

The extended Church–Turing thesis is a physical simulation claim, commonly probabilistic; polynomial equivalence of suitably costed deterministic models is a separate theorem. NP certificates and PH quantifiers are bounded in **bit length**. P=NP only accelerates polynomially bounded, efficiently verifiable searches; unrestricted program minimization stays undecidable, and information-theoretic ciphers are outside the computational-cryptography consequence. Impagliazzo's worlds are distributional/security scenarios, not five proved consistency claims.

Natural-proof barriers require constructivity in full truth-table length, largeness and usefulness against a specified circuit class, plus sufficiently strong quantitative pseudorandomness. They constrain a class of circuit arguments, not every possible P≠NP proof. Relative oracle independence does not establish independence of ordinary P versus NP from ZFC.

Primary statements additionally inspected for this repair:

- [Demaine, Hohenberger and Liben-Nowell author page (2003)](https://erikdemaine.org/papers/Tetris_COCOON2003/): offline objectives include clearing a target number of rows; exact move rules matter. The abstract was read, not the complete reduction proof.
- [Arora–Barak web draft, Theorem 3.1 and Definitions 22.4/22.10](https://theory.cs.princeton.edu/complexity/book.pdf): hierarchy gap, padding, natural-property conditions and quantitative pseudorandomness.
- [Razborov–Rudich original manuscript, introduction and section 2.1](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/natural.pdf): circuit lower bounds are a stronger route and naturalness has explicit conditions.
- [Bulatov 2017, Theorem 1](https://arxiv.org/html/1703.03021v2): each fixed finite constraint language on a finite domain.
- [Williams 2025, Theorem 1.1, Corollary 1.2 and Remark 1.6](https://arxiv.org/pdf/2502.17779): deterministic multitape scope, constructibility and RAM limitation.
- [Hirahara 2022](https://eccc.weizmann.ac.il/report/2022/119/): randomized-reduction hardness of partial MCSP.
- [Liu–Pass 2020](https://arxiv.org/abs/2009.11514): exact Kᵗ, uniform average-case scope and OWFs.
- [Li–Yang, 2021 report / STOC 2022](https://eccc.weizmann.ac.il/report/2021/023/): dated B₂ linear lower-bound example.

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
