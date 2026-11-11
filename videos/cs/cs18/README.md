# Computer Science, Built — Part 18: Graphs

Part 18 of the sixty-one-part course. The lesson connects proofs to checked outputs: a circuit with an edge
certificate, a shortest path with a settled-set invariant, a tree with an exchange argument, and a flow whose
value equals a cut. English and Chinese narration share canonical source pairs. Visual previews, speech-signal
checks and final listening/production approval have separate scopes.

The instrument is `explainer/cs/algo/graphs.py`; independent output checks and measurement protocols are in
`measurements.py`, producers in `compute.py`, and regressions in `tests/test_cs18_graphs.py`.

## What the chapters establish

- Euler circuits in undirected multigraphs, including parallel edges, twice-listed loops, empty/edgeless inputs
  and isolated vertices. Edge identifiers avoid reverse-list deletion. Non-isolated vertices must connect;
  validation and traversal take expected O(V + E) using hash tables.
- Adjacency-list and matrix models, BFS layers and odd-cycle witnesses, DFS intervals and edge classes,
  topological ordering, Tarjan/Kosaraju components, and two-SAT by comparing each literal's component with its negation.
- Nonnegative-weight Dijkstra, reachable negative-cycle detection, Floyd–Warshall, Johnson reweighting with a
  collision-free fresh vertex, and min-plus products. Bellman–Ford uses floating arithmetic and a 1e-12 relaxation
  tolerance; near-zero cycles require numerical care. Not every routine performs full input validation.
- Point-to-point routing with bidirectional search, A*, reusable landmark distances and contraction hierarchies.
  A* supports reopening for inconsistent admissible estimates with h(target) = 0. The city bounds are additionally
  checked consistent, so its expansion counts have no reopening. Panel dots are actual expansions, not parent-map keys.
- MST exchange arguments, with a **uniquely heaviest** cycle edge excluded from every MST; tied maxima need care.
  Edmonds–Karp residual cancellation, capacity/conservation certificates, and max-flow/min-cut equality.
- Unit-capacity matching, stable matching under strict complete balanced preferences, minimum-cost assignment,
  checked Bellman–Held–Karp subset DP, damped PageRank with dangling redistribution, and planar/Kempe-chain proofs.

## Measurements and model limits

Ten schema revisions replace ten of sixteen original payloads; the original data and media remain in the local
QA packet. Numerical producers verify complete outputs before reporting measurements. Cached-only QA rejects
old schemas before entering the upgrading loader.

| Experiment | What is actually observed | What the result does not establish |
| --- | --- | --- |
| Representation | Three complete scans of each fixed graph, minimum time; Python entry visits versus NumPy full boolean-row counts, both exactly 2E | A packed-bit benchmark or a cache-level causal explanation |
| Storage | Ideal eight-byte list entries/row references and packed bits; separately, reachable Python allocations and actual NumPy byte data | Process RSS, allocator peak or a claim that NumPy bool packs bits |
| All pairs | Same fixed potential-generated integer graph; all finite and unreachable pairs checked; three full runs per algorithm | A fallback graph with negative edges silently removed |
| Routing | Forty fixed queries; all five route distances checked; actual expansions, with both sides counted for bidirectional methods | Query latency, phone performance or continental scaling |
| Preprocessing | One hierarchy build and one reusable landmark-table build, stated separately | A repeated timing comparison or per-query preprocessing cost |
| Stable matching | Five uniform strict-preference trials per size, including stability checks at n = 1,000 | An exact finite expected proposal count of nH_n; that column is a scale reference |
| TSP / Euler | Three complete runs, minimum time; checked tour values and complete circuit edge multisets | A measured 50-city run; that number is an explicitly illustrative 2^n n² extrapolation |
| PageRank | Probability mass, successive L1 changes and a separately checked stationarity residual | A guarantee of human relevance or that all page orderings have stabilized |

