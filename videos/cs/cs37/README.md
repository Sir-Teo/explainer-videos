# Computer Science, Built — Part 37: Networks II: Reliable Conversation

Part 37 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act VII, *Many Machines*. IP loses, reorders and duplicates
packets; TCP turns that into a reliable byte stream. In October 1986 the Internet's throughput fell a thousandfold,
and Van Jacobson's cure, additive increase and multiplicative decrease, turned out to be the only linear rule that is
fair, and a distributed algorithm for an optimization problem. The novels arrive over our own TCP on a lossy
transatlantic link: ledger row 14.

The instruments are in `explainer/cs/net/` (tested in `tests/test_cs37_transport.py`):
* `rdt.py`: reliable delivery from scratch, event-driven: stop-and-wait (the alternating-bit protocol with one-bit
  sequence numbers), Go-Back-N and Selective Repeat, over a channel with delay, rate, loss, duplication and
  reordering; sequence numbers modulo 2^bits, so a protocol with too few fails visibly.
* `tcp.py`: a packet-level simulator of flows sharing a bottleneck (the "dumbbell"): per-packet ACKs (as with SACK),
  RACK-style loss detection by transmission order, fast recovery, Jacobson/Karels RTO with Karn's rule; congestion
  control `fixed` (the TCPs of 1986: fixed window, fixed timer, go-back-n), `reno`, `cubic` (RFC 9438), `vegas` and
  `bbr` (BBRv1: startup, drain, gain cycling, PROBE_RTT, pacing); queues drop-tail, RED or CoDel; random loss; and
  in-order, non-congestive ACK jitter per flow. Also the Mathis formula and Jain's index.
* `cc.py`: Chiu and Jain's two-user model under AIMD, AIAD, MIAD and MIMD; Kelly's network utility maximization with
  log utilities, by dual (sub)gradient ascent on link prices; max-min fairness by progressive filling.
* `app.py`: an iterative DNS resolver with TTL caching; the odds of Kaminsky's cache poisoning; a packet-level page
  load over HTTP/1.1 (six connections), HTTP/2 (one ordered connection) and QUIC (ordering per stream); Zipf fitting;
  an LRU cache and Che's approximation.

## Chapters

* **Hook.** The novels (24,971,555 bytes, 17,104 packets) from Frankfurt to San Francisco: 100 Mb/s, RTT 108 ms,
  one packet in 1,000 lost. Reno 34.9 s, CUBIC 24.2 s, BBR 3.2 s; the physics 2.2 s. Their windows over time.
* **1. The transport problem.** 10,000 datagrams across a channel like IP's: 109 lost, 18 duplicated, 284 overtaken.
  Ports and the four-number connection name; UDP's 8-byte header; the two contracts; the end-to-end argument.
* **2. Reliability from scratch.** Stop-and-wait and timers; lost ACKs and the alternating bit (Bartlett,
  Scantlebury and Wilkinson, 1969): 20 of 20 runs correct on a FIFO channel with 10% loss, 0 of 20 once 20% of
  packets are delayed (the first error at position 8, packet 6 delivered again). Utilization (L/R)/(RTT + L/R),
  measured to four digits; across the Atlantic at 1 Gb/s, 0.11 Mb/s.
* **3. Sliding windows.** The window and ACK clocking; Go-Back-N and Selective Repeat. Utilization against window
  (RTT 100 ms, 1,000 packets/s): on the formula with no loss; at 2% loss and W = 128, Go-Back-N 0.14 (4,937
  retransmissions for 2,000 packets), Selective Repeat 0.42 (88). The sequence-space theorem, proved and tested at
  its edge with S = 8: Go-Back-N W = 7 always correct, W = 8 never; Selective Repeat W = 4 always, W = 5 never.
* **4. TCP.** The header; the three-way handshake and random initial sequence numbers (first byte after 2 RTT,
  216 ms). SYN floods and Bernstein's cookies (5 bits of time, 3 of MSS, 24 of keyed hash; one built). Teardown and
  TIME_WAIT (60 s: at most 546 connections a second to one server port). Flow control: a 64 KB window caps the
  Atlantic at 4.9 Mb/s; window scaling; buffers of a bandwidth-delay product (1.35 MB).
