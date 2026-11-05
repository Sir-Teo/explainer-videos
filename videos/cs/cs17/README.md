# Computer Science, Built — Part 17: Data Structures

Part 17 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act IV, *Algorithms*. The Job is a dictionary problem: insert a
word, find it, add one. This part builds the structures that answer it, proves what they cost, measures them, and
gives the ledger its eighth row. The instruments are `explainer/cs/algo/ds.py` (universal hashing, chaining, linear
probing, double hashing, uniform probing, Robin Hood, cuckoo and FKS perfect hashing; plain, AVL, left-leaning
red–black, treap, splay and persistent search trees, skip lists and B-trees; binary, pairing and Fibonacci heaps
with Dijkstra's algorithm; union–find; tries, radix trees and a rank directory, every one counting its work) and
`explainer/cs/algo/job2.py` (the Job v2, a hash table in the Pebble language, with an exact model of its
instruction count and a C program that counts the same events on all thirty novels), tested in
`tests/test_cs17_ds.py`. Every number is computed in `compute.py`; `cache` and `practice` time code on this
machine, and `job` runs the corpus through Part 9's caches.

* **Can counting be constant-time?** Ledger row 7; what the Job really needs: 4.6 million finds and 57,895 inserts.
* **1. The dictionary, and the birthday bound.** One interface, four implementations; Luhn's hashing (1953); the
  birthday bound derived and drawn; collisions on our vocabulary (101 full-hash pairs predicted 100; 12,495 slot
  pairs predicted 12,786).
* **2. Chaining and universal hashing.** Chains against Poisson; Carter and Wegman's family, proved and checked; a
  flooding attack on a fixed hash (2,000,000 probes against 2,000); Klink and Wälde (2011), SipHash.
* **3. Open addressing.** Linear probing and its clusters; Knuth's formulas (1963) against measurement; double
  hashing; Robin Hood hashing's variance; Swiss tables.
* **4. Cuckoo hashing and perfect hashing.** Two probes per lookup; the failure threshold at load ½ and the
  cuckoo graph; FKS perfect hashing in about three slots per key.
* **5. Binary search trees.** Search and order; random trees' depth 2(1 + 1/n)Hₙ − 4, measured; sorted input; the
  bijection with quicksort (24,944 comparisons both ways).
* **6. Balanced trees: AVL and red–black.** Rotations; AVL and Fibonacci trees (h < 1.4405 lg(n + 2)); red–black
  trees as 2–3–4 trees; heights and rotations measured.
* **7. Treaps and skip lists.** Random priorities give a random tree for any input; skip lists' 2 lg n search.
* **8. Splay trees.** Zig, zig-zig, zig-zag; the access lemma by potential; static optimality; splay against AVL on
  four access sequences; dynamic optimality.
* **9. B-trees.** Wide nodes; splitting at the root; heights for five fan-outs; a billion keys in four levels.
* **10. Priority queues.** Binary, binomial, Fibonacci and pairing heaps; cascading cuts; Dijkstra with each heap,
  counted; why the Fibonacci heap loses in practice.
* **11. Union–find.** The forest; union by rank; path compression; 2,312 steps per find against 1.0; Ackermann's
  function and α(n) ≤ 4; log*.
* **12. Tries and succinct structures.** A trie of the vocabulary (154,595 nodes for 452,668 letters; a radix tree
  of 70,968); rank and select in O(1) with a 20% directory; LOUDS.
* **13. Persistence, and the memory hierarchy.** Path copying (21 nodes per version at n = 100,000); lookups timed
  on this machine from a thousand keys to ten million (red–black tree 2.3 µs, sorted array 0.33 µs, chaining
  74 ns, open addressing 31 ns).
* **14. Hash tables in practice.** Python, Java, C++, Rust and Go; the Job natively (Python 0.91 s, C++
  `unordered_map` 0.19 s, open addressing in C 0.11 s).
* **15. The Job, hashed.** The Job v2; the corpus counted exactly (1.06 slots per word); an exact 27-event
  instruction model (0.01% on held-out passages); where the time goes; the corpus through Part 9's caches (6%
  added); ledger row 8 (0.81 s: 6.3× row 7, 72× row 5, 15× four cores); hardware's 24× against algorithms' 72×.
