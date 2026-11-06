# Computer Science, Built — Part 23: Optimization

Part 23 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the eighth part of Act IV, *Algorithms*. Many problems are "choose the best point of
a polytope". The simplex method walks the polytope's edges, and duality certifies the answer from the other side.
When integrality makes a problem hard, LP relaxations and random hyperplanes still get provably close. Online,
without seeing the future, you can still be competitive. The instrument is `explainer/cs/algo/optim.py`. It holds:

* the simplex method, in floating point or exact rationals, with Dantzig's, Bland's and the greatest-improvement
  rules. It returns the path of vertices, the tableaux and the duals;
* Klee–Minty cubes and random LPs;
* the vertices and faces of 3D polytopes;
* the central-cut ellipsoid method and a log-barrier path follower with Newton steps;
* a total-unimodularity test by brute force over square submatrices;
* knapsack by LP bound, branch and bound with a tree log, dynamic programming and the FPTAS;
* vertex cover: exact, by maximal matching, and by LP rounding;
* set cover: greedy and exact, with the harmonic trap;
* the TSP: Held–Karp, Prim, the double tree, minimum-weight perfect matching, Christofides–Serdyukov, nearest
  neighbour and 2-opt;
* MAX-CUT: exact, Goemans–Williamson by a low-rank (Burer–Monteiro) SDP and random hyperplanes, and the constant
  α;
* ski rental; paging with LRU, FIFO, random, marking and Belady's OPT;
* Hedge, and multiplicative weights for zero-sum games.

It is tested in `tests/test_cs23_optim.py`:
- simplex matches SciPy's HiGHS on 30 random LPs under all three rules, and its duals certify each value;
- Klee–Minty cubes take exactly 2ⁿ − 1 pivots in exact arithmetic;
- branch and bound agrees with the DP on knapsacks, and the FPTAS keeps its guarantee;
- the covers keep their factors against brute force;
- the double tree and Christofides–Serdyukov stay within 2 and 3/2 of Held–Karp;
- the SDP bounds the exact MAX-CUT.

Every number is computed in `compute.py`.

* **The best point of a polytope.** Hook.
  - Stigler's diet (1945): 77 foods and 9 nutrients, solved by trial and insight at $39.93 a year (1939 prices).
  - Laderman's team in 1947, working by hand on desk calculators with Dantzig's new simplex method, took about 120
    person-days to reach $39.69, with a proof that nothing is cheaper.
  - Three kinds of answer: proved optimal (an LP), provably close (the TSP), and competitive without the future
    (a cache).
* **1. Linear programs.**
  - Chvátal's three-product example: max 5x₁ + 4x₂ + 3x₃ subject to three resource constraints.
  - Kantorovich (1939), Dantzig (1947), and the 1975 Nobel prize.
  - Modelling, through a transportation problem: two plants (30 and 40 units) and three stores (20, 25 and 25).
    Each store served from its cheapest plant would cost $355, but plant B can't make 50. The optimum is $365, with
    store 3 split between both plants.
  - The tricks: equations, free variables, minimax and absolute values.
  - The feasible region is a polytope with 6 vertices. The objective plane is pushed until it last touches the
    vertex (2, 0, 1), with value 13.
* **2. The simplex method.**
  - The walk (0,0,0) → (2.5,0,0) → (2,0,1): profit 0 → 12.5 → 13, in 2 pivots.
  - Each pivot drawn as a tableau: entering column, ratio test, Gaussian elimination.
  - Degeneracy and cycling; Bland's rule (also 2 pivots here); steepest edge and the revised simplex.
* **3. Duality.**
  - Bounding the profit by adding up the constraints. y = (3,0,0) gives ≤ 15 and (0,0,5/3) gives ≤ 13.33.
    (0,1.25,0) doesn't cover c, and (1,0,1) gives ≤ 13, which is the optimum.
  - Weak and strong duality, Farkas' lemma, and the separating hyperplane.
  - Shadow prices, measured by adding a unit of each resource: 1/3, 0 and 1. Resource 1's measured price is below
    its dual price y₁ = 1 because the basis changes.
  - Complementary slackness: resource 2 has slack 1 and price 0, and product 2 has reduced cost 3 and is not made.
