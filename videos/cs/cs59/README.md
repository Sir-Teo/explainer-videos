# Computer Science, Built — Part 59: Distributed Computing Theory

Part 59 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act XI, *The Research Frontier*. Part 38 proved that consensus is
impossible in one model and built Raft in another; this part is the theory underneath: what n processes can and
cannot compute when each sees only its neighbours, or may crash, or may lie. Some of the answers are lower bounds as
sharp as log* n, and one of them came from algebraic topology.

The instruments are in `explainer/cs/disttheory/` (tested in `tests/test_cs59_disttheory.py`), with two of Part 38's
reused:
* `disttheory/theory.py`: log* n; Cole and Vishkin's 3-colouring of an oriented ring of a million nodes in numpy
  (each round the bit-position step, every node at once, with the colouring checked proper on every edge; then three
  rounds that remove colours 5, 4 and 3), the colours left after each round, and the first 24 nodes' colours for
  drawing; the rounds against log* n from 10 to a million nodes; the log* table up to 2^65536; the hexagon argument
  run against a natural deterministic two-round majority protocol for three processes (six copies A0 B0 C0 A1 B1 C1
  wired in a ring with inputs 0 0 0 1 1 1, each adjacent pair checked for validity and agreement); FloodSet's table
  and Ben-Or's rounds, wrapping the two Part 38 instruments below; Sperner colourings of a triangle cut into k²
  small triangles (corners fixed, sides from their ends' colours, interiors at random), with the rainbow triangles
  listed and a 200-trial parity check; and the four-state exact-majority population protocol under a random pairwise
  scheduler: one run's counts per unit of parallel time, and parallel time against n.
* `dist/consensus.py` (Part 38): `floodset`, checked against every input vector and every crash pattern (who
  crashes, in which round, and which of its last messages still arrive); `ben_or`, Ben-Or's randomized binary
  consensus with f processes crashed from the start and each live process hearing n − f reports per vote. (Since
  exactly n − f processes are then alive, every process hears all of them, so the runs are randomized only by the
  coins; see Problem 5.)

The chromatic subdivisions of Chapter 7, and the decide-the-smallest-id protocol run on them, are computed in the
scene module `s08_topology.py` by enumerating ordered partitions; the approximate-majority run and the epidemic of
Chapter 10 are seeded simulations in `s11_population.py`. The other pictures (Linial's five-id example, the FLP
configuration graphs, the failure-detector timelines, the message matrices) are illustrative and drawn inline.

## Chapters

* **Hook.** A million processes on a ring, each knowing only its own identifier and its successor's, must
  3-colour themselves: 24 neighbours shown, a million colours at round 0, then 38, 12, 8, 6, 5, 4 and 3 — seven
  rounds, about log* n. Three questions: what can be computed locally (Linial: Ω(log* n)), what can be agreed (three
  processes cannot survive one liar; f crashes need f + 1 rounds; asynchrony rules agreement out, Part 38's FLP), and
  what can be computed at all (k-set agreement, by Sperner's lemma). Part 38 built Raft; this part is the theory
  underneath. The plan.
* **1. Models and faults.** Synchronous lockstep rounds, where a missing message proves a fault, against asynchrony,
  where a slow process looks like a dead one; partial synchrony (Dwork, Lynch and Stockmeyer 1988) in between, the
  world Raft lives in. Message passing against shared memory, and Attiya, Bar-Noy and Dolev's 1995 simulation of a
  register while a majority is correct. Crash inside omission inside Byzantine (Lamport, Shostak and Pease 1982).
  Consensus (agreement, validity, termination) and the map the part proves: synchronous crashes, any f in f + 1
  rounds; Byzantine, n > 3f or signatures; asynchronous, deterministically impossible, randomized with n > 2f (n > 3f
  for Byzantine, Bracha 1987); shared memory, a hierarchy. LOCAL and CONGEST (Peleg 2000): information moves one hop
  a round, and every problem takes at most the diameter.
* **2. Locality: colouring a ring.** On a 16-node oriented ring, a t-round algorithm is a function of 2t + 1
  identifiers in a row; on an anonymous ring no deterministic algorithm can even 2-colour. The bit-position trick on
  node 0 of our run: identifier 1,999,591 against its successor's 1,664,200, the lowest differing bit is 0, so the new
  colour is 2·0 + 1 = 1; rounds 2 and 3 tabulated (in round 3 the first difference is at position 2, and v becomes 4).
  Why neighbours still differ: 2i + b determines i and b. How fast colours shrink: b bits become 1 + ⌈log₂ b⌉, so 21
  bits, then 6, 4, 3; the bound allows 42, 12, 8 and 6 colours after rounds 1 to 4, and the run used 38, 12, 8 and 6;
  at 3 bits the trick stops. The 24 drawn nodes recoloured round by round, then colours 5, 4 and 3 removed (their
  nodes are never neighbours, so all at once): 7 rounds, proper on every edge of the million. log* 65,536 = 4,
  log* 2^65536 = 5; rounds against log* n for n = 10, 100, 1,000, 10,000, 100,000 and 1,000,000: 5 against 3, 6
  against 4, 7 against 4, 7 against 4, 7 against 5, 7 against 5 — log* n plus two or three.
* **3. Linial's lower bound.** Linial (1987; in full 1992): a t-round algorithm properly colours the neighbourhood
  graph of windows of 2t + 1 ids, hence its subgraph B_{2t+1} of increasing windows; B_1 is the complete graph and
  needs n colours. The speed-up lemma, χ(B_k) ≤ c ⇒ χ(B_{k−1}) ≤ 2^c, proved by colouring each short window with the
  set of colours of its extensions. Run on five ids, with B_2 coloured by the highest bit where a − 1 and b − 1
  differ: the sets {0, 1, 2}, {1, 2}, {0, 2}, {2} and ∅ are five different sets, at most 2³ = 8 allowed. Iterated:
  3, 8, 256, 2^256, … up to n, so log* n ≤ 2t + 2 and t ≥ ½ log* n − 1; for the million-node ring (log* n = 5) every
  algorithm needs at least 2 rounds, Cole and Vishkin used 7: Θ(log* n). Round elimination as a proof machine, and
  Brandt's 2019 automatic version for problems on locally tree-like graphs; Linial's O(Δ²) colours in O(log* n)
  rounds on any graph.
* **4. Synchronous agreement and its bounds.** FloodSet on four processes, one crash: process 2, the only holder
  of a 0, crashes after sending to process 3 alone; process 3 passes it on in round 2; all decide 0; the clean-round
  argument. An adversary defeats f rounds (f = 2: each crash passes the 0 to one process and dies). Exhaustively
  checked, every input and crash pattern: for n = 3, f = 1, 1 round can fail (104 runs), 2 always agree (200); for
  n = 4, f = 1, 528 and 1,040; for n = 4, f = 2, 1 and 2 rounds can fail (6,672 and 25,616 runs) and 3 rounds always
  agree, all 56,848 runs. Every algorithm needs f + 1 rounds: the chain of runs from all-0 to all-1, one crash per
  round (Fischer and Lynch 1982; Dolev and Strong 1983; n ≥ f + 2). Three processes cannot survive one liar: the
  hexagon (Fischer, Lynch and Merritt 1986), run against a natural two-round majority protocol, whose copies decide
  0 0 0 1 1 1 and break where they must, C0 against A1 and C1 against A0, with B the liar; n ≤ 3f by grouping.
  Dolev and Strong's signed relay: any number of faults in f + 1 rounds, and a sender who signs two values is
  exposed.
* **5. Asynchrony: FLP and randomness.** The proof's machinery for three processes (the story was Part 38's).
  Lemma 1, a bivalent start, from the chain 000, 100, 110, 111 and a process crashed from the start; Lemma 2, any
  pending step can be delivered into a bivalent configuration, since a decisive step dies in both cases (steps of
  different processes commute; if both are p's, a finite run σ without p reaches a configuration that is both
  decided and bivalent); Lemma 3, the run that never decides, with every process stepping, every message delivered
  and no crash (Fischer, Lynch and Paterson 1985). Ben-Or (1983): two votes and a coin; never two values proposed in
  a phase; a decision by more than f proposals is adopted by all. Expected phases at most 2^n with private coins.
  Measured with split inputs and f = 1, 2, 3, 4 crashed, 200 runs each: n = 4, 6, 8 and 10 take 4.8, 9.3, 18.2 and
  33.9 phases on average (longest 23, 36, 106 and 192); every run agreed and ended; the mean roughly doubles with
  every two processes, and a common coin would make it constant.
* **6. Shared memory and the consensus hierarchy.** Atomic registers (linearizable, Part 33) and wait-freedom, the
  shared-memory version of surviving n − 1 crashes. A snapshot from registers: two equal collects in a row, retried
  when a writer moves; Afek, Attiya, Dolev, Gafni, Merritt and Shavit's 1993 fix (updates embed a scan, borrowed from
  a process seen moving twice) makes every scan wait-free in at most n + 1 collects. Herlihy's hierarchy (1991):
  registers and snapshots 1; test-and-set, swap, fetch-and-add, queues and stacks 2 (two-process consensus from a
  queue holding win and lose); compare-and-swap and LL/SC ∞; no wait-free queue from registers. Registers cannot
  solve consensus for two, by the cases at a critical configuration (a read, writes to different registers, writes
  to the same one); test-and-set stops at two, because a third process sees the same memory whoever won;
  compare-and-swap returns what it found.
* **7. Topology: why k-set agreement is impossible.** A task as a map Δ between complexes: two processes' inputs form
  a square, consensus's outputs two edges. One round of write-then-immediate-snapshot (Borowsky and Gafni 1993)
  cuts an edge into a path of three, 3^r edges after r rounds, always connected, so some edge joins a 0 and a 1:
  registers cannot solve consensus. For three processes the chromatic subdivision has 13 triangles after one round
  (one per ordered partition) and 169 after two, with no holes. Sperner's lemma (1928) on k = 8: 19 rainbow
  triangles of 64, 5 boundary doors; 200 more random colourings (of a 100-triangle subdivision) have 7 to 37 rainbow
  triangles, always an odd number. k-set agreement (Chaudhuri 1990): solvable for k > f by deciding the smallest of
  n − f values; for three processes, k = 2, wait-free, "decide the smallest id seen" after two rounds is a Sperner
  colouring, and 1 of the 169 triangles is a run with three decisions. Impossible for k ≤ f (Borowsky and Gafni;
  Herlihy and Shavit; Saks and Zaharoglou, 1993); the asynchronous computability theorem; the 2004 Gödel Prize.
* **8. Failure detectors.** Chandra and Toueg (1996): a local oracle of suspicions, described by the mistakes it may
  make. Heartbeats with a timeout doubled after each false suspicion make an eventually perfect detector ◇P under
  partial synchrony. Strong and weak completeness, strong, weak and eventual accuracy: eight classes, four after
  gossiping suspicions (P, S, ◇P, ◇S, with ◇S the weakest). The rotating-coordinator algorithm with ◇S and a correct
  majority (n = 5, p₅ crashed, a suspected coordinator in round 1, a decision in round 2; two majorities intersect).
  Why a majority is needed with ◇P (three runs, two halves deciding 0 and 1), and why S needs none. Ω, a leader that
  is eventually the same correct process everywhere, is the weakest detector for consensus (Chandra, Hadzilacos and
  Toueg 1996), equivalent to ◇S, and the leader election of Paxos and Raft (Part 38). In practice: φ accrual
  (Hayashibara, Défago, Yared and Katayama 2004; a threshold of 8 means a mistake would have probability 10⁻⁸) and
  SWIM (Das, Gupta and Motivala 2002).
* **9. The cost of agreement.** One all-to-all round of seven processes: 42 messages; FloodSet's (f + 1)n(n − 1),
  about n³/3 with f near n/3; Lamport, Shostak and Pease's relays, like n^{f+1}. Dolev and Reischuk (1985): every
  deterministic Byzantine agreement protocol has runs with Ω(n + f²) messages from correct processes, even with
  signatures (illustrated for n = 25, f = 8): f²/4, about n²/36 at f = (n − 1)/3; Ω(nf) signatures for
  authenticated protocols. The proof by starving one process, as retold by Abraham et al. (2019). PBFT (Castro and
  Liskov 1999), n(n − 1) messages a phase, against HotStuff (Yin, Malkhi, Reiter, Gueta and Abraham 2019), 2(n − 1)
  with a quorum certificate; PBFT's view change O(n³) words by HotStuff's authors' count. Linear per view, but f silent
  leaders in a row cost O(fn) = O(n²): the bound is tight (Momose and Ren 2021 in synchrony; Civit et al. 2022 in
  partial synchrony). Randomness: a committee of size Θ(log n), O(n log n) messages; adaptive adversaries and
  Algorand (Chen and Micali 2019); Ω(f²) again if sent messages can be erased (Abraham et al. 2019); constant expected
  rounds (Feldman and Micali).
* **10. Population protocols.** Anonymous finite-state agents meeting in random pairs (Angluin, Aspnes, Diamadi,
  Fischer and Peralta 2004); parallel time; an epidemic among 20 agents; outputs that only stabilise. Exact majority
  with four states (Draief and Vojnović 2012; Mertzios et al. 2014): #A − #B is invariant, so with a positive margin
  everyone ends on A; a tie never settles. Our run: 100 agents, 52 for A against 48, a margin of 4; strong counts
  27 − 23 after one unit of parallel time, down to 4 − 0; the last strong B gone at time 20, every agent outputs A at
  time 58. The mop-up, about (n/2m) ln n; with margin 2, 50, 100, 200 and 400 agents take 64, 136, 284 and 673 units
  (20 runs each, all correct), against the estimate drawn as white ticks; O(log n) time with O(log n) states (Doty et
  al. 2021). Approximate majority in three states (Angluin, Aspnes and Eisenstat 2008): O(log n) time, correct with
  high probability when the margin exceeds about √n log n; an illustrative run of 10 x against 6 y; the cell-cycle
  switch (Cardelli and Csikász-Nagy 2012). Counting sick birds up to five; stably computable = semilinear =
  Presburger-definable (Angluin et al. 2004 and 2006; Angluin, Aspnes and Eisenstat 2006); chemical reaction networks
  (Chen, Doty and Soloveichik 2012) and DNA strand displacement (Soloveichik, Seelig and Winfree 2010).
* **11. Frontier: the complexity of locality.** On rings and paths every locally checkable labelling (Naor and
  Stockmeyer 1995) takes O(1), Θ(log* n) or Θ(n) rounds (three-colouring, maximal independent set and maximal
  matching are log*; two-colouring an even ring is linear); on trees and general graphs the landscape is richer
  (Chang and Pettie 2017; Balliu et al.), with gaps proved by round elimination. Rozhoň and Ghaffari's deterministic
  network decomposition (2020); CONGEST lower bounds from communication complexity; randomness against determinism;
  local ideas inside parallel and sublinear-time algorithms. Four open problems and the ★ research problem.
* **Outro.** Recap, payoffs (Parts 60, 61; Parts 38, 39 and 54), practice, problems, next part.

## Build

```bash
python -m videos.cs.cs59.compute
python -m unittest tests.test_cs59_disttheory
python tools/build.py cs59
```

## Problems, with solutions

1. **Cole–Vishkin.** Prove that one Cole–Vishkin step keeps neighbouring colours different.

   *Solution.* On an oriented ring let w = succ v, and suppose the current colouring c is proper, so c_v ≠ c_w and
   their binary expansions differ somewhere. Node v takes i_v, the lowest index at which c_v and c_w differ, and its
   new colour c′(v) = 2i_v + c_v[i_v]; node w does the same against its own successor, so c′(w) = 2i_w + c_w[i_w].
   Since a bit is 0 or 1, the number 2i + b determines i (as ⌊(2i + b)/2⌋) and b (as its parity). So if
   c′(v) = c′(w), then i_v = i_w = i and c_v[i] = c_w[i]; but i = i_v was chosen as an index where c_v and c_w
   differ, a contradiction. Hence c′ is proper whatever the colours were, the step can be repeated, and since each
   node reads only its own colour and its successor's, all nodes take it in the same round. In our run node 0 has
   identifier 1,999,591 = 111101000001011100111₂ and its successor 1,664,200 = 110010110010011001000₂; they differ
   at bit 0, where v has a 1, so c′(v) = 2·0 + 1 = 1. In round 3, colours 1 = 001₂ and 5 = 101₂ first differ at bit
   2, where v has a 0, so v becomes 4. With b-bit colours, i ≤ b − 1 and c′ ≤ 2b − 1, so the 21-bit identifiers leave
   at most 42 colours after one round; the run used 38.

2. **FloodSet.** Show that FloodSet with f crashes reaches agreement in f + 1 rounds.

   *Solution.* Each process starts with W = {its input}; in each synchronous round it sends W to everyone and adds
   every set it receives; after f + 1 rounds it decides min W. Termination is by construction, and validity holds
   because W only ever contains inputs (if every input is v, W = {v}). For agreement: at most f processes crash and
   there are f + 1 rounds, so by the pigeonhole principle some round r has no crash. Let L be the processes alive at
   the start of round r. None of them crashes during r, so each sends its set to all, and every process alive at the
   end of round r holds U = ⋃_{p ∈ L} W_p (its own set is among them). From then on every message carries U, and a
   union of copies of U is U, so all processes alive after the last round hold U and decide min U. A crash in an
   earlier round, delivering its last message to only some processes, is exactly what makes the sets differ, and a
   clean round repairs it. Our instrument checked every input vector and every crash pattern (who crashes, in which
   round, and which of its last messages arrive): with f + 1 rounds, agreement held in all 200 runs for n = 3,
   f = 1, all 1,040 for n = 4, f = 1, and all 56,848 for n = 4, f = 2; with f rounds or fewer it found a violating run
   every time, such as Chapter 4's chain of crashes passing a 0 to one new process per round. The chain argument of
   Chapter 4 shows no algorithm does better when n ≥ f + 2.

3. **The hexagon.** Use the hexagon argument to show that 3 processes cannot tolerate 1 Byzantine fault.

   *Solution.* Suppose a deterministic protocol for processes A, B and C, without signatures, solves Byzantine
   agreement (agreement, validity, termination) whenever at most one of them is faulty. Build a system S of six
   copies wired in a ring, A0 B0 C0 A1 B1 C1, each running its letter's code with its two ring neighbours in the
   places of the other two letters (A0 talks to C1 and B0), the copies with index 0 having input 0 and those with
   index 1 input 1. S is not a run of the protocol, but every copy behaves deterministically in it. Take any two
   neighbours in S, say A0 and B0. Their views in S are exactly their views in a three-process run in which A and B
   are correct with inputs 0 and 0 and C is Byzantine, showing A the behaviour of C1 and B the behaviour of C0 (C can
   compute both, by simulating S). In that run A and B decide in finite time, so A0 and B0 decide in S, and by
   validity both decide 0. Likewise A1 and B1, with C the liar, decide 1. The pair B0 and C0 sees a run with A faulty,
   so by agreement C0 decides as B0, 0; the pair C0 and A1 sees a run with B faulty and inputs 0 and 1, so by
   agreement A1 decides as C0, 0. But A1 decides 1: a contradiction, so no such protocol exists. For n ≤ 3f, split
   the processes into three groups of at most f and let A, B and C each simulate one group: a protocol for n
   processes tolerating f faults would give one for three tolerating one. Our instrument ran a natural deterministic
   two-round protocol (decide the majority of your input and the four values relayed to you) on the hexagon: A0, B0
   and C0 decide 0 and A1, B1 and C1 decide 1, so validity holds for both pairs with equal inputs, and agreement
   fails exactly on the edges C0–A1 and C1–A0, the two pairs that see a run in which B lies. With signatures the
   argument fails, because C cannot forge what A1 signed when talking to B0: Dolev and Strong's protocol tolerates
   any number of faults.

4. **Sperner's lemma.** Prove Sperner's lemma in two dimensions by counting doors.

   *Solution.* Subdivide a triangle with corners coloured 0, 1 and 2 into small triangles, and colour each vertex on
   a side with one of that side's two corner colours, interior vertices arbitrarily. Call an edge coloured 0–1 a
   door. Count pairs (small triangle, door on its boundary) in two ways. By triangles: a rainbow triangle (colours 0,
   1, 2) has exactly one door; a triangle coloured 0, 0, 1 or 0, 1, 1 has two; any other has none, since it lacks a
   0 or a 1. So the count is #rainbow + 2(…). By doors: an interior door borders two small triangles and a boundary
   door one, so the count is 2D_in + D_∂. Hence #rainbow ≡ D_∂ (mod 2). The sides from 0 to 2 and from 1 to 2 use
   only colours {0, 2} and {1, 2}, so every boundary door lies on the side from 0 to 1. Walking along that side from
   corner 0 to corner 1, the colour starts at 0, ends at 1 and takes only the values 0 and 1, so it switches an odd
   number of times: D_∂ is odd, and so is the number of rainbow triangles, which is therefore at least one. (The same
   count gives a search: enter through a boundary door and keep leaving each triangle by its other door; the walk
   never revisits a triangle, so it either stops in a rainbow triangle or leaves through another boundary door, and
   since the boundary doors are odd in number, some walk must stop in a rainbow triangle.) In our example, k = 8,
   the side from 0 to 1 is coloured 0 0 1 0 1 1 0 0 1, which has 5 doors; of the 64 small triangles 19 have one door,
   5 have two and 40 have none, so the triangle count is 19 + 10 = 29 = 2·12 + 5, with 12 interior doors, and 19 is
   odd. The 200 further random colourings (k = 10) gave 7 to 37 rainbow triangles, always odd.

5. **Build.** Implement Ben-Or's consensus and measure its rounds against n with split inputs.

   *Solution notes.* Start from `ben_or` in `explainer/cs/dist/consensus.py` and the harness `ben_or_rounds` in
   `explainer/cs/disttheory/theory.py`, but make the asynchrony real. Run the processes on an event queue with random
   message delays, as Part 38's Raft network does; a process in phase r broadcasts (r, report, x), waits for n − f
   reports of phase r, broadcasts (r, proposal, v or ?), waits for n − f proposals of phase r, and buffers messages of
   later phases. Propose v if more than n/2 of all n reports are v; decide v on more than f proposals of v, adopt v
   on at least one, and otherwise flip a private coin; a process that decides keeps taking part for one more phase
   so that others can finish. Crash up to f processes at random times, possibly in the middle of a broadcast, and
   check agreement, validity and termination in every run. Measure the phase in which the last correct process
   decides, over many seeds, for n = 4, 6, 8, 10, … with f = n/2 − 1 and inputs split half and half. For comparison,
   our instrument (f crashed from the start, 200 runs each) took 4.8, 9.3, 18.2 and 33.9 phases on average. There,
   every live process hears the same n − f = n/2 + 1 reports, more than n/2 equal only if all are, so a phase succeeds
   only when all n − f coins agree, with probability 2^{1−(n−f)}; the expected decision phase is 1 + 2^{n−f−1}, that
   is 5, 9, 17 and 33, matching the measurement and doubling with every two processes. With random delays and late
   crashes, processes hear different subsets and the numbers change, but private coins can still need exponentially
   many phases in n. Then replace the private coin by a common coin (one random bit per phase seen by all, here
   simply shared by the simulator) and observe a constant expected number of phases.

6. **★ Research.** The deterministic LOCAL complexity of maximal independent set.

   *Discussion.* Open. A maximal independent set takes Θ(log* n) rounds on rings and paths, and O(Δ + log* n) on
   graphs of maximum degree Δ (Barenboim, Elkin and Kuhn), but on general graphs the deterministic complexity as a
   function of n is not known. Since Rozhoň and Ghaffari's network decomposition (2020) it is polylogarithmic, and
   later work has lowered the exponent; the best lower bound for deterministic algorithms is Ω(min{Δ, log n / log log
   n}) (Balliu, Brandt, Hirvonen, Olivetti, Rabie and Suomela 2019, by round elimination), with Kuhn, Moscibroda and
   Wattenhofer's earlier bounds, which hold even for randomized algorithms. The gap is therefore between about
   log n / log log n and a power of log n larger than one. A full answer would give matching upper and lower bounds
   up to constant factors; good partial answers would push the lower bound above log n, bring the upper bound down to
   O(log n) or below, or settle the question on a natural family of graphs.

## 习题与解答

1. **Cole–Vishkin。** 证明 Cole–Vishkin 的一步保持相邻颜色不同。

   *解答。* 在有向环上设 w = succ v，并设当前着色 c 是正常着色，所以 c_v ≠ c_w，它们的二进制展开在某一位不同。结点 v 取
   i_v 为 c_v 与 c_w 不同的最低位，新颜色为 c′(v) = 2i_v + c_v[i_v]；结点 w 对它自己的后继做同样的事，所以
   c′(w) = 2i_w + c_w[i_w]。因为一个比特只能是 0 或 1，数 2i + b 唯一确定 i（即 ⌊(2i + b)/2⌋）和 b（即它的奇偶性）。所以若
   c′(v) = c′(w)，则 i_v = i_w = i 且 c_v[i] = c_w[i]；但 i = i_v 正是选作 c_v 与 c_w 不同的一位，矛盾。因此无论原来的颜色
   是什么，c′ 都是正常着色，这一步可以重复；而且每个结点只读自己和后继的颜色，所以所有结点在同一轮里同时进行。在我们的
   运行中，结点 0 的标识符是 1,999,591 = 111101000001011100111₂，它的后继是 1,664,200 = 110010110010011001000₂；二者在第
   0 位就不同，v 在这一位是 1，所以 c′(v) = 2·0 + 1 = 1。第 3 轮中，颜色 1 = 001₂ 和 5 = 101₂ 第一次不同在第 2 位，v 在那里
   是 0，于是 v 变成 4。颜色有 b 位时，i ≤ b − 1，c′ ≤ 2b − 1，所以 21 位的标识符在一轮之后至多剩 42 种颜色；实际用了 38 种。

2. **FloodSet。** 证明在 f 次崩溃下，FloodSet 在 f + 1 轮内达成一致。

   *解答。* 每个进程从 W = {自己的输入} 开始；每个同步轮中它把 W 发给所有进程，并把收到的集合都并进来；f + 1 轮后它决定
   min W。终止性由构造保证；有效性成立，因为 W 里只有输入值（若所有输入都是 v，则 W = {v}）。关于一致性：至多 f 个进程
   崩溃，而共有 f + 1 轮，由鸽巢原理，某一轮 r 中没有崩溃。设 L 是第 r 轮开始时活着的进程。它们在第 r 轮中都不崩溃，所以
   每个都把自己的集合发给所有进程，第 r 轮结束时每个活着的进程都持有 U = ⋃_{p ∈ L} W_p（它自己的集合也在其中）。此后每条
   消息携带的都是 U，若干个 U 的并仍是 U，所以最后一轮之后所有活着的进程都持有 U，都决定 min U。较早一轮里的崩溃只把最后
   的消息送到一部分进程，这正是集合出现差别的原因，而干净的一轮把差别抹平。我们的工具检查了每一个输入向量和每一种崩溃
   模式（谁崩溃、在哪一轮、它最后的消息还送到了谁）：用 f + 1 轮时，n = 3、f = 1 的全部 200 次运行，n = 4、f = 1 的全部
   1,040 次，n = 4、f = 2 的全部 56,848 次都达成一致；只用 f 轮或更少时，每一次都找到了破坏一致性的运行，例如第 4 章那条
   崩溃之链：每一轮把 0 只传给一个新的进程。第 4 章的链式论证表明，当 n ≥ f + 2 时，没有算法能做得更好。

3. **六边形。** 用六边形论证证明：3 个进程无法容忍 1 个拜占庭故障。

   *解答。* 假设有一个不用签名的确定性协议，在 A、B、C 三个进程中至多一个出故障时总能解决拜占庭一致（一致性、有效性、
   终止性）。构造一个由六个副本连成环的系统 S：A0 B0 C0 A1 B1 C1，每个副本运行自己字母的代码，把环上的两个邻居当作另外两
   个字母（A0 与 C1 和 B0 通信），下标为 0 的副本输入 0，下标为 1 的输入 1。S 不是协议的一次运行，但其中每个副本的行为都
   是确定的。任取 S 中两个相邻的副本，比如 A0 和 B0。它们在 S 中看到的，恰好是一次三进程运行中看到的：A 和 B 正确、输入
   都是 0，C 是拜占庭进程，对 A 表现得像 C1，对 B 表现得像 C0（C 可以通过模拟 S 算出这两种行为）。在那次运行中 A 和 B 在
   有限时间内做出决定，所以 A0 和 B0 在 S 中也做出决定，由有效性，二者都决定 0。同理，C 撒谎时，A1 和 B1 决定 1。B0 和 C0
   这一对看到的是 A 出故障的运行，由一致性，C0 和 B0 一样决定 0；C0 和 A1 这一对看到的是 B 出故障、输入为 0 和 1 的运行，
   由一致性，A1 和 C0 一样决定 0。但 A1 决定的是 1：矛盾，所以这样的协议不存在。对 n ≤ 3f，把进程分成三组，每组至多 f 个，
   让 A、B、C 各模拟一组：一个容忍 f 个故障的 n 进程协议就会给出一个容忍 1 个故障的三进程协议。我们的工具在六边形上运行了
   一个自然的确定性两轮协议（取自己的输入和转发给自己的四个值的多数）：A0、B0、C0 决定 0，A1、B1、C1 决定 1，所以两对输入
   相同的副本都满足有效性，而一致性恰好在 C0–A1 和 C1–A0 这两条边上被破坏，正是看到“B 在撒谎”的那两对。有了签名，论证就
   不成立了，因为 C 无法伪造 A1 在与 B0 通信时签过的内容：Dolev 和 Strong 的协议能容忍任意多个故障。

4. **斯佩纳引理。** 用数门的方法证明二维的斯佩纳引理（Sperner's lemma）。

   *解答。* 把一个三个角分别着色 0、1、2 的三角形剖分成小三角形，边上的顶点用该边两端的颜色之一着色，内部顶点任意着色。
   把颜色为 0–1 的边称为门。用两种方式数（小三角形，它边界上的一扇门）这样的对。按三角形数：彩虹三角形（颜色 0、1、2）
   恰有一扇门；颜色为 0、0、1 或 0、1、1 的三角形有两扇；其余的没有门，因为缺 0 或缺 1。所以总数是 #彩虹 + 2(…)。按门数：
   内部的门与两个小三角形相邻，边界上的门只与一个相邻，所以总数是 2D_in + D_∂。因此 #彩虹 ≡ D_∂ (mod 2)。从 0 到 2 和从
   1 到 2 的两条边只用颜色 {0, 2} 和 {1, 2}，所以边界上的门都在从 0 到 1 的那条边上。沿这条边从角 0 走到角 1，颜色从 0
   开始、以 1 结束，而且只取 0 和 1，所以它切换了奇数次：D_∂ 是奇数，彩虹三角形的个数也是奇数，因此至少有一个。（同样的
   计数给出一种搜索：从边界上的一扇门进入，每次从三角形的另一扇门离开；这条路不会重复经过同一个三角形，所以要么停在一个
   彩虹三角形里，要么从另一扇边界门出去；边界门的个数是奇数，所以总有一条路停在彩虹三角形里。）在我们的例子 k = 8 中，
   从 0 到 1 的边着色为 0 0 1 0 1 1 0 0 1，有 5 扇门；64 个小三角形中，19 个有一扇门，5 个有两扇，40 个没有，所以计数为
   19 + 10 = 29 = 2·12 + 5，内部有 12 扇门，而 19 是奇数。另外 200 次随机着色（k = 10）得到 7 到 37 个彩虹三角形，总是
   奇数。

5. **动手。** 实现 Ben-Or 的共识算法，在输入一半一半的情况下测量它的轮数随 n 的变化。

   *解答要点。* 从 `explainer/cs/dist/consensus.py` 里的 `ben_or` 和 `explainer/cs/disttheory/theory.py` 里的测量框架
   `ben_or_rounds` 出发，但要让异步成为真的。把进程放在带随机消息延迟的事件队列上运行，就像第38部分的 Raft 网络那样；处于
   第 r 阶段的进程广播 (r, report, x)，等待 n − f 个第 r 阶段的报告，再广播 (r, proposal, v 或 ?)，等待 n − f 个第 r 阶段的
   提议，并把更晚阶段的消息缓存起来。若全部 n 个进程中超过 n/2 报告 v，就提议 v；收到超过 f 个 v 的提议就决定 v，至少一个
   就采纳 v，否则掷一枚私有硬币；已经决定的进程再参与一个阶段，好让其他进程也能结束。在随机时刻让至多 f 个进程崩溃，可以
   在广播的中途，并在每次运行中检查一致性、有效性和终止性。对 n = 4、6、8、10、……，取 f = n/2 − 1、输入一半一半，在许多个
   随机种子上测量最后一个正确进程做出决定的阶段。作为对照，我们的工具（f 个进程一开始就崩溃，每组 200 次运行）平均用了
   4.8、9.3、18.2 和 33.9 个阶段。在那里，每个活着的进程听到的都是同样的 n − f = n/2 + 1 个报告，超过 n/2 个相同只有在全部相同时
   才会发生，所以一个阶段只有当 n − f 枚硬币全部一致时才成功，概率为 2^{1−(n−f)}；做出决定的阶段的期望是 1 + 2^{n−f−1}，
   即 5、9、17 和 33，与测量相符，并且每多两个进程就翻一倍。有了随机延迟和较晚的崩溃，各进程听到的子集不同，数字会变，
   但私有硬币仍可能需要随 n 指数增长的阶段数。然后把私有硬币换成公共硬币（每个阶段一个所有进程都看到的随机比特，这里直接
   由模拟器共享），观察到期望阶段数变成常数。

6. **★ 研究。** 极大独立集的确定性 LOCAL 复杂度。

   *讨论。* 尚未解决。极大独立集在环和路径上需要 Θ(log* n) 轮，在最大度为 Δ 的图上需要 O(Δ + log* n) 轮（Barenboim、
   Elkin 和 Kuhn），但在一般图上，它作为 n 的函数的确定性复杂度仍不清楚。自 Rozhoň 和 Ghaffari 的网络分解（2020）以来，它是
   多对数的，后来的工作又降低了指数；确定性算法最好的下界是 Ω(min{Δ, log n / log log n})（Balliu、Brandt、Hirvonen、
   Olivetti、Rabie 和 Suomela 2019，用轮消去证明），此外还有 Kuhn、Moscibroda 和 Wattenhofer 更早的、对随机算法也成立的下界。
   所以差距在大约 log n / log log n 与 log n 的某个大于一的幂之间。完整的答案应给出相差常数因子以内的上下界；好的部分结果
   可以是把下界推到 log n 以上，把上界降到 O(log n) 或更低，或在某个自然的图族上解决这个问题。

## Glossary additions

* **synchronous, asynchronous, partial synchrony** — lockstep rounds; no bound on delays or speeds; bounds that hold
  only eventually.
* **message passing, shared memory, atomic register** — sending along links; reading and writing shared objects; a
  register whose operations appear instantaneous.
* **crash, omission and Byzantine faults; n and f** — stopping for ever; losing messages; arbitrary behaviour,
  including lies; processes in all and faulty ones at most.
* **consensus: agreement, validity, termination** — no two correct processes decide differently; equal inputs force
  the decision; every correct process decides.
* **LOCAL, CONGEST, radius-t view, diameter** — synchronous rounds with unbounded messages; the same with O(log n)
  bits a link a round; what a node knows after t rounds; the rounds that suffice for anything in LOCAL.
* **oriented ring, proper colouring, Cole–Vishkin (deterministic coin tossing), log* n** — a ring where each node
  knows its successor; neighbours coloured differently; the bit-position step; logarithms taken until reaching 1.
* **neighbourhood graph, speed-up lemma, round elimination** — windows of ids joined to their shifts; one id shorter,
  exponentially more colours; turning a t-round algorithm into a (t − 1)-round one for a derived problem.
* **locally checkable labelling (LCL), network decomposition, maximal independent set** — a problem whose solution
  each node can verify locally; clusters of small diameter coloured with few colours; pairwise non-adjacent nodes
  to which no node can be added.
* **FloodSet, clean round, chain argument, hexagon argument** — flooding the values seen and deciding the minimum; a
  round with no crash; runs linked by indistinguishability; six honest copies fooling a three-process protocol.
* **authenticated (signed) agreement, Dolev–Strong** — agreement with unforgeable signatures, for any number of
  faults in f + 1 rounds.
* **valency: bivalent, univalent (0- and 1-valent), critical configuration, decisive step** — whether both decisions
  are still reachable; a configuration whose every next step fixes the outcome; a step that would decide.
* **randomized consensus, private coin, common coin** — Ben-Or's escape from FLP; coins each process flips alone;
  one coin seen alike by all.
* **wait-free, snapshot, double collect, consensus number, universality** — progress whatever the others do; reading
  all registers at one instant; two equal reads in a row; the most processes an object lets agree; consensus builds
  any object.
* **simplicial complex, simplex, chromatic subdivision, immediate snapshot** — values that can occur together, drawn
  as a shape; one round of reading, drawn as a subdivided triangle.
* **Sperner colouring, rainbow triangle, door** — corners distinct, sides from their ends; a small triangle with all
  three colours; an edge coloured 0–1.
* **k-set agreement, asynchronous computability theorem** — at most k different decisions; solvability as the
  existence of a colour-preserving map from a subdivision.
* **failure detector, completeness, accuracy, P, S, ◇P, ◇S, Ω** — a module of suspicions; crashed processes are
  suspected; correct ones are not, always or eventually; the classes; an eventual common leader.
* **heartbeat, timeout, φ accrual, SWIM** — periodic messages; a deadline for them; suspicion as −log₁₀ of the chance
  a heartbeat is still on its way; probing random members and gossiping verdicts.
* **message and word complexity, Dolev–Reischuk bound, quorum certificate, threshold signature, view change** —
  messages or values and signatures sent; Ω(n + f²); 2f + 1 votes in one signature; replacing a leader.
* **adaptive adversary, committee, after-the-fact removal** — corruption chosen as the protocol runs; a random
  subset that agrees for all; erasing messages already sent.
* **population protocol, parallel time, stable computation** — anonymous finite-state agents meeting in random
  pairs; interactions divided by n; outputs that eventually stop changing.
* **exact and approximate majority, semilinear predicate, chemical reaction network** — always right and slow, or
  fast and right with high probability; Boolean combinations of thresholds and remainders; molecules as agents.

## Sources

* N. Lynch, *Distributed Algorithms* (1996); H. Attiya and J. Welch, *Distributed Computing: Fundamentals,
  Simulations, and Advanced Topics* (2nd ed., 2004); M. Herlihy, D. Kozlov and S. Rajsbaum, *Distributed Computing
  through Combinatorial Topology* (2013); D. Peleg, *Distributed Computing: A Locality-Sensitive Approach* (2000).
* R. Cole and U. Vishkin, "Deterministic coin tossing with applications to optimal parallel list ranking",
  Information and Control 1986; N. Linial, "Locality in distributed graph algorithms", SIAM J. Comput. 1992 (FOCS
  1987); S. Brandt, "An automatic speedup theorem for distributed problems", PODC 2019.
* M. Naor and L. Stockmeyer, "What can be computed locally?", SIAM J. Comput. 1995; Y.-J. Chang and S. Pettie, "A
  time hierarchy theorem for the LOCAL model", FOCS 2017; V. Rozhoň and M. Ghaffari, "Polylogarithmic-time
  deterministic network decomposition and distributed derandomization", STOC 2020; A. Balliu, S. Brandt, J. Hirvonen,
  D. Olivetti, M. Rabie and J. Suomela, "Lower bounds for maximal matchings and maximal independent sets", FOCS 2019.
* L. Lamport, R. Shostak and M. Pease, "The Byzantine generals problem", TOPLAS 1982; M. Fischer and N. Lynch, "A
  lower bound for the time to assure interactive consistency", Information Processing Letters 1982; D. Dolev and
  H. R. Strong, "Authenticated algorithms for Byzantine agreement", SIAM J. Comput. 1983; M. Fischer, N. Lynch and
  M. Merritt, "Easy impossibility proofs for distributed consensus problems", Distributed Computing 1986.
* M. Fischer, N. Lynch and M. Paterson, "Impossibility of distributed consensus with one faulty process", J. ACM
  1985; M. Ben-Or, "Another advantage of free choice: completely asynchronous agreement protocols", PODC 1983;
  G. Bracha, "Asynchronous Byzantine agreement protocols", Information and Computation 1987; C. Dwork, N. Lynch and
  L. Stockmeyer, "Consensus in the presence of partial synchrony", J. ACM 1988.
* H. Attiya, A. Bar-Noy and D. Dolev, "Sharing memory robustly in message-passing systems", J. ACM 1995; M. Herlihy,
  "Wait-free synchronization", TOPLAS 1991; Y. Afek, H. Attiya, D. Dolev, E. Gafni, M. Merritt and N. Shavit, "Atomic
  snapshots of shared memory", J. ACM 1993.
* S. Chaudhuri, "Agreement is harder than consensus: set consensus problems in totally asynchronous systems", PODC
  1990; E. Borowsky and E. Gafni, "Generalized FLP impossibility result for t-resilient asynchronous computations",
  STOC 1993, and "Immediate atomic snapshots and fast renaming", PODC 1993; M. Herlihy and N. Shavit, "The
  topological structure of asynchronous computability", J. ACM 1999 (STOC 1993); M. Saks and F. Zaharoglou, "Wait-free
  k-set agreement is impossible: the topology of public knowledge", SIAM J. Comput. 2000 (STOC 1993); E. Sperner,
  "Neuer Beweis für die Invarianz der Dimensionszahl und des Gebietes", Abh. Math. Sem. Univ. Hamburg 1928.
* T. Chandra and S. Toueg, "Unreliable failure detectors for reliable distributed systems", J. ACM 1996; T. Chandra,
  V. Hadzilacos and S. Toueg, "The weakest failure detector for solving consensus", J. ACM 1996; N. Hayashibara,
  X. Défago, R. Yared and T. Katayama, "The φ accrual failure detector", SRDS 2004; A. Das, I. Gupta and A. Motivala,
  "SWIM: scalable weakly-consistent infection-style process group membership protocol", DSN 2002.
* D. Dolev and R. Reischuk, "Bounds on information exchange for Byzantine agreement", J. ACM 1985; I. Abraham,
  T.-H. H. Chan, D. Dolev, K. Nayak, R. Pass, L. Ren and E. Shi, "Communication complexity of Byzantine agreement,
  revisited", PODC 2019; M. Castro and B. Liskov, "Practical Byzantine fault tolerance", OSDI 1999; M. Yin,
  D. Malkhi, M. Reiter, G. Golan Gueta and I. Abraham, "HotStuff: BFT consensus with linearity and responsiveness",
  PODC 2019; A. Momose and L. Ren, "Optimal communication complexity of authenticated Byzantine agreement", DISC 2021;
  P. Civit et al., "Byzantine consensus is Θ(n²): the Dolev–Reischuk bound is tight even in partial synchrony!",
  DISC 2022; J. Chen and S. Micali, "Algorand: a secure and efficient distributed ledger", Theoretical Computer
  Science 2019; P. Feldman and S. Micali, "An optimal probabilistic protocol for synchronous Byzantine agreement",
  SIAM J. Comput. 1997.
* D. Angluin, J. Aspnes, Z. Diamadi, M. Fischer and R. Peralta, "Computation in networks of passively mobile
  finite-state sensors", PODC 2004 (Distributed Computing 2006); D. Angluin, J. Aspnes and D. Eisenstat, "Stably
  computable predicates are semilinear", PODC 2006, and "A simple population protocol for fast robust approximate
  majority", Distributed Computing 2008; M. Draief and M. Vojnović, "Convergence speed of binary interval consensus",
  SIAM J. Control Optim. 2012; G. Mertzios, S. Nikoletseas, C. Raptopoulos and P. Spirakis, "Determining majority in
  networks with local interactions and very small local memory", ICALP 2014; D. Doty, M. Eftekhari, L. Gąsieniec,
  E. Severson, G. Stachowiak and P. Uznański, "A time and space optimal stable population protocol solving exact
  majority", FOCS 2021.
* L. Cardelli and A. Csikász-Nagy, "The cell cycle switch computes approximate majority", Scientific Reports 2012;
  H.-L. Chen, D. Doty and D. Soloveichik, "Deterministic function computation with chemical reaction networks", DNA
  Computing and Molecular Programming 2012; D. Soloveichik, G. Seelig and E. Winfree, "DNA as a universal substrate
  for chemical kinetics", PNAS 2010.
