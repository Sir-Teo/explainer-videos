# Computer Science, Built — Part 36: Networks I: Moving Bits

Part 36 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the first part of Act VII, *Many Machines*. The telephone network reserved a wire
for every call; Baran and Davies proposed cutting messages into packets that find their own way. The Internet is that
idea, organized in layers with IP as the narrow waist. This part derives what limits it at each layer (Shannon's
capacity, ALOHA's 1/2e, the count to infinity, BGP's policies) and builds a small internet of its own.

The instruments are in `explainer/cs/net/` (tested in `tests/test_cs36_net.py`):
* `phy.py`: Shannon's capacity; square M-QAM with Gray labels through Gaussian noise, measured, against the textbook
  symbol error rate; the SNR each size needs for a bit error rate of 10⁻⁶ against Shannon's 2^k − 1; fibre round
  trips and bandwidth-delay products.
* `link.py`: HDLC bit stuffing and framing; Ethernet frames with their CRC-32 (Part 28's, checked against `zlib`);
  corruption trials (single bits, pairs, bursts up to 32 bits, noise).
* `mac.py`: pure and slotted ALOHA as Poisson processes; CSMA/CD with binary exponential backoff and with the
  p = 1/n contention Metcalfe and Boggs analysed; the hidden terminal with and without RTS/CTS.
* `bridge.py`: LANs of bridges; flooding (the broadcast storm); Perlman's spanning tree by rounds of configuration
  messages, with root ports and designated ports; MAC learning.
* `ip.py`: prefixes; longest-prefix match by linear scan, binary trie and multibit tries with controlled prefix
  expansion; a synthetic table with the real mix of prefix lengths; aggregation; fragmentation; NAPT; the Internet
  checksum and IPv4 and UDP headers.
* `routing.py`: synchronous distance vector (plain, split horizon, poisoned reverse) with failures; reliable
  flooding; Dijkstra; link-state reconvergence with routers updating at different times, classifying every
  source-destination pair as delivered, dropped or looping.
* `bgp.py`: a tiered AS graph with customer, provider and peer links; path-vector propagation under Gao–Rexford
  preferences and export rules; origin and sub-prefix hijacks; route-origin validation against ROAs; the stable
  paths problem, with BAD GADGET and GOOD GADGET.
* `sim.py`: **our internet**, an event-driven simulator of hosts and routers on links with bandwidth, length and
  loss; serialization, propagation and queueing; link-state routing; TTL and ICMP time exceeded; ping and
  traceroute; failures with staggered reconvergence.
* `wireless.py`: BPSK under Gaussian noise and Rayleigh fading; OFDM with an FFT, a multipath channel and a cyclic
  prefix; MIMO capacity E log₂ det(I + (SNR/n) H H*).
* `dataplane.py`: a P4-shaped pipeline (parser, ternary, exact and LPM match-action tables, deparser) and a
  data-plane verifier that finds loops and black holes from forwarding tables alone.

## Chapters

* **Hook.** "Call me Ishmael." from Pebble 1 in San Francisco to Pebble 2 in Frankfurt: 16 bytes become a 64-byte
  frame (Ethernet 14, IP 20, UDP 8, data 16, pad 2, FCS 4), shown byte by byte. Traceroute: San Francisco, New York
  (46.1 ms), Paris (103.3), Frankfurt (108.0); ping 108.04 ms, against 108.04 ms for light in 11,020 km of fibre.
* **1. Circuits and packets.** Reserved circuits against shared packets for bursty users. Statistical multiplexing:
  35 users, each active 10% of the time, on a link for 10: overflow probability 0.0004; 1,000 users need capacity for
  137. Baran (1964), Davies, ARPANET's "LO" (1969), Cerf and Kahn (1974), the 1983 flag day.
* **2. Layers.** Five layers and encapsulation, animated; a router implements three. The hourglass with IP at the
  waist. Overhead: 16 bytes of data take 84 on the wire (19%), 1,460 take 1,526 (96%). The end-to-end argument in
  numbers: a router corrupting one packet in 10⁹, a gigabyte over 15 hops: 1.0% of copies damaged with every link
  check passing.
* **3. Bits on a wire.** Nyquist and Shannon: a telephone line 36 kb/s (modems reached 33.6), 80 MHz Wi-Fi at 30 dB
  797 Mb/s. QAM clouds at 24 and 14 dB. Measured error rates on the formula; the SNR needed for 10⁻⁶ against
  Shannon: 4-QAM 13.5 against 4.8 dB, 16-QAM 20.4 against 11.8, 64-QAM 26.6 against 18.0, 256-QAM 32.5 against 24.1,
  a gap of about 8.6 dB that coding closes. Fibre round trips (New York–London 55 ms) and the bandwidth-delay product
  (688 MB at 100 Gb/s).
* **4. Frames.** Bit stuffing. Line codes and clock recovery: Manchester (50%), 4B/5B and 8b/10b (80%), 64b/66b
  (97%). CRC-32: 100,000 corrupted frames of each kind, none undetected. The Ethernet frame,
  MAC addresses, broadcast, ethertype.
* **5. Sharing a channel.** ALOHA's timeline and derivation; measured throughput on Ge^{−2G} (peak 0.184) and Ge^{−G}
  (0.368). CSMA/CD and binary exponential backoff; why frames are at least 64 bytes; 20 stations: efficiency
  measured against Metcalfe and Boggs for a = 0.01 … 0.5. The hidden terminal: throughput Ge^{−G}; RTS/CTS 0.63 at
  G = 2 against 0.27.
* **6. Bridges and switches.** A broadcast storm: 1,115,742 frames within 20 hops in a five-bridge loop. Perlman's
  spanning tree (3 rounds, 3 links blocked); the broadcast then takes 8 frames. MAC learning: 7 copies, then 3.
* **7. IP.** Prefixes, CIDR aggregation (four /24s into a /22), NAT, IPv6's 6.7 × 10²³ addresses per square metre.
  The IPv4 header, TTL, fragmentation of 4,000 bytes into a 1,500-byte MTU. ARP, and addresses hop by hop: IP addresses fixed, MAC addresses and TTL changing. Traceroute's TTL trick.
* **8. Forwarding.** Longest-prefix match. 100,000 prefixes: linear 100,000 reads (34 ms in Python), binary trie
  21 reads (5.1 µs), stride-4 trie 5.4, stride-8 trie 2.9; all equal. 400 Gb/s: a packet every 1.68 ns; TCAMs. Head-of-line blocking in an
  input-queued switch: 0.75 for 2 ports falling to 0.593 for 32 (limit 2 − √2 = 0.586); virtual output queues 1.0.
* **9. Distance vector.** Bellman–Ford as gossip: u's table settling in 4 rounds. Count to infinity on a line
  (15 rounds to 16); split horizon and poisoned reverse fix it in 2, but a triangle still counts for 15. On our internet: 4 rounds from scratch; cutting Amsterdam–Frankfurt
  settles in 3 (an equal path via Paris), 5 with split horizon.
* **10. Link state.** Flooding (London's LSA: 13 messages, 3 hops) and Dijkstra. A cable cut with staggered updates:
  of 40 packets, 5 dropped, 16 looping between London and Amsterdam, 19 delivered via Paris.
* **11. BGP.** Path vector; customer > peer > provider and valley-free export (Gao and Rexford); 125 ASes converge in
  6 rounds, mean path 3.3. The 2008 YouTube hijack; on our internet an equal-prefix hijack takes 50 of 125 ASes, a
  sub-prefix hijack all 125. RPKI: hijacked share against adoption (85% at 10%, 49% at 25%, 15% at 50%, 3% at 75%);
  if the 25 transit networks validate, 0%.
* **12. Software-defined networks.** OpenFlow's split of control and data; Google's B4; a P4-shaped pipeline
  processing four packets (forward, count, drop by ACL, TTL expiry). Data-centre fabrics: a k = 4 fat tree (16 hosts,
  20 switches, 4 paths between pods); ECMP's busiest path at 1.5–2.0 times the mean for equal flows, 2.1–5.0 for
  heavy-tailed flows.
* **13. Our internet.** Eight cities, four Pebbles, a ping matrix (London–Frankfurt 7.1 ms, Frankfurt–Tokyo 159.8
  via Singapore); delay under load on a 100 Mb/s link: queueing
  waits following Pollaczek–Khinchine, the 99th-percentile ping 14.3 ms at 95% load against 9.8 ms idle; a cut cable
  rerouted from 7.06 to 8.04 ms, with the loop of chapter 10.
* **14. Wireless.** Rayleigh fading against Gaussian noise (at 10 dB: 0.023 against 4 × 10⁻⁶). OFDM on 64
  subcarriers through a five-path echo: bit errors 0.023 without a cyclic prefix, 0.0012 with one. MIMO: 5.9, 11.3,
  22.1, 44.0 bits/s/Hz at 20 dB for 1, 2, 4, 8 antennas.
* **15. Frontier: programmable, verified, convergent.** A verifier finds chapter 13's loop in a mid-update snapshot
  (two prefixes, London–Amsterdam) and none after convergence; header space analysis, Batfish. In-network
  telemetry, NetCache, in-network aggregation. BAD GADGET
  oscillating for ever; stable-paths solvability is NP-complete. Six open problems.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs36.compute
python -m unittest tests.test_cs36_net
python tools/build.py cs36
```

## Problems, with solutions

1. **ALOHA.** Derive pure ALOHA's throughput S = Ge^{−2G} and slotted ALOHA's Ge^{−G}, and their maxima.

   *Solution.* Attempts (new and retried) form a Poisson process of rate G per frame time. A frame starting at t
   succeeds iff no other frame starts in (t − 1, t + 1), an interval of length 2: probability e^{−2G}. So
   S = G e^{−2G}; dS/dG = e^{−2G}(1 − 2G) = 0 at G = 1/2, where S = 1/(2e) ≈ 0.184. In slotted ALOHA a frame collides
   only with frames in its own slot, an interval of length 1: S = G e^{−G}, maximal at G = 1 with S = 1/e ≈ 0.368.
   Our simulation: 0.185 at G = 0.5 and 0.369 at G = 1.

2. **What a CRC catches.** Show that CRC-32 detects every burst of 32 or fewer bits, and that any CRC whose generator
   is divisible by x + 1 detects every odd number of bit errors.

   *Solution.* An error is undetected iff its error polynomial E(x) is a multiple of g(x). A burst of length
   L ≤ 32 starting at bit i is E(x) = x^i B(x) with deg B = L − 1 ≤ 31 and B(0) = 1. Since g(0) = 1, g and x are
   coprime, so g | x^i B implies g | B, impossible because B ≠ 0 has degree less than 32. If (x + 1) | g, then every
   multiple of g vanishes at x = 1; but an error with an odd number of terms has E(1) = 1. (CRC-32's own generator
   has 15 terms and is not divisible by x + 1; instead it has Hamming distance 4 for frames of Ethernet's size, so it
   catches every 1-, 2- and 3-bit error there.)

3. **Distance vector converges.** Prove that synchronous distance vector reaches the shortest distances in at most
   n − 1 rounds when costs are positive and nothing changes.

   *Solution.* By induction on k: after round k, D_x(y) is the cost of the cheapest path from x to y with at most k
   links (round 0: only x itself). Round k + 1 computes min over neighbours v of c(x, v) + D_v(y), and the cheapest
   path of at most k + 1 links is a first link to some v followed by the cheapest path from v of at most k links. With
   positive costs a shortest path is simple, so has at most n − 1 links; after round n − 1 every D is exact, and the
   next round changes nothing. Our six-node example settles in 4, its longest shortest path.

4. **Split horizon's limit.** Show that split horizon prevents every two-node loop but not a three-node one, with a
   counting example.

   *Solution.* Two nodes can only loop if A's route to y is via B and B's via A; with split horizon A never tells B
   about a route through B, so B cannot adopt it, and vice versa. Take the triangle A, B, C with D hanging off C, and
   cut C–D. A and B both route to D via C, so neither advertises D to C, and C learns at once that D is unreachable.
   But B tells A "D at 2" (B's route is via C, not A), and A tells B the same, so each adopts the other at 3. Next
   round A's route is via B, so A may advertise it to C: C adopts 4 via A. The round after, B learns 5 from C... The
   value climbs by one each round around the loop of three, exactly our table (A, B, C) = (3, 3, ∞), (∞, ∞, 4),
   (∞, 5, ∞), …, reaching 16 after 15 rounds.

5. **Build: RIP in our internet.** Add RIP to the simulator: periodic distance vectors as real packets; cut a link
   and watch packets loop while it counts.

   *Solution.* Give each router a UDP port 520 handler. Every period T (30 s in RIP; 1 s is enough here) send each
   neighbour a packet listing (prefix, metric) for every route, applying split horizon or not; on receipt, update
   routes with metric min(16, c + m) and remember the neighbour and a timeout (180 s in RIP). Forward data packets
   with the RIP table instead of `compute_tables`. On the three-router line with T = 1 s, cutting B–C makes packets
   for C bounce between A and B until their TTL expires for about 15 periods, then they are dropped with "no route";
   with split horizon they are dropped from the first period. Triggered updates (sending immediately on a change)
   shorten the plain count from 15 periods to about 15 round trips.

6. ★ **Research. Loop-free reconvergence.** After a single link failure, find an order of router updates under
   which no packet ever loops, and the fewest rounds such a schedule needs.

   *What is known, and a way in.* In chapter 10, Amsterdam (next to the failure) updated before London (one hop
   further) and the two looped. Reversing the order, London first, leaves only drops: our `ls_reconverge` reports zero
   loops at every instant. This is the oFIB rule (Francois and Bonaventure, 2007): for a link that goes down, a
   router may install its new table only after every router that currently reaches the failed link through it has
   done so, that is, in decreasing order of depth in the reverse shortest-path tree towards the failed link; for a
   link that comes up, the reverse. Each depth is a round, so the schedule takes as many rounds as the tree is deep;
   whether fewer rounds suffice, and how to schedule several simultaneous changes, is harder: for arbitrary
   forwarding changes, deciding whether a loop-free schedule of k rounds exists is NP-hard (Ludwig, Marcinkowski and
   Schmid, 2015). Open: tight bounds on rounds for the changes shortest-path routing actually produces, and schedules
   that are both loop-free and black-hole-free. Our verifier checks any proposed schedule state by state.

## 习题与解答

1. **ALOHA。** 推导纯 ALOHA 的吞吐量 S = Ge^{−2G} 与时隙 ALOHA 的 Ge^{−G}，以及它们的最大值。

   *解答。* 尝试（新帧与重传）构成每帧时间速率为 G 的泊松过程。在 t 时刻开始的帧成功，当且仅当 (t − 1, t + 1) 内没有别的帧
   开始，这是长度为 2 的区间：概率 e^{−2G}。所以 S = G e^{−2G}；dS/dG = e^{−2G}(1 − 2G) 在 G = 1/2 处为零，此时
   S = 1/(2e) ≈ 0.184。时隙 ALOHA 中帧只与同一时隙的帧冲突，区间长度为 1：S = G e^{−G}，在 G = 1 处最大，S = 1/e ≈ 0.368。
   我们的模拟：G = 0.5 时 0.185，G = 1 时 0.369。

2. **CRC 能抓住什么。** 证明 CRC-32 能检出所有长度不超过 32 位的突发错误；并证明生成多项式能被 x + 1 整除的 CRC 能检出所有
   奇数个比特的错误。

   *解答。* 错误不被检出，当且仅当错误多项式 E(x) 是 g(x) 的倍数。从第 i 位开始、长度 L ≤ 32 的突发是 E(x) = x^i B(x)，
   其中 deg B = L − 1 ≤ 31 且 B(0) = 1。由于 g(0) = 1，g 与 x 互素，所以 g | x^i B 推出 g | B，而 B ≠ 0 的次数小于 32，
   不可能。若 (x + 1) | g，则 g 的每个倍数在 x = 1 处为零；而有奇数项的错误满足 E(1) = 1。（CRC-32 自己的生成多项式有 15 项，
   不能被 x + 1 整除；但它在以太网帧的长度内汉明距离为 4，所以能抓住其中所有 1、2、3 位的错误。）

3. **距离向量会收敛。** 证明在代价为正且没有变化时，同步距离向量至多 n − 1 轮就得到最短距离。

   *解答。* 对 k 归纳：第 k 轮后，D_x(y) 是 x 到 y 至多 k 条链路的最便宜路径的代价（第 0 轮只有 x 自己）。第 k + 1 轮计算
   对邻居 v 取 c(x, v) + D_v(y) 的最小值，而至多 k + 1 条链路的最便宜路径，正是先到某个 v 的一条链路、再接从 v 出发至多 k
   条链路的最便宜路径。代价为正时最短路径是简单路径，至多 n − 1 条链路；第 n − 1 轮后所有 D 都准确，下一轮什么也不变。我们
   的六节点例子 4 轮稳定，等于其最长的最短路径。

4. **水平分割的局限。** 证明水平分割能阻止所有两节点环，却不能阻止三节点环，并给出计数的例子。

   *解答。* 两个节点要成环，只能是 A 到 y 的路由经过 B、B 的经过 A；有了水平分割，A 永远不会把经过 B 的路由告诉 B，所以 B
   不能采纳它，反之亦然。取三角形 A、B、C，D 挂在 C 上，切断 C–D。A 和 B 都经 C 到达 D，所以都不向 C 通告 D，C 立刻知道 D
   不可达。但 B 告诉 A“D 距离 2”（B 的路由经过 C 而不是 A），A 也这样告诉 B，于是双方都以 3 采纳对方。下一轮 A 的路由经过
   B，所以 A 可以通告给 C：C 以 4 经 A 采纳。再下一轮 B 从 C 学到 5……数值绕着三节点的环每轮加一，正是我们的表
   (A, B, C) = (3, 3, ∞)、(∞, ∞, 4)、(∞, 5, ∞)……，15 轮后到达 16。

5. **动手：在我们的互联网里加上 RIP。** 给模拟器加上 RIP：周期性的距离向量作为真实的分组；切断一条链路，看分组在计数期间
   打转。

   *解答。* 给每个路由器一个 UDP 520 端口的处理函数。每隔周期 T（RIP 中为 30 秒；这里 1 秒就够）向每个邻居发送一个分组，
   列出每条路由的（前缀，度量），按需应用水平分割；收到后，用 min(16, c + m) 更新路由，并记下邻居和超时（RIP 中为 180 秒）。
   转发数据分组时用 RIP 的表而不是 `compute_tables`。在三路由器的直线上取 T = 1 秒，切断 B–C 后，去往 C 的分组在 A 与 B
   之间来回，直到 TTL 耗尽，持续约 15 个周期，之后以“无路由”被丢弃；有水平分割时，从第一个周期起就被丢弃。触发更新（一有变化
   立即发送）把普通的计数从 15 个周期缩短到约 15 个往返时间。

6. ★ **研究：无环的重新收敛。** 单条链路故障后，找出一种路由器更新顺序，使得没有任何分组打转，并求这种调度所需的最少轮数。

   *已知的情况与入手的方法。* 在第十章里，阿姆斯特丹（紧邻故障）先于伦敦（远一跳）更新，两者形成了环。把顺序反过来，伦敦先
   更新，就只剩丢包：我们的 `ls_reconverge` 报告每一时刻都没有环。这就是 oFIB 规则（Francois 与 Bonaventure，2007）：对于
   断开的链路，一个路由器只有在所有通过它到达故障链路的路由器都已更新之后，才能安装新表，也就是按朝向故障链路的反向最短路径树
   的深度从大到小更新；对于恢复的链路则相反。每一层深度是一轮，所以调度的轮数等于树的深度；能否更少，以及如何调度同时发生的
   多个变化，就难多了：对任意的转发变化，判定是否存在 k 轮的无环调度是 NP 难的（Ludwig、Marcinkowski 与 Schmid，2015）。
   开放的是：对最短路径路由实际产生的变化，轮数的紧界；以及既无环又无黑洞的调度。我们的验证器可以逐状态检查任何候选调度。

## Glossary additions

* **packet switching**: data cut into packets that share links, each carrying its destination.
* **statistical multiplexing**: sizing a shared link for the likely number of simultaneous users, not the maximum.
* **encapsulation**: each layer wrapping the unit of the layer above in its own header.
* **end-to-end argument**: functions such as reliability belong at the end points, which alone can complete them.
* **channel capacity** C = B log₂(1 + S/N): the highest rate at which arbitrarily reliable communication is possible.
* **QAM**: quadrature amplitude modulation, a symbol chosen from M points of amplitude and phase.
* **bandwidth-delay product**: the data in flight on a path, rate × round-trip time.
* **bit stuffing**: inserting a 0 after five 1s so that the flag 01111110 cannot appear in data.
* **CRC**: cyclic redundancy check, the remainder of the frame divided by a generator polynomial.
* **MAC address**: a 48-bit link-layer address; **broadcast**: all ones.
* **ALOHA, CSMA/CD, CSMA/CA**: random access; carrier sense with collision detection; with collision avoidance.
* **binary exponential backoff**: after the k-th collision, wait a random number of slots below 2^k.
* **spanning tree protocol**: bridges choosing a loop-free set of active links rooted at the lowest ID.
* **CIDR**: classless prefixes of any length; **longest-prefix match**: the most specific matching route wins.
* **TTL**: a hop count decremented by every router; **ICMP**: IP's error and diagnostic messages.
* **distance vector, link state, path vector**: routing by neighbours' distances, by the whole map, by whole paths.
* **count to infinity**: distance vector's slow convergence after a failure.
* **autonomous system (AS)**: a network under one administration; **BGP**: the protocol between them.
* **prefix hijack**: announcing someone else's addresses; **RPKI, ROA**: signed statements of who may originate what.
* **SDN, OpenFlow, P4**: separating control from forwarding; programmable match-action pipelines.
* **OFDM**: many narrow subcarriers built with an FFT; **cyclic prefix**: a copy of a symbol's end before its start.
* **MIMO**: several antennas at each end, giving parallel spatial channels.

## Sources

* J. F. Kurose and K. W. Ross, *Computer Networking: A Top-Down Approach*.
* L. L. Peterson and B. S. Davie, *Computer Networks: A Systems Approach*.
* A. S. Tanenbaum and D. J. Wetherall, *Computer Networks*; W. R. Stevens, *TCP/IP Illustrated*, vol. 1.
* D. Bertsekas and R. Gallager, *Data Networks*; G. Varghese, *Network Algorithmics*.
* D. Tse and P. Viswanath, *Fundamentals of Wireless Communication*.
* P. Baran, "On Distributed Communications Networks", IEEE Trans. Communications Systems (1964).
* V. Cerf and R. Kahn, "A Protocol for Packet Network Intercommunication", IEEE Trans. Communications (1974).
* J. H. Saltzer, D. P. Reed and D. D. Clark, "End-to-End Arguments in System Design", ACM TOCS (1984).
* D. D. Clark, "The Design Philosophy of the DARPA Internet Protocols", SIGCOMM (1988).
* H. Nyquist, "Certain Topics in Telegraph Transmission Theory" (1928); C. E. Shannon, "A Mathematical Theory of
  Communication" (1948).
* W. W. Peterson and D. T. Brown, "Cyclic Codes for Error Detection", Proc. IRE (1961).
* N. Abramson, "The ALOHA System", AFIPS (1970); R. M. Metcalfe and D. R. Boggs, "Ethernet: Distributed Packet
  Switching for Local Computer Networks", CACM (1976).
* R. Perlman, "An Algorithm for Distributed Computation of a Spanning Tree in an Extended LAN", SIGCOMM (1985).
* V. Srinivasan and G. Varghese, "Fast Address Lookups Using Controlled Prefix Expansion", ACM TOCS (1999).
* J. M. McQuillan, I. Richer and E. C. Rosen, "The New Routing Algorithm for the ARPANET", IEEE Trans. Comm. (1980).
* L. Gao and J. Rexford, "Stable Internet Routing Without Global Coordination", IEEE/ACM ToN (2001).
* T. G. Griffin, F. B. Shepherd and G. Wilfong, "The Stable Paths Problem and Interdomain Routing", IEEE/ACM ToN
  (2002).
* RIPE NCC, "YouTube Hijacking: A RIPE NCC RIS case study" (2008).
* N. McKeown et al., "OpenFlow: Enabling Innovation in Campus Networks", CCR (2008); P. Bosshart et al., "P4:
  Programming Protocol-Independent Packet Processors", CCR (2014); S. Jain et al., "B4", SIGCOMM (2013).
* P. Kazemian, G. Varghese and N. McKeown, "Header Space Analysis", NSDI (2012); A. Fogel et al., "A General
  Approach to Network Configuration Analysis" (Batfish), NSDI (2015).
* P. Francois and O. Bonaventure, "Avoiding Transient Loops During the Convergence of Link-State Routing
  Protocols", IEEE/ACM ToN (2007); A. Ludwig, J. Marcinkowski and S. Schmid, "Scheduling Loop-free Network Updates:
  It's Good to Relax!", PODC (2015).
* R. W. Chang, "Synthesis of Band-Limited Orthogonal Signals for Multichannel Data Transmission", BSTJ (1966);
  G. J. Foschini and M. J. Gans, "On Limits of Wireless Communications in a Fading Environment" (1998); E. Telatar,
  "Capacity of Multi-antenna Gaussian Channels" (1999).