* **4. Exponential in theory, fast in practice.**
  - The 3D Klee–Minty cube, and the walk through all 8 of its vertices.
  - Pivots on Klee–Minty cubes: Dantzig's rule takes exactly 2ⁿ − 1 (4,095 at n = 12) and Bland's 465. Greatest
    improvement takes 1 here, though Jeroslow built cubes that defeat it.
  - Smoothed analysis (Spielman–Teng):
    - random dense LPs of size n × 2n need 3.05, 4.5, 9.2, 17.3 and 33.95 pivots on average;
    - the n = 10 cube with each entry multiplied by 1 + σg keeps all 1,023 pivots for σ ≤ 0.01, then falls to 397
      at σ = 0.1 and 76 at σ = 0.3.
* **5. Polynomial time.**
  - Khachiyan's ellipsoid finds a feasible centre in 9 cuts. Each cut shrinks the volume by at most
    e^{−1/(2(n+1))}.
  - Steps against the region's width: 1, 15, 20, 46, 64, 89 and 100 for widths 1 down to 10⁻⁶.
  - Grötschel–Lovász–Schrijver: separation ≡ optimization.
  - Karmarkar and the central path: log barrier and Newton steps, 127 in all, reach the optimum (2, 3).
* **6. When the vertices are integers.**
  - A bipartite graph's incidence matrix is totally unimodular (checked over every square submatrix). Cramer's
    rule makes every vertex integral; 0 of 100 random weighted bipartite matching LPs had a fractional optimum.
  - The triangle has a submatrix of determinant 2, and its LP puts ½ on every edge (value 1.5). 25 of 100 general
    graphs had fractional optima.
  - Edmonds' odd-set constraints; max-flow/min-cut as LP duality; interval and network matrices; Seymour.
* **7. Integer programming.**
  - Branch and bound on an 8-item knapsack with capacity 80: root bound 183.9, best 174, after 24 nodes out of 256
    choices.
  - Random knapsacks: 58.9, 116, 248 and 661 nodes on average for 20 to 160 items. The LP gap is 2.1%, 0.58%,
    0.15% and 0.063%.
  - Gomory cuts, branch and cut, and Bixby's 30,000-fold algorithmic speedup.
  - The knapsack FPTAS on a strongly correlated 20-item instance: 0.9932 of optimal at ε = 0.9, 0.9986 at 0.5 and
    0.2, and exact from 0.1 down. Tables of 5,760 to 266,660 entries.
* **8. Approximation: covers.**
  - Vertex cover by maximal matching and by LP rounding. On the drawn 9-vertex graph: OPT 6, matching 8, LP 4.5
    (all halves), rounding keeps 9.
  - On 100 random graphs: matching mean 1.50 (worst 1.78); rounding mean 1.54 (worst 2.00); LP/OPT 0.91.
  - Khot–Regev.
  - Greedy set cover and the H_n bound, proved by charging. The harmonic trap gives greedy k against OPT 2 for
    k = 2…7.
  - On 60 random instances, greedy averages 1.06 × OPT (worst 1.375). Feige; Dinur–Steurer.
* **9. The travelling salesman.**
  - Thirteen cities: optimum 22.33 (Held–Karp), double tree 28.78, Christofides–Serdyukov 24.69, nearest neighbour
    25.62, and 2-opt reaches the optimum.
  - Forty 12-city instances:
    - double tree mean 1.209 (worst 1.48);
    - Christofides 1.066 (worst 1.149);
    - nearest neighbour 1.101;
    - 2-opt 1.013 (worst 1.11).
  - Held–Karp takes 0.38 s for 15 cities.
  - 300 cities: nearest neighbour 16.23, then 13.86 after 2-opt in 0.10 s. The BHH estimate is 12.34.
  - Karlin–Klein–Oveis Gharan, Arora/Mitchell, LKH and Concorde.