On this retained run the dense 3,000-vertex graph has 1,500,000 undirected edges. Its ideal packed matrix is
1.125 MB, while the measured NumPy boolean data occupies 9 MB. The random flow network has **379 distinct
directed arcs after 400 attempted writes**, and its small example has certified flow/cut value 19. The routing
means are about 2,525 / 1,237 / 657 / 212 / 113 expansions for Dijkstra / bidirectional / straight-line A* /
landmarks / hierarchy, respectively. These are work counts on one synthetic graph.

For damping d = 0.85, dangling mass D is redistributed uniformly. The PageRank equation includes
`(1-d+dD)/n` plus linked incoming rank. Its plotted change C_k satisfies C_(k+1) ≤ d C_k. The dashed curve is
scaled from the first measured change. A final stationarity residual R bounds stationary-vector error by
R/(1-d); a small iterate change is a different quantity. The retained 20,000-page run takes 52 rounds.

Historical web percentages from Broder et al.'s May 1999 crawl are distinct from the synthetic generator,
whose outgoing-only component is empty. Fees, spreads and trade execution are omitted from the invented
arbitrage example. A cycle in an application graph alone is not evidence of fraud. Real routing, residency
matching and package managers add policies and constraints beyond these teaching models.

## Build and checks

```bash
python -m videos.cs.cs18.compute
python -m unittest tests.test_cs18_graphs -v
python tools/build.py cs18 -q l
python tools/build.py cs18
```

After a producer schema change, recompute its affected items explicitly with `--force`. A native master is not
approved by sampled previews; continuous audiovisual/listening review and Chinese synthesized-speech review
remain separate release gates.

## Problems, with solutions

1. **Euler circuits.** Prove that a connected graph in which every vertex has even degree has an Euler circuit, and
   that Hierholzer's algorithm finds one in O(V + E), including adjacency validation.

   *Solution.* Necessity first: a circuit leaves every vertex as often as it enters, so it uses an even number of
   edges at each vertex. For sufficiency, start anywhere and walk along unused edges. Each time the walk enters a
   vertex v ≠ start it has used an odd number of v's edges, so an unused one remains; the walk can therefore only
   get stuck at the start, and it closes a circuit C. If C misses edges, some vertex u on C has an unused edge,
   since the graph is connected. Every degree in the unused graph is still even, because C used an even number at
   each vertex. Walk from u in the unused edges to get a circuit C′ through u, and splice C′ into C at u. Repeat
   until no edge is unused. Hierholzer's algorithm does the splicing with a stack: push the current vertex; while
   the top has an unused edge, follow it and push; otherwise pop the top onto the output. Each edge is followed
   once and each vertex pushed and popped once per use, so with a pointer into each adjacency list the work is
   O(V + E).

2. **BFS.** Prove that breadth-first search dequeues vertices in non-decreasing order of distance from the source,
   and deduce that the BFS tree contains a shortest path to every reachable vertex.

   *Solution.* Claim: at every moment the queue holds vertices with labels d(v₁) ≤ d(v₂) ≤ … ≤ d(v_k) ≤ d(v₁) + 1.
   This holds initially (only s, label 0). Dequeuing v₁ keeps it. Each vertex enqueued while scanning v₁ gets
   label d(v₁) + 1, which is at least d(v_k) and at most d(v₂) + 1, since d(v₂) ≥ d(v₁). So labels leave the queue in
   non-decreasing order. Now show d(v) = δ(v), the true distance. The label is the length of a real path (the tree
   path), so d(v) ≥ δ(v). Suppose some vertex has d(v) > δ(v); take one with δ(v) smallest, and let u be its
   predecessor on a shortest path, so δ(u) = δ(v) − 1 = d(u). When u was dequeued, v was either undiscovered (then
   it gets d(u) + 1 = δ(v), a contradiction), or already in the queue or dequeued, with label at most d(u) + 1 by the
   claim, again a contradiction. So the tree path to every v has length δ(v).

