# Computer Science, Built — Part 46: Logs, Streams and Warehouses

Part 46 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act IX, *Systems at Scale*. Every company's data ends up in two
places: an append-only log that records everything as it happens, and a column-oriented warehouse that answers
questions about all of it, with stream processors between them computing answers continuously. The hard part is time:
events arrive late, out of order and more than once. We build a partitioned log, a stream processor with watermarks
and checkpoints, and a columnar encoder, and the Job becomes a live top twenty over a stream of novels.

The instruments are in `explainer/cs/data/` (tested in `tests/test_cs46_data.py`):
* `log.py`: a topic of partitions, each an append-only list of (offset, key, value, time) records cut into segments;
  keys hashed to partitions with CRC-32; range assignment and a sticky rebalance for consumer groups, with the number
  of partitions each moves; retention by whole segments and compaction to the last record per key; demonstrations of
  per-key order, rebalancing and compaction.
* `stream.py`: a generator of events with event times, exponential network delays, a few much later arrivals and
  some duplicates; tumbling, sliding and session windows; a windowed keyed counter with a heuristic watermark (largest
  event time seen minus a lag), allowed lateness, deduplication and refinements; a keyed counter checkpointed by
  barrier snapshots and crashed on purpose; and the Job as a stream of thirty novels in three pipelines.
* `columnar.py`: Parquet-style encodings (plain strings with lengths, dictionary with bit-packed indices, the
  RLE/bit-packing hybrid, delta for integers) with sizes measured; row groups with min/max statistics and the groups a
  filter must read; Dremel's repetition and definition levels for a nested column, and the records rebuilt from them;
  the bytes moved by broadcast and shuffle joins and their crossover; a hot key over hashed workers, with salting; a
  simplified KLL quantile sketch; and optimistic commits to a table by compare-and-swap, conflicting or appending.

## Chapters

* **Hook.** The log as the structure we keep meeting: Part 35's write-ahead log, Part 38's Raft log, Part 41's git
  history, Part 43's outbox; Kreps's "The Log" (2013). Four sources and four consumers joined pairwise need 4 × 4 = 16
  pipelines, through a log 4 + 4 = 8 connections, each consumer at its own offset. Two places for every company's
  data, and the stream processors between them.
* **1. The partitioned log.** Kafka (Kreps, Narkhede and Rao, 2011): topics, partitions, segment files named by their
  base offset, a consumer's state as one offset per partition. "the whale and the sea and the ship and the whale"
  hashed into four partitions: every key's records in order (checked: true), the common words filling two partitions
  and one holding a single "ship". Twelve partitions and a consumer group: a fourth member joins and range assignment
  moves 6 partitions against the sticky assignor's 3; member two leaves and range moves 4, sticky 3. Retention by
  time and compaction by key: 2,000 updates to 50 keys compact to 50 records that rebuild the same state. In-sync
  replicas and the high watermark, Part 39's single-leader replication.