* **10. A random hyperplane: MAX-CUT.**
  - Unit vectors on a sphere for a 12-vertex graph: SDP 18.35 against an exact maximum of 18.
  - The cut probability θ/π, and α = 0.8786 at θ ≈ 2.33.
  - Thirty 16-vertex graphs: random sides 0.686, one hyperplane 0.961 (worst 0.939), best of 200 hyperplanes
    1.000; SDP/exact 1.032.
  - KKMO and Håstad's 16/17.
* **11. Online.**
  - Ski rental with B = 10: the break-even rule is 2 − 1/B competitive; the randomized rule costs 15.37 for long
    seasons (e/(e − 1) ≈ 1.582).
  - Paging on the Job's trace: 155,266 accesses to 92 distinct 64-byte lines.
    - LRU/OPT is 1.20, 1.51, 2.19 and 6.90 at 8, 16, 32 and 64 lines.
    - At 64 lines, random (3,050) and marking (3,734) beat LRU (7,940).
  - The cyclic adversary: LRU faults on every request; OPT faults about once per k requests (253 of 1,000 at
    k = 4); marking 500. Sleator–Tarjan.
* **12. Multiplicative weights.**
  - Ten experts, one wrong 45% of the time: the weights find it within a few hundred rounds.
  - Regret 7, 14, 24, 37, 61 and 83 against the bound √((T ln n)/2): 11, 19, 34, 59, 107 and 152 for T = 100 to
    20,000.
  - The four-line potential proof.
  - A 3 × 3 zero-sum game: the gap closes from 0.19 to 0.006, towards the LP value 0.4846.
  - Boosting and approximate LP (Arora–Hazan–Kale).
* **13. Convex optimization in a page.**
  - On a stretched log-sum-exp, gradient descent with backtracking needs 40 steps to 10⁻¹⁰; Newton needs 4.
  - KKT; the LP ⊂ QP ⊂ SOCP ⊂ SDP ladder; Nesterov–Nemirovski; Rockafellar's watershed.
* **14. Frontier: faster LPs, the Hirsch question and the UGC.**
  - Interior points down to n^ω: Cohen–Lee–Song and van den Brand. Almost-linear max flow: Chen, Kyng, Liu, Peng,
    Probst Gutenberg and Sachdeva.
  - The Hirsch conjecture and Santos's counterexample. A drawn polytope with 24 random facets and 44 vertices has
    diameter 8.
  - Random 3D polytopes with 8–128 facets have mean diameter 3.6, 6.2, 9.45, 13.6 and 19.05, against Hirsch's
    5–125.
  - Kalai–Kleitman.
  - The PCP theorem, Håstad, the UGC, the 2-to-2 theorem and Raghavendra.
  - Open problems: strongly polynomial LP, polynomial Hirsch, the UGC. Outro.

## Build

```bash
python -m videos.cs.cs23.compute           # every number in the part (a few minutes)
python tools/build.py cs23 -q l            # a 480p preview
python tools/build.py cs23                 # 1080p
```

## Problems, with solutions

1. **Duality.** Prove weak duality from the definitions, and derive complementary slackness from strong duality.

   *Solution.* Let x be primal feasible (Ax ≤ b, x ≥ 0) and y dual feasible (Aᵀy ≥ c, y ≥ 0). Then
   cᵀx ≤ (Aᵀy)ᵀx = yᵀ(Ax) ≤ yᵀb. The first step uses x ≥ 0 and the second uses y ≥ 0. At optima, strong duality
   makes the two ends equal, so both inequalities are equalities: (Aᵀy − c)ᵀx = 0 and yᵀ(b − Ax) = 0. Each is a sum
   of non-negative products, so every product is zero. If yᵢ > 0 then constraint i is tight, and if xⱼ > 0 then
   dual constraint j is tight. In chapter 3, y = (1, 0, 1) meets slack (0, 1, 0), and x = (2, 0, 1) meets reduced
   costs (0, 3, 0).

