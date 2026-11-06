# Computer Science, Built — Part 22: Geometry

Part 22 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the seventh part of Act IV, *Algorithms*. Geometry looks easy until a computer gets
it wrong: a floating-point orientation test can say a point lies on both sides of a line. Get the predicates right
and beautiful structure follows. Voronoi diagrams grow as a parabolic beach line, and every Delaunay triangulation is
the shadow of a convex hull on a paraboloid. The instrument is `explainer/cs/algo/geometry.py`. It holds:

* predicates: floating-point, exact (rationals), Shewchuk-style adaptive, and integer orientation and in-circle tests,
  with Kettner's grid;
* hulls: Jarvis, Graham, Andrew's monotone chain, quickhull, and Chan with binary-search tangents, all counting
  orientation tests and sort comparisons;
* Bentley–Ottmann with an event log;
* ear clipping and Fisk's three-colouring;
* incremental Delaunay with Lawson's flips, over exact integers;
* Lawson's flips from any triangulation;
* Fortune's sweep with a list beach line;
* Seidel's 2D LP;
* kd-trees;
* trapezoidal maps;
* a single-layer navigable small world and a hierarchical one (HNSW with the diversity heuristic);
* a brute-force ham sandwich;
* Minkowski configuration spaces with a visibility-graph planner, and an RRT;
* the Euclidean MST over Delaunay edges, against Prim on all pairs;
* Welzl's smallest enclosing circle.

It is tested in `tests/test_cs22_geometry.py`: every hull agrees, Bentley–Ottmann matches brute force, and three
Delaunay constructions match the lifting map. Every number is computed in `compute.py`, and timings are taken on
this machine.

* **Left, right, or on the line?** Hook.
  - p a few ulps from (½, ½), q = (12, 12), r = (24, 24): the three rotations of one orientation test answer +1, 0
    and −1 in double precision, and exactly −1.
  - Among the 65,536 nearest floats, 13,968 disagree with themselves.
  - Kettner's picture: 11,972 wrong signs.
* **1. The one primitive.**
  - Orientation as a signed area, with in-circle as its cousin.
  - Why rounding fails, and Shewchuk's error bound (3 + 16ε)ε(|a| + |b|).
  - Adaptive predicates, over 20,000 tests of each kind:
    - random points: float wrong 0 times, the exact stage needed 0% of the time, 137 ns against 326 ns;
    - nearly collinear points: float wrong 3,713 times, the exact stage needed 70%.
  - Integer coordinates.
* **2. Convex hulls.**
  - Graham's scan, animated on 28 points.
  - Five algorithms on 10,000 points in a square (h = 22), a disk (75) and on a circle (5,513):
    - Jarvis: 219,956 tests on the square, 749,850 on the disk, and about 3 × 10⁷ on the circle;
    - Graham and the monotone chain: about 1.3–1.6 × 10⁵ including the sort;
    - Chan: 3.9–8.2 × 10⁵.
  - The Ω(n log n) lower bound by lifting numbers to a parabola (Ben-Or).
  - Chan's O(n log h), its squaring guesses, and Kirkpatrick–Seidel.
* **3. The sweep line.**
  - Bentley–Ottmann animated on seven segments, with the status and the events.
  - On 100 to 3,000 random segments, the events are exactly 2n + k and the tests about twice the events. For 3,000
    segments that is 19,812 tests against 4,498,500 pairs.
  - Chazelle–Edelsbrunner's optimal bound.
* **4. Guarding an art gallery.**
  - Chvátal's comb with 5 teeth (17 walls) needs 5 guards.
  - Fisk's proof animated on a 22-gon: ears, the dual tree, three colours 5 + 9 + 8, five guards.
  - On 200 random 60-gons, Fisk's smallest colour class averages 17.3 against the bound of 20.
  - Monotone pieces, Chazelle's linear algorithm, and NP- and ∃ℝ-hardness of the true minimum.