3. **Negative edges and reweighting.** Show that Dijkstra's algorithm can fail with a single negative edge, and
   that Johnson's reweighting w′(u, v) = w(u, v) + p(u) − p(v) preserves every shortest path.

   *Solution.* Take edges s → a of weight 2, s → b of weight 3 and b → a of weight −2. Dijkstra settles a at
   distance 2 before b, and never revisits it, but s → b → a costs 1. For reweighting, take any path
   P = v₀ → v₁ → … → v_k. The p terms telescope: w′(P) = w(P) + p(v₀) − p(v_k). Every path from v₀ to v_k
   changes by the same constant, so the shortest ones stay shortest, and cycles keep their weight, so negative
   cycles stay negative. Johnson takes p(v) = δ(q, v), distances from a new vertex q joined to every vertex by a
   zero edge, computed by Bellman–Ford. The triangle inequality δ(q, v) ≤ δ(q, u) + w(u, v) is exactly
   w′(u, v) ≥ 0, so Dijkstra can then run from every vertex: O(VE + V(V + E) log(V + E)) in all.

4. **The cut property.** Prove that for any cut of a connected weighted graph, a lightest edge crossing it belongs to
   some minimum spanning tree, and deduce that Kruskal's and Prim's algorithms are correct.

   *Solution.* Let A be a set of edges contained in some MST T, let the cut (S, V − S) cross no edge of A, and let e
   be a lightest edge crossing it. If e ∈ T we are done. Otherwise T + e contains a cycle through e, and the cycle
   crosses the cut at least twice, so it contains another crossing edge f ∉ A. Then T′ = T + e − f is a spanning
   tree, and w(e) ≤ w(f), so w(T′) ≤ w(T): T′ is an MST containing A + e. Prim grows one tree, and at each step adds a
   lightest edge crossing the cut between that tree and the rest. Kruskal adds the lightest remaining edge that
   joins two different components; it is a lightest edge crossing the cut between one of those components and
   everything else. By induction, every edge either algorithm adds keeps A inside some MST, and it ends with
   V − 1 edges, a spanning tree, so the tree is minimum.

5. **Build: Dijkstra on Pebble.** Implement a lazy binary-heap query on the emulator, using a compressed
   sparse-row graph and precisely specified integer edge weights. Compare binary and four-ary heaps.

   *Solution protocol.* Scale each synthetic road weight by 1,000 and round once; the reference must use those
   same integers, not the original floats. Store row offsets, targets and weights, with capacities large enough
   for every adjacency entry and every lazy heap push. On popping an entry, skip it if its stored distance is
   stale. Count scans, pushes, pops, comparisons and retired instructions, and check every resulting distance
   against an independent shortest-path reference. Keep initialization inside or outside both timing windows
   consistently. A four-ary heap has fewer levels but compares more children per level; measure the resulting
   instructions instead of predicting which wins. Use multiple graph sizes and report raw repeated runs.

6. **★ Research: linear-time distance-only shortest paths.** Find directed nonnegative-real single-source
   distances in O(m + n) in the comparison-addition model, without requiring sorted output, or prove a lower
   bound that rules it out. On a reachable graph with m = Ω(n), this is the usual O(m) target.

   *Where to start.* Separate distance ordering from a distance vector. The 2024 universal-optimality theorem
   fixes a graph and compares worst-case arc lengths for the ordering task, using a specified working-set heap.
   The 2025 deterministic nonnegative-real result gives O(m log^(2/3) n). A 2026 improvement gives
   O(m sqrt(log n) + sqrt(m n log n log log n)), simplifying on sparse graphs to O(m sqrt(log n log log n)).
   Read the stated assumptions and proofs before implementing a frontier-reduction component; compare all
   distances, not only the number of vertices entering an ordered structure. Thorup's classical linear result
   uses undirected positive integer weights in a different machine model.

## 习题与解答

