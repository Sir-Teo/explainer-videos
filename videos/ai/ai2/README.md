# AI, Built — Part 2: Thinking Machines

Part 2 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). The symbolic era, 1950 to 1997: what a machine can compute, search and its
heuristics, local search, games, logic and satisfiability, constraints and planning, expert systems, ELIZA, the two
AI winters, and what of it all still runs inside today's systems. Every search, solver and learner in this part runs
on the computer that renders the video (`compute.py`); numbers about historical systems are the published ones,
cited on screen.

* **Forty years to checkmate.** Simon & Newell's 1958 forecast of a computer chess champion within ten years, and
  Deep Blue's 3½–2½ win over Kasparov in May 1997; the era on a timeline, with the two winters; objectives.
* **1. Can machines think?** Turing (1936): the machine, a binary incrementer run step by step, universality; the
  halting problem by diagonalization (derived); Church (1936); Radó's busy beaver (1962): Brady's 4-state champion
  (107 steps) and Marxen & Buntrock's 5-state champion (47,176,870 steps, 4,098 ones), both run here, proved maximal
  by bbchallenge in Coq (2024). Turing (1950): the imitation game and his 70% forecast; Jones & Bergen (2025):
  GPT-4.5 with a persona judged human 73% of the time, ELIZA 23%. The Dartmouth proposal (31 August 1955, quoted);
  the Logic Theorist (Newell, Shaw & Simon 1956): 38 of the first 52 theorems of *Principia*'s chapter 2; Shrager's
  2026 reanimation of the original IPL-V code (16 of 23); the physical symbol system hypothesis (Newell & Simon 1976).
* **2. Search.** Search problems; the 8-puzzle's 181,440 states mapped by breadth-first search (the widest ring, the
  two positions 31 moves away); breadth-first and depth-first, iterative deepening (Korf 1985); uniform-cost search
  (Dijkstra 1959) as a wavefront on a grid map.
* **3. A\*.** f = g + h (Hart, Nilsson & Raphael 1968, for Shakey); Dijkstra and A\* side by side; every expanded
  cell checked to lie in the circle of radius C\* (Dijkstra) and the ellipse with foci start and goal (A\*);
  optimality from admissibility, and monotone f from consistency, derived; 200 random maps: A\*, weighted A\* (w = 2,
  within a factor 2) and greedy best-first, nodes against path cost.
* **4. Where heuristics come from.** Relaxed problems (Pearl, early 1980s): Manhattan distance and misplaced tiles
  from the 8-puzzle's rule; dominance; A\* on 100 positions per solution length with h = 0, h₁, h₂, and the effective
  branching factor; the 15-puzzle with IDA\* and an additive 5-5-5 pattern database (Culberson & Schaeffer 1998; Korf &
  Felner 2002) built here; Korf's optimal Rubik's cube (1997); DeepCubeA's learned heuristic (Agostinelli et al.
  2019).
* **5. Climbing and cooling.** Hill climbing (schematic landscape); 8 queens from 10,000 random starts (with and
  without sideways moves; random restarts); the Metropolis rule (1953) and detailed balance to Boltzmann's
  distribution, derived; simulated annealing (Kirkpatrick, Gelatt & Vecchi 1983) on berlin52 (TSPLIB, optimum
  7,542), the tour untangling as it cools; nearest neighbour, 2-opt restarts, annealing and a genetic algorithm
  (Holland 1975) on an equal cap on actual candidate-cost evaluations, including initialization (not equal CPU time); FunSearch (2023) and AlphaEvolve (2025).
* **6. Games and alpha–beta.** Von Neumann's minimax (1928); Shannon's chess paper (1950); tic-tac-toe's whole tree
  (549,946 positions, 255,168 games); alpha–beta on an illustrative tree with the window [α, β] and pruned branches
  greyed (McCarthy); the best case b^⌈d/2⌉ + b^⌊d/2⌋ − 1 derived (Knuth & Moore 1975) and checked exactly on uniform
  trees; Connect Four to depth 9: minimax, alpha–beta in random order, best-looking first, truly best first.
