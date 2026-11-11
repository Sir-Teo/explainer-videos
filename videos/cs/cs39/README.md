# Computer Science, Built — Part 39: Distributed Systems II: Scale

Part 39 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act VII, *Many Machines*. At the scale of a datacenter, every
guarantee has a price in latency or availability. CAP states the trade-off, CRDTs avoid it by making merges
commutative, and Spanner pays for it with atomic clocks. One slow server in a hundred makes most requests slow. The
Job finally runs as MapReduce on sixteen machines, one of which dies.

The instruments are in `explainer/cs/dist/` (tested in `tests/test_cs39_scale.py` and `tests/test_cs39_replicas.py`):
* `scale.py`: probabilistically bounded staleness for N, R, W; replication lag; CRDTs (G-counter, PN-counter, OR-set,
  LWW register) and a naive set under random gossip; consistent hashing with virtual nodes, jump and rendezvous
  hashing; Chord's fingers; two-phase commit behind a crashed coordinator; Spanner's commit wait; fan-out tails and
  hedged requests; the power of two choices; a metastable retry storm.
* `mapreduce.py`: the Job as MapReduce on simulated Pebbles (real counting, splits, a hashed shuffle, a crash with
  re-execution, stragglers and backup tasks, a timeline of every task attempt).
* `replicas.py`: two leaders under last-writer-wins with clock skew against version vectors; Merkle-tree
  anti-entropy; RGA, a sequence CRDT, against positional replay, and its tombstone overhead; hot keys under Zipf
  popularity, and salting.
* `service.py`: load balancing as queueing (random, round robin, two choices, shortest queue); availability in series,
  in parallel and with correlated rack failures; failure detection by fixed timeouts and phi accrual; tails through a
  chain of services; retry amplification.
* `clocks.py` (from Part 38) gains hybrid logical clocks; `history.py` is an Elle-style checker that infers the
  dependency graph of list-append transactions and finds its cycles.

## Chapters

* **Hook.** The Job on sixteen Pebbles: 48 maps, a shuffle, 16 reduces. Pebble 4 crashes at 0.4 s; three finished
  maps are redone; backup copies finish the last slow tasks. 0.60 s against 2.65 s on one Pebble, and the same top
  twenty words.
* **1. The datacenter, and replication.** Latency numbers on a scale where one cycle is a second (a datacenter round
  trip: seventeen days; California to Europe: fifteen years). Single-leader, multi-leader and leaderless replication.
  Replication lag: 67% of immediate reads miss your own post, 9% after 200 ms; read-your-writes, monotonic reads.
  Two leaders writing one key five times a second each: 19% of writes concurrent, so last-writer-wins silently loses
  9.7%; with 250 ms of clock skew, 22.7%; version vectors lose none and keep siblings.
* **2. Quorums and consistency.** R + W > N; Dynamo's sloppy quorums and hinted handoff. Probabilistically bounded
  staleness: (3, 1, 1) is stale 54%, 32%, 7.4% and 0.34% of the time at 0, 5, 20 and 50 ms; strict quorums never.
  Merkle-tree anti-entropy on a million keys: 11 KB in six round trips for ten differences, against 16 MB for one
  hash per key. The consistency hierarchy; CAP (Gilbert–Lynch) with a 40/60 partition: CP refuses 40% of requests,
  AP answers all with stale minority reads and 200 conflicting writes; PACELC.
* **3. CRDTs.** Join-semilattices: commutative, associative, idempotent merges, and the convergence theorem. A
  G-counter step by step. A thousand gossip runs each: G-counter, PN-counter, OR-set and LWW register always converge;
  a naive log-replaying set in 15. OR-sets and sequence CRDTs. Two people editing "the cat sat": positional replay
  diverges ("the fat ran sat"), RGA gives "the fat cat ran" on both; 500 random sessions: RGA 500, replay 0. The
  cost: after 20,000 edits, 8,404 visible characters, 5,798 tombstones, 42 bytes per visible character.