1. **欧拉回路。** 证明：所有顶点度数都为偶数的连通图有欧拉回路，并且 Hierholzer 算法能在 O(V + E) 时间（包含邻接校验）内找到它。

   *解答。* 先证必要性：回路离开每个顶点的次数等于进入的次数，所以在每个顶点用掉偶数条边。再证充分性：从任意顶点出发，
   沿未用过的边走。每次走进一个不是起点的顶点 v 时，v 的边已用掉奇数条，所以还剩一条没用；因此只可能在起点卡住，走出的
   是一条回路 C。如果 C 漏掉了边，由于图连通，C 上有某个顶点 u 还有未用的边。未用边构成的图中每个度数仍是偶数，因为 C 在每个
   顶点用掉偶数条。从 u 出发在未用边中走出一条过 u 的回路 C′，在 u 处把 C′ 接进 C。重复直到没有未用的边。Hierholzer 算法用
   一个栈完成拼接：把当前顶点压栈；栈顶还有未用边时，沿它走并压栈；否则把栈顶弹出到输出。每条边只走一次，每个顶点每用一次
   就压栈、出栈一次，所以给每个邻接表配一个指针，总工作量是 O(V + E)。

2. **广度优先搜索。** 证明广度优先搜索按到源点距离的非降顺序出队，并推出 BFS 树包含到每个可达顶点的最短路径。

   *解答。* 断言：任何时刻队列中的顶点标号满足 d(v₁) ≤ d(v₂) ≤ … ≤ d(v_k) ≤ d(v₁) + 1。开始时成立（只有 s，标号 0）。
   v₁ 出队后仍成立。扫描 v₁ 时入队的每个顶点标号为 d(v₁) + 1，它不小于 d(v_k)，且由于 d(v₂) ≥ d(v₁)，不大于 d(v₂) + 1。
   所以标号按非降顺序出队。再证 d(v) = δ(v)（真实距离）。标号是一条真实路径（树上路径）的长度，所以 d(v) ≥ δ(v)。假设有
   顶点 d(v) > δ(v)，取其中 δ(v) 最小的一个，设 u 是它某条最短路径上的前驱，则 δ(u) = δ(v) − 1 = d(u)。u 出队时，v 要么尚未
   发现（这时得到 d(u) + 1 = δ(v)，矛盾），要么已在队中或已出队，由断言其标号至多 d(u) + 1，同样矛盾。所以到每个 v 的树上
   路径长度都是 δ(v)。

3. **负边与重新赋权。** 说明一条负边就能让 Dijkstra 算法出错，并证明 Johnson 的重新赋权 w′(u, v) = w(u, v) + p(u) − p(v)
   保持所有最短路径不变。

   *解答。* 取边 s → a 权 2、s → b 权 3、b → a 权 −2。Dijkstra 在 b 之前以距离 2 定下 a，之后不再回头，但 s → b → a 只要 1。
   关于重新赋权，任取路径 P = v₀ → v₁ → … → v_k，p 项逐项相消：w′(P) = w(P) + p(v₀) − p(v_k)。从 v₀ 到 v_k 的每条路径都改变同一个
   常数，所以最短的仍是最短的；回路的权不变，所以负回路仍是负的。Johnson 取 p(v) = δ(q, v)，即从一个新顶点 q（用零权边连到
   每个顶点）出发、由 Bellman–Ford 算出的距离。三角不等式 δ(q, v) ≤ δ(q, u) + w(u, v) 正好就是 w′(u, v) ≥ 0，于是可以从每个顶点
   运行 Dijkstra：总计 O(VE + V(V + E) log(V + E))。

4. **割性质。** 证明：对连通带权图的任一割，穿过它的最轻边属于某棵最小生成树；并由此推出 Kruskal 算法和 Prim 算法正确。

   *解答。* 设边集 A 包含在某棵最小生成树 T 中，割 (S, V − S) 不穿过 A 的任何边，e 是穿过它的最轻边。若 e ∈ T，结论成立。
   否则 T + e 含有一个经过 e 的圈，这个圈至少两次穿过割，所以含有另一条穿过割的边 f ∉ A。于是 T′ = T + e − f 是生成树，且
   w(e) ≤ w(f)，所以 w(T′) ≤ w(T)：T′ 是包含 A + e 的最小生成树。Prim 只长一棵树，每步加入穿过"这棵树与其余顶点"之割的最轻
   边。Kruskal 加入连接两个不同连通分量的最轻剩余边；它是穿过"其中一个分量与其余一切"之割的最轻边。归纳可知，两个算法
   加入的每条边都使 A 仍在某棵最小生成树之中，而它们结束时恰有 V − 1 条边，构成生成树，所以这棵树是最小的。