2. **Half-integrality.** Prove that every vertex of the vertex-cover LP {x ≥ 0 : x_u + x_v ≥ 1 for every edge uv}
   has each x_v ∈ {0, ½, 1}.

   *Solution.* Restrict to the box 0 ≤ x ≤ 1: lowering any coordinate above 1 to 1 keeps a point feasible, so the
   box contains an optimal vertex. Let x be a vertex with some coordinate outside {0, ½, 1}. Put
   V₊ = {v : ½ < x_v < 1} and V₋ = {v : 0 < x_v < ½}, and let y = x + ε(1_{V₊} − 1_{V₋}) and
   z = x − ε(1_{V₊} − 1_{V₋}). For small ε both are feasible. An edge with slack keeps it. A tight edge
   x_u + x_v = 1 either has both ends at ½, at 0 and 1, or one end in V₊ and the other in V₋, and then the changes
   cancel. Then x = (y + z)/2 is not a vertex, a contradiction. Chapter 8's drawn graph has its LP optimum at all
   halves, value 4.5.

3. **Ski rental.** Show that renting for B − 1 days and then buying is (2 − 1/B)-competitive, and that no
   deterministic rule does better.

   *Solution.* If the season lasts d < B days we pay d, which equals OPT. If d ≥ B we pay (B − 1) + B = 2B − 1
   against OPT = B, a ratio of 2 − 1/B. A deterministic rule is "buy on day k", with k possibly ∞. The adversary
   ends the season on day k, so we pay (k − 1) + B against min(k, B). For k ≤ B the ratio is
   1 + (B − 1)/k ≥ 2 − 1/B. For k > B it is (k − 1 + B)/B ≥ 2. Never buying is unbounded. With B = 10 the rule pays
   19 against 10, as in chapter 11's chart.

4. **The constant α.** Show that θ/(1 − cos θ) is minimized on (0, π] where θ = tan(θ/2), and compute
   Goemans–Williamson's α to four digits.

   *Solution.* The derivative is [(1 − cos θ) − θ sin θ]/(1 − cos θ)². It is zero when θ = (1 − cos θ)/sin θ,
   which is tan(θ/2) by the half-angle formula. The function tends to ∞ as θ → 0 and equals π/2 at π, so this
   critical point is the minimum. Newton's method on g(θ) = θ − tan(θ/2) from θ = 2.3 gives θ ≈ 2.3311, about
   133.6°. Then α = 2θ/(π(1 − cos θ)) = 4.6622/(π · 1.6891) ≈ 0.8786, matching `optim.gw_alpha()`.

5. **Build: simplex in Pebble.** Write Bland's-rule simplex in the Pebble language, with fractions as pairs of
   integers. Solve chapter 1's LP on the emulator and print 13.

   *Solution sketch.* Store the 3 × 7 tableau and the objective row as two arrays, numerators and denominators,
   always reduced by Euclid's gcd and kept with a positive denominator.
   - Entering column, by Bland's rule: the smallest index with a negative objective entry (a negative numerator).
   - Leaving row: the ratio test compares b_i/a_ie for rows with a_ie > 0. Compare fractions by cross-multiplying,
     p/q < r/s ⇔ ps < rq, and break ties by the smallest basic index.
   - The pivot: divide the pivot row by the pivot entry, then subtract multiples of it from the other rows.
     Multiplication and subtraction of fractions need only products and a gcd.

   Chapter 2's tableaux never have a denominator above 2, so every product fits in a word. The program stops after
   2 pivots with 13 in the corner. Check each tableau against `compute.py`'s `simplex` item.

