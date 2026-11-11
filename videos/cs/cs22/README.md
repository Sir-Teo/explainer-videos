# Computer Science, Built — Part 22: Geometry

Part 22 of the [61-part series](../README.md). The [syllabus](../SYLLABUS.md)
connects geometry to optimization, databases, graphics and numerical computing.
The central question is how a geometric algorithm's arithmetic, invariants and
input conventions together justify its result.

The executed instrument is `explainer/cs/algo/geometry.py`; `compute.py` builds
17 schema-2 payloads. Raw timing repetitions, output checks and host/protocol
metadata remain in the cache. Independent references run **after** the timed
operation. Producer wall time includes setup and references and is not an
algorithm benchmark. Tests live in `tests/test_cs22_geometry.py`.

## What is built

1. **Predicates.** Integer orientation promotes NumPy scalars before products.
   Floating orientation has a conservative filter and a Python rational fallback
   for uncertain, underflowing or overflowing intermediate arithmetic. This is
   not Shewchuk's expansion implementation. The grid is the one-sided 256×256
   grid of successive binary64 coordinates starting at (1/2,1/2). A separate
   executed witness uses stored binary64 x=fl(10^-200): x>0 and its exact square
   is positive, while the floating product rounds to zero.
2. **Hulls.** Jarvis, Graham, monotone chain, quickhull and Chan, including exact
   angular ordering and collinear tangent ties. Operation totals count orientation/determinant evaluations
   and sort-comparator calls, including Quickhull farthest-point determinants.
   A comparator that calls orientation contributes both. Other arithmetic and
   tie comparisons are excluded. A dash for the largest
   circle/Jarvis case means unmeasured, not an estimate. Rounded circle inputs
   need not all be extreme. Chan's 1996 output-sensitive theorem covers 2D and 3D.
3. **Sweep.** The event trace and all output pairs up to 3,000 segments are checked.
   The measured status is a list with linear updates. The balanced-tree
   O((n+k)log n) theorem describes a different implementation and arithmetic model.
4. **Gallery.** Fisk's triangulation, three-colouring and smallest colour class
   guard a simple polygon without holes. All 200 sampled polygons receive area,
   triangulation and colouring checks. Maintained-ear algorithms are quadratic;
   our repeated candidate/containment rescans can be cubic. A guard certificate
   proves coverage, not a minimum number of guards.
5. **Voronoi.** A moving beach line explains Fortune's construction. The finite
   list implementation agrees with Qhull on every measured sample after timing.
   General-position Euler counts and numerical agreement are stated separately
   from exact arithmetic and handling of degenerate inputs.
6. **Delaunay.** Empty circles, strict Lawson flips and the CCW in-circle sign.
   Randomized integer insertion rejects duplicate and fractional inputs and uses
   a data-dependent artificial triangle. Exact local-circle, area and Euler
   certificates check the measured integer triangulations. Finite Qhull
   constructions elsewhere in the chapter remain numerical.
7. **Lifting.** Lift (x,y) to (x,y,x²+y²). Empty circles become lower supporting
   planes; strict flips lower a surface with finitely many triangulations.
   The integer example gives matching 4×4 and 3×3 determinants of 96.
8. **Random insertion.** The expected final degree is below six by Euler.
   Created-object counters include artificial and destroyed triangles and flip
   intermediates; they are not that final degree. There is no asserted strict
   9n+1 bound for this counter. Conflict-list point location gives a textbook
   expected O(n log n) algorithm; our walking locator does not inherit it.
9. **LP and enclosing circles.** Finite-box LP with explicit tolerances is checked
   by SciPy for every trial at every size. Harmonic bounds are exact sums.
   Circle certificates check containment and a boundary-support convex
   combination of the centre, which establishes numerical minimality.
10. **Range queries.** Median-partition kd-trees and fully checked closed ranges.
    A duplicate-coordinate witness returns all three records on the split plane,
    including two at the same position. Query node visits and build time are
    different metrics; O(√n+k) does not promise a constant of one.