5. **动手：在 Pebble 上跑迪杰斯特拉。** 用压缩稀疏行存图，在模拟器上实现惰性二叉堆查询，并比较二叉堆和四叉堆。

   *解答方案。* 把每条合成道路权值乘一千后只取整一次，参考算法必须使用完全相同的整数，而非原浮点权值。
   为全部邻接条目及所有惰性堆插入准备足够容量。弹出时，若存储距离已过期就跳过。分别数扫描、压入、弹出、比较和退休指令，
   并把每个结果距离与独立参考比较。两种实现的计时窗口必须一致地包含或排除初始化。四叉堆层数较少，但每层比较更多子节点；
   要测量指令数，而不是预言谁会赢。使用多个图规模，保存重复运行的原始结果。

6. **★ 研究题：只求距离的线性时间最短路径。** 在比较加法模型中，以 O(m+n) 时间求非负实数权有向单源距离，
   不要求按距离排序输出，或证明排除这一算法的下界。在 m=Ω(n) 的可达图中，这就是通常的 O(m) 目标。

   *起点。* 区分距离顺序与距离向量。2024年的普适最优性定理固定图、比较最坏弧长，针对排序任务并使用特定工作集堆。
   2025年的确定性非负实数权结果为 O(m log^(2/3)n)。2026年的改进为
   O(m sqrt(log n)+sqrt(mn log n log log n))，稀疏图可简化为 O(m sqrt(log n log log n))。
   实现前沿缩减的一个环节前，应先阅读明确假设和证明；比较全部距离，而不只统计进入有序结构的顶点数。
   索鲁普经典的线性结果针对另一机器模型中的无向正整数权图。

## Glossary additions

图 graph · 顶点 vertex · 边 edge · 度 degree · 欧拉回路 Euler circuit · 邻接表 adjacency list · 邻接矩阵 adjacency matrix ·
广度优先搜索 breadth-first search · 二分图 bipartite graph · 深度优先搜索 depth-first search · 括号定理 parenthesis theorem ·
树边 tree edge · 回边 back edge · 前向边 forward edge · 横叉边 cross edge · 白色路径定理 white-path theorem · 有向无环图
directed acyclic graph · 拓扑排序 topological sort · 强连通分量 strongly connected component · 缩点图 condensation · 低链
low-link · 蝴蝶结结构 bow-tie structure · 2-可满足性 2-SAT · 单源最短路径 single-source shortest paths · 松弛 relaxation ·
负回路 negative cycle · 套利 arbitrage · 全源最短路径 all-pairs shortest paths · 重新赋权 reweighting · 势函数 potential ·
最小加乘积 min-plus product · 双向搜索 bidirectional search · 可采纳启发式 admissible heuristic · 地标 landmarks · 收缩层次
contraction hierarchies · 捷径边 shortcut · 最小生成树 minimum spanning tree · 割性质 cut property · 圈性质 cycle property ·
流网络 flow network · 容量 capacity · 增广路径 augmenting path · 残量图 residual graph · 最大流最小割定理 max-flow min-cut
theorem · 推送–重标记 push–relabel · 二分匹配 bipartite matching · 稳定匹配 stable matching · 指派问题 assignment problem ·
匈牙利算法 Hungarian algorithm · 哈密顿回路 Hamiltonian cycle · 旅行商问题 travelling salesman problem · 随机冲浪者 random
surfer · 平稳分布 stationary distribution · 幂迭代 power iteration · 平面图 planar graph · 四色定理 four colour theorem · 肯普链
Kempe chain · 普适最优 universal optimality

## Selected primary research sources

These are dated model statements checked for this lesson, not an exhaustive literature review or a full proof
audit. None of the new theoretical algorithms is implemented by the city benchmark.