* **7. Machines that learned to play.** Samuel (1959): the scoring polynomial, Alpha and Beta, delta; the Nealey
  game (1962) and the 1966 losses (Schaeffer's account); Samuel's rule as the root of TD learning (Sutton 1988); our
  own Samuel learner on Connect Four (3 runs, weights replayed, scored against an untrained player and against our
  hand-set weights, and graded by Part 26's perfect solver); Deep Blue (Campbell, Hoane & Hsu 2002); Chinook (1994)
  and *Checkers Is Solved* (Schaeffer et al. 2007).
* **8. Logic and resolution.** Truth tables and entailment; first-order logic (Frege 1879), Gödel's completeness
  (1930), undecidability (Church, Turing 1936); resolution (Robinson 1965): a propositional refutation and a
  first-order one with unification, built by our prover; saturation against the set of support (Wos, Robinson &
  Carson 1965) on a family database; Prolog (Colmerauer & Roussel 1972; Kowalski).
* **9. Satisfiability.** Cook (1971) and Levin (1973); DPLL (Davis & Putnam 1960; Davis, Logemann & Loveland 1962)
  on an illustrative formula; the random 3-SAT phase transition for n = 25, 50, 100, 200 (Mitchell, Selman &
  Levesque 1992), the 4.267 prediction (Mézard, Parisi & Zecchina 2002), proved bounds 3.52 and 4.49; easy–hard–easy
  cost; CDCL (Marques-Silva & Sakallah 1996; Chaff 2001): an implication graph, first-UIP learning and backjumping;
  DPLL against CDCL on adder equivalence.
* **10. Constraints and plans.** CSPs (Waltz 1975; Mackworth 1977); a Sudoku made here: AC-3 replayed deletion by
  deletion, and backtracking plain, with forward checking, MRV and MAC; STRIPS (Fikes & Nilsson 1971) and the frame
  problem (McCarthy & Hayes 1969); the Sussman anomaly (both orders, and the shortest plan); blocks-world state counts
  (Lah numbers); breadth-first against A\* with h_max and greedy search with h_FF (Bonet & Geffner 2001; Hoffmann &
  Nebel 2001); Graphplan (Blum & Furst), planning as satisfiability (Kautz & Selman 1992).
* **11. Knowledge is power.** Semantic networks (Quillian 1968) and frames (Minsky 1974); forward chaining over an
  illustrative rule base; DENDRAL (1965); MYCIN's certainty factors and its blinded evaluation (Yu et al. 1979); R1 /
  XCON (McDermott 1980); the knowledge-acquisition bottleneck; Cyc (Lenat 1984); Google's Knowledge Graph (2012).
* **12. ELIZA.** Weizenbaum (1966): keywords, decomposition and reassembly; our ELIZA on the user's side of the
  conversation printed in 1966 (replies compared line by line) and on new lines; the ELIZA effect and Weizenbaum's
  *Computer Power and Human Reason* (1976); the original code found (2021) and reanimated (2024).
* **13. The winters.** ALPAC (1966); *Perceptrons* (1969); the Lighthill report and debate (1973); the first winter;
  the expert-system boom, the Fifth Generation project (1982), Strategic Computing and Alvey (1983); the 1984 AAAI
  debate; the Lisp-machine collapse (1987); Moravec's paradox (1988); the long tail measured on Part 1's thirty novels
  and the scoreboard passage.
* **14. What survives.** Deep Blue against AlphaZero (Silver et al. 2018); SAT in verification: the Pentium FDIV bug
  (1994), adders proved equal and a slipped wire caught by our solver, Z3 (2008), a billion SMT queries a day at AWS
  (Rungta 2022), and the multiplier wall; Lean, AlphaGeometry (2024), AlphaProof (2024; *Nature* 2025), Gemini Deep
  Think's IMO gold (2025); PlanBench (Valmeekam et al. 2024) and LLM+P (Liu et al. 2023); neurosymbolic AI.
* **Recap**, where it comes back (Parts 9, 26, 28, 29, 31), the problem set, Part 3's teaser.

Run from the repo root:

```
python tools/make.py ai2                            # everything: the computations, then the films, resumable
nice -n 15 python -m videos.ai.ai2.compute          # every experiment, about half an hour on one core
nice -n 15 python -m videos.ai.ai2.compute --force sat3
python tools/build.py ai2                           # English
python tools/build.py ai2 --lang zh                 # Chinese
```

Every random choice is seeded (the resolution prover also visits literals in a fixed order, so its counts don't depend
on Python's hash seed). The two long items checkpoint as they go: `sat3` (about 15 minutes) after every
(n, ratio) cell, with the random stream's state, and `cdcl` (about 7 minutes) after every solver run, in
`.cache/ai2/<item>.partial.json`; a killed run resumes there and draws the same formulas. The long-tail item reads
Part 1's novels through Part 1's `compute` (which downloads them if needed). Nothing forks or compiles C: the
inner loops are Numba, which runs on macOS (Apple Silicon) and Linux alike.

`search.py` (grid search, the 8- and 15-puzzles, pattern databases), `local.py` (queens, berlin52, annealing, the
genetic algorithm), `play.py` (game trees, alpha–beta counts, the Samuel learner; Connect Four from Part 26's
`c4.py`), `logic.py` (resolution with unification), `sat.py` (random 3-SAT, DPLL, CDCL, circuits), `csp.py`
(Sudoku), `plan.py` (STRIPS blocks world), `eliza.py` (our ELIZA) and `machines.py` (Turing machines) hold the
algorithms; `compute.py` runs them, seeded, and caches the results in `.cache/ai2/`.

References. Books: Russell & Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed. (2020); Nilsson, *The
Quest for Artificial Intelligence* (2009); Pearl, *Heuristics* (1984); Biere, Heule, van Maaren & Walsh (eds.),
*Handbook of Satisfiability*, 2nd ed. (2021); Knuth, *The Art of Computer Programming* vol. 4B (2022). Papers: Turing
(1936, 1950); McCarthy, Minsky, Rochester & Shannon (1955); Newell & Simon (1956, 1976); Simon & Newell (1958); Radó
(1962); Moore (1959); Dijkstra (1959); Hart, Nilsson & Raphael (1968); Pearl (1983); Korf (1985, 1997); Culberson &
Schaeffer (1998); Korf & Felner (2002); Agostinelli et al. (2019); Metropolis et al. (1953); Kirkpatrick, Gelatt &
Vecchi (1983); Holland (1975); Romera-Paredes et al. (2023); Novikov et al. (2025); von Neumann (1928); Shannon
(1950); Knuth & Moore (1975); Samuel (1959); Sutton (1988); Campbell, Hoane & Hsu (2002); Schaeffer et al. (2007);
Frege (1879); Gödel (1930); Robinson (1965); Wos, Robinson & Carson (1965); Colmerauer & Roussel (1972/1993); Kowalski
(1974); Davis & Putnam (1960); Davis, Logemann & Loveland (1962); Cook (1971); Levin (1973); Mitchell, Selman &
Levesque (1992); Mézard, Parisi & Zecchina (2002); Mertens, Mézard & Zecchina (2006); Díaz et al. (2008); Ding, Sly &
Sun (2015); Marques-Silva & Sakallah (1999); Moskewicz et al. (2001); Waltz (1975); Mackworth (1977); McCarthy & Hayes
(1969); Fikes & Nilsson (1971); Sussman (1975); Kautz & Selman (1992); Blum & Furst (1997); Bonet & Geffner (2001);
Hoffmann & Nebel (2001); Quillian (1968); Minsky (1974); Shortliffe (1976); Yu et al. (1979); McDermott (1982);
Lenat (1995); Singhal (2012); Weizenbaum (1966, 1976); Lane et al. (2025); Lighthill (1973); Moravec (1988); Jones
& Bergen (2025); Silver et al. (2018); de Moura & Bjørner (2008); Rungta (2022); Trinh et al. (2024); Hubert et al.
(2025); Valmeekam, Stechly & Kambhampati (2024); Liu et al. (2023); Shrager (2026).

## Problems, with solutions

**1. Manhattan is consistent.** Show that the Manhattan-distance heuristic of the 8-puzzle is consistent.

*Solution.* A move slides one tile to a neighbouring square, changing that tile's row or column by one and leaving
every other tile where it was. So h changes by exactly ±1 while the step costs 1: h(n) ≤ 1 + h(n′) for every move
n → n′, and h = 0 at the goal. That is consistency.

**2. Consistent implies admissible.** Prove that a consistent heuristic is admissible, and give an admissible
heuristic that is not consistent.

*Solution.* Induction on the number k of steps in an optimal path from n to a goal. For k = 0, n is a goal and
h(n) = 0 = h\*(n). Otherwise let n → n′ be the first step of an optimal path; then h(n) ≤ c(n, n′) + h(n′) ≤
c(n, n′) + h\*(n′) = h\*(n). For the converse, take a path s → a → g with both steps of cost 1, and h(s) = 2, h(a) = 0,
h(g) = 0. It never overestimates (h\*(s) = 2, h\*(a) = 1), but h(s) = 2 > c(s, a) + h(a) = 1.

**3. Alpha–beta's best case.** With the best move always searched first, show that alpha–beta on a uniform tree of
branching b and depth d evaluates exactly b^⌈d/2⌉ + b^⌊d/2⌋ − 1 leaves.

*Solution.* With perfect ordering the nodes searched are of three types (Knuth & Moore). The root is type 1; a type-1
node searches all its children, the first of type 1 and the others of type 2; a type-2 node searches only its first
child, which refutes it, of type 3; a type-3 node searches all its children, each of type 2. Let N₁, N₂, N₃ count the
leaves below a node of each type at height d. Then N₂(d) = N₃(d − 1), N₃(d) = b N₂(d − 1), so N₂(d) = b^⌊d/2⌋ and
N₃(d) = b^⌈d/2⌉; and N₁(d) = N₁(d − 1) + (b − 1) N₂(d − 1) = N₁(d − 1) + (b − 1) b^⌊(d−1)/2⌋ with N₁(0) = 1. Checking
d = 2k and d = 2k + 1 separately, b^⌈d/2⌉ + b^⌊d/2⌋ − 1 satisfies the same recursion and the same start, so it equals
N₁(d). (The two terms are the two proofs of the chapter: one move of yours against every reply, and every move of yours
against one refutation; they share one leaf.)

**4. Why annealing works.** Show that the Metropolis rule (symmetric proposals q; accept a move up by ΔE with
probability e^{−ΔE/T}, a move down always) satisfies detailed balance for π(s) ∝ e^{−E(s)/T}, and that as T → 0 the
distribution concentrates on the global minima.

*Solution.* Take s, s′ with E(s′) > E(s). Then P(s → s′) = q e^{−(E(s′) − E(s))/T} and P(s′ → s) = q, so
π(s) P(s → s′) = (q/Z) e^{−E(s′)/T} = π(s′) P(s′ → s); equal energies are trivial. Detailed balance makes π
stationary (and the unique stationary distribution if the moves connect all states). For a state s and a global
minimum s\*, π(s)/π(s\*) = e^{−(E(s) − E\*)/T} → 0 as T → 0 whenever E(s) > E\*, so all the probability ends on the
global minima, shared equally.

**5. Resolution.** Show that a resolvent is entailed by its parents, and refute {P ∨ Q, ¬P ∨ Q, P ∨ ¬Q, ¬P ∨ ¬Q}.

*Solution.* Suppose an assignment satisfies A ∨ x and B ∨ ¬x. If x is true, the second clause forces B; if x is
false, the first forces A; either way A ∨ B holds. Refutation: P ∨ Q and ¬P ∨ Q give Q; P ∨ ¬Q and ¬P ∨ ¬Q give ¬Q;
Q and ¬Q give the empty clause. The set is unsatisfiable.

**6. An upper bound on the threshold.** For random 3-SAT with n variables and m = αn clauses, show that the expected
number of satisfying assignments is 2ⁿ (7/8)^{αn}, and deduce that the threshold is at most ln 2 / ln(8/7) ≈ 5.19.

*Solution.* A fixed assignment falsifies a random clause only if all three literals come out false: one sign
pattern in eight. The clauses are drawn independently, so the assignment satisfies all of them with probability
(7/8)^m; summing over the 2ⁿ assignments, E[X] = 2ⁿ (7/8)^{αn} = exp(n (ln 2 − α ln(8/7))). If α > ln 2 / ln(8/7) ≈
5.19 this tends to 0, and by Markov's inequality P(X ≥ 1) ≤ E[X] → 0: almost every formula is unsatisfiable. (This first-moment argument gives only an upper bound. A large expected number of solutions need not imply a
large probability of satisfiability: many assignments may be concentrated in a small fraction of formulas. The
value near 4.267 is a statistical-physics prediction.)

## 习题与解答

**1. 曼哈顿距离是一致的。** 证明八数码的曼哈顿距离启发式是一致的。

*解答。* 每走一步，只把一个方块滑到相邻的格子，它的行或列变化1，其他方块都不动。所以h恰好变化±1，而这一步的代价是1：对每一步
n → n′ 都有 h(n) ≤ 1 + h(n′)，并且在目标处 h = 0。这就是一致性。

**2. 一致蕴含可采纳。** 证明一致的启发式一定是可采纳的，并举一个可采纳但不一致的启发式。

*解答。* 对从n到目标的最优路径的步数k做归纳。k = 0 时n就是目标，h(n) = 0 = h\*(n)。否则设 n → n′ 是最优路径的第一步，
则 h(n) ≤ c(n, n′) + h(n′) ≤ c(n, n′) + h\*(n′) = h\*(n)。反例：路径 s → a → g，两步代价都是1，取 h(s) = 2，h(a) = 0，
h(g) = 0。它从不高估（h\*(s) = 2，h\*(a) = 1），但 h(s) = 2 > c(s, a) + h(a) = 1。

**3. α-β剪枝的最好情况。** 若总是先搜索最好的走法，证明α-β在分支数为b、深度为d的均匀树上恰好评估
b^⌈d/2⌉ + b^⌊d/2⌋ − 1 个叶子。

*解答。* 在完美排序下，被搜索的结点分三类（克努特与摩尔）。根是第1类；第1类结点搜索全部子结点，第一个是第1类，其余是第2类；
第2类结点只搜索第一个子结点，它就驳倒了该结点，这个子结点是第3类；第3类结点搜索全部子结点，每个都是第2类。记N₁、N₂、N₃为高度d
处各类结点下的叶子数。则 N₂(d) = N₃(d − 1)，N₃(d) = b N₂(d − 1)，所以 N₂(d) = b^⌊d/2⌋，N₃(d) = b^⌈d/2⌉；而
N₁(d) = N₁(d − 1) + (b − 1) N₂(d − 1) = N₁(d − 1) + (b − 1) b^⌊(d−1)/2⌋，N₁(0) = 1。分d = 2k和d = 2k + 1两种情况验证，
b^⌈d/2⌉ + b^⌊d/2⌋ − 1 满足同样的递推和初值，因此等于N₁(d)。（这两项就是本章的两个证明：你的一步对上对手的每一个应对，你的每一步
对上一个驳斥；它们共享一个叶子。）

**4. 模拟退火为什么有效。** 证明梅特罗波利斯准则（对称的提议q；能量升高ΔE时以概率e^{−ΔE/T}接受，降低时总接受）对
π(s) ∝ e^{−E(s)/T} 满足细致平衡，并且当T → 0时，分布集中在全局最小值上。

*解答。* 取E(s′) > E(s)。则 P(s → s′) = q e^{−(E(s′) − E(s))/T}，P(s′ → s) = q，所以
π(s) P(s → s′) = (q/Z) e^{−E(s′)/T} = π(s′) P(s′ → s)；能量相等时显然成立。细致平衡使π成为平稳分布（若走法能连通所有状态，
它就是唯一的平稳分布）。对任一状态s和全局最小值s\*，π(s)/π(s\*) = e^{−(E(s) − E\*)/T}，只要E(s) > E\*，当T → 0时它趋于0，
所以全部概率最终落在全局最小值上，平均分配。

**5. 归结。** 证明归结式被它的两个父子句蕴涵，并用归结反驳 {P ∨ Q, ¬P ∨ Q, P ∨ ¬Q, ¬P ∨ ¬Q}。

*解答。* 设某个赋值同时满足 A ∨ x 和 B ∨ ¬x。若x为真，第二个子句迫使B成立；若x为假，第一个迫使A成立；无论哪种，A ∨ B 都成立。
反驳：P ∨ Q 与 ¬P ∨ Q 得 Q；P ∨ ¬Q 与 ¬P ∨ ¬Q 得 ¬Q；Q 与 ¬Q 得空子句。所以这组子句不可满足。

**6. 阈值的一个上界。** 对有n个变量、m = αn个子句的随机3-SAT，证明满足赋值个数的期望是 2ⁿ (7/8)^{αn}，并推出阈值至多为
ln 2 / ln(8/7) ≈ 5.19。

*解答。* 一个固定的赋值只有在三个文字都为假时才违反一个随机子句：八种符号组合里只有一种。各子句独立抽取，所以这个赋值满足全部子句的
概率是 (7/8)^m；对2ⁿ个赋值求和，E[X] = 2ⁿ (7/8)^{αn} = exp(n (ln 2 − α ln(8/7)))。若 α > ln 2 / ln(8/7) ≈ 5.19，它趋于0，
由马尔可夫不等式，P(X ≥ 1) ≤ E[X] → 0：几乎所有公式都不可满足。（这个一阶矩论证只给出上界。解的期望个数很大，并不代表公式可满足的概率很大：大量满足赋值可能集中在一小部分公式里。
4.267附近的值，是统计物理给出的预言。）

## Glossary (new terms, for AI_ZH_GUIDE.md)

| English | 中文 |
|---|---|
| Turing machine, tape, head, state | 图灵机，纸带，读写头，状态 |
| universal machine, stored-program computer | 通用机，存储程序计算机 |
| halting problem, decidable / undecidable | 停机问题，可判定 / 不可判定 |
| busy beaver | 忙碌海狸 |
| imitation game, Turing test, interrogator | 模仿游戏，图灵测试，提问者 |
| Dartmouth workshop | 达特茅斯会议 |
| Logic Theorist | 逻辑理论家 |
| physical symbol system hypothesis | 物理符号系统假设 |
| search problem, state space, goal test | 搜索问题，状态空间，目标测试 |
| breadth-first / depth-first search, iterative deepening | 广度优先 / 深度优先搜索，迭代加深 |
| uniform-cost search, Dijkstra's algorithm | 一致代价搜索，迪杰斯特拉算法 |
| frontier, wavefront, expand | 边界，波前，扩展 |
| heuristic, A\*, f = g + h | 启发式（启发函数），A\*，f = g + h |
| admissible, consistent (monotone) | 可采纳的，一致的（单调的） |
| weighted A\*, greedy best-first search | 加权A\*，贪心最佳优先搜索 |
| relaxed problem, Manhattan distance, misplaced tiles | 松弛问题，曼哈顿距离，错位方块数 |
| dominance, effective branching factor | 占优，有效分支因子 |
| 8-puzzle, 15-puzzle | 八数码，十五数码 |
| IDA\*, pattern database | IDA\*，模式数据库 |
| local search, hill climbing, local maximum, plateau | 局部搜索，爬山法，局部极大值，平台 |
| random restart, sideways move | 随机重启，横向移动 |
| simulated annealing, temperature, cooling schedule | 模拟退火，温度，降温计划 |
| Metropolis rule, detailed balance, Boltzmann distribution | 梅特罗波利斯准则，细致平衡，玻尔兹曼分布 |
| travelling salesman problem, tour, 2-opt | 旅行商问题，回路，2-opt |
| genetic algorithm, population, crossover, mutation | 遗传算法，种群，交叉，变异 |
| alpha–beta window [α, β], cutoff, move ordering | α-β窗口 [α, β]，剪枝，走法排序 |
| scoring polynomial (Samuel) | 评分多项式（塞缪尔） |
| propositional / first-order logic, entailment | 命题 / 一阶逻辑，蕴涵 |
| clause, literal, resolution, resolvent, refutation | 子句，文字，归结，归结式，反驳 |
| unification, substitution | 合一，代换 |
| set of support, Horn clause, Prolog | 支持集策略，霍恩子句，Prolog |
| satisfiability (SAT), NP-complete | 可满足性（SAT），NP完全 |
| DPLL, unit propagation, branching, backtracking | DPLL，单元传播，分支，回溯 |
| conflict-driven clause learning (CDCL), implication graph | 冲突驱动子句学习（CDCL），蕴含图 |
| first UIP, learned clause, backjumping | 第一唯一蕴含点，学习子句，回跳 |
| phase transition, clause-to-variable ratio | 相变，子句与变量之比 |
| constraint satisfaction problem, domain | 约束满足问题，值域 |
| arc consistency (AC-3), forward checking | 弧相容（AC-3），前向检查 |
| minimum remaining values (MRV), MAC | 最少剩余值（MRV），维持弧相容（MAC） |
| planning, STRIPS, precondition, add list, delete list | 规划，STRIPS，前提条件，添加表，删除表 |
| the frame problem, the Sussman anomaly | 框架问题，萨斯曼异常 |
| relaxed-plan heuristic (h_max, h_FF) | 松弛规划启发式（h_max，h_FF） |
| semantic network, is-a link, inheritance, frame, slot | 语义网络，is-a链接，继承，框架，槽 |
| expert system, rule base, forward chaining | 专家系统，规则库，前向链接 |
| certainty factor | 确定性因子 |
| knowledge engineer, knowledge acquisition bottleneck | 知识工程师，知识获取瓶颈 |
| knowledge graph | 知识图谱 |
| ELIZA, keyword, decomposition, reassembly, the ELIZA effect | ELIZA，关键词，分解规则，重组规则，伊丽莎效应 |
| AI winter, Lighthill report, Lisp machine | AI寒冬，莱特希尔报告，Lisp机 |
| Fifth Generation Computer Systems project | 第五代计算机项目 |
| Moravec's paradox, the long tail | 莫拉维克悖论，长尾 |
| formal verification, SMT, adder, multiplier, miter | 形式化验证，SMT，加法器，乘法器，比较电路（miter） |
| proof assistant (Lean) | 证明助手（Lean） |
| neurosymbolic AI | 神经符号AI |

Names: Alan Turing 图灵; Alonzo Church 丘奇; John McCarthy 麦卡锡; Marvin Minsky 明斯基; Herbert Simon 西蒙; Allen
Newell 纽厄尔; Edsger Dijkstra 迪杰斯特拉; Arthur Samuel 塞缪尔; Garry Kasparov 卡斯帕罗夫; Joseph Weizenbaum 魏岑鲍姆;
James Lighthill 莱特希尔; Hans Moravec 莫拉维克; Judea Pearl 珀尔; Richard Korf 科尔夫; Alan Robinson 鲁滨逊; Stephen Cook
库克; Leonid Levin 列文. Program names stay in Latin script: Shakey, STRIPS, DENDRAL, MYCIN, XCON, Cyc, ELIZA, DOCTOR,
Chinook, Deep Blue → 深蓝, Prolog, Lisp, Z3, Lean, AlphaProof, AlphaGeometry, FunSearch, AlphaEvolve, DeepCubeA.