* **5. Timers that learn.** 402 RTT samples from a shared bottleneck (109 to 348 ms). RFC 793's β·SRTT against
  Jacobson and Karels's SRTT + 4·RTTVAR: β = 1.3 fires early 15 times; β = 2 never, but waits 495 ms on average;
  Jacobson once, waiting 336 ms. Karn's rule and backoff; timestamps.
* **6. Congestion collapse.** October 1986, LBL to UC Berkeley, 32 kb/s to 40 b/s. Reproduced: four flows on 2 Mb/s
  with fixed windows and a fixed 200 ms timer: goodput rises to 1.94 Mb/s, then falls to 1.11 once the windows
  exceed pipe + buffer, with the link 99.9% busy and 11,189 retransmissions a minute; Reno 1.94 at every load.
  Conservation of packets, ACK clocking, the congestion window, slow start; the sawtooth (utilization 99%).
* **7. AIMD.** Chiu and Jain's phase plane; trajectories from (0.1, 0.6): AIMD reaches Jain's index 1.000 (mean load
  0.78), AIAD keeps the difference (0.81), MIMD the ratio (0.66), MIAD starves one user (0.50). The four-line proof.
* **8. The Mathis formula.** Derived from one tooth: rate = (MSS/RTT)·√(3/(2p)). Measured at RTT 100 ms: 14.30 Mb/s
  at p = 10⁻⁴ against 14.31; 4.77 against 4.52 at 10⁻³; 1.73 against 1.43 at 10⁻² (per-packet ACKs recover
  several losses a round trip). RTT unfairness: 20 ms against 50, 100 and 200 ms: ratios 2.3, 5.5, 31.9.
* **9. Queues.** Buffer sizes from 0.1 to 8 BDP: utilization 78% to 99%, then only delay (426 ms at 8 BDP).
  Bufferbloat (Gettys, 2010). A 1,000-packet buffer: drop-tail 1,051 ms mean, RED 236 ms, CoDel 2.9 ms (at 88%
  utilization). Appenzeller, Keslassy and McKeown: with 64 flows, BDP/8 keeps 97.6% against 98.5%.
* **10. Modern congestion control.** CUBIC's curve. Kleinrock's operating point. BBR's model and our BBR's window.
  Alone on the transatlantic path: Reno 97.3, CUBIC 97.3, BBR 94.1 Mb/s, with mean queues 32, 81 and 8 ms; with 0.1%
  random loss 5.5, 8.0 and 94.8. BBR beside CUBIC on 50 Mb/s: 46.9 / 1.3 (buffer BDP/4), 43.9 / 2.4 (BDP), 30.4 /
  17.9 (4 BDP). Vegas alone 9.7 Mb/s with 4.5 packets queued; beside Reno, 0.0 against 9.7. DCTCP, BBRv2 and v3.
* **11. TCP as optimization.** Kelly's problem; the dual decomposition into link prices and flow rates; dual ascent
  on two links: long flow 1/3, short flows 2/3, prices 1.5 (max-min: 1/2 each; totals 5/3 against 3/2); three links:
  1/4 and 3/4. Reno's utility −3/(2·RTT²·x), Vegas's α log x.
* **12. Names.** The DNS tree; a day of 50,000 lookups: 56% cache hits, 0.88 round trips per lookup instead of 3.
  Kaminsky (2008): 656 expected races with a fixed port (a minute), 43 million with random ports (50 days); DNSSEC.
* **13. The web's transport.** HTTP/1.0, 1.1, 2; head-of-line blocking in one TCP stream. A 41-object page over
  108 ms: mean object time HTTP/2 209 → 336 ms from 0 to 5% loss, QUIC 209 → 227 (handshakes not modelled). QUIC:
  1-RTT and 0-RTT setup (432, 324, 216, 108 ms to the first byte), fresh packet numbers, encryption, connection IDs.
* **14. Caches at the edge.** CDNs, DNS steering and anycast. Zipf's law on the novels: 4,609,954 words, 57,895
  distinct, s = 1.22 on ranks 10 to 10,000. LRU on the words as requests: 10.2%, 47.2%, 78.6%, 95.8% for caches of
  10 to 10,000 words, above Che's independent-reference prediction (7.6, 37.6, 69.7, 93.3) because words come in
  bursts.
* **15. The novels, over our TCP.** The first five seconds of each window. The account: Reno 34.9 s (323 round
  trips, 13 resent), CUBIC 24.2 s (224), BBR 3.2 s (29, 1,593 resent from its own startup); all three 3.17 s with no
  loss. Ledger row 14: fetched with CUBIC (24.2 s) and counted under PebbleOS (2.7 s), 26.8 s, 90% of it network.
