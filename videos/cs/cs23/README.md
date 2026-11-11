# Computer Science, Built — Part 23: Optimization

Part 23 of the [61-part series](../README.md), in Act IV, *Algorithms*.
Optimization needs a model, a feasible answer and the right certificate. This part
builds exact small examples alongside numerical experiments and separates their
claims from selected dated research results.

The instrument is `explainer/cs/algo/optim.py`; its 27 tests are in
`tests/test_cs23_optim.py`. Fifteen producers in `compute.py` retain full measured
instances, independent references and certificates. Schema-2 cache entries bind
the actual producer, instrument and reference-module hashes. Changing any of
those sources invalidates the cache. Repeated algorithm timings exclude input
generation, hashing and independent validation; producer wall time includes them
and is not an algorithm benchmark. Shared-host times are observations.

## What is built and checked

1. **LP and simplex.** The bounded three-product polytope has six independently
   enumerated rational vertices. The optimum `(2,0,1)` has value 13 and dual
   `(1,0,1)`. Transportation shipments and a signed supply/demand dual both give
   365; ignoring plant capacity gives an infeasible 355 allocation. A general LP
   feasible set is a polyhedron and need not be bounded. This full-tableau simplex
   requires a feasible slack basis (`b >= 0`), with no Phase I. Each pivot uses
   `O(m(n+m))` arithmetic; the selector called `steepest` tries greatest total
   improvement, rather than normalized steepest edge. Independent basis solves
   reconstruct every displayed tableau. A zero-budget witness returns a feasible
   incumbent with `iteration_limit`; one permitted pivot gives matching primal
   and dual certificates. Degeneracy can require zero-length pivots.
2. **Duality.** Weak duality applies to feasible primal/dual pairs. Feasible LPs
   with a finite optimum have attained equal dual optima. Farkas' alternatives
   use the stated signs. Shadow prices are local sensitivities within a valid
   basis range; adding a whole unit of resource one raises profit by 1/3 despite
   its original dual price 1. Exact complementary slackness is checked.
3. **Klee–Minty.** The executed zero-based variant has `c_j=2^(n-1-j)`, diagonal
   coefficients 1, earlier coefficients `2^(j-i+1)`, and `b_j=5^(j+1)`. All 33
   rule/dimension runs from 2 through 12 use exact arithmetic. Dantzig takes
   `2^n-1` pivots, with every visited point checked for feasibility, distinctness
   and strict objective increase. Greatest improvement is a different rule.
   Every one of 101 multiplicatively perturbed cubes and 100 positive dense LPs
   has an independent solver reference; statuses and full data are retained.
   This zero-preserving multiplicative Dantzig experiment is separate from
   Spielman–Teng's additive-Gaussian, two-phase shadow-vertex theorem.
4. **Ellipsoid and barrier.** Eight finite 2D regions have exact boundedness and
   radius-six enclosure checks. Floating returned centres and determinant area
   ratios are numerical observations; exhausting the cut budget is not a general
   infeasibility certificate. A log-barrier path uses strict interiors and checked
   Newton/line-search convergence. All 36 approximate points have exact rational,
   residual-corrected objective upper bounds over a proven box. The ideal central
   gap `m/t` is retained separately. The short-step iteration theorem requires
   its own centrality assumptions and is not a guarantee for this schedule.
5. **Integrality.** Exact Bareiss determinants agree with independent Leibniz/GMP
   references. All 923 square minors of the small bipartite incidence matrix and
   19 of the triangle are checked. Partial minor searches return inconclusive.
   Integer right-hand sides and bounds are essential to TU integrality. All 201
   illustrated/measured matching LPs have exact primal/dual certificates; all 100
   bipartite values also agree with an independent integer matching solver.
   Fractional optimal vertices occur in 0 bipartite and 25 general samples.
   Seymour's regular-matroid decomposition is separate from exhaustive minors.