11. **Point location.** Slabs and the 3n+1 trapezoid count assume disjoint
    nonvertical segments with distinct endpoint x coordinates in a box.
    Our drawing enumerates walls; it does not implement or time a randomized
    search DAG. The DAG's expected bounds belong to that separate algorithm.
12. **High dimensions.** Seeded unit-cube distance concentration and kd-tree
    visits illustrate distribution-dependent pruning. Teaching NSW/HNSW-style
    graphs use clustered 16D data. All 1,000 true neighbour positions for 100
    queries are checked. Mean recall@10 and query distance-evaluation counts
    exclude build work, memory traffic and latency. No LSH or production-library
    performance comparison is executed.
13. **Duality.** (a,b) maps to y=ax−b; a nonvertical line y=mx+c maps to (m,−c).
    Incidence is preserved. A point **above** a primal line gives a dual line
    **below** its dual point, since b>ma+c implies am−b<−c. Arrangement counts
    require no parallels or triple intersections. The ham-sandwich example
    verifies its actual side counts.
14. **Planning.** A translating triangle becomes a point among convex
    configuration obstacles. Boundary contact is allowed; strict interior
    collision is forbidden. A segment through two square corners demonstrates
    why fixed probes miss collisions. Full convex clipping is independently
    checked with rational interval references for path and every RRT parent edge.
    Vertex visibility assumes disjoint configuration obstacles; overlapping ones
    require union-boundary intersections that this builder does not construct.
    The 20-seed success result is a finite observation, not a universal guarantee.
    Broader roadmap theorems use semi-algebraic descriptions and include input-size
    and polynomial-degree factors. Sampling requires a metric and sampling rule.
15. **Research.** Exact predicates alone do not repair bad constructions or
    invariants. The distinct-value cubic reduction illustrates conditional 3SUM
    hardness. Selected 2015 hashing exponents include their Euclidean task,
    dimension/space factors and model. Chan–Zheng (2022) give O(n^(4/3)) planar
    incidence counting. Indyk–Xu (2023) already give hard graph-search instances
    and separate low-intrinsic-dimension guarantees for slow-preprocessing
    DiskANN. These dated results do not assert present-day open status.

The Euclidean-MST experiment compares Delaunay/Kruskal total weights with full
complete-graph Prim at every displayed size, including 8,000 points. Agreement
uses an explicit numerical tolerance and need not imply a unique tree.

## Build and verification

```bash
python -m videos.cs.cs22.compute
python -m unittest discover -s tests -p 'test_cs22_geometry.py' -v
python tools/build.py cs22 -q l
python tools/build.py cs22
```

Cached schema-2 data must be rebuilt with the corresponding instrument source;
the cached-only entry rejects stale payloads. Source/preview evidence is tracked
in `docs/qa/computer-science-built-progress.md`. Sampled silent previews and
automated speech/cue checks do not complete continuous listening, Chinese speech,
whole-video native review or runtime approval at the final narration pace.

## Problems, with worked solutions

1. **Graham's scan after sorting.** Use distinct points, an extreme pivot and a
   consistent radial tie rule. Prove fewer than 2n orientation tests in the scan.

   Each executed test either pops one stack element or ends that point's inner
   loop. Every point is pushed once and popped at most once; at most n−1 tests
   pop, and at most n−1 tests end a loop. Thus at most 2n−2 tests occur. For the
   sequence (0,0),(3,0),(1,1),(3,3),(0,3) in angular order, (1,1) is popped when
   (3,3) arrives. The stack's convex-chain invariant, with the chosen collinear
   policy, proves correctness. Sorting and its comparator calls are excluded
   from this linear scan bound; integer products must be promoted before use.