* **16. Frontier: can congestion control be fair?** The starvation theorem (Arun, Alizadeh and Balakrishnan, 2022).
  Measured, two flows on 20 Mb/s with ACK jitter on one: Vegas 9.9 / 9.6 with none, 17.7 / 1.5 at 40 ms; BBR 15.0 /
  4.1; Reno 12.5 / 7.0, no worse at 40 ms than at 20. L4S; learned and verified congestion control (Remy, Aurora,
  CCAC); coexistence. Four open problems.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs37.compute
python -m unittest tests.test_cs37_transport
python tools/build.py cs37
```

## Problems, with solutions

1. **Sequence space.** Prove that Selective Repeat with sequence numbers mod S is correct iff W ≤ S/2, and Go-Back-N
   iff W ≤ S − 1, on a FIFO channel that may lose packets.

   *Solution.* Sufficiency for Selective Repeat: when the receiver expects packets r, …, r + W − 1, every packet the
   sender can still send lies in [r − W, r + W − 1], because the sender's base is at least r − W (the receiver has
   acknowledged up to r − 1, and the sender cannot have sent beyond its base + W − 1 before seeing those ACKs) and at
   most r. That interval has 2W ≤ S numbers, so mod S they are distinct; a packet whose number falls in the
   receiver's window is the packet it seems to be, and one below it is an old duplicate, acknowledged again and
   discarded. Necessity: let the receiver accept 0, …, W − 1 and every ACK be lost; the sender resends 0, whose
   number mod S equals S, inside the new window [W, 2W − 1] when 2W > S, so it is accepted as packet S. For Go-Back-N
   the receiver's window is a single number r, and the sender's possible numbers lie in [r − W, r]: W + 1 numbers,
   distinct iff W + 1 ≤ S. With W = S, all ACKs lost and packet 0 resent, the receiver expecting packet S accepts it.
   Our tests: S = 8, Go-Back-N W = 7 and Selective Repeat W = 4 correct in 10 of 10 runs, W = 8 and W = 5 in 0.

2. **Mathis, with timeouts.** Derive the Mathis formula; then redo it when every loss is detected only by a timeout
   of 2 RTT.

   *Solution.* In steady state the window rises linearly from W/2 to W over W/2 round trips, so a cycle delivers
   (W/2)(3W/4) = 3W²/8 packets, one of which is lost: 3W²/8 = 1/p, W = √(8/(3p)), and the rate is (3W/4)·MSS/RTT
   = (MSS/RTT)√(3/(2p)). If each loss instead stalls for a timeout of 2 RTT and restarts from a window of one, each
   cycle is a slow start to W/2 (log₂(W/2) round trips, about W/2 packets), then a linear climb from W/2 to W
   (3W²/8 packets in W/2 round trips), then the 2-RTT stall. Packets per cycle ≈ 3W²/8 + W/2 = 1/p; time per cycle
   ≈ W/2 + log₂(W/2) + 2 round trips. For small p, W ≈ √(8/(3p)) still, and the rate falls by the factor
   (W/2)/(W/2 + log₂ W + 1), which matters when W is small: at p = 0.01 (W ≈ 16) the rate drops by about half. This
   is the regime Padhye et al. modelled in 1998.

3. **The four rules.** Show that AIAD and MIMD preserve, respectively, the difference and the ratio of two users'
   rates; prove AIMD converges for any a > 0 and 0 < b < 1.

   *Solution.* Under AIAD both rates change by the same ±a each round (until one hits zero), so x₂ − x₁ is invariant;
   under MIMD both are multiplied by the same factor, so x₂/x₁ is invariant. Neither approaches the fairness line
   from an unfair start. Under AIMD, increases leave d = x₂ − x₁ unchanged and decreases multiply it by b. The sum
   s grows by 2a in each increase round, so from any point it exceeds C within ⌈C/(2a)⌉ rounds; hence decreases occur
   infinitely often, and after k of them |d| = bᵏ|d₀| → 0. After convergence s oscillates between about bC and
   C + 2a, so efficiency tends to the band [b, 1]: for b = 1/2 a mean load of about 3/4, our 0.78.

4. **Three links in a row.** Solve Kelly's problem with log utilities on three links of capacity 1 in a row, with a
   long flow over all three and a short flow on each, by hand, and check the prices.

   *Solution.* By symmetry every link has the same price p, so a short flow sends 1/p and the long flow 1/(3p). Each
   link is full: 1/p + 1/(3p) = 1, so p = 4/3, the short flows get 3/4 and the long flow 1/4. KKT: ∂/∂x of
   Σ log x is 1/x, which must equal the path price: 1/(3/4) = 4/3 = p for a short flow, 1/(1/4) = 4 = 3p for the
   long one. Total 9/4 = 2.25, against max-min's four flows at 1/2, total 2. Our dual ascent: 0.250 and 0.750.

5. **Build: delayed ACKs.** Add delayed acknowledgements (one ACK per two segments, or after 40 ms) to our TCP. What
   happens to slow start, to Mathis's constant, and to BBR's bandwidth estimate?

   *Solution sketch.* In `tcp.py` the receiver acknowledges each packet as it leaves the bottleneck; buffer every
   second one (with a timer) and acknowledge both, and let a cumulative ACK credit the window for both packets (or,
   as RFC 5681 allows, by at most one, which is what makes the difference). Counting ACKs, slow start grows by 1.5×
   per round trip instead of 2× and congestion avoidance by half a packet per round trip, so the Mathis constant
   √(3/2) ≈ 1.22 becomes √(3/4) ≈ 0.87 (Mathis et al. give this as b = 2). Appropriate byte counting (RFC 3465)
   restores both. BBR's delivery-rate samples become burstier, since ACKs arrive two packets at a time; its max
   filter makes it overestimate slightly, so it pushes a little more into the queue.

6. ★ **Research: the delay–fairness trade-off.** On our dumbbell with in-order ACK jitter of up to D on one flow, find
   the least mean queueing delay any algorithm you can design needs to keep two flows' Jain index above 0.9; plot it
   against D, and compare with the 2022 starvation bound.

   *What is known.* Arun, Alizadeh and Balakrishnan prove that a delay-convergent algorithm, one whose queueing delay
   converges to a range of width δ(C), can be made to starve when non-congestive delay exceeds δ; so fairness under
   jitter D needs either an equilibrium delay range wider than D (and so queues of at least about D) or a signal
   other than delay (loss, ECN). Our measurements give points: Vegas (queueing about 4.5 packets) falls to a share of
   7% at D = 40 ms; Reno keeps 36% but fills the buffer. What is open is the exact curve: for each D, the minimum
   delay compatible with a given fairness, and algorithms that meet it. A starting point is an algorithm that
   deliberately oscillates its delay over a range larger than D (as Copa's mode switching does) and measures its
   share through the oscillation. Report Jain's index and mean queue for D = 0, 5, 10, 20, 40 ms.

## 习题与解答

1. **序列号空间。** 证明：在可能丢包的 FIFO 信道上，序列号取模 S 时，选择重传正确当且仅当 W ≤ S/2，回退 N 正确当且仅当
   W ≤ S − 1。

   *解答。* 选择重传的充分性：接收方期待 r, …, r + W − 1 时，发送方还可能发出的分组都落在 [r − W, r + W − 1] 内，因为发送方
   的窗口基至少是 r − W（接收方已确认到 r − 1，而发送方在看到这些 ACK 之前发出的不会超过基 + W − 1），至多是 r。这个区间有
   2W ≤ S 个数，取模 S 后互不相同；落在接收窗口内的编号就是它看上去的那个分组，落在下面的是旧的重复，再确认一次后丢弃。
   必要性：让接收方收下 0, …, W − 1，而所有 ACK 都丢失；发送方重传 0，它模 S 等于 S，当 2W > S 时落在新窗口 [W, 2W − 1]
   内，于是被当作分组 S 收下。回退 N 的接收窗口只有一个编号 r，发送方可能的编号在 [r − W, r] 内：W + 1 个，互不相同当且仅当
   W + 1 ≤ S。若 W = S、所有 ACK 丢失、重传分组 0，期待分组 S 的接收方会收下它。我们的测试：S = 8 时，回退 N 的 W = 7 与选择
   重传的 W = 4 在 10 次运行中全部正确，W = 8 与 W = 5 全部出错。

2. **带超时的 Mathis 公式。** 推导 Mathis 公式；再在每次丢包都只能靠 2 RTT 的超时发现时重做一遍。

   *解答。* 稳态下窗口在 W/2 个往返内从 W/2 线性升到 W，一个周期交付 (W/2)(3W/4) = 3W²/8 个分组，其中一个丢失：
   3W²/8 = 1/p，W = √(8/(3p))，速率为 (3W/4)·MSS/RTT = (MSS/RTT)√(3/(2p))。若每次丢包改为停顿 2 RTT 的超时并从窗口 1 重新
   开始，每个周期是：慢启动到 W/2（log₂(W/2) 个往返，约 W/2 个分组），再从 W/2 线性升到 W（W/2 个往返内 3W²/8 个分组），
   再停顿 2 个往返。每周期分组数 ≈ 3W²/8 + W/2 = 1/p；每周期时间 ≈ W/2 + log₂(W/2) + 2 个往返。p 小时仍有 W ≈ √(8/(3p))，
   速率按因子 (W/2)/(W/2 + log₂ W + 1) 下降；W 小时影响很大：p = 0.01（W ≈ 16）时速率约减半。这正是 Padhye 等人 1998 年建模
   的情形。

3. **四种规则。** 证明 AIAD 与 MIMD 分别保持两个用户速率之差与之比；证明对任意 a > 0、0 < b < 1，AIMD 收敛。

   *解答。* AIAD 下两个速率每轮改变相同的 ±a（直到有一个降到零），所以 x₂ − x₁ 不变；MIMD 下两者乘以同一个因子，所以
   x₂/x₁ 不变。两者都不会从不公平的起点接近公平线。AIMD 下，增加不改变 d = x₂ − x₁，减少把它乘以 b。每个增加轮总和 s
   增加 2a，所以从任何点出发，⌈C/(2a)⌉ 轮内就会超过 C；因此减少无限多次发生，k 次之后 |d| = bᵏ|d₀| → 0。收敛后 s 在约 bC
   与 C + 2a 之间振荡，效率趋于区间 [b, 1]：b = 1/2 时平均负载约 3/4，我们测得 0.78。

4. **三条串联链路。** 手工求解三条容量为 1 的串联链路上的 Kelly 问题（对数效用，一条长流经过全部三条链路，每条链路一条
   短流），并检验价格。

   *解答。* 由对称性每条链路价格都是 p，短流发送 1/p，长流 1/(3p)。每条链路都满：1/p + 1/(3p) = 1，所以 p = 4/3，短流得
   3/4，长流得 1/4。KKT 条件：Σ log x 对 x 的导数 1/x 必须等于路径价格：短流 1/(3/4) = 4/3 = p，长流 1/(1/4) = 4 = 3p。
   总量 9/4 = 2.25，而最大最小公平给四条流各 1/2，总量 2。我们的对偶上升：0.250 与 0.750。

5. **动手：延迟确认。** 给我们的 TCP 加上延迟确认（每两个报文段一个 ACK，或 40 ms 后）。慢启动、Mathis 常数和 BBR 的带宽
   估计会怎样？

   *解答要点。* 在 `tcp.py` 中，接收方在每个分组离开瓶颈时确认它；改为缓存每隔一个的分组（带定时器）并一起确认，并让累积
   ACK 为两个分组增加窗口（或者按 RFC 5681 允许的那样至多增加一个，区别就在这里）。按 ACK 计数时，慢启动每个往返增长 1.5 倍
   而不是 2 倍，拥塞避免每个往返增加半个分组，所以 Mathis 常数 √(3/2) ≈ 1.22 变成 √(3/4) ≈ 0.87（Mathis 等人记作 b = 2）。
   按字节计数（RFC 3465）可以恢复两者。BBR 的交付速率样本变得更突发，因为 ACK 两个两个地到达；它的最大值滤波器使它略微高估，
   于是向队列多推一点数据。

6. ★ **研究：时延与公平的权衡。** 在我们的哑铃拓扑上，给一条流的 ACK 加上至多 D 的保序抖动，找出你能设计的任何算法为使两条
   流的 Jain 指数保持在 0.9 以上所需的最小平均排队时延；画出它随 D 的变化，并与 2022 年的饥饿界比较。

   *已知结果。* Arun、Alizadeh 与 Balakrishnan 证明：时延收敛的算法（排队时延收敛到宽度为 δ(C) 的范围内）在非拥塞时延超过 δ
   时可以被饿死；所以在抖动 D 下要公平，要么平衡时延范围比 D 宽（因而队列至少约为 D），要么使用时延以外的信号（丢包、ECN）。
   我们的测量给出几个点：Vegas（排队约 4.5 个分组）在 D = 40 ms 时份额降到 7%；Reno 保持 36%，但填满了缓冲区。未解决的是确切
   的曲线：对每个 D，与给定公平度相容的最小时延，以及达到它的算法。一个起点是让算法有意让自己的时延在比 D 更大的范围内振荡
   （如 Copa 的模式切换），并通过振荡测量自己的份额。报告 D = 0、5、10、20、40 ms 时的 Jain 指数与平均队列。

## Glossary additions

* **transport layer**: end-to-end delivery between programs; **port**: a 16-bit number naming a program's endpoint.
* **UDP**: datagrams with ports and a checksum, no promises; **TCP**: a reliable, ordered, flow- and
  congestion-controlled byte stream.
* **ARQ**: automatic repeat request, reliability by acknowledgement and retransmission; **alternating-bit protocol**:
  stop-and-wait with one-bit sequence numbers.
* **sliding window**: up to W packets sent and unacknowledged; **Go-Back-N, Selective Repeat**: resend from the loss
  on, or only the loss.
* **cumulative ACK**: the next byte expected; **SACK**: selective acknowledgement of blocks beyond a gap.
* **three-way handshake**: SYN, SYN+ACK, ACK; **SYN cookie**: connection state encoded in the server's initial
  sequence number; **TIME_WAIT**: 2 MSL of reserving a closed connection's four numbers.
* **flow control**: the receiver's advertised window; **congestion window**: the sender's estimate of what the
  network can hold.
* **RTO**: retransmission timeout, SRTT + 4·RTTVAR; **Karn's rule**: no RTT samples from retransmissions.
* **congestion collapse**: a network busy carrying retransmissions while goodput falls; **goodput**: new data
  delivered per second.
* **slow start, congestion avoidance, fast retransmit, fast recovery**: Jacobson's mechanisms; **ACK clocking**:
  sending one packet per ACK received.
* **AIMD**: additive increase, multiplicative decrease; **Jain's fairness index**: (Σx)² / (n Σx²).
* **Mathis formula**: TCP throughput ≈ (MSS/RTT)√(3/(2p)); **RTT unfairness**: shorter round trips win more.
* **bufferbloat**: excessive buffering that adds delay without throughput; **AQM**: active queue management (RED,
  CoDel); **ECN**: explicit congestion notification, marking instead of dropping.
* **CUBIC, BBR, Vegas, DCTCP**: congestion controls by cubic growth in time, by a model of bandwidth and delay, by
  delay, and by ECN marks in data centres.
* **network utility maximization**: rates maximizing Σ U(x) under link capacities; **proportional fairness**: its
  solution for log utilities; **max-min fairness**: no rate can rise without lowering a smaller one.
* **DNS**: the hierarchical, cached name system; **TTL** (DNS): how long an answer may be cached; **cache
  poisoning**: forging answers into a resolver's cache; **DNSSEC**: signed DNS answers.
* **head-of-line blocking**: independent data delayed behind a loss in a shared ordered channel; **QUIC**: a
  transport over UDP with streams, built-in TLS 1.3 and connection IDs; **0-RTT**: sending data in the first packet.
* **CDN**: content delivery network; **anycast**: one address announced from many sites; **Zipf's law**: frequency
  ∝ rank^−s; **Che approximation**: an LRU cache's hit rate from a characteristic time.
* **starvation** (congestion control): a flow receiving an arbitrarily small share; **L4S**: low-latency, low-loss,
  scalable throughput with early ECN marking.

## Sources

* J. F. Kurose and K. W. Ross, *Computer Networking: A Top-Down Approach*, ch. 2–3; L. L. Peterson and B. S. Davie,
  *Computer Networks: A Systems Approach*, ch. 5–6.
* W. R. Stevens, *TCP/IP Illustrated*, vol. 1; I. Grigorik, *High Performance Browser Networking*.
* R. Srikant and L. Ying, *Communication Networks: An Optimization, Control and Stochastic Networks Perspective*;
  F. Kelly and E. Yudovina, *Stochastic Networks*.
* K. A. Bartlett, R. A. Scantlebury and P. T. Wilkinson, "A Note on Reliable Full-Duplex Transmission over
  Half-Duplex Links", CACM (1969).
* V. Cerf and R. Kahn, "A Protocol for Packet Network Intercommunication", IEEE Trans. Communications (1974);
  J. Postel, RFC 768 (1980) and RFC 793 (1981).
* J. Nagle, "Congestion Control in IP/TCP Internetworks", RFC 896 (1984).
* P. Karn and C. Partridge, "Improving Round-Trip Time Estimates in Reliable Transport Protocols", SIGCOMM (1987).
* V. Jacobson, "Congestion Avoidance and Control", SIGCOMM (1988).
* D.-M. Chiu and R. Jain, "Analysis of the Increase and Decrease Algorithms for Congestion Avoidance in Computer
  Networks", Computer Networks and ISDN Systems (1989).
* S. Floyd and V. Jacobson, "Random Early Detection Gateways for Congestion Avoidance", IEEE/ACM ToN (1993).
* L. S. Brakmo and L. L. Peterson, "TCP Vegas: End to End Congestion Avoidance on a Global Internet", IEEE JSAC (1995).
* D. J. Bernstein, "SYN cookies" (1996); RFC 4987 (2007).
* M. Mathis, J. Semke, J. Mahdavi and T. Ott, "The Macroscopic Behavior of the TCP Congestion Avoidance Algorithm",
  CCR (1997); J. Padhye, V. Firoiu, D. Towsley and J. Kurose, "Modeling TCP Throughput", SIGCOMM (1998).
* T. V. Lakshman and U. Madhow, "The Performance of TCP/IP for Networks with High Bandwidth-Delay Products and
  Random Loss", IEEE/ACM ToN (1997).
* F. Kelly, A. Maulloo and D. Tan, "Rate Control for Communication Networks: Shadow Prices, Proportional Fairness and
  Stability", J. Operational Research Society (1998); S. H. Low and D. E. Lapsley, "Optimization Flow Control",
  IEEE/ACM ToN (1999); S. H. Low, "A Duality Model of TCP and Queue Management Algorithms", IEEE/ACM ToN (2003).
* G. Appenzeller, I. Keslassy and N. McKeown, "Sizing Router Buffers", SIGCOMM (2004).
* S. Ha, I. Rhee and L. Xu, "CUBIC: A New TCP-Friendly High-Speed TCP Variant", OSR (2008); RFC 9438 (2023).
* M. Alizadeh et al., "Data Center TCP (DCTCP)", SIGCOMM (2010).
* J. Gettys and K. Nichols, "Bufferbloat: Dark Buffers in the Internet", ACM Queue (2011); K. Nichols and
  V. Jacobson, "Controlling Queue Delay", ACM Queue (2012).
* N. Cardwell, Y. Cheng, C. S. Gunn, S. H. Yeganeh and V. Jacobson, "BBR: Congestion-Based Congestion Control", ACM
  Queue (2016); L. Kleinrock, "Power and Deterministic Rules of Thumb for Probabilistic Problems in Computer
  Communications", ICC (1979).
* P. Mockapetris, RFC 1034/1035 (1987); D. Kaminsky, "Black Ops 2008" (2008).
* A. Langley et al., "The QUIC Transport Protocol: Design and Internet-Scale Deployment", SIGCOMM (2017); J. Iyengar
  and M. Thomson, RFC 9000 (2021).
* L. Breslau, P. Cao, L. Fan, G. Phillips and S. Shenker, "Web Caching and Zipf-like Distributions", INFOCOM (1999);
  H. Che, Y. Tung and Z. Wang, "Hierarchical Web Caching Systems: Modeling, Design and Experimental Results", IEEE
  JSAC (2002).
* K. Winstein and H. Balakrishnan, "TCP ex Machina: Computer-Generated Congestion Control", SIGCOMM (2013); V. Arun,
  M. T. Arashloo, A. Saeed, M. Alizadeh and H. Balakrishnan, "Toward Formally Verifying Congestion Control Behavior",
  SIGCOMM (2021).
* V. Arun, M. Alizadeh and H. Balakrishnan, "Starvation in End-to-End Congestion Control", SIGCOMM (2022).
* B. Briscoe et al., "Low Latency, Low Loss, and Scalable Throughput (L4S) Internet Service: Architecture", RFC 9330
  (2023).