6. ★ **Research: the polynomial Hirsch conjecture.** Our random 3D polytopes have diameter growing roughly like √n
   in the number of facets. Prove that every d-dimensional polytope with n facets has diameter bounded by a
   polynomial in n and d, or build a family that defeats every polynomial.

   *Where to start.* The best general upper bounds are quasi-polynomial:
   - Kalai and Kleitman, "A quasi-polynomial bound for the diameter of graphs of polyhedra" (1992), n^{log₂ d + 2};
   - Todd (2014), improving it to (n − d)^{log₂ d};
   - Sukegawa (2019).

   Santos, "A counterexample to the Hirsch conjecture" (Annals of Mathematics, 2012), refutes the exact bound but
   not the polynomial one. Special classes do satisfy good bounds:
   - 0/1-polytopes have diameter at most d (Naddef 1989);
   - integer polytopes with bounded subdeterminants have polynomial diameter (Bonifas, Di Summa, Eisenbrand, Hähnle
     and Niemeier 2014).

   Eisenbrand, Hähnle, Razborov and Rothvoß, "Diameter of polyhedra: limits of abstraction" (2010), studies
   connected layer families, a combinatorial abstraction. There the gap between their Ω(n²/log n) lower bound and
   the quasi-polynomial upper bound is open, and it was the subject of Polymath 3. Closing that gap is a natural
   first step.

## 习题与解答

1. **对偶。** 由定义证明弱对偶，并由强对偶推出互补松弛。

   *解答。* 设 x 原始可行（Ax ≤ b，x ≥ 0），y 对偶可行（Aᵀy ≥ c，y ≥ 0）。则 cᵀx ≤ (Aᵀy)ᵀx = yᵀ(Ax) ≤ yᵀb：第一步用到
   x ≥ 0，第二步用到 y ≥ 0。在最优处，强对偶使两端相等，所以两个不等式都取等号：(Aᵀy − c)ᵀx = 0 且 yᵀ(b − Ax) = 0。每个都是非负
   乘积之和，所以每个乘积都为零：若 yᵢ > 0，则约束 i 是紧的；若 xⱼ > 0，则对偶约束 j 是紧的。第3章中 y = (1, 0, 1) 对应松弛量
   (0, 1, 0)，x = (2, 0, 1) 对应检验数 (0, 3, 0)。

2. **半整性。** 证明顶点覆盖线性规划 {x ≥ 0：对每条边 uv 有 x_u + x_v ≥ 1} 的每个顶点都满足 x_v ∈ {0, ½, 1}。

   *解答。* 限制在盒子 0 ≤ x ≤ 1 内，其中含有一个最优顶点。设 x 是一个顶点，且有某个坐标不在 {0, ½, 1} 中。令
   V₊ = {v：½ < x_v < 1}，V₋ = {v：0 < x_v < ½}，并令 y = x + ε(1_{V₊} − 1_{V₋})，z = x − ε(1_{V₊} − 1_{V₋})。ε 足够小时
   两者都可行：有松弛的边仍有松弛；紧边 x_u + x_v = 1 要么两端都是 ½，要么是 0 和 1，要么一端在 V₊、另一端在 V₋，此时变化相互抵消。
   于是 x = (y + z)/2 不是顶点，矛盾。第8章所画的图，其线性规划最优解全是 ½，值为 4.5。

3. **租雪板。** 证明先租 B − 1 天再买是 (2 − 1/B)-竞争的，且没有确定性规则能做得更好。

   *解答。* 若雪季持续 d < B 天，我们付 d，等于 OPT；若 d ≥ B，我们付 (B − 1) + B = 2B − 1，而 OPT = B，比值为 2 − 1/B。任何确定性
   规则都是"第 k 天买"（k 可以是 ∞）。对手让雪季在第 k 天结束：我们付 (k − 1) + B，而最优为 min(k, B)。k ≤ B 时比值为
   1 + (B − 1)/k ≥ 2 − 1/B；k > B 时比值为 (k − 1 + B)/B ≥ 2；永远不买则比值无界。B = 10 时这一规则付 19 而最优付 10，与第11章的图一致。

