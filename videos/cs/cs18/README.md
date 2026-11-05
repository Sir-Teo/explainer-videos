# Computer Science, Built — Part 18: Graphs

Part 18 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act IV, *Algorithms*. Euler invented the graph to walk the bridges
of Königsberg. This part explores graphs in the two basic ways and computes shortest paths, spanning trees, flows and
matchings. It proves why each method is right, measures it, and ends at the results of 2022–25. The instrument is
`explainer/cs/algo/graphs.py`: Hierholzer's circuit; breadth- and depth-first search with edge classes; Kahn's and
DFS topological order; Tarjan's and Kosaraju's components with 2-SAT; Dijkstra, bidirectional, A*, landmarks (ALT)
and contraction hierarchies; Bellman–Ford, Floyd–Warshall and Johnson; Kruskal, Prim and Borůvka; Edmonds–Karp;
Gale–Shapley and the Hungarian algorithm; Held–Karp; PageRank; greedy and backtracking colouring; and generators
for city grids and synthetic webs, every one counting its work. It is tested in `tests/test_cs18_graphs.py`. Every
number is computed in `compute.py`.

* **Seven bridges.** Königsberg in 1736; graphs as roads, the web, compilers and markets; what the part builds.
* **1. Euler's bridges, and how to store a graph.** Degrees 5, 3, 3, 3: no walk; the even-degree theorem, proved;
  Hierholzer's circuit; adjacency lists against a matrix, in bytes and time, from sparse to dense (1.5 million
  edges on 3,000 vertices, where the matrix wins).
* **2. Breadth-first search.** Layers; shortest paths by edge count in a 24 × 14 maze (67 layers, a 59-cell path);
  bipartiteness and the odd cycle that refutes it.
* **3. Depth-first search.** Discovery and finish times; the parenthesis theorem; tree, back, forward and cross
  edges; a back edge is a cycle; the white-path theorem.
* **4. Topological sort.** A build graph ordered by Kahn's queue and by DFS finish times; a cycle detected; DAGs in
  make, spreadsheets and Part 13's compiler.
* **5. Strongly connected components.** Tarjan's low-links; Kosaraju's two passes; the condensation is a DAG; a
  20,000-page synthetic web's bow-tie (a core of 7,583 pages); 2-SAT by implication graph.
* **6. Dijkstra's algorithm.** The café in Amsterdam (1956); the invariant, proved; the wavefront over a city of
  2,400 intersections and 4,360 roads; heaps, and O(m + n log n) with Fibonacci heaps.
* **7. Negative edges.** Why Dijkstra fails; Bellman–Ford and its V − 1 rounds; negative cycles; arbitrage as a
  negative cycle in −log rates (JPY → GBP → EUR, a gain of 0.5% on illustrative rates); distance-vector routing.
* **8. All pairs.** Floyd–Warshall as dynamic programming; Johnson's reweighting by potentials, proved (150
  vertices, 894 edges, 231 negative; every reweighted edge non-negative; both methods agree); the min-plus product
  and the APSP conjecture.
* **9. How a map answers in microseconds.** On 4,800 intersections, average vertices settled per query:
  Dijkstra 2,525, bidirectional 1,237, A* 657, landmarks 208, contraction hierarchies 113 (12,072 shortcuts, built
  in 13 s in Python).
* **10. Minimum spanning trees.** The cut and cycle properties, proved; Kruskal with Part 17's union–find, Prim,
  and Borůvka's 1926 algorithm for the Moravian grid (4 rounds); all three agree on 120 points.
* **11. Flows and cuts.** Augmenting paths and the residual graph; max flow 19 equals the cut 10 + 9; the
  max-flow min-cut theorem, proved; an unlucky choice of paths takes 2,000 augmentations where Edmonds–Karp
  takes 2.