* **16. Frontier: how good can a data structure be?** Yao's conjecture refuted (Farach-Colton, Krapivin and
  Kuszmaul, 2025); dynamic optimality and tango trees; cell-probe lower bounds; learned indexes; open problems.
  Outro.

## Build

```bash
python -m videos.cs.cs17.compute           # every number in the part (about ten minutes)
python tools/build.py cs17 -q l            # a 480p preview
python tools/build.py cs17                 # 1080p
```

## Problems, with solutions

1. **Universal hashing.** Prove that h_{a,b}(x) = ((ax + b) mod p) mod m, with a uniform in {1, …, p − 1} and b
   uniform in {0, …, p − 1}, p prime and keys below p, satisfies Pr[h(x) = h(y)] ≤ 1/m for x ≠ y.

   *Solution.* Let r = (ax + b) mod p and s = (ay + b) mod p. Then r − s ≡ a(x − y) (mod p), which is nonzero
   because p is prime and neither a nor x − y is divisible by p; so r ≠ s. Conversely, each pair r ≠ s comes from
   exactly one (a, b): a = (r − s)(x − y)⁻¹ mod p and b = (r − ax) mod p. So (a, b) ↦ (r, s) is a bijection from the
   p(p − 1) choices onto the p(p − 1) ordered pairs of distinct residues, and (r, s) is uniform over them. For each
   r, the values s ≠ r with s ≡ r (mod m) number at most ⌈p/m⌉ − 1 ≤ (p − 1)/m. Hence Pr[h(x) = h(y)] ≤
   p · ((p − 1)/m) / (p(p − 1)) = 1/m.

