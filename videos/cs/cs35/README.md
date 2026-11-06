# Computer Science, Built — Part 35: Databases

Part 35 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the start of the data half of the course. In 1970 Codd said programs should ask
for *what* data they want and never *how* to find it. That one idea created a mathematics (relational algebra and
dependency theory), an optimizer that searches for the cheapest of many correct plans, and the theory of
transactions, which lets thousands of users act as if each were alone, even through crashes. The Job becomes one
line of SQL, and our own database finds Part 17's hash table by itself.

The instruments are in `explainer/cs/db/` (tested in `tests/test_cs35_db.py`, and cross-checked against `sqlite3`):
* `rel.py`: relations as sets of tuples; selection, projection, renaming, product, natural join, union, difference
  and grouping; functional dependencies, attribute closure, keys, projected dependencies, BCNF test and
  decomposition, minimal cover, Bernstein's 3NF synthesis, and the chase test for lossless joins.
* `engine.py`: **our database**. A SQL subset (SELECT, FROM with JOIN … ON, WHERE with AND, GROUP BY, ORDER BY,
  LIMIT, COUNT and SUM) parsed into a tree; tables on 100-row pages; `ANALYZE`-style statistics (rows, distinct
  values, min and max per column) and selectivity estimates under the independence assumption; B+ tree indexes;
  Volcano iterators (scan, index scan, filter, four join methods, hash and sort aggregation, a top-k heap, sort,
  project) that count the pages they read; a cost model in page I/Os; Selinger's dynamic program over connected
  subsets (left-deep, with every join method and access path), or an exhaustive search for comparison; `EXPLAIN`.
* `joins.py`: block nested loops, index nested loops, sort-merge with external merge sort and Grace hash, over
  explicit pages with every read and write counted, beside the textbook formulas.
* `bptree.py`: a B+ tree (leaf splits copy a key up, interior splits move one up, linked leaves, range scans,
  an invariant checker).