* **2. Moving a gigabyte a second.** At 200-byte messages a gigabyte a second is 5 million messages, 200 ns each;
  against Part 34's model a random flash read costs 400 budgets and a random disk read 64,803. Sequential appends
  and forward scans: 150 MB/s against 0.32 MB/s, 475× apart, so seven disks make the target. Batching (the Kafka
  paper's producer: 50,000 messages a second one at a time, 400,000 in batches of 50), `linger.ms` and compression;
  `sendfile` instead of four copies and two system calls; the page cache as the broker's only cache.
* **3. Changes as events.** Dual writes that crash or race and leave two answers; change data capture from the
  write-ahead log (logical decoding, the binary log, Debezium), keyed by primary key, starting from a snapshot; the
  outbox, a designed contract delivered at least once; state as a fold over events (balances 0, 50, 30, 40), and the
  compacted topic as exactly that fold; event sourcing and CQRS, with their costs.
* **4. Event time and processing time.** 120 simulated events, 2 a second, plotted at event time across and arrival
  upwards, the slowest 18.5 s late. Tumbling (10 s), sliding (10 s every 5 s) and session windows (a 4 s gap) over
  eight events. A heuristic watermark, the largest event time seen minus 3 s: 11 of the 120 events arrive behind it,
  and the window [0, 10) closes at 13.1 s with 19 of its 20 events, the last arriving at 14.8 s. How long to wait, on
  3,000 events in 10 s windows: no lag drops 530 events and answers 2.2 s after a window ends; 5 s drops 182
  (7.0 s); a minute drops 1, with 29 of 30 windows exact but answers 65.3 s late; a 5 s watermark with 60 s of allowed
  lateness drops none, ends with all 30 windows exact, and fires 183 refinements. Triggers (early, on time, late) and
  accumulation (discarding, accumulating, retracting); what, where, when and how.
* **5. Exactly-once state.** Keyed state on workers, and the replay question after a crash. Barriers through a
  dataflow graph (Carbone et al., 2015, after Chandy and Lamport): alignment, asynchronous snapshots, a complete
  checkpoint. Our keyed counter crashed on purpose: 3,032 events, three workers, a crash at offset 1,700, recovery
  from the checkpoint at 1,500, 200 events processed a second time and final counts equal to a failure-free run;
  rewinding the source but keeping the counts overcounts those 200 events (at-least-once). Idempotent and
  transactional sinks; exactly-once as an end-to-end property (Saltzer, Reed and Clark).
* **6. Streaming algorithms in production.** Part 20's Misra–Gries summary with 99 counters over the corpus's
  4,609,954 words: every count low by at most n/k, about 46,100 ("the": true 230,878, estimate 192,188). HyperLogLog
  on 57,895 distinct words: 26% error with 12 bytes, 0.7% with 12,288; with 3,072 bytes, 58,012 estimated, and
  4,483,876 for 4,506,123 distinct five-word phrases; merging by the larger register. A KLL sketch of 200,000
  simulated latencies keeping 95 items: p99.9 off by 0.6% in rank yet 164 against 427 in value; t-digest's clusters.
  Windowed stream joins and the state they hold; mergeable summaries.
* **7. The warehouse.** Lambda (Marz, 2011) against Kappa (Kreps, 2014); streaming as a superset of batch. OLTP
  against OLAP (Codd, 1993). The star schema of facts and dimensions (Kimball, 1996), a star join planned as hash
  joins, snowflakes, and slowly changing dimensions (type 1 overwrites, type 2 adds a version).
* **8. Columnar files.** Rows against columns (C-Store, 2005); a Parquet file's row groups, column chunks, pages and
  footer. Dictionary, bit-packing, run lengths and deltas on a small example, then measured on 300,000 words of the
  novels (30,515 distinct, so 15-bit indices): plain 2.58 MB, gzip 0.80 MB, dictionary page plus indices 0.93 MB
  (0.37 + 0.56), run lengths in reading order 0.93 MB, sorted 0.47 MB (18% of plain); 100,000 timestamps from
  0.80 MB plain to 0.14 MB delta-encoded, 8 bytes each against 11 bits. Predicate pushdown on a million rows in ten
  row groups: 1 of 10 read when sorted by x, 10 of 10 in random order.
* **9. Nested data in columns.** Dremel (Melnik et al., 2010): three books with repeated chapters and repeated
  keywords, the column `chapters.keywords` flattened to sea, whale, inn, Highbury; repetition levels 0, 2, 1, 1, 0, 0
  and definition levels 2, 2, 2, 1, 0, 2 for its six slots (four values, an empty chapter, an empty book); the
  records rebuilt exactly from the levels alone; 2-bit levels, nulls costing only their levels; Parquet and Arrow.
* **10. Tables on object storage.** Why a folder is not a table; Iceberg's snapshots, manifest lists and manifests
  with one atomic pointer swap; Delta Lake's log of numbered commits, checkpoints every ten commits and conditional
  writes; optimistic commits, measured with fifty commits per writer: when every commit conflicts, sixteen writers
  retry 3.85 times per commit and reach 2.6× one writer's rate, while appends that only renumber reach 11.1×; time
  travel, restore and vacuum; the lakehouse (Armbrust et al., 2021).
* **11. Queries on a thousand machines.** Partitioned execution with partial aggregates and an exchange (Gamma,
  1986). Broadcast (S × N rows) against shuffle ((B + S)(1 − 1/N) rows) for B a billion 100-byte rows and N = 100:
  broadcast grows from 100 MB to 1 TB, shuffle stays near 100 GB, and they cross at S* ≈ 10.0 million rows, 1% of B.
  One hot key with a fifth of 200,000 rows on 16 workers: the slowest worker carries 49,757 rows, 3.98× the ideal
  12,500; salting into eight sub-keys brings it to 15,061, 1.20×. Vectorized execution (MonetDB/X100, DuckDB's 2,048)
  against Volcano's row at a time, and compiled queries (HyPer).
* **12. Data you can trust.** Schema evolution by Avro's rules (backward, forward), a schema registry, Iceberg's
  column IDs; data contracts checked where the change is made; tests on data (dbt), run on chapter 13's stream:
  books 5 and 13 arrive twice, the word total is +6.7% without deduplication and −10.0% with a 5 s watermark (3 late
  books dropped), equal exactly once; lineage graphs; write, audit, publish.
* **13. The Job as a stream.** Thirty novels, 4,498,120 words, one event per book: books 8, 18 and 19 arrive twenty
  seconds late, books 5 and 13 are sent twice. Three pipelines: exactly once counts 4,498,120 words ("the" 227,474)
  and equals the batch answer; no deduplication counts 4,797,994 ("the" 241,278); a 5 s watermark counts 4,048,309
  ("the" 202,443). A top twenty over all time needs no watermark. Ledger row 17: 3.7 s on one machine, exact, and
  current after every book.
* **14. Frontier: streams, tables and their limits.** Incremental view maintenance, differential dataflow (McSherry
  et al., 2013) and DBSP (Budiu et al., 2023). How small a summary can be: KLL with 95, 309 and 1,326 items kept,
  rank errors at p50 of 0.83%, 0.61% and 0.02%, at p99 of 0.32%, 0.10% and 0.06%, at p99.9 of 0.58%, 0.22% and
  0.07%; optimality and lower bounds (Alon, Matias and Szegedy, 1996). Time as a guess: completeness against latency
  across watermark lags, and allowed lateness escaping the trade. Four open problems and the ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs46.compute
python -m unittest tests.test_cs46_data
python tools/build.py cs46
```

## Problems, with solutions

1. **Per-key order.** Show that a consumer of one partition sees each key's events in order, and give an example
   where a consumer of two partitions sees two keys' events in an order no producer wrote.

   *Solution.* A record's partition is hash(key) mod n, a function of the key alone, so every record of one key goes
   to the same partition. A partition is an append-only log: each append takes the next offset, and no record is
   ever changed or moved, so offsets order the records in the order the broker appended them. A consumer reads a
   partition by increasing offset, from its committed position. Hence, if the producer's records for a key are
   appended in the order it sent them (one producer, and retries that do not reorder its batches), the consumer sees
   that key's records in that order, and after a crash it resumes from a committed offset without reordering
   anything. Across partitions nothing is promised: a consumer of several partitions interleaves its fetches as
   timing dictates. In our run of "the whale and the sea and the ship and the whale" over four partitions, "the"
   (positions 0, 3, 6, 9) lands in partition 2 and "whale" (1, 10) with "and" (2, 5, 8) in partition 1. A consumer
   that fetches partition 1 first sees whale(1), and(2), …, whale(10) before the(0), so "whale" precedes "the", an
   order the single producer never wrote; within each key the order is still correct.

2. **Watermark lag.** Prove that a watermark lag of L drops exactly the events whose delay exceeds L plus the
   window's slack, and compute the share dropped for exponential delays.

   *Solution.* Take a tumbling window [s, s + T), an event in it with event time e and delay D (it arrives at e + D),
   and call σ = s + T − e ∈ (0, T] the event's slack, how far it lies before its window's end. Idealize the watermark
   as W(t) = t − L, as when the sources' newest event times keep pace with the clock. The window fires when W
   reaches s + T, at processing time s + T + L, and an event arriving after that is dropped. So the event is dropped
   if and only if e + D > s + T + L, that is D > L + σ. (With allowed lateness A the window accepts events until
   s + T + L + A, and L is replaced by L + A.) For exponential delays of mean μ and events spread evenly over the
   window, σ is uniform on (0, T], and the share dropped is
   (1/T)∫₀ᵀ e^(−(L+σ)/μ) dσ = (μ/T) e^(−L/μ) (1 − e^(−T/μ)).
   For μ = 2 s and T = 10 s this is 0.1987 e^(−L/2): 19.9% at L = 0, 7.3% at L = 2, 1.6% at L = 5 and 0.13% at
   L = 10. Our simulation also delays 5% of events by a further 20 to 60 s; for L ≤ 10 all of these are dropped,
   since D ≥ 20 > L + σ. The heuristic watermark, largest event time seen minus L, trails the clock by the age γ of
   the freshest event seen (0.48 s on average here), and the window fires at the first arrival after W passes its
   end, so the effective lag is a little more than L. Fitting an extra 0.7 s,
   0.05 + 0.95 · 0.1987 e^(−(L+0.7)/2) gives 18.3%, 13.1%, 9.9% and 6.1% for L = 0, 1, 2 and 5 s, against the
   measured 17.7%, 13.2%, 10.0% and 6.1% (530, 397, 301 and 182 of 3,000 events).

3. **Barrier snapshots.** Show that asynchronous barrier snapshots give a consistent cut (Part 38), and hence
   exactly-once state after recovery.

   *Solution.* Assume an acyclic dataflow graph with FIFO channels and replayable sources. Checkpoint n consists of
   each source's offset at the moment it emits barrier n, and each operator's state at the moment it has received
   barrier n on every input (holding back inputs whose barrier came first, which is alignment) and before it
   processes anything after the barriers. By induction in topological order, an operator's snapshot reflects exactly
   the records that precede barrier n on its inputs: alignment stops it from processing any record behind a barrier,
   and FIFO channels deliver everything ahead of the barrier before it. Each of those input records was emitted by
   its upstream operator before that operator forwarded barrier n, hence derives only from source records before the
   recorded offsets; so every snapshot is a function of the same prefix of each source. The cut is consistent: if an
   operator's state reflects a received record, the sender's snapshot reflects having sent it, and because every
   record ahead of a barrier has been consumed when the snapshot is taken, no channel holds a record that crosses the
   cut, so there is no channel state to save. (For cyclic graphs Carbone et al. also log the records in flight on
   back edges.) Recovery restores every operator's state and rewinds every source to its offset: each source record
   before the offset has affected the state exactly once, through the snapshot, and each record after it affects the
   state exactly once, in the replay, so the restored run is a failure-free run of the same input (the same run, if
   the operators are deterministic). In our instrument, 3,032 events with a crash at offset 1,700 restore from the
   checkpoint at 1,500, replay 200 events, and end with counts equal to a run that never failed; keeping the crashed
   state while rewinding the source counts those 200 events twice.

4. **Dremel levels.** Compute the repetition and definition levels of a three-level nested column by hand, and
   rebuild the records from them.

   *Solution.* Take records with repeated `shelves`, each with repeated `books`, each with repeated `tags`, and the
   column `shelves.books.tags` (three repeated fields, so r and d both run from 0 to 3):
   record 1 has shelf 1 with books [sea, whale] and [ ], and shelf 2 with book [inn]; record 2 has no shelves;
   record 3 has shelf 1 with no books and shelf 2 with book [York]. The repetition level says at which repeated field
   a value repeats (0 a new record, 1 a new shelf, 2 a new book, 3 another tag in the same book), and the definition
   level how many of the three fields are present. Walking the records in order gives seven slots:
   (sea, 0, 3), (whale, 3, 3), (null, 2, 2) for the empty book, (inn, 1, 3), (null, 0, 0) for the record without
   shelves, (null, 0, 1) for the shelf without books, and (York, 1, 3). To rebuild, read the triples in order: r = 0
   starts a new record; if d ≥ 1 and r ≤ 1, open a new shelf; if d ≥ 2 and r ≤ 2, open a new book in the current
   shelf; if d = 3, append the value to the current book. The seven triples give back
   [[[sea, whale], [ ]], [[inn]]], [ ] and [[ ], [[York]]], the three records exactly, as our `dremel` function and
   this reader confirm.

5. **Build.** Add sliding windows and allowed lateness to our stream processor, and measure the state it must keep.

   *Solution notes.* In `run_windows`, assign each event to every window `sliding(et, size, step)` returns rather
   than the one from `tumbling`, keep counts per (window, key), fire a window when the watermark reaches its end, and
   accept late events (as refinements) until the watermark passes end + allowed lateness; at that moment emit the
   final count and delete the window's state, which the present instrument never does. Track the number of open
   windows and of (window, key) entries after each event, and their maximum. A window is open from its first event
   until about end + L + A in processing time, so roughly (size + L + A)/step windows are open at once, each with up
   to one counter per key. A sketch along these lines on the instrument's 3,000 events (three keys, 10 s windows,
   L = 5 s) reproduces the cached tumbling results (182 dropped without lateness; all 30 windows exact with 60 s of
   lateness) and measures a peak of 2 open windows (6 entries) without lateness and 8 (24) with it, against
   (10 + 5 + 60)/10 = 7.5; sliding windows every 5 s need 4 (10) and 16 (46), against 15, and with 60 s of lateness
   60 of their 61 windows end exact. State grows linearly in the window size plus the lateness, and divided by the
   step.

6. **★ Research.** Which windowed stream joins can be maintained exactly in space sublinear in the window?

   *Discussion.* Open. For an equi-join of two streams over a window of w events with keys from a large domain, an
   exact answer needs Ω(w) words in the worst case: whether a new event joins depends on whether its key appeared
   among the last w events of the other stream, and a standard communication argument (the INDEX problem) shows that
   remembering a set of that kind takes space linear in it. Sublinear space is possible under extra structure: a
   small key domain (keep a count per key), constraints on the data such as ordering or bounded disorder that let
   state be discarded early (Babu, Srivastava and Widom studied such "k-constraints"), or an output that is only an
   aggregate of the join; Arasu et al. (PODS 2002) characterized the select–project–join queries over unbounded
   streams that need only bounded memory. A good answer would fix a model (time- or count-based windows, join
   predicates, whether the output is every match or an aggregate), prove lower bounds for the hard classes, give
   algorithms meeting them for the rest, and draw the line between them; a characterization for equi-joins with
   bounded disorder, or for band joins on ordered keys, would already be new.

## 习题与解答

1. **按键的顺序。** 证明一个分区的消费者按顺序看到每个键的事件，并举例说明一个消费两个分区的消费者看到的两个键的事件顺序，
   是任何生产者都没有写过的。

   *解答。* 记录的分区是 hash(key) mod n，只取决于键，所以同一个键的所有记录都进入同一个分区。分区是只追加的日志：每次追加取下一个
   偏移量，记录从不改动也不移动，所以偏移量按代理追加的顺序给记录排序。消费者从它提交的位置起，按偏移量递增读一个分区。因此，只要
   生产者对一个键的记录按发送顺序被追加（一个生产者，而且重试不会打乱它的批次），消费者就按这个顺序看到该键的记录；崩溃后它从已提交
   的偏移量继续，也不会打乱任何东西。跨分区则没有任何保证：消费多个分区的消费者按时机交错地拉取。在我们把“the whale and the sea and
   the ship and the whale”写入四个分区的例子里，“the”（位置 0、3、6、9）落在分区 2，“whale”（1、10）和“and”（2、5、8）落在分区 1。
   先拉取分区 1 的消费者会在 the(0) 之前看到 whale(1)、and(2)、……、whale(10)，于是“whale”排在“the”前面，这是唯一的生产者从未写过的
   顺序；而每个键内部的顺序仍然正确。

2. **水位线的延迟。** 证明延迟为 L 的水位线恰好丢弃那些延迟超过 L 加上窗口余量的事件，并计算延迟服从指数分布时被丢弃的比例。

   *解答。* 取一个滚动窗口 [s, s + T)，其中一个事件的事件时间为 e、延迟为 D（在 e + D 到达），称 σ = s + T − e ∈ (0, T] 为它的余量，
   即它离窗口结束还有多远。把水位线理想化为 W(t) = t − L，就像数据源最新的事件时间与时钟同步前进时那样。窗口在 W 到达 s + T 时、也就
   是处理时间 s + T + L 时触发，之后到达的事件被丢弃。所以事件被丢弃当且仅当 e + D > s + T + L，即 D > L + σ。（若允许延迟 A，窗口接受
   事件直到 s + T + L + A，把 L 换成 L + A 即可。）若延迟服从均值为 μ 的指数分布，事件在窗口内均匀分布，则 σ 在 (0, T] 上均匀，丢弃的
   比例为 (1/T)∫₀ᵀ e^(−(L+σ)/μ) dσ = (μ/T) e^(−L/μ) (1 − e^(−T/μ))。μ = 2 秒、T = 10 秒时为 0.1987 e^(−L/2)：L = 0 时 19.9%，L = 2
   时 7.3%，L = 5 时 1.6%，L = 10 时 0.13%。我们的模拟还让 5% 的事件再多延迟 20 到 60 秒；L ≤ 10 时它们全部被丢弃，因为
   D ≥ 20 > L + σ。启发式水位线是“见过的最大事件时间减 L”，它比时钟落后一段时间 γ，即所见最新事件的“年龄”（这里平均 0.48 秒），而且
   窗口在 W 越过窗口结束后的第一个到达时才触发，所以实际的延迟比 L 略大。拟合出额外的 0.7 秒，0.05 + 0.95 · 0.1987 e^(−(L+0.7)/2) 在
   L = 0、1、2、5 秒时给出 18.3%、13.1%、9.9% 和 6.1%，实测为 17.7%、13.2%、10.0% 和 6.1%（3,000 个事件中的 530、397、301 和 182
   个）。

3. **屏障快照。** 证明异步屏障快照给出一个一致割（第38部分），从而恢复后得到恰好一次的状态。

   *解答。* 设数据流图无环，通道先进先出，数据源可以重放。第 n 个检查点由两部分组成：每个数据源发出屏障 n 时的偏移量；每个算子在所有
   输入上都收到屏障 n 之后（屏障先到的输入被暂时扣住，这就是对齐）、处理屏障之后的任何记录之前的状态。按拓扑顺序归纳：一个算子的快照
   恰好反映它的输入上排在屏障 n 之前的记录，因为对齐使它不处理任何屏障之后的记录，而先进先出的通道会在屏障之前送达屏障前的一切。这些
   输入记录中的每一条，都是上游算子在转发屏障 n 之前发出的，所以只来自记录下的偏移量之前的源记录；因此每个快照都是每个数据源同一个前缀
   的函数。这个割是一致的：如果一个算子的状态反映了它收到的一条记录，发送者的快照就反映了已经发出它；而且拍快照时屏障之前的记录都已被
   消费，没有通道里留着跨越这个割的记录，所以不需要保存通道状态。（对有环的图，Carbone 等人还记录回边上正在传输的记录。）恢复时，恢复
   每个算子的状态，并把每个数据源倒回它的偏移量：偏移量之前的每条源记录通过快照恰好影响状态一次，之后的每条记录在重放中恰好影响状态
   一次，所以恢复后的运行是同一输入的一次无故障运行（如果算子是确定性的，就是同一次运行）。在我们的工具里，3,032 个事件在偏移量
   1,700 处崩溃，从 1,500 处的检查点恢复，重放 200 个事件，最终计数与从未出故障的运行相同；若倒回数据源却保留崩溃时的状态，这 200 个
   事件就被计了两次。

4. **Dremel 的级别。** 手工计算一个三层嵌套列的重复级别和定义级别，并由它们重建记录。

   *解答。* 取这样的记录：重复的 `shelves`，每个含重复的 `books`，每本书含重复的 `tags`；列为 `shelves.books.tags`（路径上有三个重复
   字段，所以 r 和 d 都从 0 到 3）。记录 1 的书架 1 上有书 [sea, whale] 和 [ ]，书架 2 上有书 [inn]；记录 2 没有书架；记录 3 的书架 1
   上没有书，书架 2 上有书 [York]。重复级别说明一个值在哪个重复字段上重复（0 为新记录，1 为新书架，2 为新书，3 为同一本书里的另一个
   标签），定义级别说明三个字段中有几个存在。按顺序走遍这些记录，得到七个位置：(sea, 0, 3)，(whale, 3, 3)，空书 (null, 2, 2)，
   (inn, 1, 3)，没有书架的记录 (null, 0, 0)，没有书的书架 (null, 0, 1)，以及 (York, 1, 3)。重建时按顺序读这些三元组：r = 0 开始一条
   新记录；若 d ≥ 1 且 r ≤ 1，打开一个新书架；若 d ≥ 2 且 r ≤ 2，在当前书架里打开一本新书；若 d = 3，把值追加到当前这本书。七个三元组
   还原出 [[[sea, whale], [ ]], [[inn]]]、[ ] 和 [[ ], [[York]]]，正是原来的三条记录，我们的 `dremel` 函数和这个读取过程都验证了这一点。

5. **动手。** 给我们的流处理器加上滑动窗口和允许延迟，并测量它必须保存的状态。

   *解答要点。* 在 `run_windows` 中，把每个事件分配给 `sliding(et, size, step)` 返回的每个窗口，而不是 `tumbling` 给出的那一个；按
   （窗口，键）保存计数；水位线到达窗口结束时触发；在水位线越过“结束 + 允许延迟”之前，接受迟到事件（作为修正）；到那一刻输出最终计数并
   删除这个窗口的状态，而现在的工具从不删除。每个事件之后记录打开的窗口数和（窗口，键）条目数，并取最大值。一个窗口从它的第一个事件起
   打开，直到处理时间大约为“结束 + L + A”，所以同时打开的窗口约为 (size + L + A)/step 个，每个至多每个键一个计数器。按这个思路在工具的
   3,000 个事件上（三个键，10 秒窗口，L = 5 秒）写的草稿，重现了缓存中的滚动窗口结果（不允许延迟时丢弃 182 个；允许 60 秒延迟时 30 个
   窗口全部精确），测得峰值为：不允许延迟时 2 个打开的窗口（6 个条目），允许时 8 个（24 个），对照 (10 + 5 + 60)/10 = 7.5；每 5 秒滑动
   的窗口需要 4 个（10 个）和 16 个（46 个），对照 15，而且允许 60 秒延迟时 61 个窗口中有 60 个最终精确。状态随窗口大小加上允许延迟线性
   增长，再除以步长。

6. **★ 研究。** 哪些窗口化的流连接能用低于窗口大小的线性空间（亚线性空间）精确维护？

   *讨论。* 尚未解决。对键取自很大值域、窗口为 w 个事件的两个流的等值连接，最坏情况下精确答案需要 Ω(w) 个字：一个新事件是否能连接，
   取决于它的键是否出现在另一个流最近的 w 个事件中，而一个标准的通信复杂度论证（INDEX 问题）表明，记住这样一个集合需要与它成线性的空间。
   在额外的结构下亚线性空间是可能的：键的值域很小（每个键保存一个计数）；数据上的约束，例如有序或乱序有界，使状态可以提前丢弃（Babu、
   Srivastava 和 Widom 研究过这类“k 约束”）；或者输出只是连接的一个聚合。Arasu 等人（PODS 2002）刻画了在无界流上只需有界内存的
   选择–投影–连接查询。好的答案应确定一个模型（基于时间还是基于计数的窗口，连接谓词，输出是每一个匹配还是一个聚合），对困难的类证明下界，
   对其余的给出达到下界的算法，并划清两者的界线；仅对乱序有界的等值连接，或对有序键上的带状连接给出刻画，就已经是新的。

## Glossary additions

* **log, topic, partition, segment, offset** — an append-only sequence of records; a named stream split into
  partitions; the files a partition is stored in; a record's position.
* **consumer group, rebalance, range and sticky assignment** — members sharing a topic's partitions; reassigning them
  when a member joins or leaves; recutting contiguous runs, or moving only what must move.
* **retention, log compaction, tombstone** — forgetting by age; keeping the latest record per key; a record that
  deletes its key.
* **in-sync replicas (ISR), high watermark** — the followers caught up with the leader; the offset up to which every
  one of them has the data, and consumers may read.
* **batching, zero-copy (`sendfile`), page cache** — one request for many messages; sending file pages to a socket
  without copying them through the program; the kernel's cache of file pages.
* **dual write, change data capture (CDC), outbox** — writing two systems without a shared transaction; publishing a
  database's committed changes from its log; a table of events committed with the state they describe.
* **event sourcing, CQRS, read model** — an application whose system of record is a log of events; separating the
  write model from the read models; a fold over the events for one question.
* **event time, processing time** — when an event happened; when the pipeline sees it.
* **tumbling, sliding and session windows** — fixed pieces of event time; overlapping windows with a size and a step;
  runs of activity ended by a gap.
* **watermark, late event, allowed lateness** — a claim that no older events are still coming; an event behind it;
  how long a fired window still accepts corrections.
* **trigger, accumulation (discarding, accumulating, retracting)** — when a window's result is emitted; how successive
  results relate.
* **keyed state, barrier, alignment, checkpoint (asynchronous barrier snapshot)** — an operator's state partitioned
  by key; a marker flowing with the records; waiting for a barrier on every input; a consistent cut of offsets and
  states.
* **at-most-once, at-least-once, exactly-once, idempotent and transactional sinks** — delivery guarantees, and the
  sinks that make a repeated write harmless or invisible until committed.
* **mergeable summary, HyperLogLog, KLL, t-digest** — a sketch that combines across partitions with the same
  guarantee; distinct counts; quantiles with rank error; quantiles accurate at the tails.
* **Lambda and Kappa architectures** — a batch and a stream path merged at query time; one stream path, replayed to
  change it.
* **OLTP, OLAP, fact, dimension, star and snowflake schemas, slowly changing dimension** — transactions against
  analysis; the events measured and what describes them; their layouts; dimensions with history.
* **columnar file, row group, column chunk, page, footer** — a table stored by column; its horizontal slices; one
  column of a slice; the unit of encoding; the schema and statistics at the end.
* **dictionary encoding, bit-packing, run-length and delta encoding, predicate pushdown** — integers for repeated
  values; packing them in as few bits as needed; runs and differences; skipping data by statistics.
* **repetition level, definition level** — at which repeated field a value repeats; how much of its path exists.
* **table format, snapshot, manifest, optimistic commit, time travel, lakehouse** — a table kept as files on object
  storage; a version of it; a list of its files; commit by compare-and-swap, retrying on conflict; reading an old
  version; a warehouse's guarantees over open files.
* **MPP, exchange, broadcast join, shuffle hash join, skew, salting** — a query spread over many machines; the
  operator that repartitions; sending the small table everywhere; repartitioning both by key; one key with too many
  rows; splitting it into sub-keys.
* **vectorized execution, selection vector** — operators that pass batches of column values; the positions in a batch
  that passed a filter.
* **schema evolution, backward and forward compatibility, schema registry, data contract** — changing a record's
  shape; new readers of old data and old readers of new; the service that checks changes; an explicit, versioned
  interface between teams.
* **data test, lineage, write–audit–publish** — a query for the rows that break a rule; the graph of what is built
  from what; staging a snapshot and publishing it only after its tests pass.
* **incremental view maintenance, differential dataflow, DBSP** — keeping a query's answer current by pushing changes
  through it.

## Sources

* M. Kleppmann, *Designing Data-Intensive Applications* (2017), ch. 3, 10–12; T. Akidau, S. Chernyak and R. Lax,
  *Streaming Systems* (2018); R. Kimball and M. Ross, *The Data Warehouse Toolkit* (3rd edn, 2013).
* J. Kreps, "The Log: what every software engineer should know about real-time data's unifying abstraction",
  LinkedIn Engineering (2013); J. Kreps, N. Narkhede and J. Rao, "Kafka: a distributed messaging system for log
  processing", NetDB 2011.
* T. Akidau et al., "MillWheel: fault-tolerant stream processing at internet scale", VLDB 2013; T. Akidau et al.,
  "The Dataflow model: a practical approach to balancing correctness, latency, and cost in massive-scale, unbounded,
  out-of-order data processing", VLDB 2015.
* K. M. Chandy and L. Lamport, "Distributed snapshots: determining global states of distributed systems", ACM TOCS
  1985; P. Carbone, G. Fóra, S. Ewen, S. Haridi and K. Tzoumas, "Lightweight asynchronous snapshots for distributed
  dataflows" (2015); J. Saltzer, D. Reed and D. Clark, "End-to-end arguments in system design", ACM TOCS 1984.
* Z. Karnin, K. Lang and E. Liberty, "Optimal quantile approximation in streams", FOCS 2016; T. Dunning and O. Ertl,
  "Computing extremely accurate quantiles using t-digests" (2019); P. Agarwal et al., "Mergeable summaries", PODS
  2012; N. Alon, Y. Matias and M. Szegedy, "The space complexity of approximating the frequency moments", STOC 1996.
* M. Stonebraker et al., "C-Store: a column-oriented DBMS", VLDB 2005; D. Abadi, P. Boncz, S. Harizopoulos, S. Idreos
  and S. Madden, "The design and implementation of modern column-oriented database systems", Foundations and Trends
  in Databases 2013; the Apache Parquet format specification.
* S. Melnik, A. Gubarev, J. J. Long, G. Romer, S. Shivakumar, M. Tolton and T. Vassilakis, "Dremel: interactive
  analysis of web-scale datasets", VLDB 2010.
* M. Armbrust et al., "Delta Lake: high-performance ACID table storage over cloud object stores", VLDB 2020;
  M. Armbrust, A. Ghodsi, R. Xin and M. Zaharia, "Lakehouse: a new generation of open platforms that unify data
  warehousing and advanced analytics", CIDR 2021; the Apache Iceberg table specification.
* D. DeWitt et al., "GAMMA: a high performance dataflow database machine", VLDB 1986; G. Graefe, "Volcano: an
  extensible and parallel query evaluation system", IEEE TKDE 1994; P. Boncz, M. Zukowski and N. Nes,
  "MonetDB/X100: hyper-pipelining query execution", CIDR 2005; T. Neumann, "Efficiently compiling efficient query
  plans for modern hardware", VLDB 2011.
* F. McSherry, D. Murray, R. Isaacs and M. Isard, "Differential dataflow", CIDR 2013; M. Budiu, T. Chajed,
  F. McSherry, L. Ryzhyk and V. Tannen, "DBSP: automatic incremental view maintenance for rich query languages",
  VLDB 2023; A. Arasu, B. Babcock, S. Babu, J. McAlister and J. Widom, "Characterizing memory requirements for
  queries over continuous data streams", PODS 2002.