* **5. Voronoi diagrams.**
  - The diagram of 14 sites, and Snow's cholera map.
  - Fortune's sweep animated: the beach line of parabolas, breakpoints tracing edges, vertices appearing at circle
    events.
  - On 250 to 2,000 sites, the circle events equal 2n − 2 − h exactly, and the triangles agree with the lifting map
    every time. For n = 2,000 there are 3,107 false alarms.
* **6. Delaunay triangulations.**
  - Empty circles, duality with Voronoi, the in-circle determinant.
  - Lawson's flips animated from a sweep triangulation of 16 points: 17 flips, with the smallest angle rising from
    0.48° to 4.81° (Sibson).
  - Meshes and TINs.
  - The Euclidean minimum spanning tree lies inside the triangulation (Shamos–Hoey). Kruskal over 23,972 Delaunay
    edges matches Prim over all 31,996,000 pairs for 8,000 points, in 0.24 s against 1.85 s.
* **7. The lifting map.** A 3D tour:
  - points lifted to z = x² + y², the lower hull, and a circle's lift lying on a plane;
  - Brown's theorem, and Edelsbrunner–Seidel in any dimension;
  - the 4 × 4 in-circle determinant equals the 3 × 3 one (96 = 96);
  - why Lawson's flips stop, and the Voronoi diagram as an upper envelope;
  - checked against scipy.
* **8. Random order and backwards analysis.**
  - One insertion's conflicts and star-shaped hole.
  - Backwards analysis: expected degree < 6 by Euler.
  - Random order makes 8.6–8.9 triangles per point at n = 1,000–16,000.
  - An adversarial order makes 874,107 triangles for 1,600 points, against 13,155 shuffled.
* **9. Linear programming in the plane.**
  - Seidel's algorithm, animated on nine constraints: the optimum moves three times.
  - Pr ≤ 2/i, hence O(n). Measured: the optimum moved 22.6 times among 100,000 constraints (2H_n = 24.2), with
    under 3 one-dimensional steps per constraint.
  - Megiddo.
  - Welzl's smallest enclosing circle, animated on 40 points. 100,000 points rebuild the circle 29 times (3 ln n is
    35), in 0.47 s.
* **10. Range searching.**
  - Bentley's kd-tree built level by level on 60 points; a query visits 46 of 119 nodes.
  - On up to 300,000 points the visits stay below √n + k (334 nodes).
  - Range trees, fractional cascading, interval and segment trees, R-trees.
* **11. Point location.**
  - Dobkin–Lipton slabs.
  - The trapezoidal map of seven segments has 22 trapezoids, which is 3n + 1. Random maps hit 3n + 1 every time.
  - Randomized incremental search structures (Mulmuley, Seidel), and Kirkpatrick.
* **12. High dimensions.**
  - Distance concentration: the farthest-to-nearest ratio falls from 103 at d = 2 to 1.11 at d = 1,000.
  - Share of a kd-tree's nodes visited for one nearest neighbour: 0.06% at d = 2, 55% at d = 12, 100% at d = 24.
  - Navigable small worlds and HNSW (four layers over 20,000 points in 16 dimensions):
    - plain nearest-neighbour links reach 41–98% recall at 197–656 distance computations;
    - HNSW's diversity rule reaches 96.7–100%, and 99.7% at 182 computations against 20,000 for brute force.
* **13. Duality and the ham sandwich.**
  - Points to lines: collinearity becomes concurrency.
  - Arrangements and the zone theorem.
  - A ham-sandwich cut of 9 red and 9 blue points (Stone–Tukey, Lo–Matoušek–Steiger).
* **14. Moving a robot.**
  - A sliding triangle: Minkowski sums, configuration space, the visibility graph and Dijkstra. The path has length
    14.08 with four bends.
  - A rapidly-exploring random tree grown in the same space: 137 nodes. Over 20 seeds every tree finds a path, on
    average 1.29× the optimum.
  - Reif's PSPACE-hardness, Canny, PRMs.