* `txn.py`: schedules; the precedence graph and the conflict-serializability test; view serializability by search;
  strict two-phase locking with deadlock detection, wait-die or wound-wait; six isolation levels (read uncommitted,
  read committed, repeatable read, snapshot, snapshot with Cahill's SSI, and serializable by 2PL) running small
  programs step by step; the five classic anomalies as programs and interleavings.
* `aries.py`: a page store with a buffer pool under steal and no-force, a write-ahead log with prevLSNs, page LSNs,
  CLRs and checkpoints; workloads of transactions under strict 2PL on pages; crashes at any record; recovery by
  analysis, redo (repeating history) and undo; crashes during undo; the committed state for checking.

## Chapters

* **Hook.** The Job twice: Part 17's program, every step chosen by hand, and one line of SQL. Over the thirty
  novels, loaded as 4,609,954 rows, both give the same twenty words; sqlite3 answers in 2.25 s. Our database's plan:
  scan, hash aggregate, top-20 heap.
* **1. Ask for what, not how.** IMS (1968) and CODASYL (1969): programs that navigate pointers. Codd (1970):
  relations, keys, a query that states its result, and data independence. System R and Ingres; SEQUEL became SQL.
  The whale query on a sample: 1,201 pages without an index, 85 with one, the query unchanged.
* **2. Relational algebra.** σ, π, ⋈, ∪, −, ρ on books and authors; a query as a tree; the books their authors
  published before 45 (Emma, Persuasion, Ulysses); Codd's theorem; rewriting trees.
* **3. Dependencies and normal forms.** Update, insertion and deletion anomalies; functional dependencies,
  Armstrong's axioms, closure, keys; BCNF and a lossless decomposition (the chase); a careless split that invents
  rows; BCNF can lose a dependency, Bernstein's 3NF keeps them.
* **4. How a query runs.** Volcano iterators: open, next, close; pipelines and blocking operators. The Job's plan run:
  4,609,954 tuples scanned, 57,895 groups, a heap of 20; 46,100 pages against 230,500 estimated for sorting; our
  engine 7.4 s, sqlite3 2.25 s. Access paths for the whale query: 1,201 pages by scan, 85 by index.
* **5. Joins, page by page.** The cost unit is the page. Block nested loops, index nested loops, sort-merge, Grace
  hash, with formulas; measured on M = 400, N = 200 pages for B = 5 … 80: BNLJ and sort-merge equal their formulas
  exactly, INL reads less (13% of keys have no match), Grace hash pays 1–9% for partial pages and stops fitting below
  B = 40. With B = 80 BNLJ wins; with B = 5 hashing wins by 15×.
* **6. The optimizer.** Plan space: n! left-deep orders, n!·C(n−1) bushy trees (28 trillion for 12 tables) against
  2^n subsets. The 120 orders of a five-table chain with hash joins: best 2,302 pages, median 43,448, worst
  24,243,824 (a cross product first), a factor of 10,532. Selinger's dynamic program, the principle of optimality,
  interesting orders; 395 plans costed against 1,200 for exhaustive search, both finding cost 550.
* **7. Guessing sizes.** Statistics and selectivity; a city and its own country: estimate 25, actual 492; a city and
  an age: 250 against 256. Skew: one guess, 9.9 rows, for every word; *the* has 6,776. Histograms and most-common
  values. Errors multiply through joins (Ioannidis and Christodoulakis 1991; Leis et al. 2015).
* **8. Indexes.** A B+ tree grown key by key, splitting and rising; search and range scans. Fanout 400: a thousand
  keys in two levels, a trillion in five; our index on the Job's 57,895 words is two levels high. Unclustered against
  clustered: the 1,704 rows from *whale* to *whales* lie on 966 pages, or 18. Hash, bitmap, LSM, inverted and covering
  indexes.
* **9. Transactions.** ACID on a bank transfer (Gray 1981; Härder and Reuter 1983). Schedules, conflicts and the
  precedence graph; the lost update's cycle; Eswaran et al.'s theorem. View serializability and blind writes;
  NP-complete to test (Papadimitriou 1979). Of 90 interleavings of three small transactions, 10 are serializable.
* **10. Two-phase locking.** Shared and exclusive locks; the growing and shrinking phases and the lock-point proof;
  strict 2PL; granularity, intention locks and phantoms. Deadlock and the waits-for graph. 400 random runs per policy,
  every schedule serializable: detection 342 aborts, wait-die 734, wound-wait 723, prevention never deadlocking.
* **11. Optimism and snapshots.** Kung and Robinson's optimistic control; timestamp ordering. MVCC (Reed 1978):
  version chains and snapshots; first committer wins. Write skew with two doctors on call: under read committed and
  snapshot isolation both commit and nobody is on call; SSI aborts T1; 2PL aborts T2. Fekete's dangerous structures
  and Cahill's SSI, PostgreSQL's SERIALIZABLE since 2011.
* **12. Isolation levels.** Six levels against five anomalies, each run: read uncommitted allows all, read committed
  stops only dirty reads, repeatable read all but phantoms, snapshot all but write skew, the serializable levels all.
  ANSI SQL-92's wording, Berenson et al.'s critique (1995), Adya's graph definitions (1999), Elle (2020).
* **13. Recovery: ARIES.** Steal, no-force and write-ahead logging; LSNs and page LSNs. A crashed log of twelve
  records: T3 and T2 committed, T1 the loser; page 0 missing committed changes, page 3 holding an uncommitted one.
  Analysis, redo from LSN 1 (4 redone, 5 skipped), undo of 11, 5 and 1 with three CLRs: exactly the committed state.
  500 random crashes recovered, and 500 crashed again during undo: all correct.
* **14. Column stores.** Rows against columns; SUM over 1,000,000 rows of 16 columns: tuple at a time 74 ms,
  vectorized row store 13.9 ms, vectorized column store 4.1 ms (16 MB read instead of 128 MB). Run-length coding of
  the Job's book column: 4.6 million values in 30 runs, 37 MB to 480 bytes; a 16-bit dictionary for the words, 24.0 MB
  to 9.7 MB. C-Store, MonetDB/X100, HyPer; Parquet to DuckDB.
* **15. Our database runs the Job.** Hash aggregate (46,100 page I/Os) against sort aggregate (230,500): Parts 16
  and 17 in one decision. sqlite3's plan (a temporary B-tree), 2.25 s; with an index, a covering index scan, 0.25 s;
  ours 7.4 s; all three equal to Part 17's answer. **Ledger row 13**: one line of SQL, 2.25 s natively. Key-value,
  document, graph and distributed SQL stores.
* **16. Frontier: joins, guesses, guarantees.** The triangle query: binary joins build 1,132,558 two-paths for 4,500
  edges where a generic join does 10,228 steps; the AGM bound N^{3/2} and worst-case optimal joins (Ngo et al. 2012,
  leapfrog triejoin). Learned cardinalities and optimizers (Neo, Bao). Checking isolation in black-box histories
  (NP-complete for serializability and SI; Elle, Cobra). Six open problems.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs35.compute          # every item (job loads 4.6 million rows into sqlite3: about a minute)
python -m unittest tests.test_cs35_db
python tools/build.py cs35
```

## Problems, with solutions

1. **Conflict serializability.** Prove that a schedule is conflict-serializable if and only if its precedence graph
   is acyclic.

   *Solution.* (⇒) Suppose the schedule is conflict-equivalent to the serial order T_{π1}, …, T_{πn}. Equivalence
   preserves the order of every pair of conflicting operations, and in the serial schedule every operation of an
   earlier transaction precedes every operation of a later one. So each edge Ti → Tj (some operation of Ti precedes
   a conflicting one of Tj) points forward in π, and a graph whose edges all point forward in a linear order has no
   cycle. (⇐) If the graph is acyclic, take a topological order π. Repeatedly swap adjacent operations of different
   transactions that are out of π's order. Such a pair cannot conflict (a conflict would be an edge pointing backward
   in π), and swapping non-conflicting adjacent operations preserves equivalence. Each swap removes one inversion, so
   the process ends in the serial schedule for π.

2. **Two-phase locking.** Prove that every schedule produced by two-phase locking is conflict-serializable, and give
   a serializable schedule that 2PL cannot produce.

   *Solution.* Let ℓ(T) be T's lock point, the moment it holds its last new lock. If Ti → Tj, some operation of Tj
   conflicts with an earlier one of Ti on an item x; Tj could lock x only after Ti released it, and Ti released
   nothing before ℓ(Ti), so ℓ(Ti) < (Ti's release of x) < (Tj's lock of x) ≤ ℓ(Tj). A cycle would give ℓ(T) < ℓ(T).
   So the graph is acyclic and, by problem 1, the schedule is serializable, in lock-point order. The schedule
   w1(x) r2(x) w1(y) is serializable (T1 then T2, the only conflict being on x), but under 2PL T1 must release x
   before T2 reads it, and then cannot lock y. 2PL's schedules are a strict subset of the conflict-serializable ones.

3. **Sort and hash costs.** Derive the I/O cost of external merge sort with B buffers, and the memory Grace hash join
   needs for one partitioning pass.

   *Solution.* Pass 0 reads M pages B at a time and writes ⌈M/B⌉ sorted runs; each later pass merges B − 1 runs into
   one (one input buffer per run, one output buffer), so ⌈log_{B−1}⌈M/B⌉⌉ merge passes follow. Every pass reads and
   writes every page: 2M(1 + ⌈log_{B−1}⌈M/B⌉⌉) I/Os, which is the formula our counts matched exactly (for M = 400,
   B = 5: 5 passes, 4,000 I/Os). Grace hash splits R into B − 1 buckets of about M/(B − 1) pages; the build phase
   holds one bucket in B − 2 pages, so it needs M/(B − 1) ≤ B − 2, about B ≥ √M. For M = 400 that is B ≥ 21; with
   uneven buckets our measurement needed B = 40, which is why the formula 3(M + N) is printed in red below that.

4. **Plan space.** Count the bushy join trees over n tables, and the work of Selinger's dynamic program on chain,
   star and clique queries.

   *Solution.* A join tree is a full binary tree with n labelled leaves. There are C_{n−1} = (2n − 2)!/(n!(n − 1)!)
   shapes (Catalan) and n! ways to place the tables, so n!·C_{n−1} = (2n − 2)!/(n − 1)! trees: 1,680 for n = 5,
   28,158,588,057,600 for n = 12. The dynamic program does work proportional to the number of (connected subset, way
   to split it) pairs. A chain has n(n + 1)/2 connected subsets (intervals), and an interval of k tables has k − 1
   splits into two intervals: Θ(n³) bushy, Θ(n²) left-deep. A star (one hub, n − 1 leaves) has 2^{n−1} connected
   subsets containing the hub, each with up to n − 1 ways to remove a leaf: Θ(n·2^n) left-deep. A clique has 2^n − 1
   subsets, all connected, and splitting every subset into two non-empty parts gives (3^n − 2^{n+1} + 1)/2 pairs:
   Θ(3^n) bushy, Θ(n·2^n) left-deep. This is why systems fall back to greedy or genetic search beyond a dozen or so
   tables (PostgreSQL's `geqo_threshold` is 12).

5. **Build: histograms.** Add a histogram per column to our database's statistics, and measure the `word = 'the'`
   estimate before and after.

   *Solution.* The simplest effective form is PostgreSQL's: a list of the k most common values with their exact
   counts, plus an equi-depth histogram (or, for equality, a uniform guess) for the rest. In `Database.analyze`, keep
   `Counter(col).most_common(k)`; in the selectivity estimate for `col = v`, return the stored count if v is in the
   list, else (rows − Σ listed counts)/(distinct − k). On the 120,000-word sample with k = 100: the top 100 words hold
   63,367 occurrences, so *the* is estimated exactly, 6,776 (it was 9.9). Every other word is now estimated at
   (120,000 − 63,367)/12,066 ≈ 4.7: *ship*, 26, is now off by 5.5× instead of 2.6×, and *whale*, 81, by 17× instead of
   8×. The list fixes the frequent values, which matter most for plan choice, and slightly worsens the rest. For
   ranges, an equi-depth histogram with b buckets bounds the error of any range estimate by about 2/b of the rows.

6. ★ **Research. False aborts.** On random workloads, how many of SSI's aborts were unnecessary? Find the fewest aborts
   any online scheduler that sees only rw-edges can make, and a rule that achieves it.

   *What is known, and a way in.* An abort is necessary only if committing the transaction would make the history
   non-serializable; SSI aborts whenever a pivot (an rw-edge in and an rw-edge out) appears, but a pivot is
   dangerous only if the two edges close a cycle. Measure first: run `txn.run_level("snapshot + SSI", …)` on random
   programs; for each abort, re-run the schedule with that transaction allowed to commit and test the committed
   history with `txn.conflict_serializable` (with the rw-, wr- and ww-dependencies of Adya's graph). Cahill's
   original rule aborted on any pivot; PostgreSQL's implementation (Ports and Grittner 2012) aborts only if the
   outgoing transaction commits first and ignores safe read-only transactions, and reports far fewer false aborts.
   A lower bound needs an indistinguishability argument: two histories identical in their rw-edges up to the moment of
   decision, one of which closes a cycle later through a wr-edge the scheduler cannot yet see. Any online scheduler
   that must decide at commit time must abort both or risk the bad one, so some false aborts are forced; the open
   question is the optimal competitive ratio against an offline scheduler that knows the whole history, and a
   practical rule that attains it.

## 习题与解答

1. **冲突可串行化。** 证明：一个调度是冲突可串行化的，当且仅当其优先图无环。

   *解答。*（⇒）设调度与串行顺序 T_{π1}, …, T_{πn} 冲突等价。等价保持每一对冲突操作的先后，而在串行调度中，较早事务的
   每个操作都在较晚事务的每个操作之前。所以每条边 Ti → Tj（Ti 的某操作先于 Tj 的一个与之冲突的操作）在 π 中都指向前方；
   边全都沿一个线性序向前的图没有环。（⇐）若图无环，取一个拓扑序 π。反复交换相邻的、属于不同事务且与 π 的顺序相反的两个
   操作。这样的一对不可能冲突（否则就是一条在 π 中向后的边），而交换相邻的非冲突操作保持等价。每次交换消除一个逆序，最终得到
   π 对应的串行调度。

2. **两阶段锁。** 证明两阶段锁产生的每个调度都是冲突可串行化的，并给出一个 2PL 无法产生的可串行化调度。

   *解答。* 记 ℓ(T) 为 T 的锁点，即它获得最后一把新锁的时刻。若 Ti → Tj，则 Tj 的某操作与 Ti 较早的一个操作在某项 x 上
   冲突；Tj 只能在 Ti 释放 x 之后才锁住 x，而 Ti 在 ℓ(Ti) 之前不释放任何锁，所以 ℓ(Ti) < （Ti 释放 x）< （Tj 锁住 x）
   ≤ ℓ(Tj)。若有环，就会得到 ℓ(T) < ℓ(T)。所以图无环，由第 1 题，调度可串行化，等价于按锁点排序的串行顺序。调度
   w1(x) r2(x) w1(y) 是可串行化的（先 T1 后 T2，唯一的冲突在 x 上），但在 2PL 下 T1 必须在 T2 读 x 之前释放 x，之后就不能
   再锁 y。2PL 能产生的调度是冲突可串行化调度的真子集。

3. **排序与哈希的代价。** 推导 B 个缓冲页下外部归并排序的 I/O 代价，以及 Grace 哈希连接一趟分区所需的内存。

   *解答。* 第 0 趟每次读入 B 页，写出 ⌈M/B⌉ 个有序段；之后每趟把 B − 1 个段归并成一个（每段一个输入缓冲，一个输出缓冲），
   共需 ⌈log_{B−1}⌈M/B⌉⌉ 趟归并。每趟读写每一页一次：总计 2M(1 + ⌈log_{B−1}⌈M/B⌉⌉) 次 I/O，正是我们的计数逐页吻合的公式
   （M = 400、B = 5 时为 5 趟，4,000 次 I/O）。Grace 哈希把 R 分成 B − 1 个桶，每桶约 M/(B − 1) 页；构建阶段要把一个桶放进
   B − 2 页，所以需要 M/(B − 1) ≤ B − 2，约为 B ≥ √M。M = 400 时是 B ≥ 21；由于桶大小不均，我们的测量需要 B = 40，所以在此
   之下公式 3(M + N) 用红色标出。

4. **计划空间。** 计算 n 张表上浓密连接树的数目，以及 Selinger 动态规划在链形、星形和完全图查询上的工作量。

   *解答。* 连接树是有 n 个带标号叶子的满二叉树：形状有 C_{n−1} = (2n − 2)!/(n!(n − 1)!) 种（卡塔兰数），放置表的方式有 n!
   种，共 n!·C_{n−1} = (2n − 2)!/(n − 1)! 棵：n = 5 时 1,680 棵，n = 12 时 28,158,588,057,600 棵。动态规划的工作量正比于
   （连通子集，拆分方式）对的个数。链有 n(n + 1)/2 个连通子集（区间），k 张表的区间有 k − 1 种拆成两个区间的方式：浓密树
   Θ(n³)，左深树 Θ(n²)。星形（一个中心、n − 1 个叶子）有 2^{n−1} 个含中心的连通子集，每个至多有 n − 1 种去掉一个叶子的方式：
   左深 Θ(n·2^n)。完全图有 2^n − 1 个子集，全部连通，把每个子集拆成两个非空部分共有 (3^n − 2^{n+1} + 1)/2 对：浓密 Θ(3^n)，
   左深 Θ(n·2^n)。所以系统在十几张表以上改用贪心或遗传搜索（PostgreSQL 的 `geqo_threshold` 为 12）。

5. **动手：直方图。** 为我们数据库的统计信息加上每列的直方图，比较 `word = 'the'` 的估计在前后的变化。

   *解答。* 最简单有效的形式是 PostgreSQL 的：k 个最常见值及其确切计数，其余部分用等深直方图（等值查询则用均匀猜测）。在
   `Database.analyze` 中保存 `Counter(col).most_common(k)`；估计 `col = v` 的选择率时，若 v 在列表中就返回保存的计数，否则
   返回 (行数 − 列表计数之和)/(不同值数 − k)。在 120,000 词的样本上取 k = 100：前 100 个词共出现 63,367 次，于是 *the* 被
   精确估计为 6,776（原来是 9.9）。其余每个词现在估计为 (120,000 − 63,367)/12,066 ≈ 4.7：*ship*（26）的误差从 2.6 倍变为
   5.5 倍，*whale*（81）从 8 倍变为 17 倍。这个列表修正了对计划选择最要紧的高频值，而略微恶化了其余的值。对范围查询，b 个桶
   的等深直方图把任何范围估计的误差限制在约 2/b 的行数之内。

6. ★ **研究：多余的中止。** 在随机工作负载上，SSI 的中止有多少是不必要的？找出只看得见读写反依赖边的在线调度器至少要中止
   多少次，以及达到这一下界的规则。

   *已知的情况与入手的方法。* 只有当提交某事务会使历史不可串行化时，中止才是必要的；SSI 只要出现枢纽（一条读写边进、一条
   读写边出）就中止，而枢纽只有在两条边闭合成环时才危险。先测量：在随机程序上运行 `txn.run_level("snapshot + SSI", …)`；
   对每次中止，让该事务提交并重放调度，再用 `txn.conflict_serializable` 检验已提交的历史（使用 Adya 图中的 rw、wr、ww 依赖）。
   Cahill 最初的规则在任何枢纽上都中止；PostgreSQL 的实现（Ports 与 Grittner，2012）只在出边一端的事务先提交时才中止，并忽略
   安全的只读事务，报告的多余中止少得多。下界需要一个不可区分性论证：两个历史在决策时刻之前的读写边完全相同，其中一个之后经由
   一条调度器尚看不见的 wr 边闭合成环。任何必须在提交时作出决定的在线调度器，要么两个都中止，要么冒险放过坏的那个，所以某些
   多余中止是不可避免的；开放的问题是相对于知道整个历史的离线调度器的最优竞争比，以及达到它的实用规则。

## Glossary additions

* **relation**: a set of tuples over named attributes; a table with no row order and no duplicates.
* **key**: a minimal set of attributes whose values identify a tuple; **foreign key**: a key of another table, stored
  to refer to its row.
* **relational algebra**: selection σ, projection π, join ⋈, union ∪, difference −, renaming ρ.
* **functional dependency** X → Y: rows that agree on X agree on Y; **closure** X⁺: everything X determines.
* **BCNF**: every non-trivial dependency's left side is a key; **3NF**: or its right side is part of a key.
* **lossless decomposition**: one whose pieces join back to exactly the original.
* **iterator (Volcano) model**: operators with open, next and close, pulling tuples from their children.
* **selectivity, cardinality**: the fraction of rows a condition keeps; the number of rows an operator produces.
* **left-deep plan**: a join tree whose right child is always a base table; **bushy**: any shape.
* **interesting order**: a sort order of an intermediate result that a later operator can use.
* **B+ tree**: a balanced search tree of page-sized nodes with all keys in linked leaves.
* **clustered index**: one whose order is the table's storage order.
* **transaction**, **ACID**: atomic, consistent, isolated, durable.
* **schedule**: an interleaving of transactions' operations; **conflict**: two operations of different
  transactions on the same item, one a write.
* **conflict-serializable**: equivalent, by swapping non-conflicting operations, to a serial schedule.
* **two-phase locking** (2PL): no lock acquired after one is released; **strict 2PL**: write locks held to commit.
* **deadlock**: a cycle of transactions each waiting for another; **wait-die, wound-wait**: prevention by age.
* **MVCC**: keeping old versions so readers see a snapshot; **snapshot isolation**: reads from the snapshot at start,
  first committer wins.
* **write skew**: two transactions read overlapping data and write disjoint data, breaking an invariant.
* **SSI**: serializable snapshot isolation, aborting pivots of rw-antidependencies.
* **isolation level**: the anomalies a database promises to prevent.
* **WAL** (write-ahead log); **LSN** (log sequence number); **steal, no-force**; **CLR** (compensation log record).
* **ARIES**: recovery by analysis, redo (repeating history) and undo, with CLRs.
* **column store**: a table stored column by column; **vectorized execution**: operators over arrays of values.
* **worst-case optimal join**: a join whose time is bounded by the AGM bound on its largest possible output.

## Sources

* A. Silberschatz, H. F. Korth and S. Sudarshan, *Database System Concepts*.
* R. Ramakrishnan and J. Gehrke, *Database Management Systems*.
* H. Garcia-Molina, J. D. Ullman and J. Widom, *Database Systems: The Complete Book*.
* J. M. Hellerstein and M. Stonebraker (eds.), *Readings in Database Systems* (the Red Book).
* J. Gray and A. Reuter, *Transaction Processing: Concepts and Techniques*.
* P. A. Bernstein, V. Hadzilacos and N. Goodman, *Concurrency Control and Recovery in Database Systems*.
* G. Weikum and G. Vossen, *Transactional Information Systems*.
* S. Abiteboul, R. Hull and V. Vianu, *Foundations of Databases*.
* E. F. Codd, "A Relational Model of Data for Large Shared Data Banks", CACM (1970); "Relational Completeness of
  Data Base Sublanguages" (1972).
* D. D. Chamberlin and R. F. Boyce, "SEQUEL: A Structured English Query Language" (1974).
* W. W. Armstrong, "Dependency Structures of Data Base Relationships" (1974); P. A. Bernstein, "Synthesizing Third
  Normal Form Relations from Functional Dependencies", ACM TODS (1976).
* R. Bayer and E. McCreight, "Organization and Maintenance of Large Ordered Indexes", Acta Informatica (1972);
  D. Comer, "The Ubiquitous B-Tree", ACM Computing Surveys (1979).
* P. G. Selinger et al., "Access Path Selection in a Relational Database Management System", SIGMOD (1979).
* G. Graefe, "Volcano — An Extensible and Parallel Query Evaluation System", IEEE TKDE (1994).
* M. Kitsuregawa, H. Tanaka and T. Moto-oka, "Application of Hash to Data Base Machine and Its Architecture", New
  Generation Computing (1983).
* Y. E. Ioannidis and S. Christodoulakis, "On the Propagation of Errors in the Size of Join Results", SIGMOD (1991).
* V. Leis et al., "How Good Are Query Optimizers, Really?", PVLDB (2015).
* K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, "The Notions of Consistency and Predicate Locks in a
  Database System", CACM (1976).
* C. H. Papadimitriou, "The Serializability of Concurrent Database Updates", JACM (1979).
* J. Gray, "The Transaction Concept: Virtues and Limitations", VLDB (1981); T. Härder and A. Reuter, "Principles of
  Transaction-Oriented Database Recovery", ACM Computing Surveys (1983).
* D. J. Rosenkrantz, R. E. Stearns and P. M. Lewis, "System Level Concurrency Control for Distributed Database
  Systems", ACM TODS (1978).
* H. T. Kung and J. T. Robinson, "On Optimistic Methods for Concurrency Control", ACM TODS (1981).
* D. P. Reed, "Naming and Synchronization in a Decentralized Computer System", MIT thesis (1978).
* H. Berenson et al., "A Critique of ANSI SQL Isolation Levels", SIGMOD (1995).
* A. Adya, "Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions", MIT
  thesis (1999).
* A. Fekete et al., "Making Snapshot Isolation Serializable", ACM TODS (2005); M. J. Cahill, U. Röhm and A. Fekete,
  "Serializable Isolation for Snapshot Databases", SIGMOD (2008); D. R. K. Ports and K. Grittner, "Serializable
  Snapshot Isolation in PostgreSQL", PVLDB (2012).
* C. Mohan et al., "ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks
  Using Write-Ahead Logging", ACM TODS (1992).
* M. Stonebraker et al., "C-Store: A Column-oriented DBMS", VLDB (2005); P. Boncz, M. Zukowski and N. Nes,
  "MonetDB/X100: Hyper-Pipelining Query Execution", CIDR (2005); T. Neumann, "Efficiently Compiling Efficient Query
  Plans for Modern Hardware", PVLDB (2011).
* J. M. Hellerstein, M. Stonebraker and J. Hamilton, "Architecture of a Database System" (2007).
* M. Stonebraker and A. Pavlo, "What Goes Around Comes Around… And Around…", SIGMOD Record (2024).
* A. Atserias, M. Grohe and D. Marx, "Size Bounds and Query Plans for Relational Joins", FOCS (2008); H. Q. Ngo,
  E. Porat, C. Ré and A. Rudra, "Worst-case Optimal Join Algorithms", PODS (2012); T. Veldhuizen, "Leapfrog Triejoin"
  (2014).
* R. Marcus et al., "Neo: A Learned Query Optimizer", PVLDB (2019); "Bao: Making Learned Query Optimization
  Practical", SIGMOD (2021); A. Kipf et al., "Learned Cardinalities" (2019).
* R. Biswas and C. Enea, "On the Complexity of Checking Transactional Consistency", OOPSLA (2019); K. Kingsbury and
  P. Alvaro, "Elle: Inferring Isolation Anomalies from Experimental Observations", PVLDB (2020); C. Tan et al.,
  "Cobra: Making Transactional Key-Value Stores Verifiably Serializable", OSDI (2020).
* S. Chu et al., "Cosette: An Automated Prover for SQL", CIDR (2017).
