# Computer Science, Built — Part 38: Distributed Systems I: Agreement

Part 38 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act VII, *Many Machines*. With no shared clock and failures that
look like slowness, agreeing on even one bit is provably impossible in general (FLP). Paxos and Raft agree anyway, by
giving up a guarantee that FLP says no one can have. We build Raft and attack it a thousand times.

The instruments are in `explainer/cs/dist/` (tested in `tests/test_cs38_dist.py`):
* `clocks.py`: random executions; Lamport and vector clocks; happened-before by transitive closure, and the
  characterization theorem checked pair by pair; NTP's offset and delay; a bank of processes on FIFO channels with a
  Chandy–Lamport snapshot, against a naive survey.
* `consensus.py`: an exhaustive explorer of tiny asynchronous protocols (every delivery order, up to f crashes) giving
  valency, disagreement and blocking; FloodSet checked against every crash pattern (who, which round, which messages
  escape); Ben-Or's randomized consensus; single-decree Paxos with several proposers, NACKs, loss and optional backoff.
* `raft.py`: Raft on a simulated network (delays, loss, partitions, crash–recovery with persistent term, vote and
  log); the four invariants of the paper's Figure 3 checked after every event; three plantable bugs (committing
  old-term entries by counting, voting without the log check, forgetting the vote on restart); random and targeted
  fault injection; randomization of election timeouts.
* `byzantine.py`: OM(m) with every lying strategy enumerated; message counts for OM, PBFT and HotStuff; Nakamoto's
  double-spend probability, the exact (negative-binomial) value and a simulation; Eyal and Sirer's selfish mining by
  formula and simulation.

## Chapters

* **Hook.** Five Pebbles run Raft for nine seconds through a crashed leader, a partition, a restart and another
  crash: 236 commands committed in 15 terms, every invariant holding; a new leader 0.22 s after the first crash. A
  thousand random storms: no violation. Lamport's definition; FLP.
* **1. Partial failure.** Partial failure, clock drift, asynchrony. The two generals (Gray 1978) as a sequence
  diagram; messengers needed for 99% and 99.9999% confidence (2 and 6 at 10% capture, 7 and 20 at 50%); the
  impossibility by induction on messages.
* **2. Time without a clock.** NTP's offset θ and delay δ; with 70 ms out and 10 ms back the estimate is 30 ms off,
  undetectably. Happened-before on a space–time diagram; Lamport clocks and the clock condition; vector clocks and the
  characterization theorem, checked on 200 executions (42,170 pairs, all exact; Lamport numbers ordered 19,143 of the
  22,869 concurrent pairs).
* **3. Snapshots.** Consistent and inconsistent cuts; Chandy and Lamport's markers. A bank of four: balances 748 plus
  252 in transit = 1,000; a naive survey 747; 50 of 50 snapshots exact, surveys from 610 to 1,006.
* **4. Models and consensus.** Crash, crash-recovery, omission, Byzantine; synchronous, asynchronous, partially
  synchronous (DLS 1988); failure detectors (Chandra and Toueg). Agreement, validity, termination. FloodSet against
  every crash pattern: f rounds fail, f + 1 succeed (n = 3, f = 1: 13 and 25 patterns; n = 5, f = 2: 10,401 and
  23,281); the counterexample; the proofs of both directions.
* **5. FLP.** Valency. Two protocols explored exhaustively: "wait for n − f" has three bivalent inputs and can
  disagree; "wait for all" never disagrees and can block. The two lemmas and the theorem. Three ways around. Ben-Or on
  five processes with two crashed: mean 4.1 rounds, 75% within 5, longest 27 of 2,000 runs.
* **6. Paxos.** Prepare/promise, accept/accepted; the safety invariant by induction on ballots. Duelling proposers
  (35 ms timers, 5% loss, 400 runs each): with four proposers retrying at once 33.6 ballots and 224 ms, with random
  backoff 4.3 and 37 ms; always safe. Multi-Paxos, Chubby, Viewstamped Replication.
* **7. Raft.** Terms and roles; elections; randomized timeouts (identical timeouts: no leader in 300 of 300 runs;
  2% spread: 249 of 300 never, 10.7 terms otherwise; [T, 2T]: 1.07 terms, median 177 ms). Log replication and log
  matching; the commit rule, the election restriction and leader completeness; Figure 8.