* **4. Partitioning.** Modulo hashing moves 91% of keys when an eleventh node joins; a consistent-hash ring 8.6%
  (minimum 9.1%); jump and rendezvous hashing. Virtual nodes: the busiest of ten nodes at 3.39× its share with one
  point, 1.16× with 256. Hot keys: Zipf(1) puts 7% of requests on one key and its shard at 7.8× the mean; salting the
  ten hottest keys twenty ways brings it to 1.8×. Range partitioning and timestamp hot spots. Chord: 2.8 hops for 16
  nodes, 7.9 for 16,384, about ½ log₂ n + 1; Kademlia.
* **5. Transactions across machines.** Two-phase commit, and its blocking: a coordinator crash after deciding leaves
  participants holding locks for 31 s. 3PC; commit over Paxos groups. Spanner's TrueTime and commit wait (2ε; free
  for ε = 1 and 4 ms, 6 ms extra for 7). Hybrid logical clocks: on four processes 5 ms apart, physical timestamps put
  21% of receipts before their sends; HLC none, within 3.4 ms of true time, counter at most 7. Chubby, ZooKeeper,
  leases and fencing tokens.
* **6. MapReduce.** Map, shuffle, reduce: 25 MB in, 6 MB shuffled, 57,895 distinct words. Five runs: plain 0.51 s;
  a crash 0.60 s with 3 maps redone; a straggler 0.59 s with backups and 0.81 s without; all correct. Scaling: 3.85 s
  on one worker, 0.55 s on 16, 0.42 s on 64 (Amdahl). Ledger row 15. Spark's lineage, streaming with watermarks,
  exactly-once by snapshots.
* **7. The tail at scale.** One request in a hundred taking a second: 1 − 0.99ⁿ of requests are slow, 63.9% at a
  fan-out of 100 (simulated). Hedging at 30 ms: the median at fan-out 100 falls from 1,000 ms to 43 ms. Two choices:
  the busiest of 1,000 servers 5.5 → 3. The supermarket model at 95% load: p99 of 82 service times for random
  routing, 46 for round robin, 10.5 for two choices, 5.4 for the shortest queue. Through a chain of 3 and 10
  services: p99 120 and 265 ms, against 192 and 648 by adding; retries through 3 layers: 64 attempts per request.
* **8. Failure at scale.** Correlated, gray and metastable failures. A cluster's first year (Dean 2009); a 6-hour job
  on 1,000 machines sees no failure 80% of the time. Nines: ten dependencies at 99.9% give 99.0%; three independent
  replicas 99.9999999%; three in one rack 99.95%. Failure detection: a 175 ms timeout raises 101 false alarms an
  hour; phi accrual has no hand tuning but the same trade-off. A retry storm: after a ten-second spike, goodput 78/s
  without retries, 0 with retries (with or without backoff), 80/s when expired requests are dropped. Chaos
  engineering and post-mortems.
* **9. Frontier: how little coordination?** The CALM theorem (monotonic iff coordination-free) and invariant
  confluence; CAC: no model stronger than real-time causal consistency is always available and convergent; COPS.
  Checking histories: Elle's dependency cycles on 2,000 list-append transactions, none on a serial store, 143 on a
  stale replica. Four open problems, and the ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs39.compute