2. **Trapezoids.** In a fixed box, let n disjoint nonvertical segments have
   distinct endpoint x coordinates, with endpoints strictly inside. Show at most
   3n+1 cells when vertical walls stop at the nearest segment or box boundary.

   Charge each cell to the endpoint defining its left boundary; charge the cell
   touching the box's left side to the box. A left endpoint defines at most two
   cells to its right, a right endpoint at most one. Hence 2n+n+1. Under these
   strict assumptions all contributions occur: n=0 gives one, and a single
   internal segment gives four. Shared endpoints and crossings require new
   counting conventions. This is a size proof, not a construction-time proof.

3. **Lifting and sign.** Let a,b,c be noncollinear and counter-clockwise.
   Derive the circle/lower-plane equivalence and in-circle determinant.

   A circle with centre (u,v) and radius r satisfies
   x²+y²=2ux+2vy+r²−u²−v². Its lift lies in the plane z=2ux+2vy+k.
   A point is inside exactly when its lifted height is below that plane.
   In the 4×4 determinant with rows (x,y,x²+y²,1), subtract d's row from each
   other row and expand the last column. Column operations remove the linear
   terms in d, leaving rows (x−d_x,y−d_y,|p−d|²). For a=(0,0), b=(4,0),
   c=(0,4), d=(1,1), the determinant is 96>0. Reversing a,b reverses the sign;
   cocircularity gives zero and needs a consistent tie policy.

4. **Seidel's expectation.** Work in exact arithmetic with a fixed bounding box,
   feasible prefixes and a consistent unique-optimum/tie convention. Show at
   most 2H_n expected changes and O(n) expected work.

   Condition on the unordered i constraints present. A basis of at most two
   input constraints fixes the chosen optimum; fixed box sides may supply part
   of the basis. Removing a constraint outside that basis cannot change the
   chosen optimum. The last input is uniform among i constraints, so the change
   probability is at most 2/i. Linearity of expectation gives Σ2/i=2H_n,
   and Σ(2/i)O(i)+O(n)=O(n). It is an upper bound over order, not an equality
   prediction. Floating tolerance, infeasibility and unboundedness need explicit
   handling; SciPy agreement on finite samples is a separate check.

5. **Build a bounded-integer hull in Pebble.** Implement orientation and monotone
   chain, using integer coordinates 0≤x,y<2^15, then test on the emulator.

   Store two coordinate arrays; mergesort lexicographically and discard duplicate
   pairs. Build a lower stack, popping while the last two points and the new
   point have orientation ≤0; append the new point. Repeat on reversed order
   for the upper stack. Concatenate both without repeated endpoints. Empty and
   singleton inputs return themselves; a collinear non-singleton set returns its
   two extreme endpoints. Each difference has magnitude at most 32767; each
   product is at most 32767²=1,073,676,289 in magnitude. Their difference is at
   most 2,147,352,578, below signed-32-bit maximum 2,147,483,647. Merely saying
   coordinates are “below 2^15” would not give a lower bound or this safety proof.
   Verify empty, duplicate, collinear, square and extreme-bound fixtures before
   10,000 points; compare vertex set and CCW order with the Python reference.
   Count actual emulator instructions separately from comparator calls. This
   episode supplies the algorithm and arithmetic proof, **not an executed
   Pebble port**; the requested implementation is the exercise.

6. ★ **Reproduce, then extend a graph-search hard instance.** Start with
   Indyk–Xu (2023), rather than claiming that bad HNSW inputs are unknown.

   First specify the exact graph construction, pruning, beam, entry point,
   distance, tie rule, random seed and query distribution. Reproduce one published
   difficult family, checking true neighbours by a full independent scan. Report
   mean recall@10 over held-out queries and the actual query distance evaluations
   at increasing n. Count repeated evaluations; exclude and separately report
   build work. Linear-looking finite data alone do not prove Ω(n).
   For an extension, change one rule and either prove a bound with explicit
   assumptions or produce a counterexample to a precise proposed claim. A
   slow-preprocessing DiskANN theorem cannot be transferred to a teaching HNSW
   implementation by name. This is a reproducible research protocol, not a
   supplied novel theorem or a claim that the extension has been executed.

## 习题与解答