* **8. Our Raft, attacked.** The four invariants. The opening storm as commit indexes. A thousand storms each:
  correct Raft 0 broken (random or targeted); counting old-term entries 1; skipping the log check 877; forgetting the
  vote 0 with random faults, 87 with one targeted fault. Replicated state machines (Schneider 1990); linearizable
  reads, ReadIndex and leases.
* **9. Byzantine generals.** The three-general impossibility; OM(m) checked over every lying strategy (3 generals and
  1 traitor broken; 4 and 1 always agree; 4 and 2 broken; 7 and 2 agree); n ≥ 3f + 1 by simulation; signatures.
  PBFT's normal case on four replicas; messages for n = 100: OM ≈ 10⁶⁶, PBFT 19,800, HotStuff 594.
* **10. Nakamoto consensus.** Sybil attacks, proof of work, the longest chain. Double-spend risk: Nakamoto's formula,
  the exact value and 200,000 simulated races (q = 0.1, z = 6: 0.024%, 0.059%, 0.062%); confirmations for 0.1%: 6, 13,
  32, 133 against 10–40% attackers. Selfish mining on Eyal and Sirer's curve (profitable above 1/3, or 1/4 with
  γ = 1/2). Energy, proof of stake, finality.
* **11. Frontier: proving and breaking.** TLA⁺ at Amazon, Jepsen, Verdi and IronFleet; our campaign. Lower bounds
  (f + 1 rounds, FLP, 3f + 1, Dolev–Reischuk Ω(n²)); quadratic worst-case BFT in partial synchrony (2022). Four open
  problems.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs38.compute