* **15. Frontier: exactness, 3SUM and nearest neighbours.**
  - Exact geometric computation: the rational test costs 124× floating point on near-degenerate input. Symbolic
    perturbation and snap rounding.
  - 3SUM as collinearity of (a, a³), checked on 14 numbers (2 triples, 2 collinear triples), and Gajentaan–Overmars.
  - LSH's optimal exponents, data-dependent hashing, and Indyk–Xu on graph indexes.
  - Open problems: 3SUM, Hopcroft's problem, guarantees for navigable graphs. Outro.

## Build

```bash
python -m videos.cs.cs22.compute           # every number in the part (about two minutes)
python tools/build.py cs22 -q l            # a 480p preview
python tools/build.py cs22                 # 1080p
```

## Problems, with solutions

1. **Graham's scan is linear after sorting.** Prove that after sorting, Graham's scan makes fewer than 2n orientation
   tests.

   *Solution.* Each test either pops the top of the stack (the turn is not counter-clockwise) or ends the inner loop
   (the turn is counter-clockwise, and the new point is then pushed). A point is pushed once, so it can be popped at
   most once: at most n − 1 tests pop. The loop ends once per point processed: at most n − 1 tests end loops. So
   there are at most 2n − 2 tests. The scan is correct because the stack is always the convex hull of the points
   seen so far, in angular order. A point popped makes a non-left turn with a later point, so it lies inside the
   triangle formed by the origin, its predecessor and that later point.

2. **Trapezoids.** Prove that the trapezoidal map of n non-crossing segments in general position (no two endpoints
   share an x-coordinate), inside a bounding box, has at most 3n + 1 trapezoids.

   *Solution.* Every trapezoid has a left side: either the box's left edge, or a wall through an endpoint p, where p
   defines the trapezoid's left boundary. Charge the trapezoid to p (or to the box, for exactly one trapezoid). A left
   endpoint has two trapezoids to its right that it bounds on the left: one above its segment and one below. A right
   endpoint has one: the trapezoid to its right that its two walls bound. So the count is at most 2n + n + 1. With
   general position equality holds, as our random maps showed.

3. **The lifting lemma.** Prove that d is inside the circle through a, b, c exactly when its lift
   (d_x, d_y, d_x² + d_y²) is below the plane through the lifts of a, b, c. Derive the in-circle determinant from it.

   *Solution.* A circle is (x − u)² + (y − v)² = r², that is x² + y² = 2ux + 2vy + (r² − u² − v²). On the paraboloid
   z = x² + y² this says z = 2ux + 2vy + k, a plane. So the lift of the circle is the intersection of the paraboloid
   with that plane. It is the plane through the lifts of a, b, c, since they lie on both. A point is inside the circle
   exactly when x² + y² < 2ux + 2vy + k, that is, when its lift is below the plane. "Below the plane through three
   lifted points" is the sign of the 3D orientation determinant of four lifted points, written with rows
   (x, y, x² + y², 1). Subtracting d's row from the others and expanding along the last column gives chapter 6's
   3 × 3 in-circle determinant. The sign convention matches when a, b, c are counter-clockwise.

4. **Seidel's LP.** Show that Seidel's algorithm moves the optimum at most 2H_n times in expectation, and does O(n)
   expected work.

   *Solution.* Fix any set of i constraints, together with the box. Its optimum is a vertex determined by at most two
   of the constraints. When the order is random, every one of the i constraints is equally likely to be the last one
   added. The optimum after step i − 1 differs from the optimum after step i only if the i-th constraint is one of
   those two. So Pr[move at step i] ≤ 2/i, the expected number of moves is at most Σ 2/i = 2H_n, and with the 1D
   problem costing O(i), the expected work is Σ (2/i) · O(i) + O(n) = O(n). Our measurement agrees: 22.6 moves at
   n = 10⁵, against 2H_n = 24.2.

