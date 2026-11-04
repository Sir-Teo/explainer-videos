# Computer Science, Built (计算机科学，从零搭建)

A forty-two-part course on computer science in English and Chinese, made to the standard of *Analysis, Built* and
*AI, Built*. It starts with Hilbert's question and Turing's paper machine. It then builds a real computer from a
single gate, along with the languages and compilers that program it and the algorithms that make it efficient. It
covers the limits on what any machine can compute, and the codes and ciphers built on those limits. It goes on to the
operating systems, databases, networks and distributed systems that share computers among programs, people and
continents. It ends with graphics, numerical computing, quantum computation, proofs of correctness, and the question
of whether the whole tower can be trusted.

Each part is a 50–60 minute lecture that derives its mathematics on screen and tells its history. It also builds
something that runs. Every number on screen comes from one of three sources: a real computation run by the part's
`compute.py`, a measurement on the machine that renders the video, or a published source, which is cited.
Schematics carry the label `schematic`, and made-up examples the label `illustrative`. The videos are `cs1` …
`cs42`.

The chapter-by-chapter plan and the production standard are in [`SYLLABUS.md`](SYLLABUS.md).

**Status:** plan of record, draft 1 (2026-11-04). No part has been built yet.

## The story

**A pebble.** *Calculus* is Latin for a small stone, the kind people once counted with. In 1928 Hilbert asked
whether a mechanical procedure, something like moving pebbles by rule, could decide every mathematical question.
In 1936 Turing answered him. He defined the machine that would have to do it, and proved that no such machine
can. The machine outlived the question it was built to answer. This series follows it from paper to planet. Each
part adds a layer to the **tower** of abstractions, resting on the layers below, and each act puts a new question
to the tower:

* **Act I, The Machine (1–5).** *What does it take to build Turing's machine?* Logic from switches, arithmetic,
  memory and time, and the stored-program computer. By the end, Pebble, the computer we build from NAND gates, runs
  its first program. It works, and it is slow.
* **Act II, Making It Fast (6–9).** *Why is the same machine a thousand times faster today?* Pipelines,
  out-of-order execution and speculation, the memory hierarchy, and parallel machines. Then physics stops the
  clock, and the free speedups end.
* **Act III, Speaking to the Machine (10–14).** *How does a sentence a person writes become bits a machine runs?*
  The running program, languages and automata, the compiler, the λ-calculus and types, and runtimes.
* **Act IV, Algorithms (15–22).** *How do you think efficiently?* Counting steps, data structures, graphs, the great
  paradigms (greedy, divide and conquer with the FFT, dynamic programming), randomness, strings, geometry and
  optimization. Here the Job's cost drops further than all of Act II's hardware made it drop. The act closes on
  problems that resist every trick.
* **Act V, Limits and Secrets (23–28).** *What can't be computed, what can't be computed fast, and how can hardness
  be put to use?* Undecidability, P versus NP, randomness and interactive proof. Then Shannon's two papers: codes
  that beat noise (1948) and ciphers that beat adversaries (1949), and the public-key cryptography built on
  hardness.
* **Act VI, One Machine, Many Programs (29–33).** *How do many programs share one machine, and how does data
  outlast power failures?* The kernel, virtual memory, concurrency, storage and databases.
* **Act VII, Many Machines (34–37).** *How do machines talk, and how do they agree when anything can fail?* Two
  parts on networks and two on distributed systems. The Job runs on a cluster that loses a node partway through.
* **Act VIII, Horizons and Trust (38–42).** *What other kinds of computation are there, and can we trust what we
  built?* Graphics, numerical computing, quantum computation and proving programs correct. The finale is Ken
  Thompson's "Reflections on Trusting Trust", carried out against our own compiler.

Every part ends on the question the next part answers. Every act ends on the limit the next act gets past.

Three devices hold the series together.

1. **Pebble** (`explainer/cs/pebble/`): the computer the series builds, in code. Each part adds the layer it
   teaches: a gate-level simulator, an ALU, a 32-bit CPU and its assembler, pipelines and caches, a compiler for a
   small language, a type checker and a garbage collector, an operating system, a file system, a database, a network
   stack, Raft, a path tracer, a quantum simulator, and a verifier. Each piece is checked against an independent
   reference: exhaustive truth tables, co-simulation, `sqlite3`, `hashlib`, published test vectors, or invariants
   over thousands of seeded fault schedules.