python -m unittest tests.test_cs39_scale tests.test_cs39_replicas
python tools/build.py cs39
```

## Problems, with solutions

1. **Quorums.** Prove that if R + W > N every read quorum meets every write quorum, and give a run with R + W ≤ N
   that returns a stale value.

   *Solution.* A read set and a write set are subsets of the N replicas of sizes R and W; if they were disjoint their
   union would have R + W > N elements, impossible. So some replica in the read set holds the latest acknowledged
   write, and taking the highest version returns it. For R + W ≤ N, take N = 3, W = 1, R = 1: write v₂ to replica A
   only, acknowledged; read from replica C, which still holds v₁. Our simulation of (3, 1, 1) returns the stale value
   54% of the time at the moment of acknowledgement.

2. **CRDT convergence.** Prove that a state-based CRDT whose merge is the join of a semilattice converges.

   *Solution.* Each replica's state is the join of its initial state and of the states it has merged, plus local
   updates, which are inflations (s ≤ u(s)). Because ⊔ is associative and commutative, the result of any sequence of
   merges is the join of the set of all updates' effects that reached the replica, independent of order and grouping;
   because ⊔ is idempotent, receiving a state twice changes nothing. Two replicas that have received the same set of
   updates therefore hold the join of the same set: the same state. Our test: 1,000 random gossip orders, every CRDT
   converged.

3. **Consistent hashing.** Show that adding an (n+1)-th node moves 1/(n+1) of the keys in expectation, and that
   h(k) mod n moves n/(n+1).

   *Solution.* With n + 1 random points on the circle, by symmetry each node's arc has expected length 1/(n+1), and
   the new node takes exactly the keys in its arc, so the expected fraction moved is 1/(n+1). For modulo: a key stays
   iff h mod n = h mod (n+1). For h uniform over a range that is a multiple of n(n+1), h mod n(n+1) is uniform, and by
   the Chinese remainder theorem (n and n+1 are coprime) the pair (h mod n, h mod (n+1)) is uniform over n(n+1)
   pairs, of which n agree (h mod n(n+1) < n). So a fraction n/(n(n+1)) = 1/(n+1) stays and n/(n+1) moves (91% for
   n = 10, as measured).

4. **Two-phase commit and Spanner.** Show that 2PC blocks if the coordinator crashes after one participant votes yes,
   and explain why commit wait makes timestamps respect real time.

   *Solution.* A participant that voted yes has promised to commit if told to, so it cannot abort on its own (the
   coordinator may have decided commit and told someone); it cannot commit either (the coordinator may have decided
   abort, for example because another participant voted no). Nothing it can learn from other participants that are
   also uncertain resolves this, so it waits for the coordinator. Spanner: a transaction T₁ picks s₁ = TT.now().latest
   and does not report commit until TT.now().earliest > s₁, so its true commit time t₁ > s₁. Any T₂ that starts after
   T₁'s commit is reported starts at true time > t₁ > s₁, and picks s₂ = TT.now().latest ≥ its true start time > s₁.
   So real-time order implies timestamp order. The wait is about 2ε.

5. **Build.** Let our MapReduce survive the master's crash.

   *Solution sketch.* The master's state is the task table: each task's state (idle, in progress, done), its worker,
   and, for finished maps, where their outputs live. Append every change to a log on stable storage (or replicate it
   with Raft from Part 38). On restart, replay the log; tasks in progress are reset to idle, since their workers may
   have died too, and finished maps whose worker is gone are reset as in a worker failure. Because tasks are
   deterministic and reducers use whichever copy of a map output they get, duplicate executions do not change the
   result. Test it by crashing the master at random times and comparing the top twenty words with the reference.

6. **★ Research.** Design a retry and admission policy for our metastable simulator that provably recovers from any
   finite spike while keeping hedging's tail benefit.

   *Discussion.* This is open in general. Directions: a retry budget (retries at most a fraction β of first attempts)
   bounds the offered load by (1 + β)λ, so if (1 + β)λ < μ the queue is stable after any spike; dropping requests
   whose deadline has passed bounds the queue's useful work; hedges count against the same budget. What is missing is
   a proof for realistic clients (timeouts, backoff, many layers) and a characterization of the largest spike each
   policy survives, ideally checked against adversarially chosen spikes in our simulator.

## 习题与解答

1. **法定人数。** 证明若 R + W > N，则每个读集合都与每个写集合相交；并给出一个 R + W ≤ N 时读到旧值的执行。

   *解答。* 读集合与写集合分别是 N 个副本中大小为 R 和 W 的子集；若二者不相交，它们的并有 R + W > N 个元素，不可能。
   所以读集合中某个副本持有最新的已确认写入，取最高版本即可读到它。若 R + W ≤ N，取 N = 3、W = 1、R = 1：v₂ 只写到副本
   A 并被确认；从仍持有 v₁ 的副本 C 读取。我们对 (3, 1, 1) 的模拟在确认的那一刻有 54% 的读是旧值。

2. **CRDT 的收敛。** 证明合并为半格上并运算（join）的基于状态的 CRDT 一定收敛。

   *解答。* 每个副本的状态是其初始状态、它合并过的状态与本地更新的并，而本地更新都是膨胀（s ≤ u(s)）。由于 ⊔
   满足结合律和交换律，任何合并序列的结果都等于到达该副本的全部更新效果之集合的并，与顺序和分组无关；由于 ⊔ 幂等，
   重复收到同一状态不改变任何东西。因此收到同一组更新的两个副本持有同一集合的并，即同一状态。我们的测试：1,000
   种随机传播顺序，每种 CRDT 都收敛。

3. **一致性哈希。** 证明加入第 n+1 个节点时期望移动 1/(n+1) 的键，而 h(k) mod n 移动 n/(n+1)。

   *解答。* 圆上有 n + 1 个随机点时，由对称性每个节点的弧期望长度为 1/(n+1)，新节点恰好接管其弧内的键，所以期望移动比例为
   1/(n+1)。取模时：键不动当且仅当 h mod n = h mod (n+1)。若 h 在 n(n+1) 的倍数范围内均匀分布，则 h mod n(n+1) 均匀，
   由中国剩余定理（n 与 n+1 互素），二元组 (h mod n, h mod (n+1)) 在 n(n+1) 个组合上均匀，其中 n 个相等（h mod n(n+1) < n）。
   所以留下的比例为 1/(n+1)，移动 n/(n+1)（n = 10 时为 91%，与测量一致）。

4. **两阶段提交与 Spanner。** 证明若协调者在某参与者投赞成票后崩溃，2PC 会阻塞；并说明提交等待为何使时间戳符合真实时间。

   *解答。* 投了赞成票的参与者已承诺“被告知就提交”，所以不能自行中止（协调者可能已决定提交并告诉了别人）；也不能提交
   （协调者可能因另一参与者投反对票而决定中止）。从同样不确定的其他参与者那里得不到能解决此问题的信息，所以它只能等协调者。
   Spanner：事务 T₁ 取 s₁ = TT.now().latest，直到 TT.now().earliest > s₁ 才报告提交，所以其真实提交时刻 t₁ > s₁。在 T₁
   报告提交后才开始的 T₂，其真实开始时刻 > t₁ > s₁，取 s₂ = TT.now().latest ≥ 其真实开始时刻 > s₁。所以真实时间顺序蕴含
   时间戳顺序。等待时间约为 2ε。

5. **动手。** 让我们的 MapReduce 在主节点崩溃后仍能完成。

   *解答要点。* 主节点的状态就是任务表：每个任务的状态（空闲、进行中、完成）、所在工作机，以及已完成 map 的输出位置。把每次
   变更追加到稳定存储上的日志（或用第 38 部分的 Raft 复制）。重启时重放日志；进行中的任务重置为空闲（其工作机可能也已死），
   工作机已不在的已完成 map 像工作机故障时一样重置。由于任务是确定性的、reduce 采用它拿到的任意一份 map 输出，重复执行不改变结果。
   测试方法：在随机时刻让主节点崩溃，把前二十个词与参考答案比较。

6. **★ 研究。** 为我们的亚稳态模拟器设计一种重试与准入策略，可证明地从任何有限的突发中恢复，同时保留对冲请求的尾延迟收益。

   *讨论。* 一般情形尚未解决。方向：重试预算（重试最多占首次请求的 β 比例）把负载限制在 (1 + β)λ，于是若 (1 + β)λ < μ，
   任何突发之后队列都稳定；丢弃已过截止时间的请求限制了队列中的有用工作；对冲请求计入同一预算。缺少的是对真实客户端
   （超时、退避、多层）的证明，以及对每种策略能承受的最大突发的刻画，最好在我们的模拟器中用对抗性选择的突发来检验。

## Glossary additions

* **quorum** — a set of replicas whose agreement suffices; read and write quorums overlap when R + W > N.
* **sloppy quorum, hinted handoff** — accepting writes on stand-in replicas during failures, delivered later.
* **anti-entropy** — background comparison and repair of replicas, usually with Merkle trees.
* **probabilistically bounded staleness (PBS)** — the probability that a read is stale, against time since the write.
* **consistency model** — what reads may return: linearizable, sequential, causal, session guarantees, eventual.
* **CAP, PACELC** — under a partition choose consistency or availability; else latency or consistency.
* **CRDT** — a replicated data type whose merge is a semilattice join, so replicas converge without coordination.
* **version vector, siblings** — per-replica counters that detect concurrent writes; the concurrent values kept.
* **RGA, tombstone** — a sequence CRDT ordering elements by unique ids; a deleted element kept as a marker.
* **consistent hashing, virtual node** — keys and nodes hashed onto a ring; each node placed many times.
* **hot key, salting** — a key with outsized traffic; splitting it into sub-keys with random suffixes.
* **two-phase commit, commit wait** — atomic commit through a coordinator; Spanner's wait of about 2ε.
* **hybrid logical clock** — (physical time heard of, counter): causal like Lamport, close to real time.
* **lease, fencing token** — a lock that expires; a number the resource checks to reject a stale holder.
* **straggler, backup task** — a slow task; a duplicate run near the end, first result wins.
* **tail latency, hedged request** — high percentiles; a second request sent after a delay.
* **power of two choices** — route each request to the less loaded of two random servers.
* **gray failure, metastable failure** — partial failures that evade detection; a bad state sustained by the
  system's own reaction.
* **phi accrual detector** — suspicion as −log₁₀ of the probability of the current silence.
* **CALM, invariant confluence** — monotonic programs need no coordination; invariants that merges preserve.

## Sources

* M. Kleppmann, *Designing Data-Intensive Applications* (2017), chs. 5–9.
* L. A. Barroso, U. Hölzle and P. Ranganathan, *The Datacenter as a Computer* (3rd ed., 2018).
* J. Saltzer and F. Kaashoek, *Principles of Computer System Design* (2009); M. van Steen and A. Tanenbaum,
  *Distributed Systems* (4th ed., 2023).
* G. DeCandia et al., "Dynamo: Amazon's highly available key-value store", SOSP 2007.
* P. Bailis et al., "Probabilistically bounded staleness for practical partial quorums", VLDB 2012; "Coordination
  avoidance in database systems", VLDB 2014.
* S. Gilbert and N. Lynch, "Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web
  services", 2002; D. Abadi, "Consistency tradeoffs in modern distributed database system design", 2012.
* M. Shapiro, N. Preguiça, C. Baquero and M. Zawirski, "Conflict-free replicated data types", SSS 2011; H.-G. Roh et
  al., "Replicated abstract data types", JPDC 2011; M. Kleppmann et al., "Local-first software", Onward! 2019.
* R. Merkle, "A digital signature based on a conventional encryption function", CRYPTO 1987.
* D. Karger et al., "Consistent hashing and random trees", STOC 1997; J. Lamping and E. Veach, "A fast, minimal
  memory, consistent hash algorithm", 2014; I. Stoica et al., "Chord", SIGCOMM 2001; P. Maymounkov and D. Mazières,
  "Kademlia", IPTPS 2002.
* J. Gray, "Notes on data base operating systems", 1978; J. Corbett et al., "Spanner", OSDI 2012; S. Kulkarni et
  al., "Logical physical clocks", OPODIS 2014.
* M. Burrows, "The Chubby lock service", OSDI 2006; P. Hunt et al., "ZooKeeper", USENIX ATC 2010.
* J. Dean and S. Ghemawat, "MapReduce", OSDI 2004; M. Zaharia et al., "Resilient distributed datasets", NSDI 2012;
  T. Akidau et al., "The dataflow model", VLDB 2015.
* J. Dean and L. A. Barroso, "The tail at scale", CACM 2013; M. Mitzenmacher, "The power of two choices in randomized
  load balancing", 1996; Y. Azar et al., "Balanced allocations", STOC 1994.
* J. Dean, "Designs, lessons and advice from building large distributed systems", LADIS 2009 keynote.
* N. Hayashibara et al., "The φ accrual failure detector", SRDS 2004.
* P. Huang et al., "Gray failure", HotOS 2017; N. Bronson et al., "Metastable failures in distributed systems",
  HotOS 2021; L. Huang et al., "Metastable failures in the wild", OSDI 2022.
* J. M. Hellerstein and P. Alvaro, "Keeping CALM", CACM 2020; T. Ameloot, F. Neven and J. Van den Bussche, "Relational
  transducers for declarative networking", JACM 2013; P. Mahajan, L. Alvisi and M. Dahlin, "Consistency,
  availability, and convergence", UT Austin TR 2011; W. Lloyd et al., "COPS", SOSP 2011.
* P. Gibbons and E. Korach, "Testing shared memories", SIAM J. Comput. 1997; K. Kingsbury and P. Alvaro, "Elle",
  VLDB 2020.