4. **常数 α。** 证明 θ/(1 − cos θ) 在 (0, π] 上的最小值点满足 θ = tan(θ/2)，并把 Goemans–Williamson 的 α 算到四位。

   *解答。* 导数为 [(1 − cos θ) − θ sin θ]/(1 − cos θ)²，当 θ = (1 − cos θ)/sin θ 时为零，由半角公式这正是 tan(θ/2)。函数在 θ → 0
   时趋于 ∞，在 π 处等于 π/2，所以这个临界点就是最小值点。对 g(θ) = θ − tan(θ/2) 从 θ = 2.3 起用牛顿法，得 θ ≈ 2.3311（约 133.6°），
   于是 α = 2θ/(π(1 − cos θ)) = 4.6622/(π · 1.6891) ≈ 0.8786，与 `optim.gw_alpha()` 一致。

5. **构造：Pebble 中的单纯形法。** 用 Pebble 语言写出 Bland 规则的单纯形法，分数用整数对表示；在模拟器上求解第1章的线性规划并打印 13。

   *解答提要。* 把 3 × 7 的单纯形表和目标行存为分子、分母两个数组，始终用欧几里得 gcd 约分，并保持分母为正。按 Bland 规则，进基列是目标行
   中第一个为负（分子为负）的下标。比值检验对 a_ie > 0 的行比较 b_i/a_ie：交叉相乘比较分数（p/q < r/s ⇔ ps < rq），平局时选基变量下标
   最小者。主元运算把主元行除以主元，再从其他行减去它的倍数；分数的乘法和减法只需要乘积和 gcd。第2章的单纯形表中分母从不超过 2，所以每个
   乘积都放得进一个字。程序在 2 次转轴后停止，右下角是 13。用 `compute.py` 的 `simplex` 条目核对每张表。

6. ★ **研究：多项式 Hirsch 猜想。** 我们的随机三维多面体的直径大致随面数 n 按 √n 增长。证明每个 n 个面的 d 维多面体的直径都以 n 和 d 的
   某个多项式为界，或者构造一族打破任何多项式界的多面体。

   *从哪里入手。* 目前最好的一般上界是拟多项式的：Kalai 与 Kleitman，"A quasi-polynomial bound for the diameter of graphs of
   polyhedra"（1992），n^{log₂ d + 2}；Todd（2014）改进为 (n − d)^{log₂ d}；以及 Sukegawa（2019）。Santos，"A counterexample to the
   Hirsch conjecture"（Annals of Mathematics，2012），否定了精确的界，但没有否定多项式的界。一些特殊类有好的界：0/1 多面体的直径至多为 d
   （Naddef 1989）；子行列式有界的整数多面体直径是多项式的（Bonifas、Di Summa、Eisenbrand、Hähnle 与 Niemeier 2014）。Eisenbrand、
   Hähnle、Razborov 与 Rothvoß，"Diameter of polyhedra: limits of abstraction"（2010），研究一种组合抽象"连通层族"：其 Ω(n²/log n) 的下界
   与拟多项式上界之间的差距仍未解决，这也是 Polymath 3 的主题。缩小这个差距是自然的第一步。

## Glossary additions

线性规划 linear program · 可行域 feasible region · 多面体 polytope · 顶点 vertex · 目标函数 objective function · 单纯形法 simplex
method · 转轴 pivot · 单纯形表 tableau · 进基 entering · 出基 leaving · 比值检验 ratio test · 退化 degeneracy · 循环 cycling ·
Bland 规则 Bland's rule · 对偶 duality · 弱对偶 weak duality · 强对偶 strong duality · Farkas 引理 Farkas' lemma · 影子价格
shadow price · 互补松弛 complementary slackness · 检验数 reduced cost · 平滑分析 smoothed analysis · 椭球法 ellipsoid method · 内点法
interior-point method · 中心路径 central path · 对数障碍 log barrier · 全单模 totally unimodular · 整数规划 integer program · 分支定界
branch and bound · 割平面 cutting plane · 整性间隙 integrality gap · 近似算法 approximation algorithm · 近似比 approximation ratio ·
完全多项式时间近似方案 FPTAS · 顶点覆盖 vertex cover · 集合覆盖 set cover · 旅行商问题 travelling salesman problem · 三角不等式
triangle inequality · 最大割 MAX-CUT · 半定规划 semidefinite program · 随机超平面 random hyperplane · 在线算法 online algorithm ·
竞争比 competitive ratio · 租雪板问题 ski rental · 页面置换 paging · 乘性权重 multiplicative weights · 遗憾 regret · 零和博弈
zero-sum game · 凸优化 convex optimization · KKT 条件 KKT conditions · Hirsch 猜想 Hirsch conjecture · 唯一博弈猜想 unique games
conjecture

