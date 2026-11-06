# Computer Science, Built — Part 33: Concurrency

Part 33 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the third part of Act VI, *One Machine, Many Programs*. Two threads each add one
to a counter, and the count goes up by one. Mutual exclusion can be built from plain reads and writes (Peterson)
until the hardware reorders them. The fix has two parts: a theory of memory models, and a hierarchy that orders
synchronization primitives by power, at whose top compare-and-swap can implement every concurrent object. Pebble gains
an atomic extension and PebbleOS gains threads.

The instruments are in `explainer/cs/conc/` (tested in `tests/test_cs33_conc.py`):
* `mc.py`, **an exhaustive interleaving model checker**:
  - programs in a tiny assembly language, one instruction list per thread (loads and stores, indexed access,
    arithmetic, branches, `cas`, `tas`, `fai`, blocking `lock` and semaphore `P`/`V`, fences, critical-section
    markers, outputs);
  - three memory models: **SC** (interleaving), **TSO** (a FIFO store buffer per thread, x86) and **PSO** (one FIFO
    per thread and variable, a stand-in for Arm's weaker model); atomics and fences drain the buffer;
  - breadth-first search over states, so every violation comes with a shortest schedule; deadlock detection;
    counting schedules of loop-free programs;
  - the part's programs: counter++, the naive flag lock, Peterson (with fences for TSO and PSO), the bakery, the
    store-buffering and message-passing litmus tests, the dining philosophers, the bounded buffer, consensus by
    registers, test-and-set and compare-and-swap, and the Treiber stack with a plain and a tagged CAS;
* `lin.py`: a linearizability checker (Wing and Gong's search with Lowe's memo) for registers, counters, queues and
  stacks; random correct and buggy histories;
* `locks.py`: TAS, TTAS, TTAS with backoff, ticket and MCS spin locks on Part 10's MESI caches, with a single bus
  that each transaction occupies for 8 cycles.

Pebble's **atomic extension** (`explainer/cs/pebble/isa.py`, `emu.py`): `cas rd, rs1, rs2` and `amoadd rd, rs1, rs2`
on opcodes 52 and 53, the two that Part 6 reserved; kept out of `OPS`, so Part 6's tables are unchanged.
**PebbleOS threads** (`explainer/cs/os/vmos.threads_vm`): PCBs that share one page table, each with its own stack.

Measured on this machine (`videos/cs/cs33/conc.c`, and the compiler):
* a counter incremented 10⁷ times by 1, 2 and 4 threads: plain, atomic and under a mutex;
* TAS, TTAS, ticket, MCS and `pthread_mutex` with 1, 2 and 4 threads;
* creating a thread against forking a process; Intel RTM transactions;
* ThreadSanitizer on the racy counter, on an atomic load-then-store, and on an atomic increment;
* `gcc -O2` on a spin loop over a plain flag and over an atomic one.

## Chapters

* **Hook.**
  - Four threads add 10⁷ each to one counter on this machine: 10,547,788 instead of 40,000,000. With one thread,
    exactly right.
  - Where an addition goes: load, add, store, interleaved.
* **1. Why concurrency.**
  - Overlap: two requests in 7 units instead of 12. Parallelism since about 2005.
  - Processes against threads; a thread created and joined in 41 µs here, a process forked and reaped in 179 µs.
* **2. The race.**
  - The tree of all 20 schedules of two increments: 2 give 2, 18 give 1.
  - The model checker. For k = 1 to 4 increments each: 20, 924, 48,620 and 2,704,156 schedules (C(6k, 3k)), but
    only 22, 138, 585 and 1,846 states. The count can end as low as 2 for any k ≥ 2. Fetch-and-add or a lock: only
    2k.
* **3. Mutual exclusion from reads and writes.**
  - Safety, progress, bounded waiting. The naive flag lock broken in 8 steps.
  - Peterson (1981) and its proof; Dekker (1965). Lamport's bakery (1974), any n, safe registers.
  - Peterson's state space: 258 states for one round; 24 of 25 region pairs reachable, never (inside, inside). The
    bakery checked with 644 states for 2 threads and 92,745 for 3. Burns and Lynch's n-register bound.
* **4. Peterson meets the store buffer.**
  - Store buffers; the store-buffering test (Part 10's run on this machine: both 0 in 942,588 of 10⁶ runs, never
    with a fence).
  - Under TSO the checker breaks Peterson in 10 steps; one fence repairs it. Under PSO it needs a second fence
    between the two stores. Message passing fails under PSO.
* **5. Hardware locks.**
  - TAS, TTAS, ticket and MCS; the MCS queue.
  - Simulated, 32 cores: bus transactions per handoff TAS 63, TTAS 46, ticket 31, MCS 7; cycles per handoff 505
    against 59; fairness 0.20 against 0.90.
  - This machine (4 cores): TAS 7 ns alone, 105 ns with 4 threads; MCS 18 and 200; `pthread_mutex` 20 and 69.
* **6. Semaphores.**
  - P and V; mutex, counting, signalling.
  - The bounded buffer: the count always ends at 0 (188 states); without the mutex, anywhere from −2 to 2.
  - Readers and writers, and starvation; *The Little Book of Semaphores*.
* **7. Monitors and condition variables.**
  - Hoare and Brinch Hansen; Mesa semantics: with `if`, a consumer takes from an empty buffer after 29 steps; with
    `while`, safe in 741 states.
* **8. Deadlock.**
  - Five philosophers deadlock in 5 steps; with one philosopher reversed, none in 3,216 states.
  - Coffman's four conditions; lock order and `lockdep`.
  - The banker's algorithm on Silberschatz's example: safe order P1, P3, P0, P2, P4; P1's (1, 0, 2) granted; P0's
    (0, 2, 0) refused as unsafe.
* **9. Memory models.**
  - The compiler reorders too: `gcc -O2` turns `while (!done);` over a plain int into a jump to itself.
  - Happens-before and data races. DRF ⇒ SC (Adve and Hill 1990): store buffering with every access locked gives
    only SC's outcomes under TSO and PSO.
  - C++ and Java atomics, release and acquire; out-of-thin-air values.
* **10. Linearizability.**
  - Intervals and instants; a linearizable queue history and one that is not.
  - Sequential consistency against linearizability; locality.
  - The checker on random histories: correct objects always pass; with stale answers a third of queue histories and
    nearly all counter histories fail.
* **11. Lock-free data structures.**
  - Treiber's stack (1986). The ABA problem found by the checker (23 steps); a tagged CAS removes it (1,536 states).
  - Hazard pointers, epochs, RCU; the Michael–Scott queue; wait-free, lock-free, obstruction-free.
* **12. Consensus numbers.**
  - Test-and-set solves 2-consensus (52 states) and fails for 3; CAS solves 3 (145 states).
  - Herlihy's hierarchy; universality as a log of agreements; why registers cannot solve it: valency.
* **13. Transactional memory, channels and actors.**
  - Hardware transactions: 999,927 of 10⁶ commit on this machine; TSX's troubles.
  - CSP and Go, actors and Erlang, async/await.
* **14. Concurrency bugs in the wild.**
  - Therac-25, Mars Pathfinder, the 2003 blackout.
  - ThreadSanitizer finds the hook's race; with an atomic load-then-store it is silent and the count is still wrong
    (1,225,222 of 2,000,000); an atomic increment gives 2,000,000.
* **15. PebbleOS gains threads and CAS.**
  - `cas` and `amoadd`; threads as PCBs sharing a page table; a CAS lock that yields.
  - Two threads, 2,000 increments each: plain load-add-store gives 2,765 at quantum 500 and 2,810 at 3,000 (4,000 at
    97, by luck); `amoadd` and the lock always 4,000.
  - The quantum sweep: every one of 75 quanta from 40 to 3,000 loses updates.
* **16. Frontier: checking concurrent programs.**
  - Linearizability checking is NP-complete; our checker's cost on random queue histories.
  - Weak-memory verification: 1,487, 21,169 and 61,051 states for Peterson under SC, TSO and PSO.
  - Laws of order, fast wait-free structures, PCT. Open problems. Outro.

## Build

```bash
python -m videos.cs.cs33.compute           # every number in the part (about three minutes)
python tools/build.py cs33 -q l            # a 480p preview
python tools/build.py cs33                 # 1080p
```

## Problems, with solutions

1. **The counter's minimum.** Prove that two threads each doing k ≥ 2 increments, load-add-store, can leave the
   counter at 2, and never below 2.

   *Solution.* Every store writes one more than a value its thread loaded, so every store writes at least 1.
   - *Never below 2.* The final value is the last store, say by thread X, of v + 1, where v is what X's last load
     read. X has done at least one increment before this one, so it had already stored a value of at least 1 before
     its last load. Every later store also writes at least 1. So X's last load read at least 1, and the final value
     is at least 2.
   - *Exactly 2 is reachable.* A loads 0 and stalls. B does k − 1 complete increments. A stores 1. B loads 1 and
     stalls. A does its remaining k − 1 increments. B adds and stores 2. For k = 1 the same argument fails (X has no
     earlier store), and indeed 1 is reachable, as the tree of 20 schedules shows.

2. **Peterson's bounded waiting.** Prove that a waiting thread enters after at most one entry of the other.

   *Solution.* Suppose P0 is waiting: it has set flag0 = 1 and turn = 1, and it waits while flag1 = 1 and
   turn = 1. If P1 enters, leaves (setting flag1 = 0) and comes back, its entry protocol sets turn = 0. From then on
   P0's condition is false (turn ≠ 1), so P0 can enter at its next look, while P1 waits (flag0 = 1 and turn = 0).
   P1 cannot pass P0 a second time. So the bypass bound is 1.

3. **The bakery with unreliable reads.** Show that the bakery algorithm is correct even if a read that overlaps a
   write may return any value.

   *Solution.* The key lemma: if Pi is in its critical section and Pk has finished choosing (number[k] ≠ 0, written
   and not being rewritten), then (number[i], i) < (number[k], k).
   - Pi, before entering, waited for choosing[k] = 0, then read number[k] and found it 0, or (number[i], i) smaller.
   - If Pk's choosing ended before Pi's read of choosing[k], then Pi's read of number[k] did not overlap Pk's write,
     so it read the true value, and the comparison was correct.
   - Otherwise Pk began choosing after Pi read choosing[k] = 0, so after Pi had finished writing number[i]; Pk's
     reads of number[i] did not overlap that write, so Pk saw number[i] and chose a larger number.

   Two threads in the critical section would each have the smaller pair, a contradiction. Only the choosing flags
   and finished writes are relied on, never a value read during a write.

4. **Queues have consensus number 2.** Prove that a FIFO queue solves 2-thread consensus, and cannot solve
   3-thread consensus.

   *Solution.*
   - *Two threads.* Initialise the queue to (WIN, LOSE). Each thread writes its proposal to prop[i], then dequeues.
     WIN decides its own value; LOSE decides prop[other], which was written before the other's dequeue.
   - *Not three.* Suppose a protocol for A, B and C. Take a critical state: A's next step makes the decision 0-valent,
     B's makes it 1-valent. Both steps must be on the same queue (steps on different objects commute).
     - Both dequeue: the two orders leave the same queue, and differ only in which of A and B got which item. Run C
       alone from both states: it sees the same queue and decides the same way. Contradiction.
     - One enqueues and one dequeues on a non-empty queue: the two orders leave the same queue too, since the
       dequeue removes the head and the enqueue adds at the tail. C alone cannot tell them apart.
     - Both enqueue, a then b in one order and b then a in the other: run A alone until it dequeues the item in the
       first of the two positions, then B alone until it dequeues the item in the second. The queue, the only shared
       object A and B touched, now holds the same contents in both executions, so C running alone decides the same in
       both, while their valencies differ. (Herlihy 1991, Theorem 6, has the details of this last case.)

5. **Build: futexes for PebbleOS.** Give PebbleOS `futex_wait` and `futex_wake`, and a mutex that sleeps instead
   of yielding; compare instructions.

   *Solution.*
   - Two system calls. `futex_wait(addr, val)`: with the timer held off, translate addr, and if the word still
     equals val, mark the thread BLOCKED with key = the physical address; otherwise return at once (someone changed
     it). `futex_wake(addr, n)`: mark up to n threads BLOCKED on that key READY.
   - Drepper's mutex ("Futexes are tricky", 2004), with states 0 (free), 1 (held), 2 (held, maybe waiters):
     lock: `c = cas(m, 0 -> 1)`; if c ≠ 0, loop: if c = 2 or `cas(m, 1 -> 2)` ≠ 0, then `futex_wait(m, 2)`;
     `c = cas(m, 0 -> 2)`; until c = 0. Unlock: if `amoadd(m, -1)` ≠ 1 then `m = 0; futex_wake(m, 1)`.
   - Test with chapter 15's two threads. The yielding lock pays a full context switch per failed attempt; the futex
     lock blocks once and is woken once. Counting instructions, at quantum 500 the futex version should cost little
     more than `amoadd`, and much less than the yielding lock's 75,953.

6. ★ **Research: minimum fence insertion.** For a program and TSO or PSO, find the fewest fences that restore a
   safety property. Is it NP-hard for PSO? Solve Peterson, the bakery and Dekker with the checker.

   *Where to start.*
   - The oracle: `explainer/cs/conc/mc.explore(program, "tso" | "pso", invariant)`. A candidate is a set of program
     points at which to insert `("fence",)`; it is correct if the checker finds no violation.
   - Counterexample guidance: each violation trace shows a store and a later load (TSO), or two stores (PSO), of one
     thread that the buffer reordered; any correct fence set must separate at least one such pair in every trace.
     So the problem is a hitting set over the reorderings that matter, found lazily. This is the method of Abdulla et
     al., "Counter-example guided fence insertion under TSO" (TACAS 2012).
   - Hardness: minimum hitting set is NP-hard; does every hitting-set instance arise from some program under PSO? A
     reduction needs a program whose violations correspond to the sets. Compare Kuperstein, Vechev and Yahav,
     "Automatic inference of memory fences" (FMCAD 2010), and Alglave et al., "Don't sit on the fence" (CAV 2014).
   - Experiments: Peterson needs 1 fence per thread under TSO and 2 under PSO (chapter 4); find the minimum for the
     bakery with 2 and 3 threads, and for Dekker, and whether it differs between threads.
   - Beyond fences: cheaper repairs (an atomic exchange instead of a store and a fence), and the cost model when
     fences differ in price.

## 习题与解答

1. **计数器的最小值。** 证明：两个线程各做 k ≥ 2 次“读—加—写”递增时，计数器可能停在 2，而且绝不会低于 2。

   *解答。* 每次存储写入的都是本线程读到的某个值加一，所以每次存储写入的值至少为 1。最终值是最后一次存储，设由线程 X 写入
   v + 1，v 是 X 最后一次读到的值。X 在这之前至少完成过一次递增，所以在最后一次读之前已经存储过至少为 1 的值，之后的任何存储也
   至少为 1。于是 X 最后一次读到的至少为 1，最终值至少为 2。可达性：A 读到 0 后停住；B 完成 k − 1 次递增；A 存入 1；B 读到 1
   后停住；A 完成其余 k − 1 次递增；B 加一并存入 2。k = 1 时论证失效（X 没有更早的存储），1 确实可达，正如 20 种调度的树所示。

2. **Peterson 的有界等待。** 证明：等待中的线程最多等对方进入一次。

   *解答。* 设 P0 在等待：已置 flag0 = 1、turn = 1，并在 flag1 = 1 且 turn = 1 时等待。若 P1 进入、离开（置 flag1 = 0）再回来，
   它的进入协议会置 turn = 0。此后 P0 的等待条件不成立（turn ≠ 1），下次检查即可进入，而 P1 在 flag0 = 1 且 turn = 0 时等待。
   P1 不可能第二次越过 P0，所以越过次数的上界是 1。

3. **读不可靠时的面包店算法。** 证明：即使与写重叠的读可以返回任意值，面包店算法仍然正确。

   *解答。* 关键引理：若 Pi 在临界区，而 Pk 已选完号码（number[k] ≠ 0，已写好且不在改写），则 (number[i], i) < (number[k], k)。
   Pi 进入前等到 choosing[k] = 0，然后读 number[k]，发现为 0，或 (number[i], i) 更小。若 Pk 的选号在 Pi 读 choosing[k] 之前
   结束，Pi 对 number[k] 的读不与 Pk 的写重叠，读到真实值，比较正确；否则 Pk 是在 Pi 读到 choosing[k] = 0 之后才开始选号，也就是
   在 Pi 写完 number[i] 之后，Pk 对 number[i] 的读不与那次写重叠，因而看到了 number[i]，选了更大的号码。两个线程同在临界区时
   各自的对都更小，矛盾。证明只依赖 choosing 标志和已完成的写，从不依赖写入过程中读到的值。

4. **队列的共识数为 2。** 证明 FIFO 队列能解决两线程共识，而不能解决三线程共识。

   *解答。* 两线程：把队列初始化为 (WIN, LOSE)。各线程先把提议写入 prop[i]，再出队；拿到 WIN 的决定自己的值，拿到 LOSE 的决定
   prop[另一方]（它在对方出队之前已写好）。三线程不行：设 A、B、C 有一个协议。取一个临界状态：A 的下一步使决定成为 0-价，B 的
   下一步使之成为 1-价。两步必须作用于同一个队列（作用于不同对象的步骤可交换）。两者都出队：两种顺序留下相同的队列，只差在 A、B
   各拿到哪一项；让 C 单独运行，它看到相同的队列，作出相同的决定，矛盾。一个入队、一个对非空队列出队：两种顺序同样留下相同队列
   （出队取头，入队加尾），C 单独运行无法区分。两者都入队，一种顺序先 a 后 b，另一种先 b 后 a：让 A 单独运行到取出前一个位置的项，再让 B 单独运行到取出后一个
   位置的项。A 和 B 只触及这个队列，此时它在两次执行中内容相同，所以单独运行的 C 在两种情况下决定相同，而两者的价不同（这一情形的
   细节见 Herlihy 1991，定理 6）。

5. **动手：给 PebbleOS 加 futex。** 加上 `futex_wait` 和 `futex_wake`，以及一个睡眠而非让出的互斥锁；比较指令数。

   *解答。* 两个系统调用。`futex_wait(addr, val)`：在暂停定时器的情况下翻译 addr，若该字仍等于 val，就把线程标为阻塞，键为物理
   地址；否则立即返回（有人改了它）。`futex_wake(addr, n)`：把最多 n 个阻塞在该键上的线程标为就绪。Drepper 的互斥锁（《Futexes
   are tricky》，2004），状态 0（空闲）、1（被持有）、2（被持有，可能有等待者）：加锁：`c = cas(m, 0 -> 1)`；若 c ≠ 0，循环：
   若 c = 2 或 `cas(m, 1 -> 2)` ≠ 0，则 `futex_wait(m, 2)`；`c = cas(m, 0 -> 2)`；直到 c = 0。解锁：若 `amoadd(m, -1)` ≠ 1，
   则 `m = 0; futex_wake(m, 1)`。用第 15 章的两个线程测试：让出式锁每次失败都付出一次完整的上下文切换；futex 锁阻塞一次、被唤醒
   一次。按指令计数，时间片 500 时 futex 版本应比 `amoadd` 多不了多少，而远少于让出式锁的 75,953 条。

6. ★ **研究：最少栅栏插入。** 对给定程序和 TSO 或 PSO，找出恢复某个安全性质所需的最少栅栏。在 PSO 下它是 NP 难的吗？用检验器
   求解 Peterson、面包店和 Dekker 算法。

   *从哪里开始。* 预言机：`explainer/cs/conc/mc.explore(program, "tso" | "pso", invariant)`。候选方案是在若干程序点插入
   `("fence",)` 的集合；检验器找不到违例即为正确。反例引导：每条违例轨迹都显示同一线程中被缓冲区重排的一对“存储—之后的读取”
   （TSO）或两次存储（PSO）；任何正确的栅栏集合都必须在每条轨迹中至少隔开一对。于是问题成为对“要紧的重排”的命中集问题，可以惰性
   地求出。这是 Abdulla 等人《Counter-example guided fence insertion under TSO》（TACAS 2012）的方法。难度：最小命中集是 NP 难的；
   是否每个命中集实例都能由某个 PSO 下的程序产生？归约需要构造一个程序，使其违例恰好对应那些集合。可参考 Kuperstein、Vechev 与
   Yahav《Automatic inference of memory fences》（FMCAD 2010）和 Alglave 等《Don't sit on the fence》（CAV 2014）。实验：Peterson
   在 TSO 下每线程需要 1 个栅栏，在 PSO 下需要 2 个（第 4 章）；求面包店算法在 2 线程和 3 线程时、以及 Dekker 算法的最小值，以及
   各线程是否不同。更进一步：更便宜的修补（用原子交换代替一次存储加一个栅栏），以及栅栏代价不同时的代价模型。

## Glossary additions

并发 concurrency · 并行 parallelism · 线程 thread · 竞争条件 race condition · 数据竞争 data race · 丢失更新 lost update ·
交错 interleaving · 调度 schedule · 模型检验 model checking · 状态空间 state space · 互斥 mutual exclusion · 临界区 critical
section · 安全性 safety · 活性 liveness · 有界等待 bounded waiting · Peterson 算法 Peterson's algorithm · 面包店算法 bakery
algorithm · 不变式 invariant · 顺序一致性 sequential consistency · 全存储序 total store order · 部分存储序 partial store order ·
存储缓冲区 store buffer · 内存栅栏 memory fence · 内存模型 memory model · 测试并设置 test-and-set · 比较并交换
compare-and-swap · 取并加 fetch-and-add · 自旋锁 spin lock · 票号锁 ticket lock · MCS 锁 MCS lock · 信号量 semaphore ·
有界缓冲区 bounded buffer · 读者—写者 readers–writers · 管程 monitor · 条件变量 condition variable · Mesa 语义 Mesa semantics ·
死锁 deadlock · 哲学家就餐 dining philosophers · 银行家算法 banker's algorithm · 先行发生 happens-before · 无数据竞争 data-race-free ·
获取与释放 acquire and release · 凭空出现的值 out-of-thin-air value · 可线性化 linearizability · 无锁 lock-free · 无等待 wait-free ·
ABA 问题 ABA problem · 风险指针 hazard pointer · 读—复制—更新 read-copy-update · 共识数 consensus number · 普适性 universality ·
价 valency · 事务内存 transactional memory · 通道 channel · 参与者 actor · 竞争检测器 race detector · 向量时钟 vector clock ·
futex

## Sources

*Canon.* Books:
- Herlihy, Shavit, Luchangco & Spear, *The Art of Multiprocessor Programming* (2nd ed., 2020);
- Arpaci-Dusseau & Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*, concurrency;
- Downey, *The Little Book of Semaphores* (2016); McKenney, *Is Parallel Programming Hard, And, If So, What Can You
  Do About It?* (2023); Lynch, *Distributed Algorithms* (1996), ch. 10;
- Sorin, Hill & Wood, *A Primer on Memory Consistency and Cache Coherence* (2nd ed., 2020).

Papers:
- Mutual exclusion: Dijkstra, "Solution of a problem in concurrent programming control" (1965); Lamport, "A new
  solution of Dijkstra's concurrent programming problem" (1974); Peterson, "Myths about the mutual exclusion
  problem" (1981); Burns & Lynch, "Bounds on shared memory for mutual exclusion" (1980/1993).
- Memory models: Lamport, "How to make a multiprocessor computer that correctly executes multiprocess programs"
  (1979); Adve & Hill, "Weak ordering: a new definition" (1990); Adve & Gharachorloo, "Shared memory consistency
  models: a tutorial" (1996); Manson, Pugh & Adve, "The Java memory model" (2005); Boehm & Adve, "Foundations of the
  C++ concurrency memory model" (2008); Sewell et al., "x86-TSO" (CACM 2010).
- Locks: Anderson, "The performance of spin lock alternatives" (1990); Mellor-Crummey & Scott, "Algorithms for
  scalable synchronization on shared-memory multiprocessors" (1991); Drepper, "Futexes are tricky" (2004).
- Waiting and deadlock: Dijkstra, "Cooperating sequential processes" (1965); Courtois, Heymans & Parnas (1971);
  Hoare, "Monitors" (1974); Brinch Hansen (1975); Lampson & Redell, "Experience with processes and monitors in Mesa"
  (1980); Coffman, Elphick & Shoshani, "System deadlocks" (1971).
- Objects: Herlihy & Wing, "Linearizability" (1990); Herlihy, "Wait-free synchronization" (1991); Treiber (1986);
  Michael & Scott (PODC 1996); Michael, "Hazard pointers" (2004); Fraser (2004); McKenney & Slingwine, RCU (1998);
  Herlihy & Moss, "Transactional memory" (1993); Hoare, "Communicating sequential processes" (1978); Hewitt, Bishop
  & Steiger (1973).
- Checking: Clarke & Emerson (1981); Queille & Sifakis (1982); Wing & Gong (1993); Gibbons & Korach (1997); Lowe
  (2017); Bouajjani, Emmi, Enea & Hamza (2015); Atig, Bouajjani, Burckhardt & Musuvathi (POPL 2010); Flanagan &
  Godefroid (2005); Savage et al., "Eraser" (1997); Flanagan & Freund, "FastTrack" (2009); Serebryany & Iskhodzhanov,
  ThreadSanitizer (2009); Burckhardt et al., PCT (2010); Attiya et al., "Laws of order" (POPL 2011); Kogan & Petrank
  (2011, 2012).
- In the wild: Leveson & Turner, "An investigation of the Therac-25 accidents" (1993); U.S.–Canada Power System
  Outage Task Force, final report (2004).
