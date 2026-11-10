# Computer Science, Built — Part 17: Data Structures

Part 17 of the [61-part series](../README.md), in [Act IV, Algorithms](../SYLLABUS.md).
The running word-count task needs a dictionary rather than sorted output. This episode connects hashing,
ordered trees, priority queues, disjoint sets, tries, persistence and the memory hierarchy through worked
diagrams and instrumented implementations. English and Chinese narration use the same 81 source blocks.

The visual examples include collision lanes, a 42-pair universal-family grid, matched-home Robin Hood tables,
a BST/quicksort split, the actual five-node splay potential change, a cascading cut, and a valid six-node LOUDS
tree beside its 11 encoding bits. A six-bucket FKS example distinguishes one outcome from an expectation.
The instruments are [ds.py](../../../explainer/cs/algo/ds.py),
[job2.py](../../../explainer/cs/algo/job2.py), [compute.py](compute.py) and
[measurements.py](measurements.py); regressions are in
[test_cs17_ds.py](../../../tests/test_cs17_ds.py).

Measurements and models have different scopes:

- The corpus has 24,971,555 bytes, 4,609,954 word occurrences and 57,895 distinct words. The fixed polynomial
  hash produces 101 full-hash collision pairs and 12,495 reduced-slot pairs. Independent uniform-hash
  expectations are separate reference quantities; pair counts and excess-key counts differ for triples.
- Robin Hood and linear probing use the same keys, insertion order and home hash for the variance comparison.
  Their occupied patterns, displacement sums and means agree. Other probing plots are finite seeded
  illustrations; an affine universal family is not fully independent random hashing.
- The lookup microbenchmark preserves zero and distinguishes keys 12 and 13. Duplicate keys use last assignment
  wins in every implementation. Every result vector is checked outside the timer. Three raw repeats and actual
  unique-key loads are retained; the reported value is each implementation's minimum. The largest open table is
  29.8% full, not 50%. Lookup plus result-vector writes are timed; construction and verification are excluded.
  Timing alone does not measure cache misses or establish a causal explanation.
- Native word counters include allocation, tokenization, counting and top-20 selection, excluding file input,
  compiler startup and output formatting. Every complete report matches the reference. On this host the minima
  were about 1.073 s for Python (three repeats), 0.222 s for C++ and 0.103 s for C (five repeats each). These
  compare complete implementations, not isolated collision schemes. Compiler/interpreter versions, source
  hashes and all repeats are stored in the cached payloads. C++ prints timings to six significant digits.
- The Job's static image explicitly accommodates this corpus: 452,740 letter bytes including a temporary-word
  margin, 57,896 entry slots, 131,072 hash slots, a 1,904,816-byte image and 4 MiB modeled memory. The same image
  runs every emulator/core sample. Full corpus native event counts reproduce the complete report; the full
  corpus has **not** been executed by the emulator or core.
- A 27-event least-squares instruction model uses 36 of 48 emulator passages, with 12 held out. The event matrix
  has rank 22 of 28 columns including the intercept; correlated coefficients do not identify unique category
  costs. The largest held-out relative error is about 0.0132%, and 22 full-corpus features exceed their training
  maximum. Roughly 954.2 million full-corpus instructions are an extrapolation, not an exact executed count.
- Three passage core samples give weighted IPC about 1.472. A separate partial data-access trace uses an assumed
  array layout and toy caches. Adding its miss penalties to fitted instructions divided by sampled IPC projects
  about 0.794 s at the ledger clock. It omits overlap, may count sampled stalls twice, and is not a proved upper
  bound. The speed ratios inherit those assumptions and use different baselines.

Theory is scoped beside its diagrams. Hash-table bounds require appropriate hashing, load and key-cost models;
fixed keys must be independent of a chosen random family. The cuckoo curve records a 500-kick cutoff over 40
seeded trials, not proof of a cycle or the asymptotic threshold. Its diagnostic insertion stops immediately on
failure. The FKS experiment validates construction hashes and counts space/retries; it does not implement a
stored dictionary query interface. Random BST depth is in edges, while balanced/B-tree height tables use node
levels, with conversions explicit. Splay bounds include positive proof weights, final-zig +1 and initial
potential. Pairing-heap bounds depend on the variant. Heap comparisons do not realize Python list costs;
all displayed Dijkstra graphs are checked with independent heapq shortest paths, with a Bellman–Ford regression.
Union-find counts upward discovery edges, excluding compression's second pass and stores; roots can move later.

The fixed 512/64-bit rank directory checks every position, including 0 and n. Its 13,312-bit directory estimate
for 65,536 input bits excludes Python object memory. It implements rank, not select, and fixed proportional
redundancy is **not** an asymptotic o(n)-bit construction. LOUDS uses zero-based node and bit indices with
rank/select conversions shown. Succinct theory and data-dependent compressed indexes are separate claims.

The frontier distinguishes a fixed-occupancy uniform-permutation experiment (5,000 independent trials per point,
exact finite expectation (m+1)/(f+1)) from theorem statements. No funnel, elastic or 2026 hashing implementation
is benchmarked. The literature snapshot is dated 10 November 2026; selected statements/abstracts were checked,
not every proof or the entire literature. Constant dynamic optimality is not resolved by the cited bounds.

QA artifacts remain local under the Git-ignored `docs/qa/evidence/cs17-polish-20261110/`. The untouched source,
19 baseline payloads and 36 explicitly inspected bilingual baseline sheets are preserved. The progress ledger records the current revised source/preview checkpoint. Continuous narrated playback/listening, synthesized Chinese speech and whole-video
native production review remain separate release gates.