5. **Build: a hull in Pebble.** Write the orientation test and Andrew's monotone chain in the Pebble language, with
   coordinates below 2¹⁵ so every product fits in a word. Hull 10,000 points on the emulator.

   *Solution sketch.* Store the points as two arrays and sort them by (x, y) with Part 16's merge sort, comparing x
   first. Orientation is (qx − px)(ry − py) − (qy − py)(rx − px). Each factor is below 2¹⁵ in absolute value, so each
   product is below 2³⁰ and the difference fits in a 32-bit word. Pebble has no bitwise operators, but none are
   needed. Build the lower hull with an array used as a stack, popping while the orientation is ≤ 0, then build the
   upper hull the same way on the reversed order. Check the output against `geometry.monotone_chain`. Count the
   emulator's instructions per point: the sort dominates, as in chapter 2's table, at about n log₂ n comparisons.

6. ★ **Research: why do navigable graphs work?** Our HNSW found 99.7% of the true ten nearest neighbours with 182
   distance computations, on clustered 16-dimensional data, and no theorem explains it. Prove a query bound for
   graphs built by HNSW's diversity rule on data of low doubling dimension, or construct inputs that force Ω(n)
   computations.

   *Where to start.* Indyk and Xu, "Worst-case performance of popular approximate nearest neighbor search
   implementations" (NeurIPS 2023). It proves guarantees for DiskANN's slow-preprocessing graph under bounded doubling
   dimension, and gives hard instances for HNSW and NSG. Also Arya and Mount (1993) on neighbourhood graphs, and
   Laarhoven (2018) on graph-based search in high dimensions. A natural first step is to formalize the diversity rule
   as an α-robust pruning rule and ask what it guarantees about greedy routing.

## 习题与解答

1. **排序之后，Graham 扫描是线性的。** 证明排序之后 Graham 扫描少于 2n 次方向测试。

   *解答。* 每次测试要么弹出栈顶（不是逆时针转向），要么结束内层循环（是逆时针转向，随后压入新点）。每个点只压入一次，所以至多被弹出
   一次：弹出的测试至多 n − 1 次。每处理一个点循环结束一次：结束循环的测试至多 n − 1 次。所以至多 2n − 2 次测试。正确性：栈始终是
   已见点按角度顺序的凸包；被弹出的点与后来的某点不构成左转，因此它位于原点、它的前驱和那个后来点组成的三角形之内。

2. **梯形。** 证明边界框内 n 条互不相交、处于一般位置（任意两个端点的 x 坐标不同）的线段的梯形图至多有 3n + 1 个梯形。

   *解答。* 每个梯形都有左边：要么是边界框的左边，要么是过某个端点 p 的墙，由 p 决定梯形的左边界。把梯形记在 p 上（恰有一个记在边界
   框上）。左端点在它右边作为左边界的梯形有两个：线段上方一个、下方一个；右端点有一个：它的两堵墙所夹、在它右边的那个梯形。所以至多
   2n + n + 1 个。一般位置下取等号，我们的随机地图正是如此。

3. **提升引理。** 证明 d 在过 a、b、c 的圆内，当且仅当它的提升点 (d_x, d_y, d_x² + d_y²) 在过 a、b、c 提升点的平面之下；并由此推出
   内圆行列式。

   *解答。* 圆是 (x − u)² + (y − v)² = r²，即 x² + y² = 2ux + 2vy + (r² − u² − v²)。在抛物面 z = x² + y² 上，这就是
   z = 2ux + 2vy + k，一个平面；所以圆的提升是抛物面与该平面的交线，而这平面过 a、b、c 的提升点，因为它们同时在两者之上。点在圆内
   当且仅当 x² + y² < 2ux + 2vy + k，即它的提升点在平面之下。“在过三个提升点的平面之下”就是四个提升点的三维方向行列式的符号，每行
   为 (x, y, x² + y², 1)；把各行减去 d 的那一行并沿最后一列展开，就得到第6章的 3 × 3 内圆行列式（a、b、c 逆时针时符号约定一致）。