## Sources

*Canon.* Books:
- Bertsimas & Tsitsiklis, *Introduction to Linear Optimization* (1997);
- Chvátal, *Linear Programming* (1983);
- Matoušek & Gärtner, *Understanding and Using Linear Programming* (2007);
- Schrijver, *Theory of Linear and Integer Programming* (1986) and *Combinatorial Optimization* (2003);
- Williamson & Shmoys, *The Design of Approximation Algorithms* (2011);
- Vazirani, *Approximation Algorithms* (2001);
- Borodin & El-Yaniv, *Online Computation and Competitive Analysis* (1998);
- Applegate, Bixby, Chvátal & Cook, *The Traveling Salesman Problem: A Computational Study* (2006);
- Boyd & Vandenberghe, *Convex Optimization* (2004).

Papers:
- Linear programming: Kantorovich (1939); Hitchcock (1941); Stigler, "The cost of subsistence" (1945); Dantzig
  (1947, 1951); Bland (1977); Klee & Minty (1972); Jeroslow (1973); Avis & Chvátal (1978); Friedmann (2011); Spielman
  & Teng, "Smoothed analysis of algorithms" (2001, 2004).
- Polynomial time: Khachiyan (1979); Grötschel, Lovász & Schrijver (1981); Karmarkar (1984); Renegar (1988); Vaidya
  (1989); Nesterov & Nemirovski (1994); Cohen, Lee & Song (2019); van den Brand (2020); Chen, Kyng, Liu, Peng,
  Probst Gutenberg & Sachdeva, "Maximum flow and minimum-cost flow in almost-linear time" (2022).
- Integrality: Hoffman & Kruskal (1956); Edmonds, "Maximum matching and a polyhedron with 0,1-vertices" (1965);
  Seymour (1980); Gomory (1958); Land & Doig (1960); Bixby (2012).
- Approximation:
  - Ibarra & Kim (1975); Johnson (1974); Lovász (1975); Chvátal (1979); Feige (1998); Dinur & Steurer (2014);
  - Christofides (1976); Serdyukov (1978); Arora (1998); Mitchell (1999); Karlin, Klein & Oveis Gharan (2021);
  - Lin & Kernighan (1973); Helsgaun (2000); Beardwood, Halton & Hammersley (1959);
  - Goemans & Williamson (1995); Burer & Monteiro (2003); Håstad (2001); Khot, Kindler, Mossel & O'Donnell (2007);
    Khot & Regev (2008).
- Online: Belady (1966); Sleator & Tarjan (1985); Karlin, Manasse, McGeoch & Owicki (1994); Fiat, Karp, Luby,
  McGeoch, Sleator & Young (1991).
- Learning: Littlestone & Warmuth (1994); Freund & Schapire (1995, 1997); Plotkin, Shmoys & Tardos (1995); Arora,
  Hazan & Kale, "The multiplicative weights update method: a meta-algorithm and applications" (2012).
- Convexity: Karush (1939); Kuhn & Tucker (1951); Rockafellar, "Lagrange multipliers and optimality" (1993).
- Frontier:
  - Hirsch (1957); Kalai & Kleitman (1992); Santos (2012); Eisenbrand, Hähnle, Razborov & Rothvoß (2010); Todd
    (2014); Sukegawa (2019);
  - Arora & Safra (1998); Arora, Lund, Motwani, Sudan & Szegedy (1998); Khot (2002); Raghavendra (2008); Khot,
    Minzer & Safra (2018); Karpinski, Lampis & Schmied (2015); Smale, "Mathematical problems for the next century"
    (1998).