6. **Knapsack.** Exact fraction ratios and bounds avoid binary64 integer ties and
   nearly integral overweight answers. The eight-item example has optimum 174,
   root bound `6437/35`, and 24 processed nodes. All 41 integer optima agree with
   independent arbitrary-precision capacity DP. An executed two-item witness has
   weights `(10^12,1)`, capacity `10^12-1`, relaxation value `200-2/10^10`, and
   integer optimum 100; rounding its heavy fraction to one exceeds capacity by 2.
   The value-scaling teaching FPTAS removes overweight items before scaling and
   checks each guarantee exactly. Its reported `nV` is a work model, not allocated
   table memory; it is not the faster original Ibarra–Kim implementation.
7. **Covers.** All 101 vertex-cover optima agree with vectorized exhaustive masks;
   exact half-integral cover/fractional-matching dual certificates check the LPs.
   Feasible maximal-matching and rounded covers satisfy their factors. All 66
   set-cover optima agree with a separate subset-union DP, with full families and
   chosen sets retained. Empty and uncoverable domains are handled explicitly.
   Finite mean ratios and tie policies do not establish worst-case tightness.
8. **Metric TSP.** Complete symmetric metric assumptions support double tree's 2
   and Christofides–Serdyukov's 3/2 guarantees. All 42 small optima agree with a
   backward subset recurrence using floating Euclidean lengths. Forty-one full
   approximation cases also check tours, Kruskal MST and blossom matching weights.
   The teaching perfect matching itself uses exponential subset DP. Nearest-neighbour plus 2-opt inherits the logarithmic metric guarantee because
   it never lengthens the starting tour. Large 2-opt timings and sample means are
   finite observations. `0.7124 sqrt(n)` is a numerical
   asymptotic prediction for independent uniform planar points, not an optimum or
   gap certificate for one instance. General nonmetric hardness assumes `P != NP`.
9. **MAX-CUT.** All 31 exact graph optima have independent exhaustive references.
   Random cuts assign one side to each vertex, not independently to each edge.
   Rank-three pictured vectors and other locally optimized vector objectives are
   separate from exact rational dual upper bounds. Positive rational LDL pivots
   certify `Diag(lambda)-L/4` positive definite in the measured cases. A one-edge
   witness has local value about 0.138 below OPT 1, while the independent dual
   `lambda=(1/2,1/2)` has a positive-semidefinite square-form certificate and upper
   bound 1. Hyperplane expectation is at least `alpha F(V)` for fixed vectors;
   `alpha OPT` requires an optimal SDP or an explicit optimization-error allowance.
   Finite sample means do not prove the universal theorem.
10. **Online models.** Discrete ski rental charges before the purchase day. At
    `B=10` the exact randomized competitive ratio is
    `1/(1-(9/10)^10) = 1.5353399328`; `e/(e-1)` is the continuous/large-B limit.
    The season is fixed independently of the random buy day. Paging replays all
    155,266 Job **data** accesses, excluding instruction fetches, on 92 distinct
    64-byte lines in an initially empty, fully associative, unit-miss model. Every
    full-trace policy result and cyclic example has a separate list/future-queue
    reference. Offline next-use preprocessing is separate from online work.
    Marking's expected `2H_k` theorem uses oblivious requests and an additive
    initial term. A fixed cycle defeats LRU, not every deterministic policy; the
    general deterministic lower bound uses policy-adaptive requests.
11. **Multiplicative weights.** Stable log weights accumulate expected loss for
    losses in `[0,1]`. Every horizon retunes eta and agrees with an independent
    vectorized prefix-loss softmax calculation. Hoeffding gives
    `ln(n)/eta + eta*T/8`; chosen eta yields `sqrt(T*ln(n)/2)`. A sampled expert's
    realized regret needs a separate deviation statement. Every finite game row
    retains actual averaged row/column strategies and valid lower/upper bounds;
    a separate rational equilibrium certifies value `63/130`. Finite gaps do not
    claim exact convergence.