- [Haeupler et al., universal optimality, 2024](https://arxiv.org/abs/2311.11793v4): distance ordering on a fixed
  graph against worst-case arc lengths, with the specified working-set heap; do not transfer the claim to an ordinary heap or every output task.
- [Duan, Jiayi Mao, Xiao Mao, Shu and Yin, 2025](https://arxiv.org/abs/2504.17033v2): deterministic directed
  nonnegative-real distance computation in the comparison-addition model, O(m log^(2/3)n).
- [Duan, Xiao Mao, Shu and Yin, 2026](https://arxiv.org/abs/2602.07868v2), with the
  [official ICALP 2026 publication](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2026.81): the improved directed bound above.
- [Bernstein, Nanongkai and Wulff-Nilsen, 2022](https://arxiv.org/abs/2203.03456v6): randomized negative-**integer**
  SSSP with O(m log^8 n log W) dependence; not arbitrary-real negative weights at the same cost.
- [Chen et al., 2022](https://arxiv.org/abs/2203.00671v2): exact directed maximum/minimum-cost flow with
  polynomially bounded integral capacities, costs and demands, in m^(1+o(1)) time in its setting. The dynamic
  minimum-ratio-cycle update guarantee is amortized and subpolynomial; practical constants and arbitrary-real inputs are separate questions.
- [Björklund, undirected Hamiltonicity, 2010](https://arxiv.org/abs/1008.0541): a randomized O*(1.657^n)
  decision algorithm, distinct from general weighted TSP. [Dallant and Kozma, 2026](https://arxiv.org/abs/2604.05645)
  improve TSP space-time tradeoffs; classical general-weight time O*((2-ε)^n) for fixed ε>0 is the question stated here.
- [Broder et al., historical web structure](https://www.math.cmu.edu/~af1p/Teaching/INFONET/Papers/PowerLaw/GSW.html):
  the historical crawl, not the synthetic generator's measurements.

The classical bibliography follows below; newer research bounds do not retroactively change the scope of the
implemented algorithms or the recorded experiments.

## Sources

*Canon.* Books: Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms*, chapters 20–26; Kleinberg & Tardos,
*Algorithm Design*, chapters 3, 4 and 7; Tarjan, *Data Structures and Network Algorithms* (1983); Even, *Graph
Algorithms*; Ahuja, Magnanti & Orlin, *Network Flows* (1993); Schrijver, *Combinatorial Optimization* (2003);
Wilson, *Four Colors Suffice* (2002).

Papers: Euler, "Solutio problematis ad geometriam situs pertinentis" (1736); Hierholzer (1873); Kempe (1879);
Heawood, "Map-colour theorem" (1890); Borůvka (1926); Kőnig (1931); Hall, "On representatives of subsets" (1935);
Kuhn, "The Hungarian method for the assignment problem" (1955); Kruskal (1956); Ford & Fulkerson, "Maximal flow
through a network" (1956); Elias, Feinstein & Shannon (1956); Prim (1957); Bellman, "On a routing problem" (1958);
Moore, "The shortest path through a maze" (1959); Dijkstra, "A note on two problems in connexion with graphs"
(1959); Floyd, "Algorithm 97" (1962); Warshall (1962); Held & Karp (1962); Kahn (1962); Gale & Shapley, "College
admissions and the stability of marriage" (1962); Hart, Nilsson & Raphael (1968); Edmonds & Karp (1972); Tarjan,
"Depth-first search and linear graph algorithms" (1972); Karp, "Reducibility among combinatorial problems" (1972);
Appel & Haken (1976); Johnson (1977); Sharir (1981); Aspvall, Plass & Tarjan (1979); Fredman & Tarjan (1987);
Goldberg & Tarjan (1988); Karger, Klein & Tarjan (1995); Robertson, Sanders, Seymour & Thomas (1996); Goldberg &
Rao (1998); Page, Brin, Motwani & Winograd, "The PageRank citation ranking" (1998); Brin & Page (1998); Roth &
Peranson (1999); Thorup (1999); Broder et al., "Graph structure in the web" (2000); Goldberg & Harrelson, "Computing
the shortest path: A* search meets graph theory" (2005); Gonthier, "A computer-checked proof of the four colour
theorem" (2005); Geisberger, Sanders, Schultes & Delling, "Contraction hierarchies" (2008); Bast et al., "Route
planning in transportation networks" (2016).