* **12. Matching.** Bipartite matching as flow; Hall and Kőnig; Gale–Shapley, with stability proved, and the
  residency match; proposals against n Hₙ (531 at n = 100); the Hungarian algorithm (166 against greedy's 308).
* **13. Easy and hard.** Hamilton's icosian game (all 30 cycles of the dodecahedron); Euler against Hamilton;
  Held–Karp's O(2ⁿn²), timed (16 cities in about a second, each two more about six times slower), against
  an Euler circuit of 180,000 edges in a fraction of a second.
* **14. PageRank.** The random surfer; the stationary distribution; power iteration on 20,000 pages (52 rounds to
  10⁻¹²); rank against in-degree.
* **15. Planar graphs and four colours.** V − E + F = 2 (54 − 133 + 81); E ≤ 3V − 6 and K₅; Guthrie, Appel and
  Haken, Gonthier; the five-colour proof by Kempe chains; our map coloured greedily with 5, then with 4, and 3
  proved impossible.
* **16. Frontier: shortest paths and flows, now.** Dijkstra universally optimal (Haeupler, Hladík, Rozhoň, Tarjan
  and Tětek, 2024); the sorting barrier broken (Duan, Mao, Mao, Shu and Yin, 2025); negative weights in near-linear
  time (2022); max flow in almost-linear time (Chen, Kyng, Liu, Peng, Probst Gutenberg and Sachdeva, 2022); open
  problems. Outro.

## Build

```bash
python -m videos.cs.cs18.compute           # every number in the part (about a minute)
python tools/build.py cs18 -q l            # a 480p preview
python tools/build.py cs18                 # 1080p
```

## Problems, with solutions

1. **Euler circuits.** Prove that a connected graph in which every vertex has even degree has an Euler circuit, and
   that Hierholzer's algorithm finds one in O(E).

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
   w′(u, v) ≥ 0, so Dijkstra can then run from every vertex: O(VE + V(E + V log V)) in all.

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

5. **Build: Dijkstra on Pebble.** Implement Dijkstra's algorithm in the Pebble language with Part 17's binary heap
   (lazy deletion: push a new entry on every improvement and skip stale ones), run it on the 2,400-intersection
   city from chapter 6 on the emulator, and count instructions per relaxed edge.

   *Solution sketch.* Store the graph in compressed sparse rows: an offset array of n + 1 words and parallel
   arrays of targets and integer road lengths (scale the lengths by 1,000 and round). Keep `dist` and a heap of
   (distance, vertex) pairs in two parallel arrays, so a sift compares one word and moves two. The main loop pops
   the minimum and skips it if its distance exceeds `dist[u]`; otherwise it scans u's row, and on each improvement
   writes `dist[v]` and pushes. The emulator's counter then splits the instructions into three parts: the edge
   scans (a handful of instructions per edge, about 8,720 edges, both directions of 4,360 roads), the pushes (one
   per improvement, each a sift-up of at most lg of the heap size levels) and the pops (one per push, each a
   sift-down of about 2 lg n comparisons). On a grid each vertex is improved little more than once, so expect the
   pops to dominate, and expect tens of instructions per edge. Check the result by comparing every distance with
   `graphs.dijkstra` on the same scaled weights. Then measure the 4-ary heap the same way: fewer levels, more
   comparisons per level, and fewer instructions overall.

6. **★ Research: linear-time shortest paths.** Find single-source shortest paths on directed graphs with
   non-negative real weights in O(m) time in the comparison-addition model, or prove a lower bound that rules it
   out.

   *Where to start.* The baselines: Dijkstra (1959) with Fibonacci heaps (Fredman and Tarjan, 1987), O(m + n log n).
   That bound is optimal if the vertices must be output in sorted order, and universally optimal in that setting:
   Haeupler, Hladík, Rozhoň, Tarjan and Tětek, "Universal optimality of Dijkstra via beyond-worst-case heaps"
   (FOCS 2024). Without the sorting requirement: Duan, Mao, Mao, Shu and Yin, "Breaking the sorting barrier for
   directed single-source shortest paths" (STOC 2025), O(m log^{2/3} n). For undirected graphs: Thorup, "Undirected
   single-source shortest paths with positive integer weights in linear time" (1999), whose component hierarchy
   avoids sorting; Pettie and Ramachandran (2005) for real weights, undirected. For integer weights, directed:
   Thorup's O(m + n log log n) priority queue (2004). Open: (a) O(m) for directed real weights; (b) whether the
   log^{2/3} n factor can fall to any slowly growing function, such as log log n; (c) here, measure: implement the
   Duan et al. frontier-reduction step on the chapter 9 city and count how many vertices ever enter a sorted
   structure, against Dijkstra's 2,400.

## 习题与解答

1. **欧拉回路。** 证明：所有顶点度数都为偶数的连通图有欧拉回路，并且 Hierholzer 算法能在 O(E) 时间内找到它。

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
   运行 Dijkstra：总计 O(VE + V(E + V log V))。

4. **割性质。** 证明：对连通带权图的任一割，穿过它的最轻边属于某棵最小生成树；并由此推出 Kruskal 算法和 Prim 算法正确。

   *解答。* 设边集 A 包含在某棵最小生成树 T 中，割 (S, V − S) 不穿过 A 的任何边，e 是穿过它的最轻边。若 e ∈ T，结论成立。
   否则 T + e 含有一个经过 e 的圈，这个圈至少两次穿过割，所以含有另一条穿过割的边 f ∉ A。于是 T′ = T + e − f 是生成树，且
   w(e) ≤ w(f)，所以 w(T′) ≤ w(T)：T′ 是包含 A + e 的最小生成树。Prim 只长一棵树，每步加入穿过"这棵树与其余顶点"之割的最轻
   边。Kruskal 加入连接两个不同连通分量的最轻剩余边；它是穿过"其中一个分量与其余一切"之割的最轻边。归纳可知，两个算法
   加入的每条边都使 A 仍在某棵最小生成树之中，而它们结束时恰有 V − 1 条边，构成生成树，所以这棵树是最小的。

5. **动手：在 Pebble 上跑 Dijkstra。** 用 Pebble 语言和第 17 部分的二叉堆实现 Dijkstra 算法（惰性删除：每次改进都压入新
   条目，弹出时跳过过时的），在模拟器上对第 6 章有 2,400 个路口的城市运行，并统计每条松弛边的指令数。

   *解答提要。* 用压缩稀疏行存图：n + 1 个字的偏移数组，加上并列的目标数组和整数路长数组（路长乘以 1,000 后取整）。`dist` 和
   堆中的 (距离, 顶点) 对各用一个并列数组存放，这样一次下沉比较一个字、移动两个字。主循环弹出最小项，若其距离大于
   `dist[u]` 就跳过；否则扫描 u 的那一行，每次改进就写 `dist[v]` 并压堆。模拟器的计数器可把指令分成三部分：边的扫描（每条
   边几条指令，约 8,720 条边，即 4,360 条路的两个方向）、压堆（每次改进一次，每次上浮至多 lg（堆大小）层）和弹堆（每次压堆
   对应一次，每次下沉约 2 lg n 次比较）。在网格上每个顶点很少被改进超过一次，所以预计弹堆占大头，每条边几十条指令。把每个
   距离与 `graphs.dijkstra` 在同样缩放后的权上的结果比较，以检验正确性。然后用同样方法测量 4 叉堆：层数更少，每层比较更多，
   总指令更少。

6. **★ 研究题：线性时间最短路径。** 在比较–加法模型下，对非负实数权的有向图在 O(m) 时间内求单源最短路径，或证明一个排除
   这种可能的下界。

   *从哪里开始。* 基线：Dijkstra（1959）配 Fibonacci 堆（Fredman 与 Tarjan，1987），O(m + n log n)。如果顶点必须按排好的顺序
   输出，这个界是最优的，而且在该设定下是普适最优的：Haeupler、Hladík、Rozhoň、Tarjan 与 Tětek，"Universal optimality of
   Dijkstra via beyond-worst-case heaps"（FOCS 2024）。不要求排序时：Duan、Mao、Mao、Shu 与 Yin，"Breaking the sorting barrier
   for directed single-source shortest paths"（STOC 2025），O(m log^{2/3} n)。无向图：Thorup，"Undirected single-source
   shortest paths with positive integer weights in linear time"（1999），其分量层次结构避开了排序；Pettie 与 Ramachandran
   （2005）处理无向实数权。有向整数权：Thorup 的 O(m + n log log n) 优先队列（2004）。未解决：（a）有向实数权的 O(m)；
   （b）log^{2/3} n 因子能否降到任意缓慢增长的函数，例如 log log n；（c）在这里动手测量：在第 9 章的城市上实现 Duan 等人的
   前沿缩减步骤，统计有多少顶点进入过有序结构，与 Dijkstra 的 2,400 比较。

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

*Frontier.* Chen, Kyng, Liu, Peng, Probst Gutenberg & Sachdeva, "Maximum flow and minimum-cost flow in
almost-linear time" (FOCS 2022); Bernstein, Nanongkai & Wulff-Nilsen, "Negative-weight single-source shortest paths
in near-linear time" (FOCS 2022); Haeupler, Hladík, Rozhoň, Tarjan & Tětek, "Universal optimality of Dijkstra via
beyond-worst-case heaps" (FOCS 2024); Duan, Mao, Mao, Shu & Yin, "Breaking the sorting barrier for directed
single-source shortest paths" (STOC 2025); Williams, "Faster all-pairs shortest paths via circuit complexity"
(2014); Vassilevska Williams & Williams, "Subcubic equivalences between path, matrix, and triangle problems" (2010).