2. **The Job and its ledger** (`explainer.cs.ledger`): one fixed task carried through every layer. The task is to
   count the words in the thirty Project Gutenberg novels that *AI, Built* reads (its Part 1's `BOOKS`) and list the
   twenty most common. Part 5 runs it on Pebble at gate level. Later parts add rows to the ledger as they change the
   cost: pipelining, caches, an optimizing compiler, a better algorithm, a hash table, a sketch that uses
   kilobytes, a SQL query on our own database, a fetch over our own TCP, and MapReduce on a sixteen-node cluster
   that loses a node. The ledger follows the data. If an algorithm beats a decade of hardware, it shows that. If it
   doesn't, it shows that.
3. **The tower** (`explainer.cs.tower`): the stack of abstractions, drawn on every chapter card next to the
   timeline strip (1800–2030). The current layer is lit. The theory parts light a side column for the limits:
   computability, complexity and information. Payoff cards ("where this comes back") link ideas forward. Callbacks
   link to *AI, Built* and *Analysis, Built* instead of repeating them.

## How it looks

The series draws in the manner of 3Blue1Brown, with the instruments of `explainer/ai/viz.py` and
`explainer/ai/lecture.py`, plus its own in `explainer/cs/`:

* **One idea per frame, drawn big.** The narration explains and the screen shows.
* **Continuity.** A truth table folds into a Boolean cube. A ripple-carry chain becomes a prefix tree. A sorted
  array becomes a binary search tree, and a red–black tree becomes a 2–3–4 tree. Derivations happen in place
  (`cmath` + `morph`).
* **The camera travels the tower.** It zooms from an instruction into the datapath, from the datapath into an
  adder, and from the adder into a NAND gate, then pulls back out. A system call goes down into the kernel and back
  up.
* **Live execution.** Code on screen is real code from the repository. A program counter steps through it while
  registers, memory, caches and stacks update from the emulator's trace.
* **Color is meaning.** Each symbol keeps one color across equations and pictures: data, control, time, cost,
  invariants, the adversary.
* **Real numbers.** Everything plotted comes from the part's `compute.py` or from a measurement on the rendering
  machine (the latency staircase of its caches, the speed of its branch predictor), and the scene asserts it.

## The parts

| # | Part | Mathematics, ideas and history | What we build or compute |
|---|---|---|---|
| **I** | **The Machine** | | |
| 1 | What Is a Computation? | Hilbert, Turing machines, robustness, universality, λ-calculus, Church–Turing, diagonalization, halting, busy beavers | a Turing machine simulator; BB(5) run for 47,176,870 steps |
| 2 | Logic from Switches | Boole, Shannon 1937, CMOS, NAND completeness, Post's lattice, normal forms, BDDs, Shannon's counting bound | the series' gate-level simulator; verified blocks |
| 3 | Arithmetic | two's complement as ℤ/2ⁿ, carry-lookahead as parallel prefix, Wallace trees, SRT and Newton division, IEEE 754, error analysis, CORDIC | Pebble's ALU; Wilkinson's polynomial |
| 4 | Memory and Time | latches as bistable dynamics, timing, metastability, FSMs, Myhill–Nerode, LFSRs over GF(2), SRAM/DRAM | the register file and memory; a metastability histogram |
| 5 | The Stored-Program Computer | ENIAC, EDVAC, the Baby, ISA design, datapath and control, microcode, assembly | **Pebble-32** from NAND gates; the Job, row 0 |
| **II** | **Making It Fast** | | |
| 6 | Pipelines | the iron law, hazards, forwarding, branch prediction (2-bit, gshare, TAGE, perceptron), Amdahl | a cycle-accurate pipeline; predictors on real traces |
| 7 | Out of Order | dependencies and renaming, scoreboard, Tomasulo, ROB, superscalar limits, speculation, Spectre, RISC vs CISC | an out-of-order model; the ILP limit study |
| 8 | The Memory Hierarchy | locality, caches, the 3C model, AMAT, cache-oblivious algorithms, the red–blue pebble game, external memory | a cache simulator; this machine's latency staircase |
| 9 | Parallel Machines | the power wall, MESI, memory consistency, SIMD, work–span and Brent, parallel scan, sorting networks and the 0–1 principle | multicore Pebble; false sharing measured |
| **III** | **Speaking to the Machine** | | |
| 10 | The Running Program | data in memory, the stack and calling conventions, the heap and allocators, linking, loading, undefined behaviour, stack smashing | Pebble's linker and loader |
| 11 | Languages and Automata | regex, NFA/DFA, Thompson, subset construction, pumping, CFGs, the Chomsky hierarchy, CYK/Earley, LL and LR | a regex engine; the Pebble language's parser |
| 12 | The Compiler | IRs and CFGs, dominators, SSA, dataflow as lattice fixed points, optimization, instruction selection, register allocation as coloring | the Pebble compiler; the Job compiled |
| 13 | Lambda and Types | λ-calculus, Church encodings, Y, Church–Rosser, STLC, progress and preservation, Hindley–Milner, System F, Curry–Howard, linear types | a λ reducer; type inference |
| 14 | Runtimes | interpreters, closures, continuations and CPS, bytecode VMs, garbage collection (copying, generational, tri-color), JITs, WebAssembly | a VM and three garbage collectors |
| **IV** | **Algorithms** | | |
| 15 | Counting Steps | models of computation, recurrences and the master theorem, the n log n lower bound, quicksort's 2n ln n, selection, generating functions, amortization | every sort, counted; the Job v1 |
| 16 | Data Structures | universal hashing, linear probing, cuckoo hashing, balanced trees, splay trees, B-trees, Fibonacci heaps, union–find and α(n) | the Job v2 (a hash table) |
| 17 | Graphs | BFS/DFS, SCCs, Dijkstra and the 2024–25 results, Bellman–Ford, MSTs, max-flow min-cut, matching and Gale–Shapley, PageRank | shortest paths on a city grid; flows |
| 18 | The Great Paradigms | greedy and matroids, Karatsuba and Strassen, **the FFT**, dynamic programming, Held–Karp, Dancing Links | FFT big-number multiplication; DP tables |
| 19 | Randomness as a Resource | Freivalds, Schwartz–Zippel, Karger, Miller–Rabin, two choices, Bloom filters, streaming sketches, HyperLogLog, LSH, the probabilistic method | the Job in kilobytes; RANDU's planes |
| 20 | Strings | Rabin–Karp, KMP, Boyer–Moore, Aho–Corasick, suffix trees and arrays, the BWT and FM-index, LZ compression, Myers' diff | a BWT compressor and FM-index on the novels |
| 21 | Geometry | robust predicates, convex hulls, sweep lines, Voronoi and Delaunay, the lifting map, kd-trees, the art gallery | Fortune's sweep; Delaunay on the paraboloid |
| 22 | Optimization | LP geometry, simplex, duality, Klee–Minty, ellipsoid and interior point, total unimodularity, approximation (Christofides, Goemans–Williamson), online algorithms, multiplicative weights | a simplex solver; TSP heuristics |
| **V** | **Limits and Secrets** | | |
| 23 | Undecidable | Rice, the recursion theorem and quines, Post's correspondence, Wang tiles, Hilbert's tenth, Gödel via halting, Kolmogorov complexity, Ω, busy beavers | quines; PRIMEGAME; tilings |
| 24 | P versus NP | the hierarchy theorems, Savitch, NP, Cook–Levin, the reduction web, PSPACE and games, Ladner, barriers, five worlds | verified reductions; our SAT solver |
| 25 | Proofs and Randomness | BPP, hardness vs randomness, circuit lower bounds, communication complexity, IP = PSPACE, zero knowledge, PCP, UGC, fine-grained and parameterized complexity, #P | sum-check and ZK protocols, run |
| 26 | Error-Correcting Codes | Hamming space, Hamming(7,4), bounds, finite fields, Reed–Solomon, CRCs, Shannon's channel theorem, LDPC, polar codes | a scratched QR code, recovered |
| 27 | Secrets | frequency analysis, Enigma, perfect secrecy, PRGs/PRFs, Feistel and AES, modes, MACs, hashes and sponges, cryptanalysis, side channels | AES from scratch; the ECB penguin |
| 28 | Public Keys | Diffie–Hellman, RSA, factoring and discrete logs, elliptic curves, PKI and TLS 1.3, lattices and ML-KEM, SNARKs, FHE, MPC | a TLS-like handshake between two Pebbles |
| **VI** | **One Machine, Many Programs** | | |
| 29 | The Kernel | protection, traps and interrupts, processes, fork/exec, scheduling (SJF, MLFQ, CFS, EDF, Liu–Layland), queueing theory | **PebbleOS** boots and runs two processes |
| 30 | Virtual Memory | paging, multi-level tables, the TLB, Belady's OPT and anomaly, working sets, copy-on-write, hypervisors and nested paging | Pebble's MMU; page replacement on real traces |
| 31 | Concurrency | races, Peterson and the bakery, atomics, MCS locks, semaphores and monitors, deadlock, memory models, linearizability, lock-free, consensus numbers | an interleaving model checker |
| 32 | Storage | disks and flash, file systems, FFS, crash consistency and journaling, LFS, copy-on-write, RAID, LSM trees | a crash-tested file system |
| 33 | Databases | the relational model, algebra and SQL, joins, Selinger's optimizer, B+ trees, serializability, 2PL, MVCC and snapshot isolation, ARIES, column stores | a relational database; the Job as SQL |
| **VII** | **Many Machines** | | |
| 34 | Networks I: Moving Bits | layering and the end-to-end argument, Shannon–Hartley, ALOHA's 1/2e, Ethernet, IP and longest-prefix match, distance vector, link state, BGP | a simulated internet of Pebbles |
| 35 | Networks II: Reliable Conversation | sliding windows, TCP, the 1986 collapse, AIMD and Chiu–Jain, the Mathis formula, bufferbloat, BBR, NUM, DNS, HTTP/3 and QUIC | our TCP; the Job fetched over a lossy link |
| 36 | Agreement | two generals, Lamport and vector clocks, snapshots, FLP, Paxos, **Raft**, Byzantine generals and PBFT, Nakamoto consensus | a fault-injected Raft cluster |
| 37 | Scale | replication and quorums, consistency models, CAP, CRDTs, consistent hashing, Chord, 2PC and Spanner, MapReduce, the tail at scale | the Job on a 16-node cluster that loses a node |
| **VIII** | **Horizons and Trust** | | |
| 38 | Light and Pixels | homogeneous coordinates, projection, rasterization, sampling and mipmaps, ray tracing, BVHs, the rendering equation, path tracing, Béziers | a rasterizer and a path tracer |
| 39 | Computing with Real Numbers | conditioning and backward stability, LU and pivoting, Householder QR, the QR algorithm, CG and Krylov, multigrid, Newton's fractal, stiffness, BLAS | the top-ten algorithms of the century, run |
| 40 | Quantum Computation | Landauer and reversibility, qubits and the Bloch sphere, interference, Simon, the QFT, Shor, Grover, BQP, error correction and the surface code | a state-vector simulator factoring 15 and 21 |
| 41 | Proving Programs Correct | Hoare logic, weakest preconditions, separation logic, model checking with BDDs and SAT, abstract interpretation, proof assistants, CompCert and seL4, fuzzing | a verifier, a model checker and a fuzzer |
| 42 | Trusting Trust | memory safety and ROP, hardware attacks, authentication, access control and HRU, the web, supply chains, **Thompson's compiler backdoor in our own compiler**, diverse double-compiling; the tower revisited | the trojan compiler, built and caught; the final ledger |

## Shared code and the Chinese edition

`explainer/cs/` will hold the series' instruments: chapter cards with the tower and timeline, the series map, the
ledger, and the CS visual instruments listed in the syllabus. The lecture set pieces (definition, theorem, history and
objectives cards, the problem set) and the text helpers are reused from `explainer.ai.lecture` and
`explainer.analysis`. Chinese narration will live in `videos/cs/csN/narration_zh.json`, on-screen text in
`videos/cs/cs_text_zh.json` (`tools/collect_text.py --check csN`), and terms in `videos/cs/CS_ZH_GUIDE.md`.