2. **Linear probing.** From the insertion cost U(α) = ½(1 + 1/(1 − α)²), derive the successful-search cost
   S(α) = ½(1 + 1/(1 − α)).

   *Solution.* A key is found by retracing the probes of its insertion, so finding the key inserted when the load
   was x costs U(x). Averaging over the keys, inserted as the load rose from 0 to α:
   S(α) = (1/α) ∫₀^α U(x) dx = (1/2α) [x + 1/(1 − x)]₀^α = (1/2α)(α + 1/(1 − α) − 1) = (1/2α)(α + α/(1 − α))
   = ½(1 + 1/(1 − α)). (Knuth's 1963 derivation of U is the hard part; it counts the ways clusters form.)

3. **Union by rank.** Show that union by rank keeps every tree's height at most lg n, and that unions without it
   can build a tree of height n − 1.

   *Solution.* Claim: a root of rank r has at least 2^r nodes. A new node has rank 0 and 1 node. Ranks change only
   when two roots of equal rank r are joined; the result has rank r + 1 and at least 2^r + 2^r = 2^{r+1} nodes. A
   node's rank bounds its tree's height (height rises only in the same event), so n ≥ 2^h and h ≤ lg n. Without
   ranks, union(1, 0), union(2, 1), …, linking each time the old tree's root under the new singleton, builds the
   path n − 1, …, 0, of height n − 1; a find on node 0 then walks n − 1 parents (the `chain` case in `compute.py`).

4. **AVL height.** Prove that an AVL tree with n nodes has height h < 1.4405 lg(n + 2).

   *Solution.* Let N(h) be the fewest nodes in an AVL tree of height h. Its root's subtrees have heights h − 1 and
   (at least) h − 2, each minimal: N(h) = N(h − 1) + N(h − 2) + 1, with N(1) = 1 and N(2) = 2. Then N(h) + 1 satisfies
   the Fibonacci recurrence with N(1) + 1 = 2 = F₃ and N(2) + 1 = 3 = F₄, so N(h) = F_{h+2} − 1. Since
   F_k > φ^k/√5 − 1, we get n + 2 ≥ N(h) + 2 = F_{h+2} + 1 > φ^{h+2}/√5, so h + 2 < log_φ(√5 (n + 2)), that is
   h < log_φ(n + 2) + log_φ √5 − 2 = 1.4405 lg(n + 2) − 0.3277.

5. **Build: a hash without a division per letter.** Rewrite the Job v2 so that it divides once per word instead of
   once per letter, in the Pebble language, and measure its instructions per cycle and its ledger row on Part 8's
   core.

   *Solution sketch.* Pebble's divider is unpipelined and takes 16 cycles, and the v2 hash puts a division on the
   critical path of every letter (19.4 million of them on the corpus). Let the hash wrap instead: h = 31h + c with
   32-bit arithmetic (one multiply per letter, which the core pipelines), and at the end of the word make it
   non-negative (one h % P, adding P if the remainder is negative) and reduce it modulo the table size once: two divisions per word, 9.2
   million instead of 24 million. Add the new events (wraps that went negative) to `features` and `FEATURES_C`, refit the
   model as in `compute_job`, and price it with `core`. Expect the instruction count to fall a little and the IPC
   to rise from 1.43 towards the sort's 2.24; report the new seconds, and check that the slot distribution is still
   good (count probes per word, as in chapter 15).

6. **★ Research: dynamic optimality.** Prove that splay trees are dynamically optimal (within O(1) of the best
   binary-search-tree algorithm on every access sequence), or give any BST algorithm that is o(log log n)-competitive.

   *Where to start.* The conjecture: Sleator and Tarjan, "Self-adjusting binary search trees" (1985). Lower bounds
   on the optimum: Wilber (1989), the interleave and funnel bounds; Lecomte and Weinstein (2020) relate them.
   O(log log n)-competitive trees: tango trees (Demaine, Harmon, Iacono and Pătraşcu, 2004), multi-splay trees
   (Wang, Derryberry and Sleator, 2006). The geometric view: Demaine, Harmon, Iacono, Kane and Pătraşcu, "The
   geometry of binary search trees" (2009), with the Greedy algorithm (Lucas 1988, Munro 2000) as the other
   candidate. Surveys: Iacono, "In pursuit of the dynamic optimality conjecture" (2013); Levy and Tarjan (2019).
   Open: (a) any O(1)-competitive BST, splay or Greedy or another; (b) whether Wilber's funnel bound is within a
   constant of the optimum; (c) here, measure: compare splay, Greedy (simulated geometrically) and an offline
   optimum on small n by search, and look for a sequence where the ratio grows.

## 习题与解答

1. **全域哈希。** 证明 h_{a,b}(x) = ((ax + b) mod p) mod m（a 在 {1, …, p − 1} 中均匀，b 在 {0, …, p − 1} 中均匀，p 为
   素数，键小于 p）对 x ≠ y 满足 Pr[h(x) = h(y)] ≤ 1/m。

   *解答。* 令 r = (ax + b) mod p，s = (ay + b) mod p。则 r − s ≡ a(x − y)（mod p），由于 p 是素数而 a 与 x − y 都不被
   p 整除，它不为零，所以 r ≠ s。反过来，每一对 r ≠ s 恰好来自一个 (a, b)：a = (r − s)(x − y)⁻¹ mod p，b = (r − ax)
   mod p。所以 (a, b) ↦ (r, s) 是从 p(p − 1) 种选择到 p(p − 1) 个不同剩余有序对的双射，(r, s) 在其上均匀分布。对每个
   r，满足 s ≠ r 且 s ≡ r（mod m）的 s 至多 ⌈p/m⌉ − 1 ≤ (p − 1)/m 个。故 Pr[h(x) = h(y)] ≤ p · ((p − 1)/m) /
   (p(p − 1)) = 1/m。

2. **线性探查。** 由插入代价 U(α) = ½(1 + 1/(1 − α)²) 推出成功查找的代价 S(α) = ½(1 + 1/(1 − α))。

   *解答。* 找到一个键就是重走它插入时的探查，所以找到在装填率为 x 时插入的键要花 U(x)。对装填率从 0 升到 α 时插入的所有
   键取平均：S(α) = (1/α) ∫₀^α U(x) dx = (1/2α) [x + 1/(1 − x)]₀^α = (1/2α)(α + 1/(1 − α) − 1) = (1/2α)(α + α/(1 − α))
   = ½(1 + 1/(1 − α))。（高德纳1963年推导 U 才是难的部分；它要数簇的各种形成方式。）

3. **按秩合并。** 证明按秩合并使每棵树的高度至多为 lg n，并证明不用它的合并能造出高度为 n − 1 的树。

   *解答。* 断言：秩为 r 的根至少有 2^r 个结点。新结点秩为 0、有 1 个结点。秩只在两个秩同为 r 的根合并时改变，结果秩为
   r + 1，至少有 2^r + 2^r = 2^{r+1} 个结点。结点的秩是其树高的上界（树高只在同一事件中增加），所以 n ≥ 2^h，h ≤ lg n。
   不用秩时，依次 union(1, 0)、union(2, 1)……，每次把旧树的根挂到新的单点下，就造出路径 n − 1, …, 0，高度为 n − 1；
   对结点 0 做一次查找要走 n − 1 个父指针（`compute.py` 中的 `chain` 情形）。

4. **AVL 树的高度。** 证明有 n 个结点的 AVL 树高度 h < 1.4405 lg(n + 2)。

   *解答。* 设 N(h) 是高度为 h 的 AVL 树最少的结点数。它的根的两棵子树高度为 h − 1 和（至少）h − 2，且各自最少：
   N(h) = N(h − 1) + N(h − 2) + 1，N(1) = 1，N(2) = 2。于是 N(h) + 1 满足斐波那契递推，N(1) + 1 = 2 = F₃，N(2) + 1 =
   3 = F₄，所以 N(h) = F_{h+2} − 1。由 F_k > φ^k/√5 − 1 得 n + 2 ≥ N(h) + 2 = F_{h+2} + 1 > φ^{h+2}/√5，故
   h + 2 < log_φ(√5 (n + 2))，即 h < log_φ(n + 2) + log_φ √5 − 2 = 1.4405 lg(n + 2) − 0.3277。

5. **动手：每个字母不做除法的哈希。** 用 Pebble 语言把任务 v2 改写成每个单词只做一次除法而不是每个字母一次，并在第8部分
   的核心上测量它的每周期指令数和账本行。

   *解答要点。* Pebble 的除法器不流水、要 16 个周期，而 v2 的哈希在每个字母的关键路径上都放了一次除法（语料上共
   1940 万个字母）。改为让哈希回绕：用 32 位算术 h = 31h + c（每个字母一次乘法，核心可以流水），在单词结束时把它变成
   非负（做一次 h % P，余数为负就加上 P），再对表大小取一次模：每个单词两次除法，共 920 万次，而不是 2400 万次。把新事件（变负的回绕）
   加进 `features` 和 `FEATURES_C`，像 `compute_job` 那样重新拟合模型，再用 `core` 定价。预计指令数略降，IPC 从 1.43
   向排序的 2.24 靠近；报告新的秒数，并检查槽位分布仍然良好（像第15章那样数每个单词的探查数）。

6. **★ 研究：动态最优性。** 证明伸展树是动态最优的（在每个访问序列上与最好的二叉搜索树算法相差 O(1) 倍以内），或者给出
   任何一个 o(log log n) 竞争比的 BST 算法。

   *从哪里开始。* 猜想：斯莱特与塔扬，《自调整二叉搜索树》（1985）。最优值的下界：威尔伯（1989）的交错界与漏斗界；
   勒孔特与温斯坦（2020）理清了二者的关系。O(log log n) 竞争比的树：探戈树（德迈纳、哈蒙、亚科诺与珀特拉什库，2004），
   多重伸展树（王、德里贝里与斯莱特，2006）。几何观点：德迈纳、哈蒙、亚科诺、凯恩与珀特拉什库，《二叉搜索树的几何》
   （2009），以 Greedy 算法（卢卡斯 1988，芒罗 2000）作为另一个候选。综述：亚科诺，《追寻动态最优性猜想》（2013）；
   列维与塔扬（2019）。尚未解决的：（a）任何 O(1) 竞争比的 BST，无论伸展树、Greedy 还是别的；（b）威尔伯的漏斗界是否
   与最优值相差常数倍以内；（c）在这里动手测量：对小的 n，用搜索比较伸展树、Greedy（用几何方式模拟）与离线最优，
   寻找比值增长的序列。

## Glossary additions

字典 dictionary · 抽象数据类型 abstract data type · 哈希 hashing · 哈希函数 hash function · 冲突 collision · 生日界
birthday bound · 装填因子 load factor · 链地址法 chaining · 全域哈希 universal hashing · 哈希洪水攻击 hash flooding ·
带密钥的哈希 keyed hash · 开放寻址 open addressing · 线性探查 linear probing · 一次聚集 primary clustering · 双重哈希
double hashing · 均匀探查 uniform probing · 罗宾汉哈希 Robin Hood hashing · 布谷鸟哈希 cuckoo hashing · 完美哈希
perfect hashing · 二叉搜索树 binary search tree · 旋转 rotation · AVL 树 AVL tree · 斐波那契树 Fibonacci tree · 红黑树
red–black tree · 2–3–4 树 2–3–4 tree · 树堆 treap · 跳表 skip list · 伸展树 splay tree · 访问引理 access lemma · 静态
最优性 static optimality · 动态最优性 dynamic optimality · B 树 B-tree · 扇出 fan-out · 优先队列 priority queue · 减小键
decrease-key · 二项堆 binomial heap · 斐波那契堆 Fibonacci heap · 级联切断 cascading cut · 配对堆 pairing heap · 并查集
union–find · 按秩合并 union by rank · 路径压缩 path compression · 阿克曼函数 Ackermann's function · 迭代对数 iterated
logarithm · 字典树 trie · 基数树 radix tree · 简洁数据结构 succinct data structure · 秩与选择 rank and select · 持久化
persistence · 路径复制 path copying · 学习型索引 learned index

## Sources

*Canon.* Books: Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms*, chapters 10–13, 18–19, 21; Knuth,
*The Art of Computer Programming*, volume 3, chapter 6; Sedgewick & Wayne, *Algorithms*, chapter 3; Tarjan, *Data
Structures and Network Algorithms* (1983); Mehlhorn & Sanders, *Algorithms and Data Structures*; Okasaki, *Purely
Functional Data Structures* (1998); Navarro, *Compact Data Structures* (2016).

Papers: Luhn's IBM memorandum (1953); Knuth, "Notes on 'open' addressing" (1963); Adelson-Velsky & Landis (1962);
Galler & Fischer (1964); Bayer & McCreight, "Organization and maintenance of large ordered indices" (1970); Hopcroft
& Ullman (1973); Liskov & Zilles, "Programming with abstract data types" (1974); Tarjan, "Efficiency of a good but
not linear set union algorithm" (1975); Vuillemin (1978); Guibas & Sedgewick, "A dichromatic framework for balanced
trees" (1978); Carter & Wegman, "Universal classes of hash functions" (1979); Gonnet (1981); Fredman, Komlós &
Szemerédi, "Storing a sparse table with O(1) worst case access time" (1984); Sleator & Tarjan, "Self-adjusting
binary search trees" (1985); Yao, "Uniform hashing is optimal" (1985); Celis, *Robin Hood Hashing* (1986); Fredman,
Sedgewick, Sleator & Tarjan, pairing heaps (1986); Fredman & Tarjan, "Fibonacci heaps" (1987); Jacobson,
"Space-efficient static trees and graphs" (1989); Driscoll, Sarnak, Sleator & Tarjan, "Making data structures
persistent" (1989); Fredman & Saks (1989); Seidel & Aragon, "Randomized search trees" (1989); Pugh, "Skip lists"
(1990); Pagh & Rodler, "Cuckoo hashing" (2001); Sedgewick, "Left-leaning red–black trees" (2008); Klink & Wälde,
"Efficient denial of service attacks on web application platforms" (28C3, 2011); Aumasson & Bernstein, "SipHash"
(2012); Larkin, Sen & Tarjan, "A back-to-basics empirical study of priority queues" (2014).

*Frontier.* Farach-Colton, Krapivin & Kuszmaul, "Optimal bounds for open addressing without reordering" (2025);
Bender, Conway, Farach-Colton, Kuszmaul & Tagliavini, "Tiny pointers" (2021); Demaine, Harmon, Iacono & Pătraşcu,
"Dynamic optimality—almost" (2004); Demaine, Harmon, Iacono, Kane & Pătraşcu, "The geometry of binary search trees"
(2009); Pătraşcu & Demaine, "Tight bounds for the partial-sums problem" (2004); Pătraşcu & Thorup, "Time-space
trade-offs for predecessor search" (2006); Kraska, Beutel, Chi, Dean & Polyzotis, "The case for learned index
structures" (2018).