## Build

```bash
python -m videos.cs.cs17.compute           # every number in the part (about ten minutes)
python tools/build.py cs17 -q l            # a 480p preview
python tools/build.py cs17                 # 1080p
```

## Problems: proofs, a build sketch, and research notes

1. **Universal hashing.** Prove that h_{a,b}(x) = ((ax + b) mod p) mod m, with a uniform in {1, …, p − 1} and b
   uniform in {0, …, p − 1}, p prime and distinct keys in {0, …, p − 1}, satisfies Pr[h(x) = h(y)] ≤ 1/m for x ≠ y.

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
   h < log_φ(n + 2) + log_φ √5 − 2 = lg(n + 2)/lg φ + log_φ √5 − 2. The leading coefficient 1/lg φ is approximately 1.44042; 1.4405 is a rounded, weaker upper coefficient.

5. **Build: a hash without a division per letter.** Rewrite the Job v2 so that it divides once per word instead of
   once per letter, in the Pebble language, and measure its instructions per cycle and its ledger row on Part 8's
   core.

   *Build sketch, not a measured result.* Keep the multiplier 33 and define a 32-bit wrapping hash explicitly,
   then normalize at the word boundary before slot reduction. Check Pebble's runtime and constant-folding
   semantics at overflow; native C/C++ probes must use defined unsigned arithmetic. Replacing the hash changes
   collisions and probe paths, so preserve full keys, test long words, ties and growth, and check every complete
   output. Refit event counts with held-out samples of one corpus-sized image, then measure core samples.
   Do not promise an IPC or runtime gain before those checks. The existing corpus has 19.4 million letters,
   but this exercise has not produced a new ledger row.

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
   h + 2 < log_φ(√5 (n + 2))，即 h < log_φ(n + 2) + log_φ √5 − 2 = lg(n + 2)/lg φ + log_φ √5 − 2。主项系数 1/lg φ 约为 1.44042，1.4405 只是取整后稍宽的上界系数。

5. **动手：每个字母不做除法的哈希。** 用 Pebble 语言把任务 v2 改写成每个单词只做一次除法而不是每个字母一次，并在第8部分
   的核心上测量它的每周期指令数和账本行。

   *构建思路，并非实测结果。* 保留乘数 33，明确定义三十二位回绕哈希，在单词边界规范化后再约简到槽。
   核对 Pebble 运行时和常量折叠的溢出语义；原生 C/C++ 探针使用有定义的无符号算术。改变哈希也会改变冲突与探查路径，
   所以要保存完整键，测试长词、平局和扩容，并核对每次完整输出。使用同一个全语料容量镜像，重新拟合事件模型、留出验证，
   再测核心段落。检验之前不要承诺 IPC 或时间提升。现有语料约有 1940 万字母，但这道练习没有生成新的账本行。

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


## Selected primary-source checks, 10 November 2026

- [Optimal bounds for open addressing without reordering, v2](https://arxiv.org/html/2501.02305v2): selected
  introduction and theorems. Per-key random probe sequences; query probe complexity is a key's sequence
  position. Elastic's constant bound is amortized expected positive-query probes; the logarithmic bound is
  worst-case **expected**, with load-range restrictions. Funnel's squared-log bounds have their own range.
- [Full-occupancy hashing preprint](https://arxiv.org/abs/2503.13628): author abstract only; non-oblivious model,
  hash assumptions and high-probability operations must accompany the claim.
- [Incremental hashing preprint, 3 November 2026](https://arxiv.org/abs/2611.04186): author abstract only;
  reordering and non-reordering results have different operation/expectation scopes.
- [Braided cuckoo preprint, October 2026](https://arxiv.org/abs/2610.33229): author abstract only;
  stated as forthcoming SODA 2027, not a completed 2027 publication.
- [Splay competitive-bound preprint, July 2026](https://arxiv.org/abs/2607.18498) and
  [Greedy competitive-bound preprint, August 2026](https://arxiv.org/abs/2608.04410): selected author abstracts,
  not proof audits. The stated sublogarithmic bounds do not establish constant competitiveness. Tango is a
  historical general-BST benchmark, not a claim that no later progress exists for these particular algorithms.
- [Pătraşcu and Demaine, Logarithmic lower bounds in the cell-probe model](https://erikdemaine.org/papers/DynamicConnectivity_SICOMP/):
  author bibliography/abstract; word size, randomization, amortization and update/query trade-offs matter.
- [Rust HashMap documentation](https://doc.rust-lang.org/std/collections/struct.HashMap.html),
  [Go Swiss-table design](https://go.dev/blog/swisstable),
  [Abseil metadata design](https://abseil.io/about/design/swisstables),
  [Java HashMap collision qualifications](https://docs.oracle.com/en/java/javase/18/docs/api/java.base/java/util/HashMap.html),
  [Java 8 collection changes](https://docs.oracle.com/javase/8/docs/technotes/guides/collections/changes8.html), and
  [CPython hash configuration](https://docs.python.org/3.13/using/configure.html): selected implementation/design
  documentation. Java hashCode and ordinary C++ std::hash are not generally secret-key defenses; reference
  stability does not mandate one specific chaining layout. Group widths and default hashes depend on platform,
  version and configuration. The direct JEP 180 page returned 403, so the Java claim uses accessible official docs.

中文范围说明：这些是注明日期的部分原始来源核对，不是穷尽综述或所有证明的审核。期望、摊还、以高概率、装填区间、
是否允许重排，以及字长和操作集合都属于结论的一部分。预印本身份与未实现的新方案在画面及旁白中单独说明。