12. **Convex and frontier.** Stable log-sum-exp uses the analytic minimizer
    `(-log(2)/2,0)` and value `log(2 sqrt(2))-.1`, rather than Newton's last iterate
    as truth. The 40-versus-4 iteration result is specific to this moderately
    conditioned example and stopping threshold. Differentiable convex KKT includes
    primal feasibility; Slater is a sufficient regularity condition. Complexity
    requires representation, barrier/oracle, conditioning and accuracy assumptions.
    All 100 random bounded 3D polytopes plus the drawn example have exact positive
    normal certificates, numerical vertex/facet checks, Euler checks and independent
    all-source BFS diameters. Rejected draws are retained. These samples do not
    establish a diameter growth law or a high-dimensional Hirsch claim.

Selected research is dated and scoped: Spielman–Teng's actual perturbation model;
Cohen–Lee–Song (2019), whose full bound includes additional exponent and accuracy
terms; van den Brand's related deterministic bound; Chen et al. (2022) for exact
flow with polynomially bounded integral data; Karlin–Klein–Oveis Gharan (2021),
whose randomized metric-TSP algorithm is not run here; and Todd (2014), refining
the historical Kalai–Kleitman bound. PCP means an NP-witness encoding with
completeness/soundness and constant queries. Raghavendra's UGC-conditional theorem
concerns each fixed finite-domain CSP and its appropriate SDP rounding framework.
None of these citations is presented as a current-best survey.