4. **Seidel 的线性规划。** 证明 Seidel 算法最优解移动次数的期望至多为 2H_n，期望工作量为 O(n)。

   *解答。* 固定任意 i 个约束（连同边界框）。其最优解是由至多两个约束决定的顶点。顺序随机时，这 i 个约束中每一个都同样可能是最后加入
   的；第 i − 1 步与第 i 步之后的最优解不同，当且仅当第 i 个约束是那两个之一。所以第 i 步移动的概率 ≤ 2/i，期望移动次数至多
   Σ 2/i = 2H_n；一维问题代价 O(i)，故期望工作量为 Σ (2/i) · O(i) + O(n) = O(n)。我们的测量与之一致：n = 10⁵ 时移动 22.6 次，
   而 2H_n = 24.2。

5. **构造：Pebble 中的凸包。** 用 Pebble 语言写出方向测试和 Andrew 的单调链，坐标小于 2¹⁵，使每个乘积都能放进一个字；在模拟器上
   对 10,000 个点求凸包。

   *解答提要。* 把点存为两个数组，用第16部分的归并排序按 (x, y) 排序（先比较 x）。方向为 (qx − px)(ry − py) − (qy − py)(rx − px)：
   每个因子的绝对值小于 2¹⁵，所以每个乘积小于 2³⁰，差能放进 32 位字。Pebble 没有位运算，但这里也不需要。用一个数组当栈构造下凸包，
   方向 ≤ 0 时弹出；再对逆序构造上凸包。用 `geometry.monotone_chain` 核对输出。统计模拟器每点的指令数：与第2章的表一样，排序占主导，
   约 n log₂ n 次比较。

6. ★ **研究：可导航图为什么有效？** 我们的 HNSW 在成簇的 16 维数据上，用 182 次距离计算找到了真正 10 个最近邻中的 99.7%，却没有定理
   能解释这一点。为按 HNSW 多样性规则构造的图，在低倍增维数的数据上证明一个查询界；或者构造迫使其做 Ω(n) 次计算的输入。

   *从哪里入手。* Indyk 与 Xu，“Worst-case performance of popular approximate nearest neighbor search implementations”（NeurIPS
   2023）：在倍增维数有界时证明了 DiskANN 慢速预处理图的保证，并给出 HNSW 与 NSG 的困难实例。另见 Arya 与 Mount（1993）关于邻域图的
   工作，以及 Laarhoven（2018）关于高维图搜索的工作。自然的第一步是把多样性规则形式化为一种 α-鲁棒剪枝规则，再问它对贪心路由能保证
   什么。

## Glossary additions

方向测试 orientation test · 内圆测试 in-circle test · 谓词 predicate · 自适应精确谓词 adaptive exact predicate · 误差界 error
bound · 凸包 convex hull · 礼品包装 gift wrapping · 单调链 monotone chain · 输出敏感 output-sensitive · 扫描线 sweep line · 事件队列
event queue · 状态结构 status structure · 美术馆问题 art gallery problem · 耳朵 ear · 三着色 three-colouring · Voronoi 图 Voronoi
diagram · 海滩线 beach line · 点事件 site event · 圆事件 circle event · Delaunay 三角剖分 Delaunay triangulation · 空圆性质
empty-circle property · 边翻转 edge flip · 提升映射 lifting map · 下凸包 lower hull · 随机增量构造 randomized incremental
construction · 反向分析 backwards analysis · 冲突 conflict · 半平面 half-plane · kd 树 kd-tree · 范围查询 range query · 分散层叠
fractional cascading · 点定位 point location · 梯形图 trapezoidal map · 维数灾难 curse of dimensionality · 可导航小世界图 navigable
small world · 对偶 duality · 排列 arrangement · 火腿三明治定理 ham-sandwich theorem · 构形空间 configuration space · Minkowski 和
Minkowski sum · 可见性图 visibility graph · 3SUM 难 3SUM-hard