python -m unittest tests.test_cs38_dist
python tools/build.py cs38
```

## Problems, with solutions

1. **Vector clocks.** Prove that a → b iff V(a) < V(b).

   *Solution.* (⇒) Along each step of a happened-before chain the vector never decreases (local steps increment one
   entry; a receipt takes a maximum that includes the message's vector), and the step to b's own event increments
   b's entry, so V(a) ≤ V(b) with V(a) ≠ V(b). (⇐) Let a be on process i, with V(a)[i] = k: a is the k-th event of i.
   If V(a) ≤ V(b) then V(b)[i] ≥ k. Entry i of any vector only grows by i's own events or by maxima with vectors that
   carried i's count along messages, so b's knowledge of "k events of i" must have travelled from i's k-th event, a,
   to b along a chain of program order and messages: a → b (or a = b, excluded since V(a) ≠ V(b)). Our check: 200
   executions, 42,170 pairs, no exception.

2. **FloodSet.** Prove that f + 1 rounds solve consensus with up to f crashes, and give a run defeating f rounds for
   n = 4, f = 2.

   *Solution.* With f + 1 rounds and at most f crashes, some round r has no crash. In round r every process alive
   sends its set W to every other alive process, so after r all live processes hold the union of the live sets, the
   same set. Later rounds only merge equal sets (and sets of processes that crash, which are subsets of the union), so
   the sets stay equal; all decide its minimum, a proposed value. For f rounds: inputs (0, 1, 1, 1); in round 1, P0
   crashes after sending only to P1; in round 2, P1 crashes after sending only to P2. Now P2 has seen 0 and P3 has
   not: P2 decides 0, P3 decides 1 (our checker's counterexample).

3. **Paxos's invariant.** Prove that if v is chosen in ballot b, every accept request with ballot b′ > b carries v.

   *Solution.* Strong induction on b′. The proposer of b′ received promises from a majority Q. The majority A that
   accepted (b, v) intersects Q in an acceptor a; a accepted (b, v) before promising b′ (it would have refused b
   after promising b′ > b), so its promise reported an accepted ballot c_a with b ≤ c_a < b′. Hence the highest
   reported ballot c satisfies b ≤ c < b′, and the proposer must use the value accepted in c. If c = b that value is
   v (one value per ballot); if c > b, the accept request of ballot c carried v by the induction hypothesis. So b′'s
   accept request carries v; and any value chosen in a later ballot was in such a request, so equals v.

4. **Three generals.** Show that OM(1) fails for three generals and one traitor, and that no protocol succeeds.

   *Solution.* OM(1): commander loyal sends "attack"; traitor L1 relays "retreat" to L2; L2 sees one of each and its
   majority with ties to retreat decides retreat, disobeying a loyal commander (our exhaustive check found this as
   the only strategy needed). Impossibility: suppose a protocol works. World A: commander loyal orders attack, L1
   traitor behaves as if it had received retreat. World B: commander traitor tells L2 attack and L1 retreat, L1 loyal.
   World C: commander loyal orders retreat, L2 traitor behaves as if it had received attack. L2's view is the same in
   A and B, and it must attack in A, so it attacks in B. L1's view is the same in B and C, and it must retreat in C,
   so it retreats in B. In B the loyal lieutenants disagree: contradiction. (The same scaling argument gives n ≥ 3f + 1.)

5. **Build: membership changes.** Add membership change to our Raft and extend the checker.

   *Solution sketch.* The simplest safe method changes one server at a time (Ongaro's thesis, §4): a configuration
   entry in the log takes effect as soon as a server appends it (not when committed), and a leader will not start a
   second change until the first commits. Any two majorities of configurations differing by one server intersect, so
   election safety holds. Extend `Cluster` with `add(i)`/`remove(i)` as special commands, make majorities computed
   from the latest configuration in each server's log, and add an invariant: no two leaders in a term even across
   configurations. A removed leader must step down after committing its removal. Fault-inject around the moments the
   configuration entry is appended and committed.

6. ★ **Research: finding bugs fast.** Design a fault-injection strategy that exposes all three planted bugs in few
   runs, and argue it generalizes.

   *What is known.* Our numbers: random storms found the Figure 8 bug in 1 of 1,000 runs and the forgotten vote in
   none; crashing voters immediately after they vote found the latter in 87 of 1,000. Approaches that work in practice:
   targeting the moments between persistent-state changes and messages (crash after vote, crash after append before
   acknowledgement); lineage-driven fault injection (Alvaro et al., 2015), which removes the messages a successful
   result depended on; coverage-guided search over schedules; deterministic simulation (FoundationDB) that makes every
   failing seed replayable. The Figure 8 bug needs a leader to replicate an old-term entry to a majority, crash, and
   be replaced by a leader that lacks it: a strategy that preferentially crashes a leader just after it has replicated
   an entry from an earlier term to a bare majority should find it far faster than random. What is open is a theory:
   for which classes of bugs does a strategy of bounded "depth" (Burckhardt et al.'s probabilistic concurrency testing,
   2010) guarantee detection in a polynomial number of runs?

## 习题与解答

1. **向量时钟。** 证明 a → b 当且仅当 V(a) < V(b)。

   *解答。*（⇒）沿 happened-before 链的每一步，向量都不会减小（本地事件给一个分量加一；接收取最大值，而最大值包含消息携带的向量），
   而到 b 自身事件的那一步会给 b 的分量加一，所以 V(a) ≤ V(b) 且 V(a) ≠ V(b)。（⇐）设 a 在进程 i 上，V(a)[i] = k：a 是 i 的第
   k 个事件。若 V(a) ≤ V(b)，则 V(b)[i] ≥ k。任何向量的第 i 个分量只会因 i 自己的事件增长，或者因与沿消息携带了 i 的计数的向量取
   最大值而增长，所以 b 对“i 的 k 个事件”的了解一定是沿着程序顺序与消息组成的链，从 i 的第 k 个事件 a 传到 b 的：a → b（a = b 的
   情形被 V(a) ≠ V(b) 排除）。我们的检验：200 次执行，42,170 对事件，无一例外。

2. **FloodSet。** 证明 f + 1 轮能在至多 f 次崩溃下解决共识，并对 n = 4、f = 2 给出一个击败 f 轮的运行。

   *解答。* f + 1 轮、至多 f 次崩溃时，必有某一轮 r 没有崩溃。在第 r 轮，每个存活进程都把自己的集合 W 发给每个其他存活进程，所以
   r 之后所有存活进程都持有存活集合的并集，是同一个集合。之后的轮次只合并相等的集合（以及崩溃进程的集合，它们都是该并集的子集），
   所以集合保持相等；大家都决定它的最小值，一个被提议过的值。f 轮的反例：输入 (0, 1, 1, 1)；第 1 轮 P0 只发给 P1 后崩溃；第 2 轮
   P1 只发给 P2 后崩溃。此时 P2 见过 0 而 P3 没有：P2 决定 0，P3 决定 1（我们的检查器找到的反例）。

3. **Paxos 的不变式。** 证明：若 v 在选票 b 中被选定，则每个选票 b′ > b 的 accept 请求都携带 v。

   *解答。* 对 b′ 作强归纳。b′ 的提议者收到了某个多数派 Q 的承诺。接受了 (b, v) 的多数派 A 与 Q 相交于某个接受者 a；a 在承诺 b′
   之前接受了 (b, v)（承诺 b′ > b 之后它会拒绝 b），所以它的承诺报告了一个已接受的选票 c_a，满足 b ≤ c_a < b′。于是报告中最高的选票
   c 满足 b ≤ c < b′，提议者必须使用 c 中被接受的值。若 c = b，这个值就是 v（每个选票只有一个值）；若 c > b，由归纳假设，选票 c 的
   accept 请求携带 v。所以 b′ 的 accept 请求携带 v；之后任何选票中被选定的值都出自这样的请求，因而等于 v。

4. **三将军。** 证明 OM(1) 对三个将军、一个叛徒失败，并且没有协议能成功。

   *解答。* OM(1)：忠诚的指挥官发出“进攻”；叛徒 L1 向 L2 转述“撤退”；L2 各收到一个，多数（平局取撤退）决定撤退，违背了忠诚的指挥
   官（我们的穷举检查只需这一种策略就找到了它）。不可能性：假设某协议可行。世界 A：指挥官忠诚，命令进攻，叛徒 L1 装作收到的是撤退。
   世界 B：叛徒指挥官对 L2 说进攻、对 L1 说撤退，L1 忠诚。世界 C：指挥官忠诚，命令撤退，叛徒 L2 装作收到的是进攻。L2 在 A 与 B 中
   的所见相同，而在 A 中它必须进攻，所以在 B 中也进攻。L1 在 B 与 C 中的所见相同，而在 C 中它必须撤退，所以在 B 中也撤退。在 B 中两个
   忠诚的副将意见不一：矛盾。（同样的放缩论证给出 n ≥ 3f + 1。）

5. **动手：成员变更。** 给我们的 Raft 加上成员变更，并扩展检查器。

   *解答要点。* 最简单的安全方法是一次只变更一台服务器（Ongaro 的博士论文第 4 章）：日志中的配置条目在服务器追加它时立即生效（而不
   是提交时），并且在第一次变更提交之前，领导者不开始第二次变更。相差一台服务器的两个配置的任意两个多数派都相交，所以选举安全成立。
   给 `Cluster` 加上作为特殊命令的 `add(i)`/`remove(i)`，让多数派按每台服务器日志中最新的配置计算，并加一条不变式：即使跨越配置，同
   一任期也不能有两个领导者。被移除的领导者在提交自己的移除后必须下台。在配置条目被追加和被提交的时刻附近注入故障。

6. ★ **研究：快速找到错误。** 设计一种故障注入策略，在很少的运行次数内暴露全部三个植入的错误，并论证它能推广。

   *已知结果。* 我们的数据：随机风暴在 1,000 次运行中只有 1 次暴露了 Figure 8 错误，遗忘投票则一次也没有；让投票者在投票后立即崩溃，
   在 1,000 次中有 87 次暴露了后者。实践中有效的方法：瞄准持久状态改变与消息之间的时刻（投票后崩溃、追加后确认前崩溃）；基于血缘的故障
   注入（Alvaro 等，2015），去掉一个成功结果所依赖的消息；对调度做覆盖率引导的搜索；确定性模拟（FoundationDB），让每个失败的种子都能
   重放。Figure 8 错误需要一个领导者把旧任期的条目复制到多数派、崩溃，再被一个缺少该条目的领导者取代：优先在领导者刚把旧任期条目复制
   到恰好多数派之后让它崩溃的策略，应当比随机快得多。未解决的是理论：对哪些类别的错误，有界“深度”的策略（Burckhardt 等 2010 年的概率
   并发测试）能保证在多项式次运行内发现它们？

## Glossary additions

* **partial failure**: some components fail while others continue; **asynchrony**: no bound on message delay.
* **happened-before** (→): the causal order of program order and messages; **concurrent** (∥): neither precedes.
* **Lamport clock**: a counter consistent with →; **vector clock**: a vector that characterizes →.
* **consistent cut, snapshot**: a global state in which every received message was sent; **Chandy–Lamport**: markers
  on FIFO channels.
* **crash, crash-recovery, omission, Byzantine**: failure models; **synchronous, partially synchronous**: timing
  models; **failure detector**: an oracle that suspects processes.
* **consensus**: agreement, validity, termination; **valency**: which decisions remain reachable; **bivalent**: both.
* **FLP**: no deterministic consensus in an asynchronous system with one crash.
* **Paxos**: ballots, promises and majorities; **Multi-Paxos**: one instance per log slot with a stable leader.
* **Raft**: terms, elections, log replication; **log matching, leader completeness, election restriction**.
* **replicated state machine**: deterministic replicas fed one agreed sequence of commands; **lease**; **fencing
  token**.
* **Byzantine generals, OM(m)**; **n ≥ 3f + 1**; **PBFT, view change, HotStuff, threshold signature**.
* **Sybil attack**: one party posing as many; **proof of work, longest chain, confirmations, selfish mining, proof of
  stake, finality**.
* **Jepsen, TLA⁺, model checking, deterministic simulation**: ways to find distributed bugs.

## Sources

* N. Lynch, *Distributed Algorithms*; H. Attiya and J. Welch, *Distributed Computing*.
* C. Cachin, R. Guerraoui and L. Rodrigues, *Introduction to Reliable and Secure Distributed Programming*.
* M. van Steen and A. S. Tanenbaum, *Distributed Systems*; M. Kleppmann, *Designing Data-Intensive Applications*,
  ch. 8–9.
* J. Gray, "Notes on Data Base Operating Systems" (1978) (the two generals).
* L. Lamport, "Time, Clocks, and the Ordering of Events in a Distributed System", CACM (1978).
* C. J. Fidge (1988); F. Mattern, "Virtual Time and Global States of Distributed Systems" (1988).
* D. L. Mills, "Internet Time Synchronization: the Network Time Protocol", IEEE Trans. Comm. (1991).
* K. M. Chandy and L. Lamport, "Distributed Snapshots", ACM TOCS (1985).
* M. Fischer and N. Lynch, "A Lower Bound for the Time to Assure Interactive Consistency", IPL (1982); D. Dolev and
  H. R. Strong, "Authenticated Algorithms for Byzantine Agreement", SIAM J. Comput. (1983).
* M. Fischer, N. Lynch and M. Paterson, "Impossibility of Distributed Consensus with One Faulty Process", JACM (1985).
* M. Ben-Or, "Another Advantage of Free Choice", PODC (1983).
* C. Dwork, N. Lynch and L. Stockmeyer, "Consensus in the Presence of Partial Synchrony", JACM (1988).
* T. D. Chandra and S. Toueg, "Unreliable Failure Detectors for Reliable Distributed Systems", JACM (1996).
* L. Lamport, "The Part-Time Parliament", ACM TOCS (1998); "Paxos Made Simple" (2001).
* B. Oki and B. Liskov, "Viewstamped Replication", PODC (1988).
* T. Chandra, R. Griesemer and J. Redstone, "Paxos Made Live", PODC (2007); M. Burrows, "The Chubby Lock Service",
  OSDI (2006).
* F. B. Schneider, "Implementing Fault-Tolerant Services Using the State Machine Approach", ACM Computing Surveys
  (1990).
* D. Ongaro and J. Ousterhout, "In Search of an Understandable Consensus Algorithm", USENIX ATC (2014); D. Ongaro,
  *Consensus: Bridging Theory and Practice*, PhD thesis (2014).
* L. Lamport, R. Shostak and M. Pease, "The Byzantine Generals Problem", ACM TOPLAS (1982).
* G. Bracha and S. Toueg, "Asynchronous Consensus and Broadcast Protocols", JACM (1985); D. Dolev and R. Reischuk,
  "Bounds on Information Exchange for Byzantine Agreement", JACM (1985).
* M. Castro and B. Liskov, "Practical Byzantine Fault Tolerance", OSDI (1999); M. Yin et al., "HotStuff: BFT
  Consensus with Linearity and Responsiveness", PODC (2019); A. Lewis-Pye, "Quadratic Worst-Case Message Complexity
  for State Machine Replication in the Partial Synchrony Model" (2022).
* S. Nakamoto, "Bitcoin: A Peer-to-Peer Electronic Cash System" (2008); M. Rosenfeld, "Analysis of Hashrate-Based
  Double Spending" (2014); I. Eyal and E. G. Sirer, "Majority Is Not Enough: Bitcoin Mining Is Vulnerable", FC (2014).
* C. Newcombe et al., "How Amazon Web Services Uses Formal Methods", CACM (2015); K. Kingsbury, Jepsen analyses
  (2013–); J. R. Wilcox et al., "Verdi", PLDI (2015); C. Hawblitzel et al., "IronFleet", SOSP (2015).
* P. Alvaro, J. Rosen and J. M. Hellerstein, "Lineage-driven Fault Injection", SIGMOD (2015).