Primary sources for the selected research checks:
[Spielman–Teng](https://arxiv.org/abs/cs/0111050),
[Cohen–Lee–Song](https://arxiv.org/abs/1810.07896),
[van den Brand](https://arxiv.org/abs/1910.11957),
[Chen et al.](https://arxiv.org/abs/2203.00671),
[Karlin–Klein–Oveis Gharan](https://arxiv.org/abs/2007.01409), and
[Todd](https://arxiv.org/abs/1402.3579).

## Build and verification

```bash
python -m videos.cs.cs23.compute
python -m unittest tests.test_cs23_optim -v
python tools/build.py cs23 -q l
python tools/build.py cs23
```

The source/preview checkpoint is recorded in
`docs/qa/computer-science-built-progress.md`. Sampled silent previews and automated
speech/alignment checks leave continuous audiovisual/listening review, Chinese
synthesized listening, whole-video native production review and final-pace runtime
approval as separate release gates. The Pebble exercise below is **not executed**.

## Six exercises, with worked solutions

1. **Duality.** Prove weak duality and complementary slackness for
   `max c^T x : Ax<=b, x>=0` and `min b^T y : A^T y>=c, y>=0`.

   For feasible x,y, `c^T x <= y^T Ax <= y^T b`. At an attained equal optimal pair,
   both inequalities are equalities. Therefore `y^T(b-Ax)=0` and
   `x^T(A^T y-c)=0`. Each summand is nonnegative, so each product vanishes.
   The chapter's primal `(2,0,1)` and dual `(1,0,1)` both give 13; primal slack
   `(0,1,0)` and reduced costs `(0,3,0)` satisfy these products. Check feasibility
   before interpreting an equal objective as a certificate.

2. **Half-integrality.** Show every vertex of the unbounded vertex-cover LP
   `{x>=0 : x_u+x_v>=1}` lies in `{0,1/2,1}^V`.

   If `x_v>1`, every edge incident to v has positive slack. Perturb x_v both ways
   by a sufficiently small amount; feasibility persists, so x is not a vertex.
   Thus every vertex already lies in the unit box; merely showing a box optimum
   exists would not prove the statement. Let `V+={v:1/2<x_v<1}` and
   `V-={v:0<x_v<1/2}`. If either is nonempty, perturb by
   `±epsilon(1_V+ - 1_V-)`. Every tight edge either joins 0 to 1, joins two halves,
   or joins V+ to V-, in which case changes cancel. Finitely many slack edges
   remain feasible for sufficiently small epsilon. This expresses x as a midpoint
   of distinct feasible points, a contradiction.

3. **Ski rental.** Prove the discrete deterministic optimum ratio `2-1/B`.

   Renting `B-1` days then buying costs d when `d<B`, and `2B-1` otherwise.
   A deterministic rule buys on a fixed day k if the season persists. End the
   season **on** day k: cost `k-1+B` versus `min(k,B)`. For `k<=B`, ratio is
   `1+(B-1)/k >= 2-1/B`; for `k>B` it is at least 2. Never buying has unbounded
   ratio. At B=1 the optimal action is immediate purchase, with ratio 1.
   This deterministic adversary must not be reused after observing a randomized
   buy day when claiming the oblivious-season randomized theorem.

4. **Hyperplane constant.** Minimize `r(theta)=theta/(1-cos(theta))` on `(0,pi]`.

   Its derivative has numerator `1-cos(theta)-theta*sin(theta)`. An interior
   stationary point obeys `tan(theta/2)=theta`. The derivative is negative near
   zero and positive near pi. The function `tan(theta/2)-theta` decreases then
   increases (its derivative crosses zero once), giving a unique positive root
   near 2.3311. Compare the endpoint and the limit at zero to obtain the minimum.
   Then `alpha=2*r(theta)/pi≈0.8786`. This scalar calculation proves the edgewise
   inequality, not global convergence of the local vector solver.

5. **Build: a bounded Pebble port.** Implement Bland simplex for **only the fixed
   3×3 integer LP in chapter one**, using reduced signed numerator/positive
   denominator pairs. Verify status, objective 13 and both feasibilities on the
   emulator before claiming the port works. Arbitrary matrices are outside scope.

   Guidance: append the identity slacks and b; initialize the objective row to
   `(-5,-4,-3,0,0,0,0)`. Bland bases are `(3,4,5)`, `(0,4,5)`, `(0,4,2)` using
   zero-based columns. The two pivots have values 2 and 1/2; the last objective
   row is `(0,3,0,1,0,1,13)`. Implement gcd normalization after every fraction
   operation, a positive denominator, signed comparisons by cross-products,
   minimum-index entering choice and Bland ratio ties. Report iteration limit
   separately, and reject input outside this fixed contract.

   Word proof for this path: inspect the initial, normalized-pivot and updated
   tableaux; stored reduced numerators have magnitude at most 25 and denominators
   at most 2. A multiply-then-subtract update has intermediate numerator bounded
   by `25^2*2+25*2^2=1350` and denominator at most `2^3=8`. A ratio comparison has
   cross-product magnitude at most `(25*2)^2=2500`. Division numerators and
   denominators are at most 50. Thus all these integer intermediates are below
   `2^12`, safely within Pebble's signed 32-bit words for this specified trace.
   This is a bounded design and reference trace, not a completed emulator run.

6. **Research-style finite study.** Generate bounded 3D polytopes from unit
   normals, certify boundedness before construction, and compare a fixed routing
   rule with independently computed shortest paths. Do not infer a general Hirsch
   result from random samples.

   Worked method: require four affinely independent normals with strictly positive
   rational barycentric weights summing to one and weighted sum zero. Their convex
   hull contains a neighbourhood of zero, so their inequalities bound every
   direction. Record rejected draws rather than treating solver failure as proof
   of unboundedness. Construct vertices numerically, record tolerances, check
   active facets, connectivity and Euler's relation, then run independent BFS
   from every vertex. Specify the routing rule before inspecting results; include
   trapped paths, ties and iteration limits in the report. Preserve normals,
   vertices, graph, seeds and path certificates. A polynomial graph diameter bound
   would still not by itself give an efficient improving simplex pivot rule.

## 中文要点与习题解答

本部分区分模型、可行解、最优证书、有限观测与历史定理。十五个生产器按实际
源码哈希使缓存失效，保留实例和独立核验；三次计时取最小值，生成与验证在计时
之外，生产器总耗时不是算法基准。精确整数或有理数证书与浮点构造有不同范围。

- LP 可行域一般是可能无界的凸多面体，本例有界且有六个顶点。单纯形从非负
  右端项的可行松弛基开始，没有第一阶段；预算耗尽不等于最优。弱对偶需要双方
  可行，有限最优下强对偶给相等目标。影子价格只在有效基区间内是局部边际值。
- Klee–Minty 使用明确的幂系数版本；乘性扰动 Dantzig 实验不同于影子顶点法的
  加性高斯平滑分析。椭球有限预算不是不可行证书；近似障碍点用残差修正有理数
  上界，不能直接套理想中心点的 m/t。
- TU 需要整数矩阵、整数右端项与界，部分子式检查只能未定。分数背包用精确
  比值与分支，避免几乎整数却超重的解；FPTAS 的 nV 是工作模型而非分配内存。
- 度量 TSP 的 Christofides 因子是二分之三；教学
  匹配用指数动态规划。根号 n 公式是均匀点的数值渐近预测，不是实例最优值。
- 最大割局部向量值不是认证上界；一般样本使用独立有理数对偶半正定证书。
  超平面期望至少为 alpha 倍自身目标，推出 alpha 倍整数最优还需全局优化或
  误差控制。有限样本均值不证明通用保证。
- B=10 滑雪租赁的离散比值约 1.53534，连续极限约 1.58198；季节独立于随机
  购买日。换页只重放数据访问，模型初始为空、全相联、单位缺失成本。固定循环
  不能证明所有确定性策略的下界；随机标记定理针对非自适应请求。
- 乘性权重计期望损失，每个时域重新选择 eta。博弈保留双方平均策略和有限
  上下界，另以有理数均衡认证值。凸 KKT 需要原始可行及正则条件，复杂度还要
  指定表示、预言机、精度与条件数。三维有限多面体样本不支持一般直径增长律。

六道习题的解答要点：

1. 对可行 x,y，有 `c^Tx<=y^TAx<=y^Tb`。最优目标相等迫使两个非负松弛内积
   都为零，进而每项互补乘积都为零。本例 `(2,0,1)` 与 `(1,0,1)` 都给 13。
2. 若原 LP 顶点的某坐标大于一，关联边均有松弛，可以双向微扰，所以不是
   顶点。再对大于半且小于一的坐标加 epsilon，对零与半之间的坐标减 epsilon，
   反向也做一次。紧边变化抵消，松弛边在足够小扰动下仍合法，故非半整数点不是顶点。
3. 租 B-1 天再买的最坏比值为 `2-1/B`。对购买日 k 的确定性策略，在购买当天
   结束季节，比较 `k-1+B` 与 `min(k,B)`；k<=B 得至少 `2-1/B`，k>B 得至少二。
   永不购买无界，B=1 立即购买。不能在看到随机购买日后再沿用此对手。
4. 求导 `theta/(1-cos theta)`，驻点满足 `tan(theta/2)=theta`。正根约 2.3311，
   比较边界与零端极限得最小值，算出 `alpha≈0.8786`；这不证明局部向量优化收敛。
5. 仅移植固定三乘三 LP。零基下标依次为 `(3,4,5)`、`(0,4,5)`、`(0,4,2)`，
   转轴值为二与二分之一，最终目标行 `(0,3,0,1,0,1,13)`。每个分数运算后约分，
   分母保持正，比较用交叉乘法并处理 Bland 平局。此路径约分后的分子绝对值至多
   25、分母至多二；更新中间分子至多 1350，比例比较交叉乘积至多 2500，均小于
   2 的十二次方，适合指定轨迹的有符号32位字。仍须在模拟器验证，未声称完成移植。
6. 有界三维多面体的四个法向量应仿射独立，且有严格正的有理数重心权重，使
   加权和为零。这样法向量凸包包含零的邻域，约束在所有方向有界。记录拒绝抽样、
   数值容差、活跃面、Euler 检查与所有顶点 BFS；预先指定路由规则并保留失败、
   平局和预算耗尽。保存输入与证书，有限成功不能解决多项式 Hirsch 猜想。

四项生产发布门仍单列：连续有声视听审查、中文合成语音听审、全片原生分辨率
审查，以及所选语速下的最终时长批准。