## Sources

*Canon.* Books:
- de Berg, Cheong, van Kreveld & Overmars, *Computational Geometry: Algorithms and Applications* (3rd ed., 2008);
- Preparata & Shamos, *Computational Geometry: An Introduction* (1985);
- O'Rourke, *Computational Geometry in C* (1998) and *Art Gallery Theorems and Algorithms* (1987);
- Devadoss & O'Rourke, *Discrete and Computational Geometry* (2011);
- Edelsbrunner, *Geometry and Topology for Mesh Generation* (2001);
- LaValle, *Planning Algorithms* (2006).

Papers:
- Hull and sweep algorithms: Graham (1972); Jarvis (1973); Andrew (1979); Bentley & Ottmann (1979); Kirkpatrick &
  Seidel, "The ultimate planar convex hull algorithm?" (1986); Chazelle & Edelsbrunner (1992); Chan, "Optimal
  output-sensitive convex hull algorithms in two and three dimensions" (1996).
- Lower bounds: Ben-Or (1983).
- Art galleries and triangulation: Chvátal (1975); Meisters (1975); Fisk (1978); Garey, Johnson, Preparata & Tarjan
  (1978); Lee & Lin (1986); Chazelle, "Triangulating a simple polygon in linear time" (1991); Abrahamsen, Adamaszek
  & Miltzow (2018).
- Voronoi and Delaunay: Voronoi (1908); Delaunay (1934); Lawson (1977); Sibson (1978); Brown, "Voronoi diagrams from
  convex hulls" (1979); Guibas & Stolfi (1985); Edelsbrunner & Seidel (1986); Fortune, "A sweepline algorithm for
  Voronoi diagrams" (1987); Guibas, Knuth & Sharir (1992); Ruppert (1995).
- Randomized algorithms: Clarkson & Shor (1989); Mulmuley (1990); Seidel, "Small-dimensional linear programming and
  convex hulls made easy" (1991) and "Backwards analysis of randomized geometric algorithms" (1993); Welzl (1991).
- Linear programming and enclosing circles: Megiddo (1983, 1984); Welzl (1991).
- Spanning trees: Shamos & Hoey, "Closest-point problems" (1975).
- Range search and point location: Bentley, "Multidimensional binary search trees" (1975); Dobkin & Lipton (1976);
  Kirkpatrick (1983); Guttman, "R-trees" (1984); Chazelle & Guibas, "Fractional cascading" (1986).
- Duality and arrangements: Stone & Tukey (1942); Lo, Matoušek & Steiger (1994).
- Robustness and exact computation: Edelsbrunner & Mücke, "Simulation of simplicity" (1990); Shewchuk, "Adaptive
  precision floating-point arithmetic and fast robust geometric predicates" (1997); Yap, "Towards exact geometric
  computation" (1997); Hobby (1999); Kettner, Mehlhorn, Pion, Schirra & Yap, "Classroom examples of robustness
  problems in geometric computations" (2008).
- Motion planning: Lozano-Pérez & Wesley (1979); Reif (1979); Canny (1988); Kavraki, Švestka, Latombe & Overmars
  (1996); LaValle (1998).
- 3SUM: Gajentaan & Overmars, "On a class of O(n²) problems in computational geometry" (1995); Grønlund & Pettie
  (2014); Chan (2018).
- Nearest neighbours: Indyk & Motwani (1998); Andoni & Indyk (2006); O'Donnell, Wu & Zhou (2014); Andoni &
  Razenshteyn (2015); Malkov & Yashunin, "Efficient and robust approximate nearest neighbor search using hierarchical
  navigable small world graphs" (2016, 2018); Indyk & Xu (2023).