1. **排序后的 Graham 扫描。** 假设点互异、选取极端枢轴并一致处理同射线平局。
   每次方向测试要么弹栈，要么结束当前内循环。每点只压入一次、至多弹出一次，
   因此两类测试各至多 n−1 次，总数至多 2n−2。例中角序
   (0,0),(3,0),(1,1),(3,3),(0,3)，加入 (3,3) 时弹出 (1,1)。
   凸链不变量证明正确性；排序与比较器调用不包含在扫描界中，整数乘法前须提升。

2. **梯形计数。** 框内互不相交的非竖直线段，端点严格在框内且横坐标互异。
   把单元记到决定其左边界的端点上，最左单元记到框上。左端点至多贡献两个，
   右端点至多一个，加框共至多 3n+1。严格假设下各项都出现：零线段为一格，
   一条内部线段为四格。共享端点和交叉需要另立约定；空间计数不证明构建时间。

3. **提升与符号。** a、b、c 不共线且逆时针。圆方程展开为
   x²+y²=2ux+2vy+r²−u²−v²，所以圆提升后位于平面 z=2ux+2vy+k。
   圆内等价于提升高度低于该平面。四阶行列式的前三行各减 d 行，再沿最后一列展开，
   通过列运算消去 d 的线性项，得到行 (x−d_x,y−d_y,|p−d|²) 的三阶式。
   a=(0,0)、b=(4,0)、c=(0,4)、d=(1,1) 时值为 96>0；交换 a、b 则变号。
   共圆得到零，需要一致的平局处理。

4. **Seidel 的期望。** 采用精确算术、固定边界框、可行前缀和一致的唯一最优解或平局规则。
   固定当前 i 个约束集合，至多两个输入约束构成决定所选最优解的基，框边也可能参与。
   删除基外约束不会改变所选解。最后输入在 i 个约束中均匀分布，改变概率至多 2/i。
   故期望改变次数至多 Σ2/i=2H_n，期望工作为 Σ(2/i)O(i)+O(n)=O(n)。
   这是顺序上的上界，不是单次预测。浮点容差、不可行与无界必须另行处理；样本 SciPy
   核对是独立的数值检查。

5. **Pebble 有界整数凸包。** 整数坐标须满足 0≤x,y<2^15。双数组存点，归并排序、去重，
   用栈构造下链，非左转时弹出；逆序构造上链，拼接时去掉重复端点。空、单点原样返回，
   共线集保留两极端点。差的绝对值至多 32767，乘积至多 1,073,676,289，两个乘积之差
   的绝对值至多 2,147,352,578，小于有符号 32 位最大值 2,147,483,647。
   只说“小于 2^15”没有给出下界，不能据此证明安全。先测空、重复、共线、正方形与极限坐标，
   再测一万点；与 Python 参考核对顶点和逆时针顺序。模拟器指令数须实际测量。
   本章提供算法与算术证明，并未执行 Pebble 移植；实现与验证是练习内容。

6. ★ **复现再扩展图困难实例。** 从 Indyk–Xu（2023）出发，已有坏例不能当成尚无人构造。
   明确构图、剪枝、束宽、入口、距离、平局、种子和查询分布。复现一个发表的困难族，
   用独立完整扫描求真邻居。随 n 增长报告留出查询的平均 recall@10 和实际查询距离计算数，
   重复计算也计入；构建工作单独报告。有限数据看似线性并不证明 Ω(n)。扩展时只改一条规则，
   对精确命题证明带假设的界或给出反例。慢速预处理 DiskANN 的定理不能凭名称移到教学 HNSW。
   这里提供可复现协议，并不声称已经执行扩展或得到新定理。

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

Selected primary-source links:

- Chan (1996): https://www.cs.jhu.edu/~misha/Spring20/Chan96.pdf
- Andoni–Razenshteyn (2015): https://arxiv.org/abs/1501.01062
- Chan–Zheng (2022): https://arxiv.org/abs/2111.03744
- Indyk–Xu (2023): https://arxiv.org/abs/2310.19126
