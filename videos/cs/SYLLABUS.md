# Computer Science, Built: the syllabus (plan of record, draft 3)

Goal: a university computer-science degree in video, followed by the curriculum industry actually works from. It
aims to be **as comprehensive as the standard textbooks, as technical as a graduate course, as practical as a senior
engineer's working knowledge, and as close to the frontier as primary sources allow**. It tells how the field got
here alongside the mathematics. It is made in English and Chinese to the standard of *Analysis, Built* and *AI,
Built*, and renders on macOS and Linux. Each part runs **50–60 minutes**, and its content decides where in that range
it lands. Sixty-one parts come to about **58 hours**: a degree in fifty-five, and a research tier in six more.

The plan has the shape of a degree plus a career:
- **Act I** opens with discrete mathematics (Lehman, Leighton & Meyer) and then builds the machine. Acts I and II
  together are a computer-organization and architecture sequence (Harris & Harris, Patterson & Hennessy, Hennessy &
  Patterson).
- **Act III** covers systems programming, compilers and programming languages (CS:APP, the Dragon Book, Cooper &
  Torczon, TAPL, SICP).
- **Act IV** is a two-semester algorithms course that ends in algorithm engineering (CLRS, Kleinberg & Tardos, Knuth,
  Motwani & Raghavan, de Berg et al., Williamson & Shmoys, Skiena).
- **Act V** covers the theory of computation, complexity, coding theory and cryptography (Sipser, Arora & Barak,
  MacKay, Katz & Lindell, Boneh & Shoup).
- **Act VI** covers operating systems, storage and databases (OSTEP, Herlihy & Shavit, Silberschatz et al., the Red
  Book).
- **Act VII** covers networks and distributed systems (Kurose & Ross, Peterson & Davie, Lynch, Kleppmann).
- **Acts VIII and IX are the industry curriculum**: software engineering and its tools, the web, services, product
  experimentation, the cloud, data engineering, search, system design and reliability (Ousterhout, *Software
  Engineering at Google*, Kleppmann, Xu, the SRE books, Manning et al., Kohavi et al.).
- **Act X** covers graphics, numerical analysis, quantum computing, formal methods and security (PBRT, Trefethen &
  Bau, Nielsen & Chuang, Baier & Katoen, Anderson).
- **The research tier** runs through the whole series and ends in its own act. Every part closes with a *Frontier*
  chapter at the level of a PhD qualifying exam or a first-year graduate seminar (§1.1). **Act XI** (Parts 56–61)
  then covers the graduate breadth a degree leaves out: spectral graph theory and expanders, learning theory,
  programming-language semantics, distributed-computing theory, domain-specific hardware, and how research itself
  is done (Spielman, Hoory–Linial–Wigderson, Shalev-Shwartz & Ben-David, Winskel, Harper, Lynch, Attiya & Welch,
  Hennessy & Patterson ch. 7, Jain).

Each part's **Reading** line names the textbooks, the classic papers and the frontier papers it follows, and its
reference card shows them on screen. Each part's **In practice** line names the industrial systems, roles and
interview topics it maps to. §2.4 maps the whole series onto the ACM/IEEE-CS/AAAI CS2023 curriculum and onto the jobs
graduates do.

*Draft 2 (2026-11-04)* adds Part 2 (discrete mathematics), Part 24 (algorithms in practice), Acts VIII and IX (Parts
40–50, industry practice), the *In practice* lines and the degree and industry maps, and renumbers the parts to match.
The decisions in §7 are confirmed.

*Draft 3 (2026-11-04)* adds the research tier at the user's request: a *Frontier* chapter and a research problem in
every part (§1.1), and Act XI (Parts 56–61). Parts 1–55 keep their numbers.

## 1. The standard every part meets

The standard is *AI, Built*'s ([`../ai/SYLLABUS.md`](../ai/SYLLABUS.md) §1, and the working guide
[`../ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md)), plus the rules specific to a built series, marked **(CS)**.

**A part is a story.** It opens on a hook: a question, a failure or a famous moment. It closes on the answer, and on
the question the next part takes up. Each part below states its **story** in one or two sentences. Every chapter
serves that story. A chapter that doesn't is cut, or moved to the part it serves.

**A chapter is a lecture segment of 3–5 minutes.** It runs in this order:

1. A motivating question or failure.
2. A definition card.
3. The derivation on screen, every step, each with a margin reason ("exchange argument", "potential drops by 1",
   "pigeonhole").
4. A computed experiment, or a run of the thing we built, that checks the result.
5. A worked example or a *pause-and-predict* question.
6. The takeaway, with a forward link.

**Per part:**
- An objectives card.
- Theorem, definition and algorithm cards. Pseudocode is typeset, and code taken from the repository is excerpted and
  highlighted line by line as it runs.
- A problem set: 4–6 problems, about 90 s on screen, with full solutions in the part's README in English and Chinese.
  **(CS)** At least one problem is a *build* problem against the repository's code, for example "add a `mul`
  instruction to Pebble and re-run the Job", with the expected result in the README. **(CS)** Parts with an
  interview-style counterpart (Acts IV, VII–IX) add one problem in that style, such as "design a rate limiter for…",
  with a worked answer.
- A reference card listing textbooks, the classic papers and the frontier papers.
- **(CS)** An *In practice* card in the outro: the systems, roles and skills the part maps to (the plan's *In
  practice* line).
- **(CS, research tier)** A *Frontier* chapter before the outro, and a research problem (★) in the problem set
  (§1.1).

**The history thread.**
- Every part opens with its era ("how we got here", 2–3 min), lit on the timeline strip (1800–2030).
- Every idea is credited with its people and year, its dead ends included: delay lines, Itanium, the Lisp machines,
  CODASYL, the OSI stack, waterfall.
- The timeline strip gains each part's milestones. The tower strip lights the part's layer.

**Frontier sweep.** Before a part is written, its literature is checked against primary sources (papers, standards,
RFCs, vendor documentation, engineering post-mortems) up to the writing date. Recent results the plan relies on
(mostly from 2024 on) are marked **(verify)** below, and must be checked against their primary sources before they go
on screen. **(CS)** Industry facts (prices, product behaviour, defaults) are dated on screen ("as of …"), because they
change.

**Numbers are real.**
- Computed numbers come from the part's `compute.py`, cached under `.cache/csN/`. Published numbers are cited.
  Schematics carry the label `schematic`, and made-up examples the label `illustrative`.
- **(CS)** Measurements of the machine that renders the video (cache latencies, branch-prediction costs,
  context-switch time, matrix-multiply throughput) are labelled `measured on this machine`. They are reported as
  measured, and the narration follows them, so the Mac build and the Linux build may say different numbers.
- **(CS)** Everything we build is checked against an independent reference (§2.1) before its numbers go on screen.
  Those checks live in `tests/test_cs_*.py`.
- CPU budget: ≤ 2 h per part by default, seeded and resumable (`CACHE.partial`). The named exceptions are listed per
  part.
- Scene assertions use tolerances, not exact equality.
- Narration that states a result is an f-string over the data. When a verdict depends on the data (an algorithm
  beats hardware, a predictor wins, a cache helps), the sentence branches on the computed result.

**Bilingual standard (as *Analysis, Built* and *AI, Built*).**
- Every narration line has its entry in `narration_zh.json`, or in the part's `zh_lines.py` template when the line is
  computed.
- Every on-screen string is in `cs_text_zh.json`, and `tools/collect_text.py --check csN` is clean.
- The glossary in `CS_ZH_GUIDE.md` grows with every new term (图灵机, 停机问题, 与非门, 流水线, 乱序执行, 缓存一致性, 虚拟内存,
  死锁, 共识, 线性一致性, 幂等, 限流, 灰度发布, 可观测性, …).
- Code on screen is never translated. Comments and captions are.

**Gates per part:** `tools/lecture_length.py` (fails under 50 min), `contact_sheet.py`, `dead_air.py`,
`collect_text.py --check`, `check_narration.py`, `zh_lines.py --verify`, and the part's `tests/test_cs*_*.py`.

### 1.1 The research tier

A degree teaches what is settled; a PhD starts where that stops. Every part therefore ends its content with a
**Frontier** chapter (5–8 minutes, one or two scenes), written to the level of a qualifying exam or a first-year
graduate seminar. It does four things:

1. **The limit.** What is the best possible, and how close does the state of the art come? Where we can, the limit is
   computed, not quoted: a limit study on our own traces, a lower bound proved on screen, an idealised machine run
   beside the real one.
2. **What is open**, stated precisely, with the current record and its date ("ω < 2.371339: Alman, Duan, Vassilevska
   Williams, Xu, Xu & Zhou, 2024 **(verify)**").
3. **Recent papers**: two or three from the last five or so years where the field has them, with what each changed.
   Each is checked in the frontier sweep before it goes on screen.
4. **A research problem (★)** in the problem set: open-ended, and possibly open. The README says what is known, how
   a researcher would attack it, and which tool in the repository is the place to start.

The README's reading list is split into the *qualifying-exam canon* and *recent work*. The table gives each part's
Frontier topic; each is refined in that part's frontier sweep.

| Part | Frontier chapter |
|---|---|
| 1 | how BB(5) was proved (non-halting certificates, deciders); BB(6) in Knuth's arrows; Antihydra, run and decoded, and the gambler's-ruin heuristic; machines beyond ZFC (7,910 → 432 states) |
| 2 | Ramsey numbers: R(3,3) by pigeonhole and exhaustion, the Paley graph on 17, Erdős's bounds, the 2023–24 exponential improvements; explicit constructions and Paley clique numbers (computed) |
| 3 | exact minimum circuits for every 3-input function (computed); the census wall at five inputs; gate elimination and the 3.1n record; MCSP and meta-complexity |
| 4 | integer multiplication measured on this machine and the race to n log n; correct rounding of eˣ measured, the table-maker's dilemma, CORE-MATH; the hardest float32 eˣ (computed) |
| 5 | falling Rowhammer thresholds; PARA's probability and Misra–Gries counting, derived; a many-sided attack simulated; Half-Double, RowPress, PRAC |
| 6 | mutation analysis of random co-simulation (computed); coverage-guided CPU fuzzing (DifuzzRTL, Cascade); Sail, Kami, Silver; verifying speculative cores |
| 7 | the limits of branch prediction, computed: idealised PPM against TAGE at every storage budget; the perceptron's linear blind spot; TAGE-SC-L, BranchNet; the data-centre front-end bottleneck |
| 8 | value prediction in the limit study (computed: perfect prediction of every load +19% on the Job, a stride predictor loses at every confidence); secure speculation: an STT/NDA-style rule built into the core, blocking the gadget for 3.5%; speculative non-interference; the cost floor |
| 9 | learned replacement: insertion policies against Belady on the Job's scans (computed), Hawkeye, Glider; the tight red–blue pebble bound for matrix multiply; memory disaggregation |
| 10 | out-of-thin-air values (the load-buffering test enumerated, with and without value speculation) and the unsolved C/C++ memory model; work-stealing constants simulated, locality and heterogeneity open; dark silicon and Landauer's floor |
| 11 | Robson's bound with its adversary run against first fit, and the open exact worst case of first and best fit; CompCert, Cerberus and pointer provenance; CHERI capabilities, a miniature on Pebble stopping the stack smash |
| 12 | regex matching under SETH (Backurs–Indyk), with Thompson's m × n work measured; Valiant's parsing as matrix multiplication, Lee's converse and the clique-based lower bound; Brzozowski derivatives as minimal DFAs, and their revival in real engines |
| 13 | a superoptimizer rebuilt (eight functions, shortest Pebble programs proved by z3; the exponential wall measured); rewrite rules refuted with counterexamples; STOKE, Souper, AlphaDev; equality saturation and e-graphs; MLGO; spilling on SSA left open |
| 14 | dependent and cubical type theory; gradual-typing soundness; effect handlers; Hindley–Milner's DEXPTIME-completeness |
| 15 | pause-time lower bounds for garbage collection; meta-tracing JITs; mechanized WebAssembly |
| 16 | smoothed analysis; lower bounds beyond comparisons; fine-grained complexity |
| 17 | the dynamic optimality conjecture; recent optimal open addressing and tiny pointers **(verify)**; succinct structures |
| 18 | almost-linear max-flow (2022); negative-weight shortest paths (2022); universally optimal Dijkstra (2024); directed SSSP beyond the sorting barrier (2025) |
| 19 | the matrix-multiplication exponent ω; SETH-hardness of edit distance; the limits of the laser method |
| 20 | derandomization (PRIMES in P; identity testing open); optimal sketches and their lower bounds |
| 21 | compressed indexes in O(r) space; edit-distance lower bounds |
| 22 | robust and exact geometric computation; lower bounds for high-dimensional nearest neighbours |
| 23 | near-linear-time linear programming; the polynomial Hirsch conjecture; hardness of approximation and the UGC |
| 24 | learned indexes and algorithms with predictions; the theory–practice gap measured |
| 25 | the smallest Turing machine independent of ZFC; Hilbert's tenth problem over other rings |
| 26 | the three barriers; geometric complexity theory; meta-complexity; recent time–space simulations **(verify)** |
| 27 | the 2-to-2 theorem (2018); MIP* = RE (2020); succinct arguments in practice |
| 28 | polar and Reed–Muller codes achieving capacity; locally decodable codes; list decoding |
| 29 | collisions found in practice (SHA-1, 2017); indistinguishability obfuscation from standard assumptions (2021) |
| 30 | post-quantum standards (2024); SIKE's break (2022); fast bootstrapping in FHE |
| 31 | verified kernels at scale; scheduling for tail latency; verified eBPF |
| 32 | translation-reach research; memory tiering; formal models of virtual memory |
| 33 | the complexity of checking linearizability; weak-memory verification; the cost of wait-freedom |
| 34 | the LSM design space; verified crash consistency; zoned storage |
| 35 | worst-case optimal joins and the AGM bound; learned optimizers; checking isolation levels |
| 36 | programmable data planes (P4); network verification; routing convergence |
| 37 | congestion control's impossibility results (starvation, 2022); the theory of fairness |
| 38 | lower bounds for consensus; linear-communication BFT (HotStuff); verified distributed systems |
| 39 | the limits of consistency under availability (CAC); CRDT theory; Jepsen's findings |
| 40 | empirical software engineering's evidence base; evaluating AI coding agents |
| 41 | structured merge; complete version solving; formally correct builds |
| 42 | layout complexity; JIT-engine security; formal web security models |
| 43 | session types; API evolution, measured; exactly-once, formalized |
| 44 | causal inference under interference; always-valid inference |
| 45 | bin-packing schedulers' guarantees; serverless cold starts; carbon-aware scheduling |
| 46 | Kahn networks and dataflow semantics; differential dataflow; approximate query processing |
| 47 | graph-based nearest-neighbour search and its guarantees; learned sparse retrieval |
| 48 | load balancing in heavy traffic (JSQ, power of d); TTL-cache theory |
| 49 | interleaving anomalies in collaborative editing (Fugue); verified payment protocols |
| 50 | metastable failures, formalized; gray failure; automated root-cause analysis |
| 51 | differentiable and neural rendering (NeRF, Gaussian splatting); ReSTIR |
| 52 | randomized numerical linear algebra; mixed-precision iterative refinement |
| 53 | below-threshold surface codes (2024); quantum-advantage claims and classical spoofing; Regev's factoring (2023) |
| 54 | verification at scale; proof automation with language models; Iris |
| 55 | formal defences against speculation; memory safety at scale; verified bootstrapping |
| 56–61 | each Act XI part is research-level throughout; its Frontier chapter is the open problems of its field |

Parts 1–6 were built before the research tier; their Frontier chapters were added in a retrofit after Part 7
(2026-11-04), with their notes, research problems and Chinese editions.

## 2. The devices

### 2.1 Pebble, the machine we build

Pebble lives in `explainer/cs/pebble/`. It is real, tested Python, with a C fast path wherever speed matters (built
with the system `cc`, with a pure-Python fallback, per the working guide). Each layer is built in the part that
teaches it. Each layer is also checked against something that does not share its code.

| Layer | Module | Built in | Checked against |
|---|---|---|---|
| Netlists and a bit-parallel gate simulator (64 test vectors per `uint64` word, levelized evaluation, unit and real delays) | `hdl.py` | 3 | exhaustive truth tables; random vectors |
| Adders (ripple, Kogge–Stone, Brent–Kung), multipliers (array, Booth, Wallace), divider, ALU, shifter | `blocks.py` | 4 | Python integer arithmetic over all edge cases; exhaustive at 8 bits |
| Latches, flip-flops, register file, SRAM/DRAM models, FSM synthesis | `seq.py` | 5 | cycle-by-cycle reference models |
| **Pebble-32**: the ISA, the gate-level single-cycle CPU, the fast ISA emulator, the assembler | `isa.py`, `cpu.py`, `emu.py`, `asm.py` | 6 | co-simulation of gate level against the emulator on random programs; disassembly round trips |
| Pipeline (5-stage, cycle-accurate), branch predictors, out-of-order core (Tomasulo plus ROB), caches, multicore with MESI | `uarch/` | 7–10 | architectural state equals the emulator's after every program |
| Object format, linker, loader, allocators, the stack smash and its defences | `link.py`, `heap.py`, `jobv1.py`, `smash.py` | 11 | relocation round trips; allocator invariants |
| The **Pebble language** (a small C-like language with functions, arrays, structs and pointers): regex engine, lexer, LL and LR parsers, type checker, SSA compiler with optimizations and register allocation | `lang/` (`regex.py`, `automata.py`, `grammar.py`, `pebble_lang.py` in Part 12) | 12–13 | a Python reference interpreter for the language; differential testing of compiled against interpreted code |
| The λ-core (a small ML: closures, ADTs, Hindley–Milner), bytecode VM, three garbage collectors | `lang/ml/` | 14–15 | a substitution-based reducer; GC heap invariants after every collection |
| **PebbleOS**: traps, timer, processes, schedulers, MMU and paging, locks, a file system on a simulated disk | `os/` | 31–34 | invariants under randomized interrupt timing and crash points |
| A relational database: SQL parser, optimizer, executor, B+ tree, WAL and recovery | `db/` | 35 | `sqlite3` from the standard library, on the same queries and data |
| A network: links with loss and delay, Ethernet-like framing, IP routing, TCP-lite | `net/` | 36–37 | delivery and ordering invariants under seeded loss |
| Distributed systems: a deterministic event simulator, Raft, MapReduce, CRDTs, consistent hashing | `dist/` | 38–39 | safety invariants over thousands of seeded fault schedules |
| Developer tools: a git-compatible object store, a build engine with early cutoff, a version solver, a merge queue | `dev/` | 41 | real git's object hashes (where git is installed); brute-force resolution on small instances |
| A toy browser: an HTML-subset tokenizer and tree builder, the CSS cascade, block and inline layout | `web/` | 42 | hand-computed layouts; a subset of the HTML specification's tokenizer tests |
| Services: RPC with protobuf-style encoding, queues, idempotency keys, sagas; a partitioned log and a stream processor; an inverted index | `svc/`, `stream/`, `search/` | 43, 46, 47 | the published encoding examples; exactly-once invariants under seeded loss and duplication; brute-force query evaluation |
| The cluster substrate: a reconciler, a bin-packing scheduler, an autoscaler, load balancers, caches, rate limiters, fault injection, and metrics, traces and profiles | `cloud/`, `ops/` | 45, 48–50 | closed-form queueing results; exhaustive optimal packing on small instances |
| Cryptography (**educational, never for real use**, said on screen): AES, SHA-256, HMAC, RSA, ECC, a toy LWE, a TLS-like handshake | `crypto/` | 29–30 | FIPS-197 and FIPS-180 vectors, `hashlib`, `hmac`, Python's `pow` |
| A rasterizer and a path tracer | `render/` | 51 | analytic images (the white-furnace test, a lit sphere) |
| A state-vector quantum simulator | `quantum/` | 53 | closed-form states; unitarity and norm checks |
| A VC generator, an explicit and a BDD model checker, abstract interpretation, a fuzzer | `verify/` | 54 | known-answer suites |

**Pebble-32** is our own clean 32-bit RISC in the RISC-V mould. It has sixteen registers with `r0 = 0`,
byte-addressed little-endian memory, four instruction formats and about thirty instructions:
- ALU: `add sub and or xor sll srl sra slt sltu` and their immediate forms, plus `lui`;
- memory: `lw lb lbu sw sb`;
- branches: `beq bne blt bge bltu bgeu`;
- jumps: `jal jalr`.

Later parts add extensions as the series reaches them:
- `mul/div` (Part 4's multiplier, wired into the CPU in Part 7);
- `ecall/eret` and control registers (Part 31);
- a page-table MMU (Part 32);
- `cas` and `amoadd` (Parts 10 and 33).

I/O is memory-mapped: a console, the *tape* (the input stream), a timer, a disk and a network card. A card in Part 6
compares Pebble-32 with RV32I and says where it differs and why. Two speeds are documented: the gate-level CPU runs
a paragraph, and the emulator runs a novel. From Part 43 on, the simulated machines are "nodes" in the event
simulator of `dist/`. The industry acts run their services on that substrate, so every failure they survive is one we
injected.

### 2.2 The Job and its ledger

**The Job:** count the words in the thirty novels and list the twenty most common. The text is the reading of *AI,
Built*'s first part (`BOOKS` in `ai1`'s `compute.py`: thirty Project Gutenberg novels, several million words,
measured exactly in Part 6), so `make.py` computes `ai1` first. The ledger (`explainer.cs.ledger`,
`.cache/cs*/ledger.json`) keeps one row per change. Each row records:
- what changed;
- Pebble cycles per byte of text (simulated);
- the projected time for all thirty novels at a stated clock;
- from Part 16 on, the time measured on this machine;
- memory used;
- from Act IX on, p99 latency, availability and cost in dollars.

| Row | Part | What changes |
|---|---|---|
| 0 | 6 | single-cycle Pebble at gate level, hand-written assembly, words kept in an unsorted list (linear search). Projected at relay speed (the Z3's ~5 Hz), at ENIAC's, and at 1 GHz |
| 1 | 7 | 5-stage pipeline: a faster clock, CPI from the stall breakdown |
| 2 | 8 | 4-wide out-of-order core |
| 3 | 9 | realistic caches (and what the list does to them) |
| 4 | 10 | four cores, SIMD character scanning |
| 5 | 13 | the Job written in the Pebble language: `-O0` against optimized |
| 6 | 15 | the Job in the λ-core, garbage-collected: what GC costs |
| 7 | 16 | **algorithm**: sort then count, n log n |
| 8 | 17 | **algorithm**: a hash table, expected linear time. Rows 0 → 8 are set beside rows 0 → 4: the narration says which mattered more, from the data |
| 9 | 20 | Count-Min and a heap: the top twenty in kilobytes. The ledger's memory column, and the accuracy given up |
| 10 | 24 | **engineering**: a SIMD tokenizer and a Swiss-table-style map, native, against the textbook version |
| 11 | 31 | under PebbleOS: system calls and context switches |
| 12 | 34 | the novels read from our file system |
| 13 | 35 | `SELECT word, COUNT(*) … GROUP BY word ORDER BY 2 DESC LIMIT 20` on our database: the plan it chose |
| 14 | 37 | the novels fetched over our TCP on a lossy link: bytes, round trips, time |
| 15 | 39 | MapReduce on sixteen simulated Pebbles, one of which crashes |
| 16 | 45 | on autoscaled containers: the bill in dollars, at cited and dated prices |
| 17 | 46 | as a stream: a live top-20 with event-time windows, late and duplicate events, exactly-once state |
| 18 | 49 | as a service at a million books a day: p50 and p99 latency, cache hit rate, cost |
| 19 | 50 | that service under crashes, partitions and slow nodes: availability and SLO burn |
| 20 | 55 | the final ledger: every row, and native Python and C on this machine |
| 21 | 60 | **research tier**: the Job in hardware, a word-counting accelerator built in Pebble's HDL; then Part 61 puts confidence intervals on every measured row |

### 2.3 The tower, the timeline and the payoffs

- `explainer.cs.tower`: the stack drawn on every chapter card, with the part's layer lit. From the bottom:
  1. physics, switches, gates;
  2. arithmetic and memory;
  3. the ISA and the microarchitecture;
  4. machine code, languages, algorithms;
  5. the OS, storage and data;
  6. networks and distributed systems;
  7. services and the cloud;
  8. applications (the web, search, products).

  Two side columns sit beside it. *The limits* (computability, complexity, information) is lit by Act V and by the
  theory chapters. *The practice* (engineering, tooling, operations) is lit by Acts VIII–IX.
- `explainer.cs.timeline`, 1800–2030. Among its milestones:

  | Era | Milestones |
  |---|---|
  | 1822–1945 | Babbage (1822, 1837), Boole (1854), Hilbert (1928), Gödel (1931), Church and Turing (1936), Shannon (1937), Z3 (1941), ENIAC and EDVAC (1945) |
  | 1947–1970 | the transistor (1947), the Baby (1948), Shannon (1948, 1949), Hamming (1950), FORTRAN (1957), the IC (1958), Dijkstra (1959), LISP (1960), the NATO software-engineering conference (1968), Unix (1969), Codd (1970) |
  | 1971–1998 | Cook (1971), Make (1976), Diffie–Hellman (1976), RSA (1977), TCP/IP (1983), Paxos (1989), the Web (1991), Shor (1994), Google (1998) |
  | 2004–2025 | MapReduce (2004), git (2005), EC2 and S3 (2006), Kafka (2011), Raft (2014), Kubernetes (2014), Spectre (2018), BB(5) (2024), ML-KEM (2024), and on |
- `payoff_card` ("where this comes back") and `reference_card` from `explainer.ai`. The **callbacks** to other series
  are cards, not repeats:

| Here | Elsewhere |
|---|---|
| 1 Computation, 25 Undecidable | *AI, Built* 2 (Turing, the halting problem sketched); *Analysis, Built* 1 (Cantor's diagonal) |
| 2 Proof and Counting | *Analysis, Built* 1–2 (proof in analysis, ε–δ) |
| 4 Arithmetic, 52 Real Numbers | *AI, Built* 4 (floats and numerics), 17 (number formats) |
| 7–10 Architecture | *AI, Built* 17 (GPUs, the roofline), 18 (collectives) |
| 16–17 Sorting, hashing | *AI, Built* 1 (bits from a comparison, Huffman) |
| 18 Graphs | *AI, Built* 2 (A*), 5 (Markov chains, PageRank's power iteration) |
| 19 FFT, DP | *Analysis, Built* 9 (the Fourier transform); *AI, Built* 7 (Viterbi), 26 (AlphaTensor) |
| 20 Randomness | *AI, Built* 3 (Johnson–Lindenstrauss), 5 (concentration, MCMC), 18 (MinHash dedup) |
| 21 Strings | *AI, Built* 1 (compression), 23 (BPE) |
| 23 Optimization | *AI, Built* 4 (Lagrange, KKT), 6 (boosting), 11 (gradient methods) |
| 26 P vs NP | *AI, Built* 2 (DPLL, CDCL, the 3-SAT phase transition) |
| 28 Codes | *AI, Built* 1 (typical sets), 7 (belief propagation) |
| 44 People and Products | *AI, Built* 26 (bandits), 31 (Goodhart, privacy) |
| 47 Search | *AI, Built* 6 (boosted trees for ranking), 15 (retrieval), 24 (embeddings) |
| 51 Graphics | *AI, Built* 22 (NeRF, Gaussian splatting) |
| 53 Quantum | *Quantum Mechanics, Visualized* and *Part 2* (the physics) |
| 54 Proofs | *AI, Built* 25 (Lean and AlphaProof) |
| 55 Trust | *AI, Built* 31 (can we trust it?) |

### 2.4 The degree and the industry

**A CS degree, course by course.** The areas are those of the ACM/IEEE-CS/AAAI curriculum guidelines (CS2023). The
AI area is the companion series, *AI, Built*.

| Course | CS2023 area | Parts |
|---|---|---|
| Discrete mathematics, probability for CS | MSF | 2 (with 16, 20, 44) |
| Theory of computation | AL | 1, 5, 12, 25 |
| Digital logic, computer organization | AR, SF | 3–6 |
| Computer architecture | AR | 7–10 |
| Systems programming | SF, SDF | 11, 15 |
| Compilers | FPL | 12–13 |
| Programming languages | FPL | 14–15 |
| Algorithms and data structures (two semesters) | AL | 16–24 |
| Computational complexity | AL | 26–27 |
| Coding theory and cryptography | SEC, MSF | 28–30 |
| Operating systems | OS, SF | 31–34 |
| Databases | DM | 35 (with 34, 46) |
| Computer networks | NC | 36–37 |
| Distributed systems | PDC | 38–39 |
| Parallel computing | PDC | 10, 33 |
| Software engineering | SE, SEP | 40–41, 54 |
| Web and mobile development | SPD, HCI | 42–43 |
| Human–computer interaction | HCI | 44 |
| Cloud computing | PDC, SPD | 45 |
| Data engineering | DM, PDC | 46 |
| Information retrieval | DM | 47 |
| System design | PDC, SE | 48–49 |
| Reliability and performance | SF, SE | 50 (with 7–9) |
| Computer graphics | GIT | 51 |
| Numerical methods | MSF | 52 |
| Quantum computing | AR (quantum architectures) | 53 |
| Formal methods | FPL, SE | 54 |
| Security | SEC, SEP | 55 (with 8, 11, 29–30) |
| Society, ethics and the profession | SEP | 40, 44, 55 (with *AI, Built* 31) |

Embedded and real-time systems (SPD) are covered in Parts 5, 6 and 31: memory-mapped I/O, interrupts, RTOS
scheduling, and synchronizers. Games are covered in Parts 22 and 51.

**The industry, role by role.** Each part's outro *In practice* card says which of these it serves.

| Role | Core parts |
|---|---|
| Backend and product engineer | 16–18, 35, 37, 40–43, 48–50 |
| Infrastructure, platform and SRE | 31–34, 36–39, 41, 45, 50 |
| Data engineer | 35, 39, 46, 47 |
| Frontend and mobile engineer | 42, 44, 51 |
| Security engineer | 8, 11, 29–30, 54–55 |
| Systems and performance engineer | 7–10, 24, 31–34, 50 |
| Compiler, language and runtime engineer | 12–15, 54 |
| Hardware, FPGA and chip designer | 3–10 |
| Search and ML infrastructure | 20, 45–47 (with *AI, Built*) |
| Low-latency and quantitative systems | 9–10, 24, 33, 37, 52 |
| Embedded and robotics | 5–6, 22, 31, 52 |
| Researcher | 1–2, 16–30, 53–54 |

**Interviews.** Coding interviews draw on Parts 16–24. System design interviews draw on Parts 39 and 45–50 (Part 49 is
the canon of case studies). Engineering judgement and collaboration questions draw on Parts 40–41 and 50.

## 3. Visual instruments

The series reuses `explainer/ai/viz.py` (`cmath`, `morph`, `LiveBars`, `glow_dot`, `frame_to`, `loss_surface`, axes
and curves), `explainer/ai/lecture.py` (the cards) and `explainer/ai/games.py` (`SearchTree`, `GridView`). New, in
`explainer/cs/viz.py`:

| Instrument | What it shows |
|---|---|
| `Netlist` | gates and wires placed from the simulator's netlist; signals as pulses with real gate delays; the critical path lit |
| `Waveform` | timing diagrams: clock, signals, setup and hold windows, glitches |
| `Datapath` | Pebble's block diagram, with instructions flowing through it as colored packets; zooms down to a `Netlist` |
| `PipelineChart` | instructions × cycles, stalls as bubbles, forwarding as arrows, flushes as strikes |
| `MemoryStrip` | bytes and words with addresses; pointers as arrows; stack frames, heap blocks, free lists |
| `CacheView` | sets × ways with tags; hits and misses flashing; address bits splitting into tag, index and offset |
| `TapeView` | a Turing machine's tape, head and state, with its space–time history scrolling down |
| `Automaton` | state diagrams with tokens moving; the subset construction merging states |
| `TreeView` | BSTs, heaps, tries, parse trees, ASTs, λ-terms, DOM trees; rotations, splays and reductions morph |
| `GraphView` | graphs carrying algorithm state: frontiers, distances, flows, colors, cuts |
| `ArrayView` | arrays as bars and cells; DP tables filling, with traceback; Fenwick and segment trees over arrays |
| `Lattice` | Hasse diagrams: dataflow lattices, CRDT joins, the consistency hierarchy, complexity classes |
| `Gantt` | schedules, job pipelines, MapReduce phases, pipeline bubbles, CI pipelines |
| `SpaceTime` | Lamport diagrams: processes, messages, logical clocks, consistent cuts |
| `SequenceDiagram` | protocols (TCP, TLS, Raft RPCs, Paxos, OAuth, sagas), with loss and retransmission |
| `InterleavingTree` | thread interleavings branching; reachable bad states lit |
| `CommitGraph` | git's DAG: commits, branches, merge bases, a rebase replaying commits |
| `ArchDiagram` | system-design diagrams whose boxes are live simulations: requests flow as packets, queues fill, caches flash hit or miss, a box zooms into its internals |
| `TraceWaterfall` / `FlameGraph` | distributed traces with the critical path lit; profiles as flame graphs |
| `SLOBoard` | error budgets draining, burn rates, latency percentiles over time |
| `QCircuit` / `BlochSphere` / `AmpBars` | quantum circuits, states on the sphere, amplitudes colored by phase |
| `Tower` / `Ledger` | the series devices |

3D camera tours: the Boolean cube and Hamming space; the simplex walking an LP polytope (and the squashed Klee–Minty
cube); Delaunay lifted to the paraboloid; RANDU's points turning until fifteen planes appear; the Bloch sphere; rays
bouncing in our scene; the memory hierarchy as a zoom from registers to disk ("if a cycle were a second"); a data
center zoomed from building to rack to container.

## 4. Part by part

Lengths are targets; the content decides. Each part lists its **story**, its chapters, what is **computed**, the
signature **visuals**, **in practice**, and its **reading**.

---

## Act I · The Machine

### Part 1 · What Is a Computation? (~55)
*Story:* Hilbert asks for a machine that settles every mathematical question. Turing defines the machine, shows that
one machine can imitate all the others, and proves that no machine can do what Hilbert asked. The universal machine
outlives the proof, and the series sets out to build one.
1. Hook: pebbles. *Calculus* means a small stone. Leibniz's *calculemus*; Hilbert's 1928 Entscheidungsproblem.
2. Algorithms before machines: Euclid's GCD and its termination by descent; al-Khwārizmī; what "mechanical" meant.
3. Babbage's Difference Engine: the method of finite differences, which tabulates a polynomial using additions alone
   (computed). The Analytical Engine; Lovelace's Note G and its Bernoulli-number program (1843).
4. Hilbert's program, and Gödel 1931 in one picture (paid off in Part 25).
5. Turing's machine (1936): tape, head, states, transition table. Definition card. Our simulator runs an
   incrementer and a unary adder, with the tape's space–time history drawn.
6. Programming a Turing machine: palindromes, copying, binary addition, subroutines. What they cost: palindromes take
   Θ(n²) on one tape, by the crossing-sequence argument (sketched).
7. Robustness: a multitape machine simulated on a single tape with quadratic slowdown (proved by construction);
   two-way tapes and larger alphabets; nondeterminism adds no power, at an exponential cost in simulation.
8. The universal machine: encoding machines as strings, so that U simulates any M. This is the stored-program idea,
   paid off in Part 6. Small universal machines.
9. Other models with the same power:
   - the λ-calculus (Church 1936): Church numerals computing 2 + 3 on screen;
   - μ-recursive functions;
   - Minsky's two-counter machines, via the 2ᵃ3ᵇ trick;
   - Post systems;
   - Rule 110 (Cook 2004) and Conway's Life.
10. The Church–Turing thesis: what it claims and what it doesn't. The physical thesis, and the extended
    (complexity-theoretic) thesis that Part 53 challenges.
11. Diagonalization: Cantor's argument, then counting. There are countably many machines and uncountably many
    languages, so almost every problem is unsolvable.
12. The halting problem: Turing's proof, animated as an infinite table with its diagonal flipped; the paradoxical
    program.
13. Reductions: from halting to "does M ever print 1?" and "does M halt on a blank tape?". Rice's theorem as a teaser
    (proved in Part 25).
14. Busy beavers (Radó 1962):
    - BB(2) = 6, BB(3) = 21 and BB(4) = 107 steps, recomputed by our simulator;
    - BB(5) = 47,176,870 (bbchallenge, Coq-verified, 2024). We run the champion for all 47 million steps and draw
      its tape;
    - BB grows faster than any computable function (proved).
15. What the series will do: computation is symbol manipulation, one machine is universal, and there are limits.
    Pebble, the tower and the Job are introduced.
16. Outro: recap, problems, payoff cards.

*Computed:* the TM simulator (a C fast path for BB(5)); BB(2–5) step counts; a λ reducer counting β-steps; a Minsky
machine; Rule 110 and a Life glider gun.
*Visuals:* the tape with its history scrolling down like a cellular automaton; the diagonal flipping; BB(5)'s 47
million steps as one giant space–time image, the camera diving in; Church numerals as towers of function boxes.
*In practice:* interpreters, emulators and VMs (the JVM, QEMU, smart-contract VMs) are universal machines; undecidability is why linters, static analyzers and virus scanners must guess.
*Reading:* Turing 1936; Church 1936; Petzold, *The Annotated Turing*; Sipser ch. 3; Moore & Mertens, *The Nature of
Computation* ch. 7; Minsky, *Computation: Finite and Infinite Machines*; Davis, *The Universal Computer*; Aaronson,
"The Busy Beaver Frontier" (2020); bbchallenge (2024–25).

### Part 2 · Proof and Counting (~55)
*Story:* Hilbert's question was about proofs, so before building anything we learn what a proof is. Logic supplies
the grammar. Induction and invariants supply the moves that every later correctness argument uses, from the adder to
Raft. Counting tells us how many things there are (pigeons, subsets, paths, programs), which is the raw material of
every bound in the series. The hook is a puzzle that sold millions of copies and has no solution, and an invariant
proves it.
1. Hook: the 14–15 puzzle (Loyd's $1,000 prize). An invariant (permutation parity plus the blank's row) proves the
   swapped position unreachable (Johnson & Story 1879). BFS on small sliding puzzles finds exactly half the positions
   reachable (computed).
2. Propositions, connectives, truth tables; vacuous truth; equivalences; predicates and quantifiers. Negating ∀∃
   statements, played as a game between a prover and a skeptic (callback to *Analysis, Built* 2's ε–δ).
3. Proof techniques:
   - direct proof, contrapositive and contradiction (√2 is irrational; there are infinitely many primes);
   - proof by cases;
   - constructive against non-constructive proof (irrational a, b with aᵇ rational).
4. Induction: ordinary, strong and well-ordering, and why they are equivalent; the "all horses are one color" trap;
   tiling a 2ⁿ × 2ⁿ board with L-trominoes (recursion animated).
5. Structural induction on recursively defined strings and trees, the form used for parse trees and type
   derivations (Parts 12 and 14).
6. Invariants and variants: the state-machine method (Lehman, Leighton & Meyer); the Die Hard water jugs and their
   gcd invariant; termination by a decreasing measure. This previews Floyd and Hoare (Part 54).
7. Sets, relations, functions:
   - injections, surjections, bijections;
   - equivalence relations and partitions (Myhill–Nerode in Part 5);
   - partial orders and Hasse diagrams; lattices (dataflow in Part 13, CRDTs in Part 39);
   - Dilworth's theorem, briefly.
8. Cardinality: countable sets (ℚ by Cantor's pairing, computed); Cantor–Schröder–Bernstein; Part 1's
   uncountability, revisited.
9. Counting I:
   - the sum and product rules; permutations and combinations;
   - bijective proofs; the binomial theorem; Pascal's triangle (Sierpiński mod 2);
   - Vandermonde's identity, proved combinatorially; stars and bars.
10. The pigeonhole principle:
    - generalized pigeonhole;
    - **Erdős–Szekeres** (a monotone subsequence of length √n, proved);
    - no lossless compressor shrinks every input (callback to *AI, Built* 1).
11. Inclusion–exclusion: derangements (→ 1/e), surjections, Euler's φ; Bonferroni bounds.
12. Counting with recurrences: Fibonacci tilings; **Catalan numbers** with their bijections (parentheses, binary trees,
    triangulations, lattice paths, morphing into each other); Stirling numbers. Generating functions wait for Part 16.
13. Number theory: divisibility; gcd and Bézout (Euclid from Part 1); congruences as clock arithmetic; **the Chinese
    remainder theorem**; the fundamental theorem of arithmetic. Part 30 builds RSA on these.
14. Discrete probability:
    - conditional probability and Bayes (Monty Hall); independence;
    - **linearity of expectation**: in the hat-check problem, the expected number of fixed points is 1 for every n;
    - indicator variables, the tool behind quicksort's analysis (Part 16);
    - Markov, Chebyshev and the union bound.
15. Graph basics: the handshake lemma; trees (n − 1 edges, and the equivalent definitions); bipartite iff no odd
    cycle (Part 18 builds on these). Outro.

*Computed:* reachable-state counts for sliding puzzles and the parity split; Cantor pairing; derangement ratios
converging to 1/e; Catalan bijections enumerated; hat-check simulations; Erdős–Szekeres over random permutations.
*Visuals:* the 15-puzzle with its invariant ticking; the recursive tromino tiling; Pascal's triangle turning into
Sierpiński's; Hasse diagrams; Catalan objects morphing into one another.
*In practice:* invariants are what assertions, code review and property-based tests check; counting is capacity
planning; probability is load and failure analysis; all three appear in the first round of technical interviews.
*Reading:* Lehman, Leighton & Meyer, *Mathematics for Computer Science*; Rosen, *Discrete Mathematics and Its
Applications*; Graham, Knuth & Patashnik, *Concrete Mathematics*; Velleman, *How to Prove It*; Pólya, *How to Solve
It*; Aigner & Ziegler, *Proofs from THE BOOK*; Stanley, *Enumerative Combinatorics* vol. 1 ch. 1; Johnson & Story
1879.

### Part 3 · Logic from Switches (~55)
*Story:* Boole turns logic into algebra, and a 21-year-old Shannon notices that relays obey that algebra. One gate,
NAND, turns out to be enough for everything. Yet almost every function needs an astronomically large circuit, and no
one can point to a single one that does.
1. Boole (1854): the laws of thought as algebra; the axioms; De Morgan; Venn diagrams and truth tables.
2. Shannon's 1937 master's thesis: switches in series are AND, in parallel are OR; the relay circuit as a Boolean
   expression.
3. From relays to tubes to transistors: the MOSFET as a voltage-controlled switch; nMOS and pMOS; the CMOS inverter
   and its transfer curve and noise margins; NAND and NOR in CMOS by series–parallel duality; why CMOS spends power
   only when it switches.
4. NAND is complete (proved: NOT, AND and OR from NAND, then any function by DNF). Post's lattice (1941): a set of
   gates is complete iff it escapes all five maximal clones (monotone, affine, self-dual, 0-preserving,
   1-preserving).
5. Normal forms: DNF and CNF from a truth table, and their exponential cost. Karnaugh maps as Gray-coded faces of the
   Boolean cube (3D) and the 4-variable torus. Prime implicants; Quine–McCluskey; minimization is Σ₂ᵖ-complete
   (Umans).
6. Multiplexers, decoders, encoders. Shannon expansion f = x·f₁ + x̄·f₀. The mux as a lookup table, which is how
   FPGAs work.
7. Binary decision diagrams (Bryant 1986): reduce and share to get a canonical form. Variable order changes the size
   exponentially (computed). Part 54 uses them.
8. Circuit complexity:
   - size and depth;
   - Shannon's counting argument (1949): almost all n-input functions need ≳ 2ⁿ/n gates (proved by counting
     circuits against functions);
   - Lupanov's matching upper bound;
   - yet the best lower bound for an explicit function is about 3.1n. The gap returns in Part 27.
9. Formulas against circuits; parity needs 2ⁿ⁻¹ terms in depth two.
10. Gates take time: propagation delay, the critical path, glitches and hazards, fan-out, RC delay. Our simulator with
    unit delays shows a glitch.
11. The blocks Pebble needs, built and gate-counted: comparators, parity trees, priority encoders, a log-depth barrel
    shifter.
12. The series' hardware layer: netlists in Python, bit-parallel simulation (64 vectors per word), exhaustive
    verification of every block.
13. History: Zuse's Z1–Z3 (1938–41), Stibitz's relay calculators, Atanasoff–Berry, Colossus (1944); Moore's 1965
    paper.
14. Reversible gates (Toffoli, Fredkin) as a preview of Part 53. Outro.

*Computed:* gate counts and critical paths of every block; exhaustive checks; BDD sizes under good and bad variable
orders; Shannon's counting curves; glitch traces.
*Visuals:* relay contacts clicking into series and parallel; the CMOS inverter's transfer curve; truth table →
Boolean cube → K-map faces; a BDD collapsing as nodes merge; two towers of numbers, 2^(2ⁿ) functions against the
circuits of size s.
*In practice:* FPGAs and hardware description languages (Verilog, VHDL, Chisel), logic synthesis, BDD- and SAT-based hardware verification.
*Reading:* Harris & Harris, *Digital Design and Computer Architecture* ch. 1–2; Nisan & Schocken, *The Elements of
Computing Systems* ch. 1; Petzold, *Code*; Shannon 1938, 1949; Bryant 1986; Wegener, *The Complexity of Boolean
Functions*; Jukna, *Boolean Function Complexity*; Knuth, TAOCP 4A §7.1; Weste & Harris, *CMOS VLSI Design* ch. 1;
Li & Yang 2022 (3.1n).

### Part 4 · Arithmetic (~55)
*Story:* A machine has only finitely many bits, so its integers live on a clock and its reals are a sparse,
uneven ruler. The carry chain that makes addition slow becomes, seen the right way, a parallel prefix computation.
Floating point is carefully engineered, and still a wrong number can bring down a rocket.
1. Positional notation; why binary (noise margins); hexadecimal.
2. Integers mod 2ⁿ: overflow as wraparound on a clock. Two's complement as a relabeling of ℤ/2ⁿℤ, so one adder
   serves signed and unsigned. Negation = invert + 1 (proved). Sign extension.
3. Half and full adders. The ripple-carry adder, correct by induction, with delay Θ(n) measured.
4. Carry lookahead: generate and propagate. The carry operator (g, p) ∘ (g′, p′) is associative, which gives a
   parallel prefix tree. Kogge–Stone, Brent–Kung and Sklansky drawn: depth O(log n), with their size, depth and
   fan-out trade-offs. The prefix tree returns in Part 10 (scan).
5. Carry-select and carry-skip adders (√n). Critical paths measured in our netlists.
6. Multiplication: shift-and-add; the array multiplier; Booth recoding; carry-save 3:2 compressors; Wallace and Dadda
   trees, depth O(log n).
7. Division: restoring and non-restoring. SRT, and the Pentium FDIV bug (1994): five missing table entries and a
   $475M charge. Newton–Raphson reciprocals with quadratic convergence (derived); Goldschmidt.
8. Pebble's ALU assembled (add, sub, logic, shifts, compare): its gate count and critical path.
9. Fixed point, and why its dynamic range isn't enough.
10. IEEE 754 (1985, Kahan):
    - sign, exponent, significand;
    - the logarithmic spacing of floats (the camera zooms along the number line);
    - ulp and machine ε;
    - subnormals and gradual underflow; ±0, ∞, NaN;
    - rounding modes and correctly rounded operations.
11. Error analysis:
    - the model fl(x ∘ y) = (x ∘ y)(1 + δ), |δ| ≤ u;
    - catastrophic cancellation in (1 − cos x)/x²;
    - Kahan's compensated summation, error bound proved against naive summation's nu, and pairwise summation;
    - the Patriot clock (1991; 0.34 s after 100 hours) and Ariane 5 (1996; a 64-bit to 16-bit conversion).
12. Conditioning against stability (Wilkinson): perturb one coefficient of ∏(x − k), k = 1…20, by 2⁻²³ and watch the
    roots fly into the complex plane (computed).
13. Beyond IEEE: bfloat16 and FP8 (callback to *AI, Built* 17); posits; interval arithmetic; bignums (Karatsuba waits
    for Part 19).
14. Computing sin, exp and log: range reduction, minimax polynomials, CORDIC shift-and-add rotations (the HP-35).
    Outro.

*Computed:* ripple against lookahead delay over n; Wallace against array depth; a deliberately broken SRT table;
Kahan against naive summation; Wilkinson's roots; CORDIC iterations.
*Visuals:* the 2ⁿ clock; a prefix tree of carries lighting level by level; the float number line with its spacing
doubling at each power of two; the roots scattering.
*In practice:* integer-overflow bugs and CVEs, money in fixed point (never in floats), numerical libraries, ML number formats, the FDIV recall as a lesson in testing.
*Reading:* Harris & Harris ch. 5; Parhami, *Computer Arithmetic*; Koren, *Computer Arithmetic Algorithms*; Goldberg,
"What Every Computer Scientist Should Know About Floating-Point Arithmetic" (1991); Higham, *Accuracy and Stability
of Numerical Algorithms* ch. 1–4; Muller et al., *Handbook of Floating-Point Arithmetic*; Knuth, TAOCP 2 §4.1–4.3;
Overton, *Numerical Computing with IEEE Floating Point Arithmetic*.

### Part 5 · Memory and Time (~55)
*Story:* Connect a circuit's output back to its input and it can remember. Memory brings time into the design, and a
cost that never quite vanishes: a flip-flop can balance between 0 and 1 for an unbounded time. The same machines
that remember turn out to be the first rung of a theory of languages.
1. Feedback: the SR latch from two NANDs. The cross-coupled inverters as a dynamical system: two stable fixed points
   and a saddle, in the computed phase portrait. Metastability is that saddle.
2. The D latch and the edge-triggered flip-flop (master–slave); the clock; registers.
3. Timing: setup, hold, clock-to-Q; f_max = 1/(t_cq + t_logic + t_setup) derived on a timing diagram; clock skew.
4. Metastability: resolution time P(t > τ) ∝ e^{−t/τ}; MTBF = e^{t_r/τ}/(T₀ f_clk f_data); the two-flip-flop
   synchronizer (computed).
5. Finite-state machines, Moore and Mealy: a sequence detector; binary, one-hot and Gray state encodings.
6. FSMs are DFAs: the Myhill–Nerode theorem (proved), and minimization by partition refinement (Hopcroft's
   n log n). The bridge to Part 12.
7. Counters and shift registers. LFSRs: maximal-length sequences from primitive polynomials over GF(2) (period
   2ⁿ − 1), with the LFSR as multiplication by x in GF(2ⁿ). Returns in CRCs (Part 28) and stream ciphers (Part 29).
8. The register file from decoders, multiplexers and flip-flops; what each extra port costs.
9. Memory arrays:
   - the 6T SRAM cell (cross-coupled inverters again), word and bit lines, sense amplifiers;
   - the 1T1C DRAM cell, destructive reads, refresh every 64 ms, row buffers;
   - why DRAM is dense and slow. Part 9 builds on this.
10. Rowhammer (2014): hammering one DRAM row flips bits in its neighbours, and the hardware abstraction leaks (Part
    42 returns to it).
11. The synchronous discipline, and why nearly everyone clocks; asynchronous circuits and the Muller C-element.
12. ROMs, PLAs, FPGAs: memory as logic; a preview of microcode.
13. History: mercury delay lines (EDSAC), Williams tubes, core memory (Forrester, Whirlwind 1953), the Intel 1103
    DRAM (1970); flash previewed for Part 34.
14. Outro.

*Computed:* the cross-coupled-inverter ODE phase portrait; a metastability histogram; Myhill–Nerode minimization;
LFSR periods for every polynomial of degree ≤ 8; the register file in the simulator.
*Visuals:* a ball rolling into one of two wells or balancing on the saddle; setup and hold windows on a waveform;
the DRAM capacitor leaking charge until refresh.
*In practice:* clock-domain crossings in chip design, DRAM refresh and ECC in servers, Rowhammer mitigations, state machines in embedded firmware and protocol code.
*Reading:* Harris & Harris ch. 3; Nisan & Schocken ch. 3; Sipser ch. 1; Hopcroft, Motwani & Ullman ch. 4; Jacob, Ng &
Wang, *Memory Systems*; Golomb, *Shift Register Sequences*; Kim et al. 2014 (Rowhammer); Ginosar, "Metastability and
Synchronizers" (2011).

### Part 6 · The Stored-Program Computer (~60)
*Story:* ENIAC was programmed with cables. The EDVAC report put the program in memory, alongside the data. We build
that machine, Pebble, from the gates of Parts 3–5. It runs Euclid, runs a Turing machine, and runs the Job, which
closes the loop back to Part 1. It also turns out to be very slow.
1. History: ENIAC (1945) and its six programmers; von Neumann's *First Draft* (1945); the Manchester Baby (21 June
   1948); EDSAC (1949), Wilkes and the Wheeler jump.
2. The idea: instructions are data. Fetch, decode, execute; the program counter.
3. Designing an ISA: Pebble-32's word size, registers, formats and encodings (bit fields on screen); the design
   rules (regularity, simple decode, the common case fast); comparison card with RV32I.
4. The single-cycle datapath, built step by step (R-type, loads and stores, branches, jumps), with data flowing
   through it.
5. The control unit: decoding as a truth table, as combinational logic, and as microcode (Wilkes 1951); the
   trade-offs.
6. The assembler: two passes, labels, the symbol table, pseudo-instructions.
7. First programs: sum 1…n, and Part 1's Euclid on gate-level Pebble, traced.
8. Loops, arrays and branches; the cost model, time = cycles × clock period, with the period taken from the measured
   critical path.
9. Memory-mapped I/O: the console and the tape that delivers the novels' characters.
10. The Job, version 0: hand-written assembly with an unsorted word list. A paragraph runs at gate level and a chapter
    on the emulator, with identical results. Ledger row 0, projected to the Z3's relays, ENIAC and 1 GHz.
11. Universality closed: a Turing-machine interpreter in Pebble assembly runs Part 1's BB(3); a TM can simulate
    Pebble. Part 1's loop closes.
12. Code as data: self-modifying code in EDSAC's day, and why we forbid it later (W^X, Part 55).
13. Interrupts and exceptions previewed (Part 31).
14. The whole machine counted: Pebble's gates and critical path, against the 6502 (~3,500 transistors) and a modern
    core (cited).
15. Outro.

*Computed:* the whole CPU netlist; gate-level/emulator co-simulation on random programs; the Job v0; BB(3) on Pebble.
*Visuals:* instruction bits lighting their fields; the datapath with glowing packets; the camera zooms from the
block diagram into one NAND gate and back, the first trip down the tower.
*In practice:* ISA design (RISC-V, ARM, x86), emulators and simulators (QEMU, gem5), memory-mapped peripherals in embedded firmware.
*Reading:* Patterson & Hennessy, *Computer Organization and Design (RISC-V)* ch. 2, 4; Harris & Harris ch. 6–7;
Nisan & Schocken ch. 4–6; von Neumann 1945; Wilkes 1951; Haigh, Priestley & Rope, *ENIAC in Action*; the RISC-V
unprivileged specification.

---

## Act II · Making It Fast

### Part 7 · Pipelines (~55)
*Story:* The iron law says time is instructions × CPI × clock period. Pipelining shrinks the clock period, like
starting the next load of laundry before the first is dry. That creates hazards, and the hardest is the branch,
because the machine must guess where the program goes next. The guessers inside every CPU are small learning
machines, and the best of them is a perceptron.
1. The iron law, derived as a product of ratios; the MIPS myth.
2. Pipelining as laundry: throughput against latency; why the ideal speedup k is never reached; the optimal
   pipeline depth (overhead against hazard penalty, derived).
3. The 5-stage Pebble pipeline built (IF ID EX MEM WB), with its pipeline registers.
4. Structural hazards.
5. Data hazards: RAW; stalls; forwarding paths drawn; the load-use stall.
6. Control hazards: the branch penalty; MIPS's delayed branch as a historical choice.
7. Branch prediction: static; 1-bit against 2-bit saturating counters (Part 5's FSMs); accuracy measured on the Job's
   branch trace.
8. Correlating predictors:
   - global history and gshare;
   - tournament predictors;
   - TAGE, with geometric history lengths (Seznec);
   - the perceptron predictor (Jiménez & Lin 2001), a neural network inside every CPU (callback to *AI, Built*).
9. Branch target buffers and return-address stacks.
10. Precise exceptions in a pipeline.
11. The Job's CPI on the cycle-accurate pipeline, with its stall breakdown. Ledger row 1.
12. The deep-pipeline era and its end: the Pentium 4's 31 stages, the frequency race, and the power wall (Part 10).
13. Amdahl's law, derived, with its corollaries.
14. The sorted-array puzzle, measured on this machine: why sorting data makes a branchy loop several times faster;
    branchless code and conditional moves.
15. Outro.

*Computed:* the cycle-accurate pipeline; CPI breakdowns; 1-bit, 2-bit, gshare, TAGE-lite and perceptron accuracy on
traces of the Job and other programs; sorted against unsorted branches timed on this machine.
*Visuals:* the pipeline chart with bubbles, forwarding arrows and flushes; predictor state machines flipping; the
perceptron's weights as a heatmap over branch history.
*In practice:* performance work with hardware counters (`perf stat`: IPC, branch misses); branchless code in databases, codecs and trading systems.
*Reading:* Patterson & Hennessy ch. 4; Hennessy & Patterson, *Computer Architecture: A Quantitative Approach* ch. 3,
App. C; Shen & Lipasti, *Modern Processor Design*; Smith 1981; Yeh & Patt 1991; McFarling 1993; Seznec & Michaud
2006; Jiménez & Lin 2001; Amdahl 1967.

### Part 8 · Out of Order (~55)
*Story:* An in-order machine waits whenever one instruction waits. Tomasulo's 1967 idea is to let instructions run
as soon as their operands are ready. Add renaming, a reorder buffer and speculation, and modern cores keep hundreds
of instructions in flight. The guesses leave traces, and in 2018 Spectre showed how to read them.
1. The limits of in-order: one cache miss stalls everything. The dataflow graph of a basic block: its critical
   path against the machine's width.
2. Dependencies: true (RAW) against name (WAR, WAW). Renaming removes the false ones.
3. Scoreboarding (CDC 6600, 1964, Thornton and Cray).
4. Tomasulo's algorithm (IBM 360/91, 1967), step by step: reservation stations, the common data bus, tag broadcast.
5. The reorder buffer and in-order commit (Smith & Pleszkun 1985): precise exceptions with out-of-order execution.
   The physical register file and the RAT. The modern pipeline: fetch, rename, dispatch, issue, execute, write back,
   commit.
6. Superscalar issue, and the ILP wall: Wall's 1991 limits study, repeated on our traces with an oracle machine at
   widths 1–16.
7. Speculation past predicted branches, and recovery.
8. Memory disambiguation: load and store queues; store-to-load forwarding.
9. Spectre and Meltdown (2018): speculation leaves cache footprints. The bounds-check-bypass gadget runs in our
   out-of-order model, with a simulated cache-timing channel (Part 55 returns to it).
10. VLIW and EPIC (Itanium): the compiler-scheduled alternative and why it lost; list scheduling and software
    pipelining (Part 13).
11. RISC against CISC: the IBM 801 (Cocke), Berkeley RISC, Stanford MIPS, x86 µops, ARM, RISC-V; the 2017 Turing
    Award.
12. Simultaneous multithreading.
13. Modern cores in numbers (cited): ROB sizes, decode widths, port counts.
14. The Job on our out-of-order model. Ledger row 2.
15. *Frontier*: past the dataflow limit, safely. Value prediction in the limit study (perfect +19%, a stride
    predictor loses); a secure-speculation rule built into the core (blocks the gadget for 3.5%); speculative
    non-interference and the open cost floor.
16. Outro.

*Computed:* the out-of-order simulator (Tomasulo plus ROB) on Pebble traces; IPC against width and ROB size; the
dataflow-limit study; the Spectre toy.
*Visuals:* the CDB broadcasting tags as glowing pulses; the Job's inner-loop dataflow graph with its critical path;
the ROB as a ring buffer filling and retiring.
*In practice:* CPU design teams, Spectre mitigations in kernels, browsers and clouds, reading microarchitecture guides for tuning.
*Reading:* Hennessy & Patterson ch. 3; Tomasulo 1967; Thornton, *Design of a Computer: The Control Data 6600*; Smith &
Pleszkun 1985; Shen & Lipasti; Wall 1991; Patterson & Ditzel 1980; Kocher et al. 2019; Lipp et al. 2018.

### Part 9 · The Memory Hierarchy (~55)
*Story:* Processors got fast and memory didn't; by the 1990s a DRAM access cost hundreds of instructions. Locality
saves us, through caches. The deepest version of the idea is a theorem about pebbles: a lower bound on how much data
any matrix multiply must move.
1. The memory wall (Wulf & McKee 1995): the CPU–DRAM gap over decades (cited).
2. Locality, temporal and spatial; reuse distance; the Job's memory trace as an address-against-time scatter.
3. Direct-mapped caches: tag, index and offset bits; hits and misses animated.
4. Associativity; replacement (LRU, pseudo-LRU, random); write-back against write-through; write-allocate.
5. The 3C model (compulsory, capacity, conflict) measured on traces; miss-rate curves.
6. AMAT = hit time + miss rate × miss penalty, applied recursively across levels.
7. Measured on this machine: the pointer-chasing latency staircase (L1, L2, L3, DRAM, TLB) and a bandwidth test.
   The scale, if one cycle were a second: L1 ≈ 4 s, DRAM minutes, an SSD days, a disk months.
8. Programming for caches: loop interchange; tiled matrix multiply (callback to *AI, Built* 17); arrays of structs
   against structs of arrays. Speedups measured.
9. The ideal-cache model (Frigo et al. 1999): cache-oblivious transpose and multiply; the van Emde Boas tree layout.
10. **The red–blue pebble game** (Hong & Kung 1981): any schedule for n × n matrix multiply with M words of fast
    memory moves Ω(n³/√M) words (proof idea). Our tiled multiply against the bound.
11. External memory (Aggarwal & Vitter 1988): the sorting bound (N/B) log_{M/B}(N/B); B-trees (Parts 17, 35).
12. Prefetching: stride prefetchers and software prefetch.
13. DRAM in depth: banks, rows, CAS and RAS, row-buffer hits; HBM (callback to *AI, Built* 17). The TLB previewed
    (Part 32).
14. The Job with a cache model. Ledger row 3.
15. *Frontier*: learning to replace. Insertion policies on the Job's scans (LRU 63%, bimodal insertion 47%, Belady
    33%, computed); Hawkeye and Glider; online policies against Belady, pebble bounds beyond matrix multiply,
    disaggregated memory.
16. Outro.

*Computed:* a cache simulator on the Job and other traces; 3C breakdowns; this machine's latency staircase and
bandwidth; tiled matmul speedups; the pebble-game bound against simulated misses.
*Visuals:* address bits splitting; cache sets as shelves with tags; the staircase; the camera zooming down the
hierarchy on the "cycle = second" scale.
*In practice:* cache-friendly data layout in game engines, databases and HPC; NUMA tuning; the latency numbers behind every system design.
*Reading:* Hennessy & Patterson ch. 2, App. B; Bryant & O'Hallaron, *Computer Systems: A Programmer's Perspective*
ch. 6; Jacob, Ng & Wang; Drepper, "What Every Programmer Should Know About Memory" (2007); Frigo, Leiserson, Prokop &
Ramachandran 1999; Hong & Kung 1981; Aggarwal & Vitter 1988; Wulf & McKee 1995.

### Part 10 · Parallel Machines (~55)
*Story:* Around 2005 the clocks stopped getting faster, because power density had hit a wall. The way forward was
more cores. That brought new trouble: caches that disagree, memory that reorders, and programs whose speed is set by
their longest chain of dependencies. The adder's carry tree from Part 4 comes back as the core of parallel
computation.
1. The power wall: P = αCV²f; Dennard scaling (1974) and its end; fifty years of microprocessor trends (cited); dark
   silicon.
2. Multicore and shared memory; the Job split across four Pebble cores.
3. Cache coherence: the problem; snooping MSI and MESI as state machines, animated; directories; coherence misses;
   false sharing measured on this machine.
4. Memory consistency: sequential consistency (Lamport 1979); store buffers break it, as the store-buffering litmus
   test shows (both threads read 0); TSO, weak models, fences. The deep dive is Part 33.
5. Atomic instructions: test-and-set, CAS, LL/SC, fetch-and-add (Part 33 uses them).
6. SIMD and vectors: Cray-1 (1976), SSE and AVX, NEON, SVE; vectorizing the Job's character scan.
7. GPUs in one chapter: SIMT, warps, divergence (callback to *AI, Built* 17).
8. The work–span model: T₁, T∞, parallelism T₁/T∞; **Brent's theorem** T_p ≤ T₁/p + T∞ (proved); greedy
   scheduling; work stealing (Blumofe & Leiserson) and its bounds.
9. Parallel prefix (scan): Part 4's carry tree reappears. Blelloch's work-efficient scan and its uses (radix sort,
   stream compaction, lexing).
10. Sorting networks: the **0–1 principle** (proved); Batcher's bitonic sort, depth O(log² n); AKS; optimal small
    networks found by computer search (cited).
11. Amdahl against Gustafson (both derived); strong and weak scaling.
12. Models: PRAM (EREW, CREW, CRCW), BSP (Valiant 1990), LogP; message passing and MPI collectives (callback to *AI,
    Built* 18's all-reduce).
13. Interconnects: bus, crossbar, mesh, torus, hypercube, fat tree; bisection bandwidth.
14. Supercomputers from the Cray-1 to exascale (Top500, cited). Ledger row 4.
15. *Frontier*: thin air, stealing, dark silicon. The load-buffering test enumerated (only (0, 0) in order; any
    self-confirming guess under value speculation); out-of-thin-air values and the unsolved C/C++ memory model
    (Batty et al. 2011, promising semantics 2017); what work-stealing bounds leave out (the constant, about 1.6 spans
    simulated; locality, space, heterogeneous cores); near-threshold computing, 3-D stacking, Landauer's limit.
16. Outro.

*Computed:* the MESI simulation; a false-sharing benchmark on this machine; the work and span of the parallel Job;
Brent's bound against simulated greedy schedules; the 0–1 principle checked exhaustively for n ≤ 10; bitonic
networks; scan.
*Visuals:* cache lines changing color through MESI; the litmus test as two timelines; a work–span DAG with its
critical path glowing; a bitonic network's wires; the scan tree's up-sweep and down-sweep.
*In practice:* multithreaded servers, OpenMP, TBB and Rayon, SIMD intrinsics, GPU kernels, HPC and MPI.
*Reading:* Hennessy & Patterson ch. 5; Sorin, Hill & Wood, *A Primer on Memory Consistency and Cache Coherence*;
Herlihy & Shavit ch. 1; Blelloch 1990; Blumofe & Leiserson 1999; Knuth, TAOCP 3 §5.3.4; Leighton, *Introduction to
Parallel Algorithms and Architectures*; Valiant 1990; Dennard et al. 1974; Esmaeilzadeh et al. 2011.

---

## Act III · Speaking to the Machine

### Part 11 · The Running Program (~55)
*Story:* Follow one program from source to process. Its data turns into bytes, its control flow into branches, its
function calls into a stack, its names into addresses. The linker stitches the pieces together and the loader brings
them to life. Then one unchecked copy overwrites a return address, and the program does something its author never
wrote.
1. A program's life: compiler, assembler, linker, loader, process; one call followed from source to a patched jump.
2. Data in memory: bytes and words; endianness (Cohen 1980, after Swift), measured here; alignment and padding
   (struct sizes measured); row-major arrays; pointers and pointer arithmetic.
3. Control flow in machine code: conditionals and loops as branches (the unsigned range test); a switch compiled by
   gcc into a jump table, its cases ending in tail calls.
4. Procedures: the call stack, activation records, Pebble's calling convention (caller- and callee-saved registers);
   `fact(10)`'s stack depth traced instruction by instruction; gdb's backtrace walking the same frames on this machine.
5. Recursion: Ackermann's function on Pebble (A(3, 6): 172,233 calls, 511 frames); tail calls (1,616 bytes of stack
   against none); guard pages, recursion limits, mutual recursion.
6. The heap: `malloc` and `free`; free lists, boundary tags (Knuth 1968), coalescing; a real trace (Perl counting
   *Pride and Prejudice*, 146,336 allocations, recorded through `LD_PRELOAD`).
7. Five allocators replayed on that trace: first, next and best fit, segregated fits, buddies (Knowlton 1965);
   fragmentation and search cost; internal against external fragmentation; ptmalloc, jemalloc, tcmalloc, mimalloc.
8. Knuth's fifty-percent rule, proved by counting and checked by simulation; Robson's worst-case bound (1971, 1974),
   with its adversary run against first fit.
9. Object files: ELF sections (.text, .data, .bss, relocations), symbol tables, strong and weak symbols, read from
   real object files with readelf; the linker's rules.
10. Linking, step by step with Pebble's linker: symbol resolution, layout, relocation; static archives and why link
    order matters (measured).
11. Static against dynamic linking (measured); position-independent code (GOT and PLT, lazy binding); shared
    libraries; interposition.
12. Loading: `/proc/self/maps`, ASLR measured over three runs, `_start`, argv on the stack.
13. Undefined behaviour: why it exists, and what optimizers do with it (signed overflow; a deleted null check, the
    2009 TUN driver); sanitizers (UBSan, AddressSanitizer) catching four bugs, shadow memory, and their cost measured.
14. The stack smash (the Morris worm 1988; Aleph One 1996) on our Pebble stack, and four defences built and run:
    canary, no-execute stack, randomization, bounds. Part 55 picks this up.
15. The Job, version 1: four assembly files linked by Pebble's linker, frames and a heap list, against Part 6's
    single file.
16. *Frontier*: bounds, semantics, capabilities. CHERI capabilities (Watson et al. 2015; Arm Morello 2022), with a
    miniature on Pebble trapping the smash at the 65th byte; CompCert (Leroy 2006 onward), Cerberus (Memarian et al.
    2016) and pointer provenance; the exact worst case of first and best fit, why real programs fragment so little
    (Johnstone and Wilson 1998), use-after-free defences.
17. Outro. (Exceptional control flow, previewed in the original plan, moves wholly to Part 31.)

*Computed:* Pebble's linker and loader; first-fit, best-fit and segregated allocators on traces, with fragmentation;
stack-depth traces.
*Visuals:* memory as a tall strip, the stack growing down and the heap up; frames pushing and popping; relocation
arrows patching addresses; free lists as chains.
*In practice:* debugging with gdb and lldb, reading compiler output, ABI and linker errors, the exploit mitigations every binary ships with.
*Reading:* Bryant & O'Hallaron ch. 3, 7, 9; Levine, *Linkers and Loaders*; Wilson et al. 1995 (the allocation
survey); Knuth, TAOCP 1 §2.5; Aleph One 1996; the System V ABI.

### Part 12 · Languages and Automata (~60)
*Story:* To program a machine in sentences, we need machines that read sentences. The finite automata from Part 5
read regular languages, and a stack is what lets a machine handle nesting. The Chomsky hierarchy orders languages by
the memory needed to recognize them. A regex can also run in exponential time and take down a large part of the
web.
1. Languages as sets of strings; recognition against parsing; the ladder of memory.
2. Regular expressions (Kleene 1951); the divisible-by-3 DFA (callback to Part 5); Kleene's theorem as a triangle.
3. Thompson's construction (1968): regex to NFA, simulated on sets of states in O(mn), measured.
4. The subset construction (Rabin and Scott 1959) and Moore's minimization; the n-th-from-end language needs 2ⁿ
   states (computed to n = 12; Myhill–Nerode checked); lazy determinization as grep and RE2 do it, on real text.
5. Kleene's theorem: DFA to regex by state elimination; closure properties; decidable equivalence.
6. The pumping lemma, with aⁿbⁿ not regular (every split enumerated); nesting is out of reach.
7. Backtracking engines: (a+)+b measured in Python, Perl and grep; the 2019 Cloudflare and 2016 Stack Overflow
   outages; Cox's argument for RE2; back-references (a composite-number regex) and NP-hardness.
8. Lexing: maximal munch; the lexer for the Pebble language; Python's INDENT/DEDENT stack.
9. Context-free grammars (Chomsky 1956; BNF for ALGOL 60): derivations, parse trees, ambiguity (Catalan counts,
   dangling else), undecidability of ambiguity.
10. Pushdown automata (aⁿbⁿ run; palindromes need nondeterminism); the Chomsky hierarchy; the CFL pumping lemma;
    real languages at the edges (C's lexer hack, C++ and Perl).
11. CYK in O(n³) as dynamic programming (Part 19); Earley's algorithm; both measured.
12. Top-down parsing: recursive descent; LL(1) with FIRST and FOLLOW; removing left recursion; Pratt parsing.
13. Bottom-up parsing: shift–reduce; LR(0) items and the LR automaton (Knuth 1965); SLR, LALR (yacc), LR(1);
    conflicts; checked against bison.
14. The Pebble language parsed: its grammar (79 rules, a conflict-free 146-state LALR table), its parser, its ASTs,
    its error messages.
15. *Frontier*: how fast can we parse? Thompson's O(mn) measured; Myers; Backurs and Indyk (2016) under SETH;
    Valiant (1975), Lee (2002), Abboud–Backurs–Williams (2015); Brzozowski derivatives, which give the minimal DFA on
    every example, and their revival (Owens–Reppy–Turon 2009, parsing with derivatives 2011, .NET 2022).
16. Outro. (Undecidable questions about grammars are previewed in chapter 9 and proved in Part 25.)

*Computed:* our Thompson regex engine against a backtracking one (timing blow-up); subset-construction sizes; CYK
and Earley on ambiguous sentences; the LR tables for the Pebble grammar.
*Visuals:* tokens multiplying along ε-edges; states merging in the subset construction; the pumping lemma cutting a
string; parse trees growing top-down and bottom-up; the LR automaton.
*In practice:* regex engines (RE2, PCRE), parser generators and incremental parsers (ANTLR, tree-sitter), configuration and query languages, protocol parsers.
*Reading:* Sipser ch. 1–2; Hopcroft, Motwani & Ullman; Aho, Lam, Sethi & Ullman, *Compilers* (the Dragon Book) ch.
2–4; Grune & Jacobs, *Parsing Techniques*; Thompson 1968; Knuth 1965; Cox 2007; Pratt 1973; Nystrom, *Crafting
Interpreters*.

### Part 13 · The Compiler (~60)
*Story:* In 1957 FORTRAN had to produce code as good as hand-written code, or nobody would use it. The compiler
turns a parse tree into a graph. On that graph, optimization becomes a fixed-point computation over lattices, and
register allocation becomes graph coloring: NP-hard in general, but solvable in polynomial time on SSA programs. Our
own compiler, about 2,500 lines, beats Part 6's hand-written Job by 12% in instructions, and finds Part 6's pointer
by itself.
1. History: Hopper's A-0 (1952); FORTRAN (Backus 1957, eighteen person-years, "half as fast"); front, middle and
   back ends; M + N instead of M × N (UNCOL 1958, GCC, LLVM); the list Job through every stage, counted.
2. Semantic analysis: scopes as a stack of symbol tables (lexical scope, ALGOL 60); typing rules as inference rules;
   four rejected programs; struct layout and alignment (`Node` 16 bytes, `Entry` 12); globals, virtual registers,
   address-taken locals.
3. Three-address code, basic blocks and leaders, control-flow graphs (Allen 1970); clang's LLVM IR beside ours.
4. Dominators: the definition checked against "delete d"; the iterative algorithm (Cooper–Harvey–Kennedy; 2 passes
   on every function of the Job); dominator trees; dominance frontiers; Lengauer–Tarjan mentioned.
5. SSA (Cytron et al. 1991): φ-functions at iterated dominance frontiers, pruned; renaming down the dominator tree;
   clang's `mem2reg` places the same φs; out-of-SSA copies.
6. Dataflow analysis: liveness iterated on screen (14 visits); reaching definitions and available expressions;
   monotone frameworks on lattices (Kildall 1973), the lattice of subsets and its height; Knaster–Tarski and Kleene;
   meet-over-paths and Kam & Ullman.
7. Optimizations: the constant lattice and SCCP (Wegman & Zadeck 1991); copy propagation and DCE as mark and sweep;
   value numbering (−20% on the array Job); algebra and its traps; phase ordering (clang `-O2`: 88 pass runs).
8. Loops: back edges and natural loops; loop inversion and preheaders; invariant code motion with a type-based load
   rule; induction-variable strength reduction (−36%), which rediscovers Part 6's pointer; unrolling,
   vectorization and the polyhedral model described.
9. Inlining; the call graph and summaries; alias analysis (type-based, address-taken, points-to, `restrict`),
   undecidable in general (Rice; the reduction shown).
10. Instruction selection: tiles; maximal munch; Aho–Johnson dynamic programming and iburg; DAG tiling NP-hard;
    compare-and-branch fusion.
11. Register allocation:
    - interference graphs and Chaitin's coloring (1981): simplify, spill, select; Briggs/George coalescing;
      rematerialization; NP-hard by reduction from coloring;
    - **SSA interference graphs are chordal** (Hack et al. 2006), checked on every function of the Job, and the
      4-hole that leaving SSA creates;
    - the register sweep (13 → 4 registers); linear scan.
12. Instruction scheduling: the dependence DAG and false dependences; list scheduling; on Part 7's pipeline, loop
    inversion costs cycles without prediction and wins with it; software pipelining (callback to Part 8).
13. The Job compiled from the Pebble language, pass by pass and level by level; on Part 8's core (11% fewer
    instructions, the same cycles); ledger row 5; gcc `-O0` … `-O3` on this machine.
14. Correctness: Csmith (Yang et al. 2011); our fuzzer (240 programs, 0 mismatches, and the two bugs it found while
    the compiler was built); five rewrite rules proved or refuted by z3; Alive; translation validation; CompCert
    previewed (Part 54).
15. *Frontier*: the full employment theorem; a superoptimizer (Massalin 1987) rebuilt with z3 proofs; STOKE, Souper,
    AlphaDev; equality saturation and e-graphs (egg, Cranelift); MLGO; open problems. Outro.

*Computed:* our compiler with each pass switched on in turn (instructions on the emulator, cycles on Parts 7 and 8);
fixpoint iterations; coloring with spills and a register sweep; a chordality check on SSA interference graphs; a
differential fuzzer; z3 rule checks; a superoptimizer; clang's IR and gcc's levels on this machine.
*Visuals:* dataflow facts flowing around the CFG; φs landing at dominance frontiers; the interference graph being
colored; the code shrinking pass by pass; an e-graph.
*In practice:* LLVM and GCC, JIT tiers, compiler engineering, reading optimizer output (Compiler Explorer, `-Rpass`),
choosing optimization levels, PGO and LTO.
*Reading:* the Dragon Book; Cooper & Torczon, *Engineering a Compiler*; Appel, *Modern Compiler Implementation in
ML*; Muchnick, *Advanced Compiler Design and Implementation*; Rastello & Bouchez, *SSA-based Compiler Design*;
Nielson, Nielson & Hankin, *Principles of Program Analysis*; Cytron et al. 1991; Chaitin 1981; Kildall 1973; Hack et
al. 2006; Poletto & Sarkar 1999; Lattner & Adve 2004; Yang et al. 2011; Massalin 1987; Willsey et al. 2021.

### Part 14 · Lambda and Types (~55)
*Story:* Church's λ-calculus is a whole programming language made of functions alone. Types tame it. Well-typed
programs cannot go wrong, which we prove and then test. A type can be inferred without being written. And types turn
out to be propositions and programs to be proofs, which is the foundation of the proof assistants of Part 54. The
hook: the Job, written in a λ-core with no type annotations, and every type inferred.
1. λ-terms: three kinds of term and their trees; free and bound variables, α-equivalence; capture-avoiding
   substitution and the capture trap.
2. β-reduction rewriting a subtree; normal forms; Ω = (λx.xx)(λx.xx).
3. Church encodings: booleans, numerals as stacked function boxes, arithmetic measured in β-steps (plus, times, pow);
   pairs and lists; the predecessor (Kleene's trick, 9 + 10n steps).
4. Recursion: the Y combinator derived; factorial by Y (1, 1, 2, 6, 24 in up to 10,384 steps); Y diverges under
   call-by-value and Z does not.
5. Reduction strategies: normal order, applicative, call-by-name, call-by-value, call-by-need, compared on the same
   terms (β counts with sharing, 43/33/33 against 4/4/6); standardization.
6. **Church–Rosser**: every reduction of a small term drawn as a graph (6 terms, 7 steps) and a larger one (30 terms,
   93 steps, one normal form), confluence checked on the whole graph; the diamond, and why parallel reduction proves
   it; de Bruijn indices (environments against substitution, Part 15).
7. Why types: Milner's slogan (1978); stuck terms; the simply typed λ-calculus with its rules as inference rules and
   derivation trees generated by our checker.
8. **Type safety = progress + preservation**, proved by induction on derivations (canonical forms, the substitution
   lemma), then checked on 5,000 random well-typed terms (50,516 steps, none stuck, none changing type).
9. Strong normalization (Tait 1967, logical relations sketched): Ω cannot be typed; 136 of 2,000 random untyped terms
   never stop, no typed one fails to; so STLC is not Turing-complete, and fix brings general recursion back.
10. Hindley–Milner: algorithm W and unification (Robinson 1965), traced on the Job (11 types, 295 unifications);
    let-polymorphism; the occurs check; the exponential let (2^(2^n) leaves, cheap with sharing).
11. System F (Girard 1972, Reynolds 1974); Church encodings typed; parametricity and a free theorem tested (Wadler
    1989): four polymorphic functions hold 200/200, "add one" fails at once.
12. **Curry–Howard**: implication, conjunction and disjunction as function, product and sum types; our prover searches
    for a λ-term and Kripke countermodels refute the rest (fifteen formulas); call/cc and Peirce's law (Griffin 1990).
13. Dependent types: Vec, Π and Σ; Martin-Löf; the calculus of constructions; Agda, Lean and Rocq (Part 54); linear,
    affine and relevant combinators counted; Rust's ownership and borrowing, with rustc's E0382 and E0502 on this
    machine (Part 55).
14. Algebraic data types and pattern matching; option instead of null; subtyping and variance; TypeScript's covariant
    arrays measured (tsc --strict accepts, node throws); gradual typing, sound and unsound (Siek and Taha 2006,
    Takikawa et al. 2016).
15. *Frontier*: HM inference linear in practice and DEXPTIME-complete in theory (McAllester 2003); refinement types
    and SMT (liquid types, F*, Dafny); homotopy type theory and cubical univalence; effect handlers (Plotkin and
    Pretnar 2009, OCaml 5); open problems. Outro.

*Computed:* our λ reducer under four strategies and a lazy environment machine (β-step counts, Church arithmetic,
reduction graphs, confluence checks); the STLC checker, its derivations and a random safety test; HM inference with
traces and the exponential let; free theorems tested in the λ-core; a propositional prover with countermodels;
rustc, tsc and node on this machine.
*Visuals:* β-reduction rewriting a subtree; Church numerals as stacked function boxes; reduction graphs; the
Church–Rosser diamond; derivation trees; unification merging type variables; the Curry–Howard dictionary.
*In practice:* the type systems of TypeScript, Rust, Haskell, OCaml and Scala; generics; IDE type inference; gradual
typing in large codebases; proof assistants.
*Reading:* Pierce, *Types and Programming Languages*; Harper, *Practical Foundations for Programming Languages*;
Barendregt, *The Lambda Calculus*; Hindley & Seldin; Sørensen & Urzyczyn, *Lectures on the Curry–Howard
Isomorphism*; Girard, Lafont & Taylor, *Proofs and Types*; Wadler 1989, 2015; Milner 1978; Damas & Milner 1982;
Siek & Taha 2006; Jung et al. 2018.

### Part 15 · Runtimes (~55)
*Story:* A program needs a runtime to live in. Environments make closures, continuations turn the stack into data,
and a virtual machine provides a portable instruction set; we build one for the λ-core, write it in the Pebble
language and run it on Pebble. The garbage collector cleans up memory while the program keeps running, kept correct
by an invariant stated in three colors. The hook: the Job allocates 79 words per byte of text and never frees one.
1. Interpreters: SICP's eval/apply; McCarthy's eval and Russell's interpreter; metacircularity; `fib(32)` on every
   runtime on this machine (gcc, Go, HotSpot and `-Xint`, V8 and `--jitless`, CPython).
2. Environments and closures; lexical against dynamic scope (both computed); the funarg problem (Moses 1970);
   closure conversion (`CLOSURE`, `FREE`); flat against linked closures.
3. Continuations and CPS: the stack made explicit (CPS factorial on our VM); tail calls as jumps (the Job's stack
   with and without them); call/cc as an early exit on a CEK machine; exceptions and generators from continuations;
   Peirce's law.
4. Bytecode VMs: our 36-instruction stack machine with tagged words; `bump` compiled; the opcode mix; CPython's
   `dis`; stack against register (Lua 5, Shi et al. 2008).
5. The Pebble VM: the VM and Cheney's collector in the Pebble language, co-simulated with the reference count for
   count; 47 instructions per bytecode; dispatch order; switch against threaded code measured in C.
6. Why garbage collection exists (McCarthy 1960): reachability. Reference counting (Collins 1960): the cascade;
   cycles, and CPython's cycle collector measured; what counting would cost the Job; deferred RC.
7. Tracing collectors:
   - mark–sweep and mark–compact, animated; fragmentation; four collectors on the Job in the same memory;
   - Cheney's copying collector (1970), traced with its two pointers;
   - the cost model, work per allocated word ~ L/(S − L), measured against heap size.
8. The generational hypothesis (Lieberman & Hewitt 1983, Ungar 1984), measured: 87% of the Job's objects never
   survive a collection; nurseries of six sizes; remembered sets and write barriers, and why the λ-core needs none.
9. Incremental and concurrent GC: the tri-color invariant (Dijkstra et al. 1978), strong and weak; a lost object,
   move by move; Dijkstra's and Yuasa's barriers tested on 2,000 random cycles; pause times of the JVM's four
   collectors and Go's on this machine.
10. JITs: V8's tiers measured; inline caches against the number of shapes (Deutsch & Schiffman 1984; Self's PICs);
    hidden classes; speculation and deoptimization traced (Hölzle 1992); tracing JITs.
11. Dynamic dispatch: vtables measured, interfaces, multiple dispatch.
12. Implementing exceptions: zero-cost tables against setjmp, measured.
13. WebAssembly: a module assembled by hand and run by node; validation is type checking, and node's error.
14. Other paradigms: Prolog as resolution and unification (append run backwards), actors (Erlang), dataflow.
15. The Job in the λ-core, garbage-collected, on the Pebble VM: ledger row 6 (about 2.4 hours, 149× row 5; the
    collector under 4%). *Frontier*: memory against time (Hertz & Berger 2005); minimum mutator utilization and
    Metronome; the Futamura projections, PyPy and Truffle; warmup (Barrett et al. 2017); verified runtimes; open
    problems. Outro.

*Computed:* the λ-core compiled to bytecode and run by a reference VM under copying, mark–sweep, mark–compact and
generational collectors (work, pauses, holes, lifetimes, nursery sizes); the same VM in the Pebble language on the
emulator and on Part 8's core; reference-count traffic; tri-color marking under a hostile mutator; a CEK machine and
a tiny Prolog; CPython, V8, HotSpot, Go, gcc and node timed and traced on this machine.
*Visuals:* the heap filling and emptying; eval and apply; a closure capturing its environment; the stack as a chain
of closures; the mark wavefront and the sweep; Cheney's scan and free pointers; the tri-color loss; tiers and inline
caches as bars.
*In practice:* the JVM, V8, CPython, .NET and the Go runtime; GC tuning (pause targets, heap sizing); allocation
profiling; embedded interpreters; WebAssembly runtimes.
*Reading:* Abelson & Sussman, *SICP* ch. 4–5; Friedman & Wand, *Essentials of Programming Languages*; Appel,
*Compiling with Continuations*; Jones, Hosking & Moss, *The Garbage Collection Handbook*; Smith & Nair, *Virtual
Machines*; Nystrom; Ierusalimschy et al. 2005; Hölzle et al. 1991–92; Haas et al. 2017; Hertz & Berger 2005.

---

## Act IV · Algorithms

### Part 16 · Counting Steps (~50)
*Story:* The Job v0 is quadratic, and no hardware from Act II rescues it: its cost per byte rises from about 290
cycles on 10 kB to 4,279 on the corpus. Sorting is where computer science learned to count steps: recursion trees, a
lower bound that comes from information, and a randomized algorithm whose average case, 2n ln n, is a small piece of
calculus.
1. The ledger so far, and the question it raises: can thinking beat silicon?
2. Models of computation: the RAM and the word-RAM (w ≥ log n); the pitfall of unit cost, repeated squaring timed in
   CPython (each step about three times the last); Turing machines, the comparison model, cell probes (Yao 1981),
   external memory (Aggarwal & Vitter 1988).
3. Asymptotic notation, precisely (Bachmann 1894, Knuth 1976); the growth-rate ladder on log–log axes; the largest n
   per second, day and year at a nanosecond a step; Stirling's formula checked.
4. Insertion sort: the loop invariant animated; inversions, n(n − 1)/4 derived and measured; binary insertion (fewer
   comparisons, the same moves).
5. Merge sort: merging animated, stability; the recursion tree for T(n) = 2T(n/2) + n, drawn; the substitution
   method; comparisons against n lg n and ⌈lg n!⌉.
6. The **master theorem** in its three cases, as level-by-level bars (Karatsuba, merge sort, a heavy combine); the
   geometric-series proof; five recurrences; Akra–Bazzi computed.
7. The **comparison lower bound**: insertion sort's decision tree on three keys; log₂ n! = n log₂ n − n log₂ e +
   O(log n); each comparison gives at most one bit (callback to *AI, Built* 1); min-and-max by adversary, ⌈3n/2⌉ − 2
   (Pohl 1972); Ford–Johnson merge insertion meets the bound for n ≤ 11 (verified exhaustively for n ≤ 8), and 30 > 29
   at n = 12 (Wells 1965).
8. Heapsort (Williams 1964); Floyd's heapify in O(n) (Σ h/2ʰ derived; under 2 comparisons per element measured);
   1.8 n lg n measured; introsort.
9. Quicksort (Hoare 1961): partition and Hoare's two pointers animated; expected comparisons 2(n + 1)Hₙ − 4n ≈
   1.39 n log₂ n, derived from the 2/(j − i + 1) argument and measured; first element, median of three and random
   pivots on sorted input (1,999,000 against about 21,000); dual pivot (Yaroslavskiy 2009).
10. Concentration: the recurrence solved by telescoping; 10,000 runs at n = 1,000 (σ = 0.639 n against theory's
    √(7 − 2π²/3) n = 0.648 n); the tails; McDiarmid & Hayward 1996.
11. Beating n log n: counting and radix sort, radix sort animated; timed in C (ten million keys: radix sort 3.8× faster
    than `std::sort`, 6.7× than `qsort`); Hollerith; integer sorting on the word-RAM (Han & Thorup 2002, cited).
12. Selection: quickselect (3.36 n measured, (2 + 2 ln 2) n theory); **median of medians** (Blum, Floyd, Pratt, Rivest
    & Tarjan 1973), T(n) ≤ T(n/5) + T(7n/10) + O(n) solved, 7.8 n measured; why groups of five (three fails, seven
    works).
13. Generating functions: Fibonacci and Binet, checked to n = 61; Catalan numbers from C = 1 + zC²; the singularity at
    1/4 and 4ⁿ/(√π n^{3/2}), with the ratio computed (Flajolet & Sedgewick).
14. Amortized analysis: the doubling array; a binary counter; aggregate, accounting and potential (Tarjan 1985);
    factor 2 against 1.5 on a million appends, and memory reuse below the golden ratio.
15. Practice: Timsort's comparisons on presorted data; the 2015 run-stack bug found by KeY (de Gouw et al.); pdqsort;
    external merge sort and replacement selection (runs of 2,001 for M = 1,000).
16. The Job v1 in the Pebble language, sort then count: 15.0 billion key comparisons against 103 million on the
    corpus; a 24-event instruction model (within 0.5% on held-out passages) applied through a C event counter; where
    the instructions go (half in comparison calls, a fifth in copying back); ledger row 7 (5.1 s, 11× row 5, 2.3×
    row 4). *Frontier*: smoothed analysis measured on quicksort (Spielman & Teng 2001); integer sorting results;
    fine-grained complexity (SETH, 3SUM, APSP; Backurs & Indyk 2015); open problems. Outro.

*Computed:* comparison counts for every sort on random, sorted and adversarial input, fitted to their formulas; the
quicksort histogram and tails; the decision-tree bound against Ford–Johnson for n ≤ 12; repeated squaring, radix
sort, `std::sort` and `qsort` timed on this machine; the Job v1 on the emulator, its instruction model, and the full
corpus counted by a C program.
*Visuals:* bars with the invariant region lit; merging and partitioning with pointers; recursion trees summing level
by level; a decision tree whose leaves are permutations; the growth ladder; radix passes; the histogram.
*In practice:* choosing standard-library sorts, complexity arguments in code review, the first questions of a coding interview.
*Reading:* Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms* (CLRS) ch. 1–9, 16–17; Knuth, TAOCP 3 ch.
5; Sedgewick & Flajolet, *An Introduction to the Analysis of Algorithms*; Graham, Knuth & Patashnik, *Concrete
Mathematics*; Kleinberg & Tardos ch. 2, 5; Erickson, *Algorithms*; Flajolet & Sedgewick, *Analytic Combinatorics*;
Hoare 1962; Blum et al. 1973; de Gouw et al. 2015; Spielman & Teng 2001.

### Part 17 · Data Structures (~50)
*Story:* The Job is a dictionary problem: insert, look up, count. Hashing does it in expected constant time, if the
hash function can't be gamed. Balanced trees guarantee their time, and splay trees earn it on average. The ledger
records the drop: 0.81 s, and the verdict of Act IV so far, hardware's 24× against algorithms' 72×.
1. Abstract data types against implementations (Liskov & Zilles 1974); Luhn's hashing (1953); the birthday bound,
   1 − e^{−n²/2m} (derived), and on our vocabulary (101 full-hash collisions predicted 100; 12,495 slot pairs
   predicted 12,786).
2. Chaining against Poisson; **universal hashing** (Carter & Wegman 1979), ((ax + b) mod p) mod m proved universal
   and checked; a flooding attack on a fixed hash; Klink & Wälde (2011) and SipHash.
3. Open addressing: linear probing's ½(1 + 1/(1 − α)²) (Knuth 1963), measured over α, with primary clustering shown;
   double hashing against uniform probing; Robin Hood hashing's variance; Swiss tables.
4. Cuckoo hashing (Pagh & Rodler 2001): two probes, kicks animated, the failure threshold at load ½ (the cuckoo
   graph, Erdős–Rényi); FKS perfect hashing (1984) in about three slots per key.
5. BSTs: random BSTs have expected depth 2(1 + 1/n)Hₙ − 4, measured; height (Devroye); sorted input; the bijection
   with quicksort, counted (24,944 both ways).
6. Rotations; AVL trees, with height < 1.4405 lg(n + 2) via Fibonacci trees; red–black trees **as 2–3–4 trees**
   (Guibas & Sedgewick 1978); left-leaning red–black trees (Sedgewick 2008); heights and rotations measured.
7. Treaps (Seidel & Aragon 1989) on sorted input, and skip lists (Pugh 1990), measured.
8. Splay trees (Sleator & Tarjan 1985): the three steps; the access lemma by potential; static optimality; splay
   against AVL on sequential, uniform, Zipf and hot-set sequences; the dynamic optimality conjecture.
9. B-trees (Bayer & McCreight 1970): fan-out and height log_t n, splitting at the root, five fan-outs measured; a
   billion keys in four levels (Part 35).
10. Priority queues: binary, binomial, **Fibonacci heaps** (Fredman & Tarjan 1987) with cascading cuts, pairing
    heaps; Dijkstra with each, counted; why the Fibonacci heap loses in practice (Larkin, Sen & Tarjan 2014).
11. **Union–find** (Galler & Fischer 1964): union by rank and path compression, 2,312 parent steps per find against
    1.0; O(m α(n)) (Tarjan 1975), optimal (Fredman & Saks 1989); Ackermann's function and log*.
12. Tries (Fredkin 1960) and radix trees on the vocabulary; rank and select in O(1) with a 20% directory (Jacobson
    1989); LOUDS (Part 21 builds on them).
13. Persistent structures (path copying, Driscoll et al. 1989; Okasaki); lookups timed on this machine from 10³ to
    10⁷ keys (red–black tree 2.3 µs, sorted array 0.33 µs, chaining 74 ns, open addressing 31 ns: callback to Part
    9).
14. Hash tables in practice: Python, Java, C++, Rust and Go; the Job natively (Python 0.91 s, C++ 0.19 s, C 0.11 s).
15. The Job v2, a hash table in the Pebble language: 1.06 slots per word on the corpus; an exact 27-event
    instruction model (0.01% on held-out passages); the corpus through Part 9's caches (+6%); ledger row 8 (0.81 s:
    6.3× row 7, 72× row 5, 15× row 4); rows 0 → 4 against rows 5 → 8. *Frontier*: Yao's conjecture refuted
    (Farach-Colton, Krapivin & Kuszmaul 2025) against measured uniform probing; dynamic optimality and tango trees;
    cell-probe lower bounds; learned indexes; open problems. Outro.

*Computed:* probe counts against Knuth's formula over α; chain lengths against Poisson; cuckoo failure rates; FKS
space; BST depths and the quicksort bijection; AVL and red–black heights and rotations; treaps and skip lists;
splay costs on four sequences; B-tree heights; Dijkstra's heap comparisons; union–find path lengths; the
vocabulary's trie; persistence; lookups and the Job timed natively; the Job v2 on the emulator, its model, the
corpus counted in C and run through Part 9's caches.
*Visuals:* buckets filling while clusters form; chains; cuckoo kicks; rotations; 2–3–4 ↔ red–black; a treap and a
skip list; B-tree splits; a union–find path compressing; a trie; path copying.
*In practice:* hash maps and their DoS hardening, B-trees in every database, priority queues in schedulers and timers, union–find in compilers and image processing.
*Reading:* CLRS ch. 10–13, 18–19, 21; Knuth, TAOCP 3 ch. 6; Sedgewick & Wayne, *Algorithms* ch. 3; Tarjan, *Data
Structures and Network Algorithms*; Mehlhorn & Sanders, *Algorithms and Data Structures*; Okasaki, *Purely Functional
Data Structures*; Navarro, *Compact Data Structures*; Carter & Wegman 1979; Pagh & Rodler 2004; Sleator & Tarjan
1985; Fredman & Tarjan 1987; Farach-Colton, Krapivin & Kuszmaul 2025.

### Part 18 · Graphs (~50)
*Story:* Euler invented the graph to walk the bridges of Königsberg. Graphs are now the shape of road maps, the
internet, compilers and markets. Dijkstra designed his algorithm in twenty minutes at a café, and in 2024–25 it was
proved universally optimal and also beaten. Flows and cuts turn out to be two faces of one theorem, and the gap
between an Euler tour and a Hamiltonian cycle is the first glimpse of P against NP.
1. Königsberg (1736): degrees 5, 3, 3, 3; the even-degree theorem (proved) and Hierholzer's circuit in O(E);
   adjacency lists against a matrix, measured from sparse to dense (the matrix wins at 1.5 million edges on 3,000
   vertices).
2. BFS: layers in a 24 × 14 maze (67 layers, a 59-cell path; Moore 1959); the queue lemma (proved, animated);
   bipartiteness and the odd cycle that refutes it.
3. DFS: discovery and finish times; the parenthesis and white-path theorems; tree, back, forward and cross edges;
   a back edge is a cycle (Trémaux 1882; Hopcroft & Tarjan).
4. Topological sort: a compiler's build graph by DFS finish order and by Kahn's queue (1962); cycles; make,
   spreadsheets, Part 13's reverse postorder, critical paths.
5. SCCs: Tarjan's low links, traced step by step with the stack; Kosaraju; the condensation; a 20,000-page synthetic
   web (a core of 7,583) and Broder's bow tie; 2-SAT by the implication graph (Aspvall, Plass & Tarjan 1979).
6. Dijkstra (1956/59): the invariant proved with the settled-set picture; Part 17's heap; the wavefront over a city of
   2,400 intersections with arterial roads.
7. Negative edges: Dijkstra's failure; Bellman–Ford round by round; negative cycles; arbitrage as a negative cycle
   in −log rates (illustrative rates: JPY → GBP → EUR, +0.5%); distance-vector routing (Part 36).
8. All pairs: Floyd–Warshall as DP; Johnson's reweighting (proved, with a worked example; 150 vertices and 231
   negative edges, matching Floyd–Warshall); the min-plus product and the APSP conjecture (Part 27).
9. Route planning: A* (callback to *AI, Built* 2), landmarks, contraction hierarchies; vertices settled per query on
   4,800 intersections: Dijkstra 2,525, bidirectional 1,237, A* 657, landmarks 208, CH 113.
10. MSTs: the cut property, proved on a worked example, and the cycle property; Kruskal with Part 17's union–find,
    Prim/Jarník, Borůvka (1926, for the Moravian grid; 4 rounds); Karger, Klein & Tarjan.
11. **Max-flow min-cut**: augmenting paths and the residual graph; the theorem (proved; 19 = 10 + 9); Edmonds–Karp
    against an unlucky path choice (2 augmentations against 2,000); push–relabel.
12. Matching: bipartite matching as flow; Hall and Kőnig; **Gale–Shapley** with stability proved; proposals against
    n Hₙ; the Hungarian algorithm (166 against greedy's 308).
13. Easy and hard: Hamilton's icosian game (all 30 Hamiltonian cycles of the dodecahedron); Euler against Hamilton
    (Part 26); Held–Karp timed against brute force.
14. PageRank (Brin & Page 1998): the random surfer's stationary distribution (callback to *AI, Built* 5); power
    iteration on 20,000 pages (52 rounds to 10⁻¹²); rank against in-degree.
15. Planarity: V − E + F = 2 (54 − 133 + 81); E ≤ 3V − 6 and K₅; Guthrie to Appel–Haken (1976) and Gonthier's Coq
    proof (2005); the five-colour theorem by Kempe chains (proved, animated); our map coloured greedily with 5,
    with 4 by backtracking, and 3 refuted by an odd wheel.
16. *Frontier*: universally optimal Dijkstra (Haeupler, Hladík, Rozhoň, Tarjan & Tětek, FOCS 2024); directed SSSP
    in O(m log^{2/3} n), beyond the sorting barrier (Duan, Mao, Mao, Shu & Yin, STOC 2025); negative weights in
    near-linear time (Bernstein, Nanongkai & Wulff-Nilsen 2022); max flow in almost-linear time (Chen, Kyng, Liu,
    Peng, Probst Gutenberg & Sachdeva 2022); open problems. Outro.

*Computed:* every number above, in `videos/cs/cs18/compute.py` with `explainer/cs/algo/graphs.py` (tested in
`tests/test_cs18_graphs.py`): BFS, DFS and SCC traces; the representation timings; Dijkstra, bidirectional, A*, ALT
and CH on one city; Bellman–Ford, Floyd–Warshall and Johnson; Kruskal, Prim and Borůvka; Edmonds–Karp; Gale–Shapley
and the Hungarian algorithm; Held–Karp; PageRank; planar colouring.
*Visuals:* the Königsberg multigraph; the BFS flood and its queue; DFS stamps and parentheses; Tarjan's stack; the
Dijkstra wavefront and settled-set proof; search footprints for A*, landmarks and CH; the cut-property swap; flows
as flashes along paths, and the min cut; Kempe chains.
*In practice:* route planning in maps, network routing, dependency graphs, social graphs, scheduling, graph databases.
*Reading:* CLRS ch. 20–26; Kleinberg & Tardos ch. 3, 4, 7; Tarjan; Ahuja, Magnanti & Orlin, *Network Flows*; Even,
*Graph Algorithms*; Schrijver, *Combinatorial Optimization*; Dijkstra 1959; Ford & Fulkerson 1956; Tarjan 1972; Gale &
Shapley 1962; Chen et al. 2022; Haeupler et al. 2024; Duan et al. 2025.

### Part 19 · The Great Paradigms (~50)
*Story:* Most good algorithms come from a handful of ideas: be greedy when an exchange argument allows it, divide
and conquer, or remember subproblems. Divide and conquer, applied to the right points (the roots of unity), gives
the most important algorithm of the twentieth century, the FFT. The part opens with a million digits of π and two
million-digit numbers multiplied four ways, and closes with one problem solved four ways.
1. Greedy: interval scheduling by earliest finish, proved by exchange; four rules on 2,000 random instances with
   counterexamples; coins {1, 3, 4} and Kozen–Zaks; Huffman's code on the corpus's 27 symbols (4.12 bits against an
   entropy of 4.08).
2. **Matroids**: Whitney's axioms; the Rado–Edmonds greedy theorem (proved); forests (Kruskal) optimal 400 of 400,
   matchings 248 of 400 (never below half).
3. Karatsuba (1960), which refuted Kolmogorov's n² conjecture: 1234 × 5678 by three products; the recursion tree;
   measured in Python (pure Karatsuba loses below 4,096 digits; with a 32-digit cutoff it wins from 64); CPython's
   cutoff; Toom–Cook.
4. Strassen (1969): the seven products; exact operation counts; the history of ω from 2.807 to 2.3713 (Alman,
   Duan, Vassilevska Williams, Xu, Xu & Zhou 2024); galactic algorithms; against numpy's BLAS (3–5× slower, 10×
   rounding error); AlphaTensor (callback to *AI, Built* 26).
5. **The FFT, I**: coefficients against values; ± pairs; the roots of unity squaring onto half as many points (the
   centerpiece animation); the algorithm in ten lines.
6. **The FFT, II**: Gauss (c. 1805) and Cooley–Tukey (1965); the butterfly network and bit reversal; the inverse by
   orthogonality (proved); DFT against FFT in Python (272× at 2,048 points); numpy.
7. Multiplication by FFT: integers as polynomials; floating-point exactness measured to ten million digits; the
   NTT modulo 119 · 2²³ + 1 (Part 30) and Python's `decimal`; Schönhage–Strassen to Harvey & van der Hoeven's
   n log n (2019).
8. Closest pair in the plane: the strip argument with at most seven neighbours (proved); 100,000 points in 1.3 s.
9. **Dynamic programming**: Bellman (1957) and the story of the name; Fibonacci's call tree; memoization against
   tabulation; DP as paths in a DAG of subproblems.
10. Edit distance (Wagner–Fischer), the *intention*/*execution* table and traceback; LCS, `diff` (Parts 21, 41),
    Needleman–Wunsch.
11. Knapsack's O(nW) table; greedy by value per weight fails; the same problem with ever larger numbers
    (pseudo-polynomial time); NP-hardness (Part 26) and Ibarra–Kim's approximation scheme.
12. Matrix chains (15,125 against 58,000 worst); optimal BSTs and Knuth's O(n²) speedup (33× fewer steps at 200
    keys).
13. DP on trees (independent sets, 200,000 vertices in 0.3 s), on graphs (Bellman–Ford, Floyd–Warshall,
    Held–Karp, DAG paths) and on sequences (Viterbi, CYK, speedups, Hirschberg).
14. Backtracking and branch-and-bound: n-queens (2,057 nodes for eight); Sudoku as exact cover with **Dancing
    Links** (Knuth 2000) against plain backtracking on three puzzles.
15. One problem, four paradigms: maximum subarray by brute force O(n³), running sums O(n²), divide and conquer
    O(n log n), and Kadane's DP O(n), timed to a million numbers.
16. *Frontier*: the limits of the laser method (Ambainis, Filmus & Le Gall 2015; Alman & Vassilevska Williams 2018);
    edit distance and SETH (Backurs & Indyk 2015) and its approximation (Andoni & Nosatzki 2020); lower bounds for
    the FFT and multiplication (Morgenstern 1973; Afshani et al. 2019); open problems. Outro.

*Computed:* every number above, in `videos/cs/cs19/compute.py` with `explainer/cs/algo/paradigms.py` (tested in
`tests/test_cs19_paradigms.py`): a million digits of π by Chudnovsky's series; four multipliers on million-digit
numbers; Karatsuba against school; Strassen's counts, time and error; DFT against FFT; FFT exactness; closest pair;
DP tables; Dancing Links on Sudoku; maximum subarray four ways.
*Visuals:* the roots of unity squaring onto half as many points; butterflies; Strassen's seven products coloured;
DP tables with traceback; the exchange argument as swapped bars; the matroid exchange on a graph; queens and
dancing links.
*In practice:* diff tools, bioinformatics, the FFT in audio, images and radios, GMP and BLAS, dynamic programming in
pricing and scheduling, SAT and constraint solvers.
*Reading:* CLRS ch. 4, 14–15, 30; Kleinberg & Tardos ch. 4–6; Dasgupta, Papadimitriou & Vazirani, *Algorithms* ch. 2,
5–6; Knuth, TAOCP 2 §4.3.3 and 4B; Bentley, *Programming Pearls*; Cooley & Tukey 1965; Strassen 1969; Karatsuba &
Ofman 1962; Harvey & van der Hoeven 2021; Bellman 1957; Edmonds 1971; Alman et al. 2024.

### Part 20 · Randomness as a Resource (~55)
*Story:* A coin flip can stand in for cleverness. With one, you can check a matrix product in n², find a minimum
cut by contracting random edges, test primality in milliseconds, and count the top words of thirty novels in a few
kilobytes. Randomness has to come from somewhere, though, and some generators hide fifteen planes. The part opens
with the Job's top twenty counted twice, from 1.9 MB and from 18.6 KB, and ends by asking whether the coins can be
removed at all.
1. Las Vegas against Monte Carlo: randomized quicksort's 400 runs on 2,000 keys (mean 24,761 against the exact
   24,730); one-sided error and 2^{−k}; majority votes and Hoeffding.
2. **Freivalds** (1977), error ≤ ½ per round, proved by deferred decisions; at n = 2,000, 24 million operations
   against 16 billion (23 ms against BLAS's 0.13 s); one wrong entry passes 50.9%, 25.1%, 12.4%, … of 4,000 trials.
3. The **Schwartz–Zippel** lemma (proved); a false identity against 3/|S|; an 8 × 8 Vandermonde identity; the
   Tutte matrix (Lovász 1979) against Edmonds' blossoms on 48 random graphs; a 61-bit fingerprint of the corpus
   (false match ≤ 1.2 × 10^{−10}).
4. **Karger's min cut** (1993), contraction animated (one success, one failure): ≥ 2/(n(n − 1)) proved, 13.1%
   measured against 0.83%; the 10-cycle's 45 = C(10, 2) minimum cuts; Karger–Stein.
5. Primality: Fermat; 561 and Korselt; 43 Carmichael numbers below 10⁶; **Miller–Rabin** (561's sequence 263, 166,
   67, 1; Rabin's ¼, attained at 9); random primes to 2,048 bits timed; AKS (2002).
6. Random walks: Papadimitriou's 2-SAT as a gambler's ruin (≤ n², about 2n flips measured); Schöning's (4/3)ⁿ
   against restarts measured on unique-solution formulas to n = 20; PPSZ.
7. Balls into bins, animated with one and two choices; max loads to 10⁶ (10 against 4); the full histograms; why
   two choices square the tail.
8. Bloom filters (1970): 32 bits drawn with two false positives; (1 − e^{−kn/m})ᵏ and k = (m/n) ln 2 (derived); the
   novels' vocabulary at 10 bits per word (0.815% against 0.819%); counting and cuckoo filters.
9. Streaming: reservoir sampling (proved uniform, 50,000 trials); Misra–Gries (99 counters); **Count-Min** and its
   (ε, δ) guarantee, measured on every word of the novels.
10. **The Job in kilobytes**: Count-Min with conservative update and double hashing, 32 candidates in a heap, in the
    Pebble language; every instruction emulated (1.07 billion); 18,588 bytes against 1.9 MB; ledger row 9, 1.00 s
    against 0.81 s; the same algorithm over 20 hash functions in C (exact 25% of the time at 16 KB, 95% at 64 KB;
    the top 20 always among the candidates).
11. Distinct counting: Flajolet–Martin, **HyperLogLog** (error against 1.04/√m from 16 to 16,384 registers), the
    corpus and its 4.5 million five-word phrases in 3 KB.
12. The AMS F₂ sketch (1996) from 4-wise independent signs; the median of means; linear sketches as random
    projections (callback to *AI, Built* 3's Johnson–Lindenstrauss).
13. LSH: MinHash (Broder 1997, proved) and banding (Indyk & Motwani 1998), the S-curve matched by 600 planted
    copies; near-duplicate paragraphs among 34,525 in the novels, checked by an inverted index; SimHash.
14. The probabilistic method: K₁₇ coloured at random and by Paley; R(k, k) > 2^{k/2}; the 2023 upper bound; the
    Lovász local lemma and Moser–Tardos (2010) on 10-SAT inside the lemma's condition.
15. Derandomization: conditional expectations (MAX-CUT ≥ m/2, 176 of 265 edges); pairwise independence from k
    bits; expanders (Part 56); where random bits come from: **RANDU's fifteen planes** on a rotating cube, Mersenne
    Twister, PCG, cryptographic PRGs (Part 29), physical entropy.
16. *Frontier*: coins removed one problem at a time (AKS; Reingold; deterministic near-linear min cut; matching in
    quasi-NC); hardness against randomness (Nisan–Wigderson, Impagliazzo–Wigderson); PIT and circuit lower bounds
    (Kabanets–Impagliazzo); optimal sketches and their lower bounds; open problems. Outro.

*Computed:* every number above, in `videos/cs/cs20/compute.py` with `explainer/cs/algo/randomized.py` and
`explainer/cs/algo/job3.py` (tested in `tests/test_cs20_randomized.py`): Freivalds' error rates; Schwartz–Zippel and
Tutte; Karger's success rate against the bound; Miller–Rabin's liars; walks; max loads; Bloom filters against theory;
reservoir, Misra–Gries and Count-Min on the novels; the Job v3 emulated (ledger row 9) and swept in C; HLL, KMV and
AMS on the novels; MinHash duplicates; Ramsey and Moser–Tardos; MAX-CUT; RANDU.
*Visuals:* a graph contracting edge by edge; bins filling with one and two choices; **RANDU's cube rotating until the
planes appear**; a Bloom bit array lighting up; HyperLogLog's registers; the LSH S-curve; K₁₇ in two colourings.
*In practice:* Bloom filters in databases and caches, HyperLogLog in Redis and analytics engines, Count-Min in network monitoring and cache admission, MinHash dedup in data pipelines, Miller–Rabin in TLS.
*Reading:* Motwani & Raghavan, *Randomized Algorithms*; Mitzenmacher & Upfal, *Probability and Computing*; Alon &
Spencer, *The Probabilistic Method*; Cormode & Yi, *Small Summaries for Big Data*; Muthukrishnan, *Data Streams*;
Knuth, TAOCP 2 ch. 3; Karger 1993; Flajolet et al. 2007; Alon, Matias & Szegedy 1996; Moser & Tardos 2010.

### Part 21 · Strings (~50)
*Story:* Text is the oldest data. Searching it efficiently led to automata built from patterns, then to indexes of
every suffix, then to a reversible transform that sorts a book into compressible runs and lets you search the
compressed result. Each `git diff` runs a shortest-path algorithm on a grid. The part opens with Queequeg found four
ways in the 25 MB of novels, from 24,974,844 character comparisons down to 16 rank queries.
1. Matching, naive: about one comparison per character on English (1 + f(p₁) + f(p₁p₂) + ⋯ predicts the measured
   cost to four decimals); the worst case (n − m + 1)m, 99 million comparisons at n = 10⁵, m = 10³.
2. **Rabin–Karp** (1987): the rolling window animated on digits (one hit, one spurious); collisions ≤ (m − 1)/p by
   Schwartz–Zippel; Queequeg in *Moby-Dick* with moduli from 101 (12,042 false alarms against n/p = 12,056) to 10⁹.
3. **KMP** (1977): borders and the shift animated; the failure table as Part 12's automaton, run over a text; ≤ 2n
   comparisons (proved, amortized); the worst case of chapter 1 in 199,901 comparisons.
4. **Boyer–Moore** (1977): compare from the right; bad character and good suffix (ANPANMAN, a shift of 6);
   comparisons per character against pattern length on *Moby-Dick* (KMP ≈ 1, Boyer–Moore ≈ 1/m, Horspool on top);
   Queequeg in 3,500,231 comparisons; why grep is fast.
5. **Aho–Corasick** (1975): the trie of he, she, his, hers with failure links built level by level; 45 character
   names in one pass over the corpus (231 states, 25.5 million steps, against 1.1 billion characters read separately).
6. **Suffix trees**: banana$ and a walk for ana; Ukkonen's suffix links and open leaves drawn on the tree; the deepest
   branching node; *Moby-Dick*'s 741 billion distinct substrings; 10–20 bytes per character.
7. **Suffix arrays** (Manber & Myers 1990): sorted suffixes and the block for t; prefix doubling as a rank table on
   banana$; SA-IS and Kasai's LCP; all 24,971,556 suffixes of the novels in 105 s (100 MB); Queequeg's 253 in 167
   comparisons; the longest repeat (383 characters of chapter headings).
8. **The Burrows–Wheeler transform** (1994): rotations sorted; LF arrows walking banana$ back out (proved; all of
   *Moby-Dick* inverted exactly); what precedes he, hi and ho in *Moby-Dick* (72% t before he); nH_k for every k
   (Manzini 2001); 578,682 runs, move-to-front, bzip2 against zlib.
9. The **FM-index** (Ferragina & Manzini 2000): backward search for ana; wavelet trees and Jacobson's rank; the
   novels indexed (counts in a fraction of a millisecond; our teaching index larger than the text, bzip2 of L 7.1 MB).
10. Compression, part one: LZ77 arcs over *A Tale of Two Cities*; DEFLATE's alphabets, buckets and lazy matching;
    an LZ78 parse drawn; Ziv–Lempel universality; our LZ77 + Huffman within 6% of zlib -9 on three novels, against
    LZW, bzip2 and xz.
11. Compression, part two: Huffman's whole bits against skewed sources (rANS 0.287 against 0.286 bits at p = 0.95);
    **ANS** (Duda) worked on four symbols; H₀, H₁, H₂ = 4.44, 3.48, 2.81 bits: compression is prediction; zstd.
12. Alignment: Needleman–Wunsch on intention/execution with its traceback; Smith–Waterman lining up two versions of
    the Monte Cristo letter word for word (90,000 cells, score 322); Gotoh's three tables; BLAST and seeds; **no
    O(n^{2−ε}) edit distance under SETH** (Backurs & Indyk 2015; Part 27).
13. **Myers' diff** (1986): the edit graph of ABCABBA against CBABAC; the furthest-reaching D-paths drawn for D = 0 … 5;
    patience diff, three-way merge; every revision of this syllabus diffed (all minimal; git's `--minimal` 2–4 lines
    longer on 8 of 26).
14. rsync and chunking: 24 bytes inserted into *Moby-Dick* (297 of 595 fixed blocks survive); rsync's rolling
    checksum (593 blocks found, 3,257 literal bytes); content-defined chunks drawn (120 chunks, one new, 14 KB).
15. Periodicity: Fine–Wilf with periods 5 and 8 drawn (tight at 11); Manacher over 19.4 million letters (*able was I
    ere I saw Elba*, Lenehan in *Ulysses*); Lyndon words and Duval.
16. *Frontier*: BWT runs drawn for the novels against 27 versions of this syllabus (n/r = 2.3 against 48; xz 63×);
    the r-index (Gagie, Navarro & Prezza 2018); r = O(z log² n) (Kempa & Kociumaka 2020); the quadratic wall and its
    escapes; open problems. Outro.

*Computed:* every number above, in `videos/cs/cs21/compute.py` with `explainer/cs/algo/strings.py` (tested in
`tests/test_cs21_strings.py`): every matcher's comparisons on the novels; Aho–Corasick over the corpus; the suffix
array, LCP and longest repeats of all 25 MB; the BWT of *Moby-Dick* inverted, its runs, MTF entropy and contexts; the
FM-index of the novels; our LZ77 + Huffman, LZW and rANS against zlib, bzip2 and xz; Smith–Waterman on the Monte
Cristo letters; Myers' diff on this file's history, checked against LCS and git; rsync and content-defined chunking;
Manacher over the corpus; BWT runs of the syllabus versions.
*Visuals:* the KMP shift and automaton; Boyer–Moore's skips; the Aho–Corasick trie and its links; suffix trees with
suffix links; the BWT's rotation matrix and LF arrows; context bars; the wavelet tree; LZ back-references as arcs;
the ANS state table; alignment tables with tracebacks; Myers' D-paths in the edit graph; fixed blocks against
content-defined chunks; BWT run strips.
*In practice:* grep and ripgrep, gzip, zstd and bzip2, genome alignment, git diff, rsync and deduplicating backups.
*Reading:* Gusfield, *Algorithms on Strings, Trees, and Sequences*; Crochemore, Hancart & Lecroq, *Algorithms on
Strings*; Mäkinen, Belazzougui, Cunial & Tomescu, *Genome-Scale Algorithm Design*; Navarro, *Compact Data
Structures*; Salomon & Motta, *Handbook of Data Compression*; Knuth, Morris & Pratt 1977; Burrows & Wheeler 1994;
Ferragina & Manzini 2000; Ziv & Lempel 1977–78; Myers 1986; Gagie, Navarro & Prezza 2018.

### Part 22 · Geometry (~50)
*Story:* Geometry looks easy until a computer gets it wrong: a floating-point orientation test can say a point lies
on both sides of a line. Get the predicates right and beautiful structure follows. Voronoi diagrams grow as a
parabolic beach line, and every Delaunay triangulation is the shadow of a convex hull on a paraboloid. The part opens
with one orientation test asked three ways in double precision and getting three answers.
1. The primitive: orientation as a signed area; why rounding fails and Shewchuk's error bound; Kettner's grid computed
   (11,972 wrong signs of 65,536); adaptive predicates measured (exact stage needed 0% on random input, 70% on nearly
   collinear input; float wrong 3,713 times in 20,000 there).
2. Convex hulls: Graham's scan animated; Jarvis, Graham, monotone chain, quickhull and Chan counting their work on
   10,000 points in a square, a disk and on a circle; the Ω(n log n) lower bound by lifting to a parabola (proved);
   Chan's O(n log h) with binary-search tangents and squaring guesses; Kirkpatrick–Seidel.
3. The sweep line: Bentley–Ottmann animated with its status and events; events exactly 2n + k, 19,812 pair tests
   against 4.5 million pairs at n = 3,000; Chazelle–Edelsbrunner.
4. **The art gallery theorem**: Chvátal's comb; Fisk's three-colouring proof animated; ear clipping; random 60-gons
   (17.3 guards against the bound of 20); monotone pieces, Chazelle's linear time, NP- and ∃ℝ-hardness.
5. Voronoi diagrams; **Fortune's sweep** animated with its beach line of parabolas; circle events exactly 2n − 2 − h,
   checked against the lifting map up to n = 2,000.
6. Delaunay triangulations: the empty circle; duality with Voronoi; Lawson's flips animated (17 flips, smallest angle
   0.48° to 4.81°, Sibson); the Euclidean MST inside the Delaunay edges (Shamos–Hoey), checked against Prim on 32
   million pairs.
7. **The lifting map**: a 3D tour of the paraboloid, the lower hull, and a circle lifting to a plane; the in-circle
   test as a 4 × 4 determinant; why Lawson's flips stop; the Voronoi diagram as an upper envelope; checked against
   scipy.
8. Randomized incremental construction and **backwards analysis**: one insertion's conflicts; expected degree < 6 by
   Euler; 8.6–8.9 triangles per point in random order, 874,107 for 1,600 points in a bad order.
9. Seidel's LP animated (the optimum moves three times in nine); Pr ≤ 2/i measured against 2H_n up to 10⁵; Megiddo;
   Welzl's smallest enclosing circle animated and measured.
10. Range searching: a kd-tree built level by level; queries below √n + k up to 300,000 points; range trees,
    fractional cascading, interval and segment trees, R-trees.
11. Point location: Dobkin–Lipton slabs; the trapezoidal map (3n + 1, hit on every random map); Mulmuley and
    Seidel's randomized search structure; Kirkpatrick.
12. High dimensions: distance concentration measured to d = 1,000; a kd-tree visiting 100% of its nodes at d = 24;
    LSH (callback to Part 20); a navigable small world and **HNSW** built (99.7% recall for 182 distance computations
    against 20,000).
13. Duality and arrangements; the zone theorem; a ham-sandwich cut (Stone–Tukey; Lo–Matoušek–Steiger).
14. Motion planning: Minkowski sums and configuration space; the visibility graph and Dijkstra; an RRT grown in the
    same space (1.29× the optimum on average); Reif, Canny, sampling planners; BVHs (Part 51).
15. *Frontier*: exact geometric computation and its price (124×); symbolic perturbation and snap rounding; 3SUM as
    collinearity of (a, a³), drawn and checked; Gajentaan–Overmars; LSH's optimal exponents, data-dependent hashing,
    Indyk–Xu on graph indexes; open problems (3SUM, Hopcroft's problem, guarantees for navigable graphs). Outro.

*Computed:* every number above, in `videos/cs/cs22/compute.py` with `explainer/cs/algo/geometry.py` (tested in
`tests/test_cs22_geometry.py`): Kettner's grid and the adaptive filter's rates and costs; five hulls counting their
work; Bentley–Ottmann against brute force; ear clipping and Fisk's colouring; Fortune's sweep; Delaunay three ways
(incremental, Lawson, Fortune) against scipy's lifted hull; the EMST over Delaunay against Prim; Seidel's LP against
scipy; Welzl; kd-tree visits; trapezoid counts; distance concentration, kd-trees against dimension, NSW and HNSW
recall; a ham-sandwich cut; configuration spaces, the visibility graph and an RRT; 3SUM as collinearity.
*Visuals:* the speckled grid of wrong signs; Graham's stack; the sweep's status; Fisk's three colours; Fortune's
beach line drawing the diagram; Lawson's flips; the paraboloid in 3D; conflicts and the star-shaped hole; Seidel's
optimum moving; kd-tree cells; trapezoids; HNSW's layers; points and dual lines; a robot sliding among grown
obstacles, and a random tree exploring; the cubic of 3SUM.
*In practice:* GIS and maps (PostGIS, S2), CAD and meshing (CGAL, Triangle), robot motion planning (OMPL), collision
detection and rasterization in graphics, vector search (FAISS, pgvector).
*Reading:* de Berg, Cheong, van Kreveld & Overmars, *Computational Geometry: Algorithms and Applications*; Preparata &
Shamos; O'Rourke, *Computational Geometry in C*; Devadoss & O'Rourke, *Discrete and Computational Geometry*;
Edelsbrunner, *Geometry and Topology for Mesh Generation*; LaValle, *Planning Algorithms*; Shewchuk 1997; Kettner et
al. 2008; Fortune 1987; Seidel 1991, 1993; Chan 1996; Malkov & Yashunin 2016.

### Part 23 · Optimization (~60)
*Story:* Many problems are "choose the best point of a polytope." The simplex method walks the polytope's edges.
Duality certifies the answer from the other side. When integrality makes a problem hard, LP relaxations and random
hyperplanes still get provably close. Online, without seeing the future, you can still be competitive.
1. Hook: Stigler's diet ($39.93 by insight, 1945); Laderman's simplex by hand ($39.69 and a proof, about 120
   person-days); the three kinds of answer (proved, provably close, competitive).
2. Linear programs: Chvátal's three-product LP; Kantorovich (1939), Dantzig (1947); modelling a transportation problem
   (Hitchcock 1941; $355 infeasible, $365 optimal) and the standard tricks; the feasible region as a 3D polytope with 6
   vertices and the objective plane pushed to (2, 0, 1).
3. **Simplex**: the walk 0 → 12.5 → 13 in 2 pivots, drawn in 3D and as tableaux (ratio test, elimination); degeneracy,
   cycling and Bland's rule; steepest edge and LU updates.
4. **Duality**: the family of bounds (15, 13⅓, an infeasible one, 13); weak and strong duality, Farkas' lemma and a
   separating hyperplane; shadow prices measured (⅓ against y₁ = 1); complementary slackness.
5. The Klee–Minty cube walked through all 8 vertices; 2ⁿ − 1 Dantzig pivots to n = 12, Bland 465, greatest
   improvement 1 (Jeroslow, Avis–Chvátal, Zadeh); smoothed analysis (Spielman & Teng 2001): random LPs and perturbed
   cubes (1,023 → 397 → 76 pivots).
6. Polynomial time: Khachiyan's ellipsoid (9 cuts; steps against width); separation ≡ optimization (Grötschel, Lovász
   & Schrijver); Karmarkar's interior point, the log barrier and the central path (127 Newton steps).
7. **Total unimodularity**: bipartite incidence matrices checked, Cramer's rule, 0 of 100 fractional; the triangle
   (det 2, all halves), 25 of 100; Edmonds' odd sets; max-flow/min-cut as duality (Part 18); Seymour.
8. Integer programming: knapsack branch and bound (24 nodes of 256; a few hundred at n = 160, LP gap 0.06%); Gomory
   cuts; Bixby's speedups; the FPTAS by rounding (Ibarra & Kim).
9. Approximation: vertex cover 2 by matching and by half-integral LP rounding, measured; Khot–Regev; greedy set cover
   H_n (proved), the harmonic trap, Feige.
10. TSP: no factor in general; double tree, Christofides–Serdyukov; forty instances against Held–Karp (2-opt best at
    1.013); Karlin–Klein–Oveis Gharan, Arora/Mitchell; 300 cities and BHH; LKH and Concorde.
11. **Goemans–Williamson**: vectors on a sphere and a random hyperplane; θ/π against (1 − cos θ)/2, α = 0.8786 at
    134°; thirty graphs against exact MAX-CUT; KKMO and Håstad.
12. Online: ski rental (2 − 1/B; e/(e − 1) randomized); paging on the Job's trace (LRU 1.2–6.9× Belady; random and
    marking win at large k); the cyclic adversary and Sleator–Tarjan.
13. **Multiplicative weights**: regret against √((T ln n)/2), measured; the potential proof; a zero-sum game converging
    to its LP value; boosting (*AI, Built* 6) and approximate LP (Arora, Hazan & Kale).
14. Convex optimization in a page: gradient descent (40 steps) against Newton (4) on a stretched log-sum-exp; KKT; the
    LP ⊂ QP ⊂ SOCP ⊂ SDP ladder; Rockafellar's watershed (callbacks to *AI, Built* 4 and 11).
15. *Frontier*: LP in matrix-multiplication time (Cohen, Lee & Song; van den Brand) and almost-linear max flow (Chen et
    al. 2022); the Hirsch conjecture, a drawn random polytope and random diameters against n − 3, Santos, Kalai–Kleitman;
    hardness of approximation (PCP, Håstad, the UGC, the 2-to-2 theorem, Raghavendra); open problems (strongly
    polynomial LP, polynomial Hirsch, the UGC). Outro.

*Computed:* every number above, in `videos/cs/cs23/compute.py` with `explainer/cs/algo/optim.py` (tested in
`tests/test_cs23_optim.py`): the simplex under three rules, exact and floating, against HiGHS; the transportation
optimum; duals, shadow prices and slacks; Klee–Minty, perturbed and random pivot counts; ellipsoid runs; the central
path; total unimodularity by brute force; branch and bound, DP and the FPTAS; vertex and set cover against brute
force; Held–Karp and the TSP heuristics; Goemans–Williamson by a Burer–Monteiro SDP against exact MAX-CUT; ski rental
and paging on the Job's trace; Hedge regret and a zero-sum game; gradient descent and Newton; random 3D polytope
diameters.
*Visuals:* the polytope with the objective plane and the simplex walk; tableaux pivoting; the dual's family of bounds
and a separating hyperplane; the squashed Klee–Minty cube; ellipsoids shrinking; the central path; the
branch-and-bound tree; covers on a graph; tours being built; a hyperplane slicing a sphere of unit vectors; the α
curve; expert weights converging; zigzagging gradient descent against Newton; a random polytope's longest path.
*In practice:* operations research (logistics, crew scheduling, ad allocation), LP and MIP solvers (Gurobi, HiGHS,
OR-Tools), cache replacement as an online problem.
*Reading:* Bertsimas & Tsitsiklis, *Introduction to Linear Optimization*; Chvátal, *Linear Programming*; Matoušek &
Gärtner, *Understanding and Using Linear Programming*; Schrijver, *Theory of Linear and Integer Programming*;
Williamson & Shmoys, *The Design of Approximation Algorithms*; Vazirani, *Approximation Algorithms*; Borodin &
El-Yaniv, *Online Computation and Competitive Analysis*; Applegate, Bixby, Chvátal & Cook, *The Traveling Salesman
Problem*; Boyd & Vandenberghe; Goemans & Williamson 1995; Arora, Hazan & Kale 2012; Karlin, Klein & Oveis Gharan 2021.

### Part 24 · Algorithms in Practice (~55)
*Story:* Big-O hides constants, and in production the constants and the machine decide. This part covers the
everyday tools of real code and of interviews: prefix sums, Fenwick and segment trees, two pointers, monotonic
stacks, bit tricks. It then turns to algorithm engineering, where a textbook hash table, sort or binary search
becomes ten times faster by respecting the caches, branch predictors and SIMD units of Act II. Theory meets the
machine, and the ledger gets its native row.
1. Hook: an array and a shuffled linked list, both O(n), 5× apart at a thousand elements and 143× at sixteen million
   (measured).
2. Prefix sums and difference arrays; the integral image (Crow 1984; Viola–Jones, *AI, Built* 6); the parallel scan
   (Hillis–Steele, Blelloch).
3. **Fenwick trees** (1994): the lowbit trick i & −i; responsibility ranges drawn; both loops proved logarithmic; four
   structures timed (52 ns against 142 for a segment tree and 130–155 µs for the naive ones).
4. **Segment trees**: covering nodes; a four-number node for the maximum subarray; lazy propagation (57 nodes against
   17,552 elements); persistence.
5. Range minimum and LCA: the sparse table (idempotence); LCA by Euler tour and by binary lifting; the Cartesian tree
   (Bender & Farach-Colton 2000; Fischer & Heun).
6. Two pointers: the sliding-window maximum's deque; the longest stretch without a repeat; monotonic stacks (next
   greater element, the largest rectangle in a histogram).
7. Searching: binary search on the answer; a binary search to trust (invariants, half-open ranges, Bloch's overflow);
   galloping (Bentley & Yao 1976); ternary search.
8. Bits: popcount, the lowest set bit, Gray codes; submask enumeration (exactly 3ⁿ); **the Four Russians** in C,
   bitset closure (10×) and bit-parallel LCS (103×).
9. Meet in the middle (Horowitz & Sahni 1974); square-root decomposition; Mo's order.
10. Algorithm engineering I, layouts: sorted, branch-free, Eytzinger with prefetch and a 16-key B-tree layout with
    AVX-512 (Khuong & Morin 2017), 1 K to 64 M keys (908 against 184 ns); branch prediction measured (5.3 against
    0.9 ns per element).
11. Algorithm engineering II: an AVX2 word scan (8.8×); auto-vectorization; Swiss-style tables against linear probing
    and `std::unordered_map` (66, 171 and 82 ns at 7/8 full).
12. Sorting in practice: introsort, pdqsort and Timsort; the radix crossover at about 64 keys and 3.5× at 16 M; the
    top 20 of 16 M (a heap, 94× faster than sorting).
13. Benchmarking honestly: warm-up and spread over thirty runs; environment size (Mytkowicz et al. 2009; Stabilizer);
    dead-code elimination.
14. Problem solving as a craft: Pólya's four steps on a worked problem with a stress test; the interview repertoire
    mapped to the series' parts.
15. The Job, engineered: an AVX2 tokenizer, word-at-a-time hashing and a Swiss-style table with inline keys, natively,
    against Part 17's C (155 against 75 ms); Amdahl's law; ledger row 10, the first measured on real hardware.
16. *Frontier*: a learned index over the corpus's word offsets (PGM-style; 64 segments, 1.5× faster than binary
    search); ski rental with predictions (consistency and robustness); the theory–practice gap (external memory,
    cache-oblivious); open problems. Outro.

*Computed:* every number above, in `videos/cs/cs24/compute.py` with `explainer/cs/algo/practice.py` (tested in
`tests/test_cs24_practice.py` against brute force): the structures' operation counts; and native C and C++
benchmarks, each checked against a reference before it is timed: array against list, four range structures,
search layouts, branches, SIMD word finding, vectorization, three hash tables, radix against comparison sort, top-k,
benchmark spread and layout bias, dead code, the Job engineered, a learned index. Ski rental with predictions in
Python.
*Visuals:* Fenwick responsibility ranges as bars by lowbit; a segment tree lighting its covering nodes; the sparse
table's windows; an Euler tour; a Cartesian tree; a sliding window with its deque; a histogram's best rectangle; a
sorted array against its Eytzinger layout; a word's letters as a bitmask; a Swiss-table group; benchmark
distributions as strips of dots; Amdahl's bars; the ledger's tenth row.
*In practice:* the data structures inside databases, search engines, game engines and trading systems; the core
repertoire of coding interviews; performance work on hot paths.
*Reading:* Skiena, *The Algorithm Design Manual*; Bentley, *Programming Pearls*; Warren, *Hacker's Delight*;
Laaksonen, *Guide to Competitive Programming*; Halim & Halim, *Competitive Programming*; Müller-Hannemann & Schirra
(eds.), *Algorithm Engineering*; Fenwick 1994; Bender & Farach-Colton 2000; Khuong & Morin 2017; Mytkowicz et al.
2009; Langdale & Lemire 2019 (simdjson); Kraska et al. 2018; Ferragina & Vinciguerra 2020.

---

## Act V · Limits and Secrets

### Part 25 · Undecidable (~55)
*Story:* Part 1 proved that one problem can't be solved. This part finds the same impossibility in Diophantine
equations, in tilings of the plane, in Gödel's theorem and in randomness itself. A program can print its own source,
and that fact is enough to prove all of it. The busy beaver marks where provability runs out.
1. Formally: decidable, recognizable, co-recognizable; the halting set K.
2. Mapping reductions; A_TM, E_TM, EQ_TM; recognizable but undecidable; neither.
3. **Rice's theorem** (proved): every non-trivial semantic property is undecidable. What that means for compilers,
   antivirus and static analysis, and how Part 54 escapes it by approximation.
4. **The recursion theorem** (Kleene): programs that know their own code; quines in the Pebble language and in
   Python; a shorter proof of halting's undecidability.
5. Post's correspondence problem (1946), via computation histories (dominoes animated); ambiguity of CFGs (callback
   to Part 12).
6. Tiling: Wang tiles (1961); Berger's aperiodic set and undecidability (1966); Penrose tilings; the 2023 aperiodic
   monotile, "the hat".
7. Hilbert's tenth (Matiyasevich 1970, on Davis, Putnam and Robinson): every r.e. set is Diophantine; the
   prime-producing polynomial (Jones et al. 1976), shown.
8. Gödel via halting: a sound r.e. theory that proved every true halting statement would decide halting (proved); the
   second theorem; Gödel numbering.
9. Oracles and degrees; the arithmetic hierarchy (Σ₁, Π₁, Σ₂; FIN and TOT); Post's problem (Friedberg–Muchnik).
10. **Kolmogorov complexity**: the invariance theorem (proved); incompressible strings exist (counting); K is
    uncomputable (Berry); Chaitin's incompleteness.
11. Chaitin's Ω: random, uncomputable, its bits answering famous questions.
12. Busy beavers again: how BB(5) was proved (deciders, cryptids, Coq); BB(6) bounds and the Collatz-like Antihydra
    (2025) **(verify)**; BB(n) is uncomputable and eventually independent of ZFC (Yedidia & Aaronson 2016, and later
    smaller machines **(verify)**).
13. The boundary:
    - decidable: Presburger arithmetic, at double-exponential cost (Fischer & Rabin 1974), and real closed fields
      (Tarski);
    - undecidable: the word problem for groups (Novikov, Boone), matrix mortality, generalized Collatz
      (Conway's FRACTRAN).
14. In the wild: Magic: The Gathering is Turing-complete (2019); Java generics and C++ templates; type checking that
    never ends. Outro.

*Computed:* a bounded PCP solver and the reduction; Wang tilings; compressors as a Kolmogorov proxy on random against
structured strings; BB champions; Conway's PRIMEGAME producing primes; Collatz trajectories.
*Visuals:* the PCP domino stack; a Wang tiling growing; the hat; the arithmetic hierarchy as a ladder; Ω's bits.
*In practice:* why static analyzers report false positives and no virus scanner can be perfect; self-reproducing code.
*Reading:* Sipser ch. 4–6; Rogers, *Theory of Recursive Functions and Effective Computability*; Soare, *Turing
Computability*; Boolos, Burgess & Jeffrey, *Computability and Logic*; Li & Vitányi, *An Introduction to Kolmogorov
Complexity*; Davis 1973; Matiyasevich, *Hilbert's Tenth Problem*; Chaitin 1975; Aaronson 2020; Smith et al. 2023.

### Part 26 · P versus NP (~60)
*Story:* In 1956 Gödel wrote to von Neumann asking whether finding a proof could be as easy as checking one. Cook
and Levin turned that question into SAT, and Karp showed that twenty-one famous problems are all secretly the same
problem. Here is why the question has resisted fifty years of work, and what each answer would mean.
1. Edmonds (1965) and Cobham: polynomial time as "efficient", and why it is a robust choice.
2. The **time hierarchy theorem** by diagonalization (proved); space classes; **Savitch**, NSPACE(s) ⊆ SPACE(s²), by
   midpoint recursion (proved).
3. NP: certificates and nondeterminism are equivalent; SAT, clique, Hamiltonian cycle, subset sum; graph isomorphism
   in quasi-polynomial time (Babai 2015).
4. Polynomial reductions; hardness and completeness.
5. **Cook–Levin** (1971/73): SAT is NP-complete, via the tableau proof (cells and 2 × 3 windows, animated).
6. The reduction web: SAT → 3SAT → independent set → clique and vertex cover; 3SAT → 3-coloring (gadgets drawn);
   3SAT → subset sum (digits); Hamiltonian cycle; Karp's 21 as a family tree.
7. NP-completeness everywhere (Garey & Johnson): Tetris, Minesweeper, generalized Sudoku, scheduling, folding.
8. Strong against weak NP-hardness; pseudo-polynomial algorithms (knapsack, Part 19).
9. coNP; NP ∩ coNP (factoring lives there); the polynomial hierarchy and its collapses.
10. Space:
    - TQBF is PSPACE-complete;
    - games: generalized geography, Go (Lichtenstein & Sipser), n × n chess, which is EXPTIME-complete;
    - NL = coNL (Immerman–Szelepcsényi); L against P.
11. Time in square-root space (Williams 2025, building on Cook & Mertz's tree evaluation) **(verify)**.
12. **Ladner's theorem**: if P ≠ NP, intermediate problems exist (sketch).
13. SAT in practice (callback to *AI, Built* 2): CDCL; industrial verification; the Boolean Pythagorean triples proof
    (200 TB, 2016) and Schur number five.
14. Why it's hard: relativization (Baker, Gill & Solovay 1975; oracles both ways), natural proofs (Razborov & Rudich),
    algebrization (Aaronson & Wigderson).
15. **Impagliazzo's five worlds** (Algorithmica, Heuristica, Pessiland, Minicrypt, Cryptomania): where cryptography
    lives (Parts 29–30).
16. If P = NP: Gödel's letter, and the consequences. Outro.

*Computed:* our reductions, implemented and verified (a SAT instance → 3-coloring → solved → mapped back); a
Cook–Levin tableau for a tiny NTM; our CDCL solver on reduced instances; the 3-SAT phase transition with our solver;
generalized geography.
*Visuals:* the tableau grid with sliding windows; gadget graphs assembling; the reduction family tree; the five
worlds as a map; the class zoo as nested sets, zoomed.
*In practice:* recognizing NP-hard problems at work (scheduling, packing, configuration, dependency resolution) and reaching for SAT or ILP solvers, or heuristics.
*Reading:* Sipser ch. 7–8; Arora & Barak, *Computational Complexity: A Modern Approach* ch. 1–6; Papadimitriou,
*Computational Complexity*; Garey & Johnson, *Computers and Intractability*; Moore & Mertens ch. 4–6; Goldreich, *P,
NP, and NP-Completeness*; Cook 1971; Karp 1972; Levin 1973; Aaronson, "P =? NP" (2016); Impagliazzo 1995; Fortnow, *The
Golden Ticket*.

### Part 27 · Proofs and Randomness (~60)
*Story:* Two ideas change what a proof is. With randomness, a verifier can check an exponentially long argument by
asking a few questions, and can be convinced that a statement is true while learning nothing else. The PCP theorem
says a few random bits of a proof are enough. That one fact explains why many approximation algorithms can't be
improved.
1. RP, coRP, ZPP, BPP; amplification by Chernoff (callback to *AI, Built* 5); BPP ⊆ P/poly (Adleman, proved);
   BPP ⊆ Σ₂ (Sipser–Gács–Lautemann).
2. Hardness against randomness: Nisan–Wigderson; Impagliazzo–Wigderson (exponential circuit lower bounds for E imply
   P = BPP); primality as the poster child.
3. Circuit lower bounds:
   - Karp–Lipton;
   - parity ∉ AC⁰ via **Håstad's switching lemma**, with random restrictions animated;
   - Razborov–Smolensky;
   - monotone clique (Razborov);
   - NEXP ⊄ ACC⁰ (Williams 2011): algorithms imply lower bounds.
4. Communication complexity (Yao 1979): equality, deterministic n against randomized O(log n); disjointness Ω(n);
   fooling sets and rank; streaming lower bounds (callback to Part 20).
5. Interactive proofs: graph non-isomorphism; GMR (1985), Babai's Arthur–Merlin.
6. Arithmetization and **sum-check** (Lund, Fortnow, Karloff & Nisan 1990), step by step over a finite field; #SAT ∈
   IP; **IP = PSPACE** (Shamir 1990).
7. **Zero knowledge**: Ali Baba's cave; GMW's 3-coloring protocol with commitments; simulation; Fiat–Shamir (Part 30).
8. **The PCP theorem** (AS, ALMSS 1992; Dinur 2005): checking a proof by reading O(1) bits; gap amplification.
9. Hardness of approximation: MAX-3SAT can't beat 7/8 (Håstad 2001), so a random assignment is optimal; clique
   n^{1−ε}; set cover ln n.
10. The **Unique Games Conjecture** (Khot 2002): vertex cover 2 and MAX-CUT 0.878 would be optimal (Part 23); the
    2-to-2 theorem (2018).
11. Fine-grained complexity: SETH, OV, 3SUM, APSP; edit distance (Part 21); what conditional lower bounds buy.
12. Parameterized complexity: FPT; vertex cover by bounded search trees; kernels (Buss); W[1]-hardness of clique;
    treewidth and Courcelle.
13. Counting: #P (Valiant 1979); the permanent against the determinant; Toda's theorem; approximate counting
    (Jerrum, Sinclair & Vigoda; callback to MCMC).
14. Average case and one-way functions, the bridge to Part 29. Outro.

*Computed:* Adleman's union bound in numbers; sum-check on a small #SAT instance, where a cheating prover is caught
with the computed probability; ZK 3-coloring with cheating probability (1 − 1/m)ᵏ; equality by fingerprints; random
assignments against the best found on MAX-3SAT; FPT vertex cover; permanent against determinant timings.
*Visuals:* a DNF collapsing under a random restriction; sum-check's rounds as univariate polynomials; a ZK coloring
revealing one edge; the PCP verifier sampling a few bits from a giant proof.
*In practice:* zero-knowledge proofs in identity systems and blockchains, succinct proofs in rollups, conditional lower bounds that say when to stop optimizing.
*Reading:* Arora & Barak ch. 7–11, 13–14, 18–22; Goldreich, *Computational Complexity: A Conceptual Perspective*;
Wigderson, *Mathematics and Computation*; Kushilevitz & Nisan, *Communication Complexity*; Jukna; Thaler, *Proofs,
Arguments, and Zero-Knowledge*; Cygan et al., *Parameterized Algorithms*; O'Donnell, *Analysis of Boolean Functions*;
Vassilevska Williams 2018 (survey); Håstad 2001; Khot 2002; Dinur 2007; Shamir 1992.

### Part 28 · Error-Correcting Codes (~55)
*Story:* In 1947 Hamming's weekend jobs kept dying on bad bits, so he taught the machine to fix them. A year later
Shannon proved that noise costs only a fixed fraction of the channel's rate, but not how to get there. It took fifty
years and several rediscoveries (Reed–Solomon, LDPC, turbo and polar codes) to reach that limit. We scratch a QR code
and get its message back.
1. Hamming at Bell Labs (1947–50); the binary symmetric channel; repetition codes.
2. Hamming distance and the Hamming cube (3D, 4D projected); d detects d − 1 errors and corrects ⌊(d − 1)/2⌋.
3. **Hamming(7,4)**: parity checks as a matrix; the syndrome names the bad bit; the Venn picture; a perfect code.
4. Bounds: Hamming (sphere packing), Singleton, Gilbert–Varshamov, on the rate–distance plane.
5. Linear codes and duality; the Golay code (Voyager, cited) and the Leech lattice, briefly.
6. Finite fields GF(p) and GF(2ᵐ) from irreducible polynomials (callback to Part 5's LFSRs); a cyclic multiplicative
   group.
7. **Reed–Solomon** (1960):
   - codewords as evaluations of polynomials, MDS by counting roots (proved);
   - erasures by Lagrange interpolation;
   - errors by **Berlekamp–Welch**, linear algebra on screen; Berlekamp–Massey;
   - CDs, QR codes, deep space, RAID-6.
8. **Our QR code**: encode a message, scratch the image, decode it back.
9. Cyclic codes and CRCs: polynomial division over GF(2) as a shift-register circuit; guarantees for burst errors;
   CRC-32 (Part 36).
10. **Shannon's channel coding theorem** (1948): BSC capacity 1 − H(p); random coding by typical sets (callback to
    *AI, Built* 1), proved; the converse via Fano.
11. Concatenated codes (Forney); convolutional codes and Viterbi (callbacks to *AI, Built* 7 and Part 19).
12. Turbo codes (1993) and the rediscovery of **LDPC** (Gallager 1962; MacKay & Neal): Tanner graphs, belief
    propagation (callback to *AI, Built* 7), density evolution, the computed waterfall.
13. **Polar codes** (Arıkan 2009): channel polarization computed and animated, with capacities splitting toward 0 and
    1; successive cancellation; 5G.
14. List decoding (Sudan, Guruswami–Sudan); locally decodable and testable codes and PCPs (Part 27).
15. Storage codes: RAID-5 and 6, LRCs (Azure), fountain and LT codes (Luby). Quantum codes previewed (Part 53).
    Outro.

*Computed:* Hamming(7,4) BER curves; the bounds; RS encode and decode of a scratched QR-like image; CRC detection
rates; random codes at small n; the LDPC waterfall; polarization.
*Visuals:* spheres around codewords in Hamming space; the Venn diagram; a polynomial through points with a corrupted
point pulled back; the polarization fan; messages flowing on a Tanner graph.
*In practice:* ECC memory, RAID and erasure-coded cloud storage, QR codes, Wi-Fi, 5G and satellite links, the CRC in every protocol.
*Reading:* MacKay, *Information Theory, Inference, and Learning Algorithms*; Cover & Thomas ch. 7; Guruswami, Rudra &
Sudan, *Essential Coding Theory*; MacWilliams & Sloane; Roth, *Introduction to Coding Theory*; Richardson & Urbanke,
*Modern Coding Theory*; Lin & Costello; Hamming 1950; Reed & Solomon 1960; Gallager 1962; Berrou et al. 1993; Arıkan
2009; Shannon 1948.

### Part 29 · Secrets (~55)
*Story:* For two thousand years ciphers were broken by counting letters. Shannon proved that perfect secrecy needs a
key as long as the message. Modern cryptography gets around that by assuming the adversary's computing power is
limited, and builds pseudorandomness, block ciphers and hashes on that assumption. The attacks show how much care it
takes.
1. Caesar, substitution and Vigenère; al-Kindi's frequency analysis, breaking a substitution cipher on a novel's
   paragraph; Kasiski and the index of coincidence.
2. Enigma: rotors as permutations. Rejewski (1932) saw that the cycle structure survives the plugboard, because
   conjugation preserves cycle type. Turing's Bombe; Colossus and Lorenz.
3. **Perfect secrecy** (Shannon 1949): the one-time pad; |K| ≥ |M| is necessary (proved); VENONA's reused pads.
4. Modern definitions: Kerckhoffs; PPT adversaries; negligible functions; IND-CPA drawn as a game.
5. **PRGs**: indistinguishability and next-bit unpredictability (Yao); Blum–Micali, hard-core bits
   (Goldreich–Levin); ChaCha20.
6. **PRFs**: the GGM tree, by a hybrid argument; PRPs and Luby–Rackoff (three Feistel rounds give a PRP).
7. Block ciphers:
   - DES (1977; broken by brute force by Deep Crack in 1998);
   - **AES** (2001): SubBytes (inversion in GF(2⁸), callback to Part 28), ShiftRows, MixColumns (an MDS matrix),
     AddRoundKey;
   - the avalanche effect, where one flipped bit changes half the output.
8. Modes: **the ECB penguin** (computed on our own image); CBC and Vaudenay's padding oracle (2002); CTR.
9. Integrity: CBC-MAC and HMAC; authenticated encryption; GCM's GHASH as polynomial evaluation; ChaCha20-Poly1305.
10. Hashes:
    - the birthday bound 2^{n/2} (callback to Part 17);
    - Merkle–Damgård and length extension;
    - MD5 and SHA-1 collisions (Wang 2004; SHAttered 2017);
    - the **SHA-3 sponge**.
11. Hash applications: Merkle trees (git, certificate transparency, Part 38's blockchains); commitments; salted,
    slow, memory-hard password hashing (bcrypt, scrypt, Argon2).
12. Cryptanalysis on a toy SPN: differential (Biham & Shamir; DES's S-boxes, hardened against it in 1974) and linear
    (Matsui); meet-in-the-middle and why 2DES fails.
13. Side channels: timing (Kocher 1996) and constant-time code; power analysis; cache attacks on AES T-tables
    (callback to Parts 8–9).
14. Randomness failures: the Debian OpenSSL bug (2008); Dual_EC_DRBG. Outro.

*Computed:* frequency analysis breaking a cipher; an Enigma simulation and its cycle structures; the ECB penguin
(our own logo); AES from scratch against FIPS-197 vectors; avalanche statistics; a toy differential attack on a
4-round SPN; birthday collisions on truncated SHA-256.
*Visuals:* the penguin under ECB against noise under CBC; AES's 4 × 4 state transforming round by round; an avalanche
heatmap; rotors stepping; the sponge absorbing and squeezing.
*In practice:* TLS cipher suites, disk and database encryption, password storage, HMAC-signed tokens, constant-time code review.
*Reading:* Katz & Lindell, *Introduction to Modern Cryptography*; Boneh & Shoup, *A Graduate Course in Applied
Cryptography*; Goldreich, *Foundations of Cryptography* I–II; Menezes, van Oorschot & Vanstone, *Handbook of Applied
Cryptography*; Daemen & Rijmen, *The Design of Rijndael*; Ferguson, Schneier & Kohno, *Cryptography Engineering*;
Kahn, *The Codebreakers*; Singh, *The Code Book*; Shannon 1949; Heys' tutorial on linear and differential
cryptanalysis.

### Part 30 · Public Keys (~60)
*Story:* Two strangers who have never met agree on a secret while everyone listens. It took Diffie and Hellman
(1976), RSA (1977) and the number theory of groups to make that possible. Elliptic curves made it compact, and
lattices may keep it safe against a quantum computer. By the end, two of our Pebbles carry out a TLS 1.3–style
handshake.
1. Key distribution; Merkle's puzzles (a quadratic gap); Diffie–Hellman (1976); GCHQ's earlier, secret work (Ellis,
   Cocks, Williamson).
2. The toolkit: modular arithmetic; extended Euclid and Bézout (animated); inverses; exponentiation by squaring.
3. Groups: ℤ_p^* is cyclic; Fermat via Lagrange; Euler; the discrete log.
4. **Diffie–Hellman**: paint mixing, then the mathematics; CDH and DDH; man-in-the-middle, so authentication is
   needed.
5. **RSA**: key generation, correctness via CRT and Euler (proved); textbook RSA's malleability; OAEP; hash-and-sign;
   Bleichenbacher (1998).
6. Factoring: Pollard's ρ (the birthday bound once more; the ρ shape); the quadratic sieve (smooth numbers, linear
   algebra over GF(2)); the number field sieve L_n[1/3]; RSA-250 (2020, cited).
7. Discrete logs: baby-step giant-step; ρ; Pohlig–Hellman; index calculus.
8. **Elliptic curves**:
   - the chord-and-tangent group law over ℝ (the 3B1B-style centerpiece);
   - the point cloud over F_p; scalar multiplication;
   - ECDH and ECDSA; Curve25519;
   - why no index calculus means smaller keys;
   - nonce reuse (the 2010 PS3 key recovery, recomputed on a toy curve).
9. Signatures and PKI: certificates, chains of trust, certificate transparency (Part 29's Merkle logs).
10. **TLS 1.3** (RFC 8446) as a sequence diagram between two simulated Pebbles: ECDHE, signatures, HKDF, AEAD;
    forward secrecy.
11. Shor's threat (Part 53), and "harvest now, decrypt later."
12. **Lattices**:
    - bases and shortest vectors; LLL (1982), animated in 2D;
    - **LWE** (Regev 2005) and worst-case to average-case reductions;
    - **ML-KEM** (FIPS 203, 2024): module-LWE with the NTT (callback to Part 19);
    - ML-DSA and SLH-DSA; Lamport one-time signatures and Merkle trees.
13. Zero knowledge in practice: Schnorr and Fiat–Shamir (Part 27); SNARKs from polynomial commitments (KZG), sketched.
14. Beyond: FHE (Gentry 2009, bootstrapping); MPC (Yao's garbled circuits; Shamir sharing, the Reed–Solomon
    polynomials again); differential privacy (callback to *AI, Built* 31). Outro.

*Computed:* extended-Euclid traces; 2048-bit RSA keys from our Miller–Rabin, checked; Pollard ρ timings as the
semiprimes grow; BSGS; the group law over ℝ and F_p; ECDSA nonce-reuse key recovery; a TLS-like transcript; LLL
breaking a toy knapsack; toy LWE and its noise; Shamir sharing.
*Visuals:* the elliptic curve's chord, third point and reflection; the F_p cloud; lattice bases reducing; LWE's
blurred lattice; the handshake.
*In practice:* TLS certificates and Let's Encrypt, SSH keys, code signing, passkeys, the post-quantum migration.
*Reading:* Katz & Lindell ch. 9–14; Boneh & Shoup parts II–III; Hoffstein, Pipher & Silverman, *An Introduction to
Mathematical Cryptography*; Washington, *Elliptic Curves*; Silverman & Tate, *Rational Points on Elliptic Curves*;
Shoup, *A Computational Introduction to Number Theory and Algebra*; Crandall & Pomerance, *Prime Numbers*; Diffie &
Hellman 1976; Rivest, Shamir & Adleman 1978; Regev 2009; Peikert 2016; NIST FIPS 203–205 (2024); RFC 8446.

---

## Act VI · One Machine, Many Programs

### Part 31 · The Kernel (~55)
*Story:* Early computers ran one job at a time, and an expensive machine sat idle while a person thought.
Time-sharing gave every user the illusion of a whole machine. That needed protection, interrupts, processes and a
scheduler. Queueing theory explains why a server at 90% load feels ten times slower than one at 50%. PebbleOS boots.
1. History: batch monitors; CTSS (1961) and time-sharing; Multics (1965); Unix (Thompson & Ritchie 1969–74); Linux
   (1991).
2. Protection: user and kernel mode, privileged instructions. Pebble gains a mode bit, `ecall`, and a timer
   interrupt.
3. Traps, exceptions and interrupts: the hardware sequence (save the PC, switch mode, vector); the system-call path
   drawn end to end.
4. The process: address space, registers and state; the state diagram; the PCB; PebbleOS's process table.
5. Context switches: what is saved, and the cost (measured on this machine by pipe ping-pong).
6. fork, exec and wait: why Unix split them; a shell in a few lines; pipes and file descriptors.
7. Scheduling metrics; FCFS and the convoy effect; **SJF minimizes mean completion time** (exchange argument); SRTF.
8. Round robin and the quantum; **MLFQ** (Corbató 1962) and how to game it.
9. Proportional share: lottery and stride (Waldspurger 1994–95); CFS's virtual runtime in a red–black tree (2007;
   callback to Part 17); EEVDF (Linux 6.6).
10. Multiprocessor scheduling: affinity, load balancing, work stealing (callback to Part 10).
11. Real time: rate-monotonic scheduling and **Liu–Layland's U ≤ n(2^{1/n} − 1) → ln 2** (1973, sketched); EDF is
    optimal; priority inversion on Mars Pathfinder (1997) and priority inheritance.
12. **Queueing theory**: Little's law L = λW (proved by areas); M/M/1's 1/(μ − λ) (derived) and its hockey stick;
    Pollaczek–Khinchine (variance matters); SRPT is optimal (Schrage 1968).
13. Kernel designs: monolithic, microkernel (Mach, L4; the Tanenbaum–Torvalds debate of 1992), exokernel, unikernel;
    seL4 (Part 54).
14. **PebbleOS boots on the emulator** and runs two processes doing the Job concurrently. Ledger row 11. Outro.

*Computed:* PebbleOS traces (traps, timer, context switches); simulations of FCFS, SJF, RR, MLFQ, stride and
CFS-lite; M/M/1 against the formula; RMS and EDF schedulability; context-switch cost on this machine.
*Visuals:* Gantt charts; the system call as a camera dive into the kernel and back; a queue's random walk under the
hockey-stick curve; the process state machine.
*In practice:* Linux internals (CFS and EEVDF, system calls, `strace`), real-time and embedded RTOSes, eBPF, capacity planning with queueing.
*Reading:* Arpaci-Dusseau & Arpaci-Dusseau, *Operating Systems: Three Easy Pieces* (OSTEP), virtualization of the
CPU; Tanenbaum & Bos, *Modern Operating Systems*; Silberschatz, Galvin & Gagne; Anderson & Dahlin, *Operating Systems:
Principles and Practice*; Cox, Kaashoek & Morris, *xv6*; Ritchie & Thompson 1974; Corbató et al. 1962; Liu & Layland
1973; Harchol-Balter, *Performance Modeling and Design of Computer Systems*; Kleinrock, *Queueing Systems*.

### Part 32 · Virtual Memory (~55)
*Story:* Every program believes it owns a huge, private, contiguous memory. None of them does. Address translation
maintains the illusion with a radix tree walked in hardware and cached in the TLB. Because memory is finite, some
page must leave, and Belady showed both which page is optimal and that adding memory can make things worse.
1. The problem: protection and relocation; Atlas (1962) invents paging.
2. Base and bounds; segmentation; external fragmentation (callback to Part 11).
3. Paging: VPN | offset split, animated; PTE bits (valid, protection, dirty, accessed).
4. Multi-level page tables as a radix-tree walk (x86-64 four and five levels); inverted and hashed tables.
5. **The TLB**, a cache for translations (callback to Part 9): reach, ASIDs, huge pages. The TLB-miss staircase is
   measured on this machine.
6. Page faults: demand paging and swapping; effective access time (why one fault per million accesses matters).
7. Replacement:
   - **Belady's OPT is optimal** (exchange argument);
   - FIFO and **Belady's anomaly** (a computed example where more frames give more faults);
   - LRU and the stack property, which rules out the anomaly (proved);
   - CLOCK and WSClock; 2Q, ARC, LIRS.
8. Working sets (Denning 1968) and thrashing; the Job's trace replayed through every policy, with miss curves
   against frames.
9. Copy-on-write fork; zero pages; mmap; shared libraries (callback to Part 11).
10. The kernel's own mapping; KPTI after Meltdown (callback to Part 8).
11. Kernel allocators: buddy and slab (Bonwick 1994).
12. Virtualization:
    - **Popek–Goldberg** (1974) and trap-and-emulate;
    - x86's non-virtualizable instructions and VMware's binary translation (1999);
    - VT-x and nested paging's 2D walk (up to 24 memory references, derived);
    - Xen's paravirtualization.
13. Containers: namespaces and cgroups; isolation without a second kernel, and what it costs in security.
14. PebbleOS gains virtual memory: two processes at the same virtual address, isolated, and a protection fault
    caught. Outro.

*Computed:* page-table walks on Pebble's MMU; Belady's anomaly; OPT, LRU, FIFO, CLOCK and ARC curves on real
traces; the TLB staircase on this machine; the nested-walk count.
*Visuals:* address bits walking down a radix tree; frames shuffling to disk and back; the anomaly curve rising; the
CLOCK hand sweeping.
*In practice:* hypervisors (KVM, Xen), containers (Docker, cgroups, namespaces), huge pages for databases, OOM debugging.
*Reading:* OSTEP (virtualization of memory); Tanenbaum & Bos ch. 3; Denning 1970; Belady 1966; Belady, Nelson &
Shedler 1969; Mattson et al. 1970; Kilburn et al. 1962; Bonwick 1994; Popek & Goldberg 1974; Adams & Agesen 2006;
Bhargava et al. 2008; Gorman, *Understanding the Linux Virtual Memory Manager*.

### Part 33 · Concurrency (~60)
*Story:* Two threads each add one to a counter, and the count goes up by one. Mutual exclusion can be built from
plain reads and writes (Peterson) until the hardware reorders them. The fix has two parts: a theory of memory
models, and a hierarchy that orders synchronization primitives by power. In that hierarchy, compare-and-swap can
implement every concurrent object.
1. Why concurrency: overlapping I/O, using cores; threads against processes.
2. **The race**: counter++ as load, add, store. Interleavings counted (C(2n, n)); the lost update found by our
   exhaustive interleaving model checker.
3. Mutual exclusion (safety, liveness, fairness): Dekker (1965); **Peterson (1981), proved by invariant**; Lamport's
   bakery (1974); the Burns–Lynch n-register lower bound.
4. Peterson breaks under TSO: the store-buffer litmus test (callback to Part 10), checked under SC and TSO models, and
   repaired with a fence.
5. Hardware locks: TAS, TTAS with backoff, ticket locks, **MCS** (1991) and its cache-line traffic (callback to
   MESI).
6. Semaphores (Dijkstra 1965): the bounded buffer; readers–writers; puzzles from *The Little Book of Semaphores*.
7. Monitors and condition variables (Hoare 1974, Brinch Hansen); Mesa semantics, and why `while` and not `if`.
8. **Deadlock**: Coffman's four conditions (1971); resource-allocation graphs; lock ordering; the banker's algorithm;
   the dining philosophers, deadlocked and then fixed.
9. Memory models: happens-before; **DRF ⇒ SC** (Adve & Hill 1990); the C++11 and Java models; acquire and release;
   out-of-thin-air values.
10. **Linearizability** (Herlihy & Wing 1990), on timelines; a computed history checker.
11. Lock-free structures: the Treiber stack and ABA; tags, hazard pointers, epochs and RCU; the Michael–Scott queue.
12. Progress conditions, and **consensus numbers** (Herlihy 1991): registers 1, test-and-set and queues 2, CAS ∞,
    proved by valency (a preview of FLP in Part 38); the universality of consensus.
13. Transactional memory (Herlihy & Moss 1993; TSX's troubles).
14. Other models: CSP (Hoare 1978) and Go channels; actors and Erlang; async/await.
15. In the wild: Therac-25 and the 2003 blackout (cited); race detectors with vector clocks (Part 38).
16. PebbleOS gains a CAS mutex and threads. Outro.

*Computed:* exhaustive interleavings for counter++, Peterson and the bakery with property checks; SC against TSO
model checking; a lock benchmark (C on this machine where available, otherwise a cache-traffic simulation);
linearizability checking; the ABA scenario; dining philosophers; the banker's algorithm.
*Visuals:* interleavings branching as a tree; Peterson's state graph with the bad state unreachable; the MCS queue as
linked waiters; the consensus ladder.
*In practice:* mutexes, channels and async runtimes (Go, Rust's tokio, java.util.concurrent), race detectors (TSan), lock-free queues in low-latency systems.
*Reading:* Herlihy & Shavit, *The Art of Multiprocessor Programming*; OSTEP (concurrency); Downey, *The Little Book of
Semaphores*; Lynch, *Distributed Algorithms* ch. 10; Sorin, Hill & Wood; McKenney, *Is Parallel Programming Hard?*;
Lamport 1974, 1979; Dijkstra 1965; Hoare 1974, 1978; Herlihy 1991; Herlihy & Wing 1990; Adve & Gharachorloo 1996;
Boehm & Adve 2008; Mellor-Crummey & Scott 1991.

### Part 34 · Storage (~55)
*Story:* Memory forgets when the power goes, so data must live on spinning platters or in leaky flash. An append
that needs three writes can be cut short by a crash between any two of them. Journals, logs and copy-on-write trees
are the answers, and RAID's parity is Part 28's codes at work.
1. Persistence and the bottom of the hierarchy (callback to Part 9).
2. Disks: seek + rotation + transfer (computed); random against sequential (100×); SSTF, SCAN, C-SCAN.
3. Flash:
   - cells, pages, erase blocks, wear;
   - the FTL as a log, with garbage collection;
   - **write amplification**, simulated against over-provisioning;
   - TRIM; NVMe queues.
4. Files and directories, inodes, links; the Unix API (open, read, write, fsync).
5. A simple file system: superblock, bitmaps, inodes, data blocks; indirect blocks and the maximum file size; a path
   lookup.
6. Locality: FFS (McKusick et al. 1984) and cylinder groups; extents.
7. **Crash consistency**: fsck; journaling (data and metadata, ordered mode), with a replay animated; soft updates;
   our file system **crashed at every write point** and checked each time.
8. Log-structured FS (Rosenblum & Ousterhout 1992): segment cleaning and cost–benefit; bimodal utilization.
9. Copy-on-write (ZFS, btrfs): Merkle checksums (callback to Part 29); snapshots for free.
10. **RAID** (Patterson, Gibson & Katz 1988): levels 0/1/4/5/6 (callback to Part 28); the small-write problem; the
    chance of a second failure during rebuild (computed).
11. Reliability in the field (Schroeder & Gibson 2007, cited); latent sector errors; end-to-end checksums.
12. fsync and the illusion of durability: write caches and barriers; "fsyncgate" (2018).
13. **LSM trees** (O'Neil et al. 1996): memtables, SSTables, leveled against tiered compaction; read, write and space
    amplification (the RUM conjecture); Bloom filters per run (callback to Part 20).
14. Our file system and key-value store on PebbleOS's disk; the novels stored and read back. Ledger row 12. Outro.

*Computed:* the disk-time model; an FTL simulator; crash injection; LSM against B-tree amplification; RAID rebuild
risk; LFS cleaning.
*Visuals:* the head seeking while the platter spins; erase blocks being collected; the journal replaying after a
crash; LSM levels compacting in cascades.
*In practice:* choosing ext4, XFS or ZFS, SSD endurance in production, fsync and durability bugs, RocksDB and LSM tuning.
*Reading:* OSTEP (persistence); McKusick et al. 1984; Rosenblum & Ousterhout 1992; Patterson, Gibson & Katz 1988;
Pillai et al. 2014; O'Neil et al. 1996; Petrov, *Database Internals* part I; Agrawal et al. 2008; Giampaolo,
*Practical File System Design*; Schroeder & Gibson 2007.

### Part 35 · Databases (~60)
*Story:* In 1970 Codd said programs should ask for *what* data they want and never *how* to find it. That one idea
created a mathematics (relational algebra), an optimizer that searches for the cheapest plan, and the theory of
transactions, which lets thousands of users act as if each were alone, even through crashes. The Job becomes one
line of SQL.
1. Before Codd: IMS and CODASYL. **Codd 1970** and data independence.
2. Relations, keys, **relational algebra** (σ π ⋈ ∪ − ρ) acting on tables; relational calculus and Codd's theorem;
   SEQUEL and System R (1974).
3. Functional dependencies, Armstrong's axioms, BCNF and 3NF; update anomalies.
4. **The Job as SQL**, and the question of how a database answers it.
5. Query processing: iterators (Volcano, Graefe); scans; index selection.
6. Joins: nested loops, block, index, sort–merge, Grace hash. I/O costs derived (callback to Part 9's external
   memory).
7. **Selinger's optimizer** (1979): dynamic programming over join orders with interesting orders; the size of plan
   space (Catalan × n!); cardinality estimation and how independence assumptions fail.
8. Indexes: B+ trees (three levels index a billion rows); clustered against unclustered; hash and bitmap indexes;
   LSM (Part 34).
9. Transactions: ACID; schedules; **conflict serializability by precedence graphs** (a cycle means not
   serializable, proved); view serializability is NP-complete.
10. **2PL ⇒ serializable** (proved); strict 2PL; deadlock handling (wait-die, wound-wait); intention locks.
11. Optimistic concurrency and timestamps; **MVCC**; snapshot isolation and **write skew** (two doctors on call);
    serializable SI (Cahill 2008).
12. Isolation levels and their anomalies (Berenson et al. 1995; Adya 1999).
13. **Recovery**: WAL, steal/no-force; **ARIES** (Mohan 1992) with its analysis, redo and undo passes over LSNs;
    checkpoints.
14. Analytics: column stores (C-Store, MonetDB/X100, DuckDB); compression (callback to Part 21); vectorized against
    compiled execution.
15. **Our database** runs the Job's SQL on the novels and shows the plan it chose against the alternatives, with
    costs, cross-checked against `sqlite3`. Ledger row 13.
16. Beyond relational: key-value, document and graph stores; distributed transactions (Part 39). Outro.

*Computed:* join I/O against formulas; Selinger DP against exhaustive search; estimation errors under correlation; a
serializability checker; 2PL; write skew; ARIES on crashed logs; row against column scans; our database.
*Visuals:* tables transformed by algebra operators; join trees with costs; a precedence-graph cycle lighting up;
ARIES' three sweeps over the log; row against column layouts.
*In practice:* PostgreSQL and MySQL internals, reading query plans (`EXPLAIN`), index design, isolation-level bugs, SQLite everywhere, DuckDB for analytics.
*Reading:* Silberschatz, Korth & Sudarshan, *Database System Concepts*; Ramakrishnan & Gehrke; Garcia-Molina, Ullman &
Widom, *Database Systems: The Complete Book*; Hellerstein & Stonebraker, *Readings in Database Systems* (the Red
Book); Gray & Reuter, *Transaction Processing*; Weikum & Vossen; Bernstein, Hadzilacos & Goodman; Abiteboul, Hull &
Vianu, *Foundations of Databases*; Codd 1970; Selinger et al. 1979; Mohan et al. 1992; Berenson et al. 1995; Adya
1999; Hellerstein, Stonebraker & Hamilton 2007.

---

## Act VII · Many Machines

### Part 36 · Networks I: Moving Bits (~55)
*Story:* The phone network reserved a wire for every call. Baran and Davies proposed cutting messages into packets
that find their own way. The Internet is that idea, organized in layers, with IP as the narrow waist. This part
derives what limits it at each layer: Shannon's capacity, ALOHA's 1/2e, the count-to-infinity problem, and BGP's
policies.
1. History: circuit switching; Baran (1964) and Davies; ARPANET (1969, "LO"); Cerf & Kahn (1974); the 1983 flag day.
2. Layering and encapsulation (headers nesting, animated); the hourglass; **the end-to-end argument** (Saltzer, Reed
   & Clark 1984); Clark's design philosophy (1988).
3. Physical layer: Nyquist and **Shannon–Hartley C = B log₂(1 + S/N)**; QAM constellations in noise; fiber and the
   speed of light; the bandwidth–delay product.
4. Link layer: framing and bit stuffing; CRC (callback to Part 28); MAC addresses.
5. Multiple access: **ALOHA, S = G e^{−2G}, max 1/(2e)** (derived); slotted 1/e; CSMA/CD and exponential backoff
   (Metcalfe 1973); Wi-Fi's CSMA/CA and hidden terminals.
6. Bridges and switches; Perlman's spanning tree (1985); VLANs.
7. IP: CIDR, NAT, IPv6; fragmentation; ICMP and traceroute's TTL trick.
8. Forwarding: longest-prefix match with tries (callback to Part 17); TCAMs; nanoseconds per packet at 400 Gb/s.
9. **Distance vector = distributed Bellman–Ford** (callback to Part 18); count-to-infinity animated; split horizon and
   poisoned reverse.
10. Link state: flooding plus Dijkstra (OSPF); convergence and transient loops.
11. **BGP**: path vector; policy (Gao–Rexford); hijacks (YouTube, 2008, cited); RPKI.
12. SDN and programmable data planes (OpenFlow, P4).
13. Our internet: Pebbles on simulated links and routers; count-to-infinity and traceroute in the simulation.
14. Wireless and cellular: fading, OFDM (FFT callback), MIMO capacity. Outro.

*Computed:* ALOHA, slotted ALOHA and CSMA against their formulas; QAM error rates against the Shannon limit; LPM
lookups; distance-vector and link-state convergence; a BGP policy example; traceroute in the simulation.
*Visuals:* envelopes nesting headers; collisions on an ALOHA timeline; noisy constellations; distance-vector tables
counting up; an AS graph.
*In practice:* subnets and CIDR, BGP at ISPs and clouds, Ethernet and Wi-Fi troubleshooting, `traceroute` and `tcpdump`.
*Reading:* Kurose & Ross, *Computer Networking: A Top-Down Approach*; Peterson & Davie, *Computer Networks: A Systems
Approach*; Tanenbaum & Wetherall; Stevens, *TCP/IP Illustrated* vol. 1; Bertsekas & Gallager, *Data Networks*;
Varghese, *Network Algorithmics*; Tse & Viswanath, *Fundamentals of Wireless Communication*; Baran 1964; Cerf & Kahn
1974; Saltzer, Reed & Clark 1984; Abramson 1970; Metcalfe & Boggs 1976; Clark 1988.

### Part 37 · Networks II: Reliable Conversation (~55)
*Story:* IP loses, reorders and duplicates packets, and TCP turns that into a reliable stream. In October 1986 the
Internet's throughput fell a thousandfold, and Van Jacobson's fix, additive increase and multiplicative decrease,
turned out to be a distributed optimization algorithm. The Job's novels arrive over our own TCP on a lossy link.
1. The transport problem; UDP against TCP.
2. Reliability from scratch:
   - stop-and-wait and the alternating-bit protocol;
   - utilization (L/R)/(RTT + L/R), derived;
   - sliding windows: Go-Back-N and Selective Repeat;
   - sequence space ≥ 2 × window (proved).
3. TCP: sequence numbers, cumulative ACKs, the handshake and SYN cookies, teardown and TIME_WAIT, flow control.
4. RTT estimation (Jacobson/Karels EWMAs, Karn's rule, RTO).
5. The 1986 collapse (32 kb/s → 40 b/s); Jacobson (1988): slow start, congestion avoidance, fast retransmit and
   recovery.
6. **AIMD and the Chiu–Jain phase plot** (1989): AIMD converges to fair and efficient (proved geometrically,
   animated); MIMD and AIAD don't.
7. The sawtooth and **the Mathis formula** ≈ (MSS/RTT)·√(3/2)/√p (derived); RTT unfairness.
8. Router queues: drop-tail, **bufferbloat**, RED and CoDel; buffer sizing at RTT·C/√n (Appenzeller 2004).
9. Modern congestion control: CUBIC; **BBR** (2016) and Kleinrock's optimal operating point; Vegas; DCTCP.
10. **Network utility maximization** (Kelly 1998): TCP as a dual algorithm; proportional fairness (callback to Part
    22's duality).
11. DNS (Mockapetris 1983): hierarchy, caching, TTLs; Kaminsky's poisoning (2008).
12. The web: HTTP/1.1 and head-of-line blocking; HTTP/2; **QUIC** (RFC 9000) and HTTP/3: streams over UDP, 0-RTT,
    migration; TLS 1.3 inside (callback to Part 30).
13. CDNs and anycast; Zipf's law of requests, fitted on the novels' words.
14. Our TCP fetching the novels over a lossy link: cwnd traces. Ledger row 14. Outro.

*Computed:* our rdt and TCP-lite under loss and reordering; utilization against window; Chiu–Jain trajectories;
sawtooth throughput against Mathis; bufferbloat delays; BBR-lite against Reno-lite; NUM by dual ascent; the Zipf fit.
*Visuals:* sequence diagrams with drops and retransmits; a window sliding over the byte stream; Chiu–Jain zig-zags
toward the fairness line; the cwnd sawtooth; queues swelling.
*In practice:* TCP tuning, CDNs, HTTP/2 and HTTP/3 deployments, DNS operations, Wireshark.
*Reading:* Kurose & Ross ch. 2–3; Peterson & Davie ch. 5–6; Stevens; Srikant & Ying, *Communication Networks*;
Grigorik, *High Performance Browser Networking*; Jacobson 1988; Chiu & Jain 1989; Mathis et al. 1997; Kelly, Maulloo &
Tan 1998; Cardwell et al. 2016; Langley et al. 2017; Nichols & Jacobson 2012.

### Part 38 · Distributed Systems I: Agreement (~60)
*Story:* "A distributed system is one in which the failure of a computer you didn't even know existed can render
your own computer unusable" (Lamport). With no shared clock and failures that look like slowness, even agreeing on
one bit is provably impossible in general (FLP). Paxos and Raft agree anyway, by giving up a guarantee that FLP
says no one can have. We build Raft and try to break it.
1. Partial failure, no global clock, asynchrony.
2. **The two generals** cannot agree over a lossy link (proved by induction on messages).
3. Time: NTP and its limits; **happened-before and Lamport clocks** (1978) on space–time diagrams; **vector clocks**
   characterize causality (proved); race detectors (callback to Part 33).
4. **Chandy–Lamport snapshots** (1985): consistent cuts, animated.
5. Failure models (crash, omission, Byzantine); synchrony, asynchrony, partial synchrony (DLS 1988); failure
   detectors (◇S).
6. Consensus defined; synchronous crash consensus in f + 1 rounds, with the lower bound.
7. **FLP** (1985): the bivalence proof walked through (an initial bivalent configuration; the critical step).
8. Ways around FLP: randomization (Ben-Or), failure detectors, partial synchrony.
9. **Paxos** (Lamport 1989/98): prepare/promise and accept/accepted; the safety invariant (proved); Multi-Paxos.
10. **Raft** (Ongaro & Ousterhout 2014): randomized elections, log replication, log matching, the commit rule, the
    safety argument, membership changes.
11. **Our Raft**: five nodes on our network, with crashes and partitions; the logs animated; invariants checked over
    thousands of seeded fault schedules.
12. Replicated state machines (Schneider 1990); linearizable reads; leases.
13. **Byzantine generals** (Lamport, Shostak & Pease 1982): n ≥ 3f + 1 is necessary (the three-general proof) and
    sufficient; signatures; PBFT (1999); HotStuff.
14. **Nakamoto consensus** (2008): proof of work, the longest chain, the double-spend probability recomputed;
    selfish mining; proof of stake.
15. Checking protocols: TLA+ at Amazon (Part 54); Jepsen's findings (cited). Outro.

*Computed:* vector-clock causality; snapshots; FLP's valency explored exhaustively on a tiny protocol; Raft with
fault injection and invariant checks; the Byzantine counterexample; PBFT message counts; Nakamoto's probabilities
against Monte Carlo.
*Visuals:* space–time diagrams with clock stamps; consistent and inconsistent cuts; Raft terms and logs lining up;
configuration graphs colored by valency; a traitor sending split messages.
*In practice:* etcd, ZooKeeper and Consul, leader election inside every distributed database, blockchains.
*Reading:* Lynch, *Distributed Algorithms*; Attiya & Welch, *Distributed Computing*; Cachin, Guerraoui & Rodrigues,
*Introduction to Reliable and Secure Distributed Programming*; van Steen & Tanenbaum, *Distributed Systems*;
Kleppmann, *Designing Data-Intensive Applications* ch. 8–9; Lamport 1978, 1998, 2001; Fischer, Lynch & Paterson 1985;
Ongaro & Ousterhout 2014; Lamport, Shostak & Pease 1982; Castro & Liskov 1999; Nakamoto 2008; Dwork, Lynch &
Stockmeyer 1988; Chandy & Lamport 1985.

### Part 39 · Distributed Systems II: Scale (~55)
*Story:* At planet scale, every guarantee has a price in latency or availability. CAP states the trade-off, CRDTs
avoid it by making merges commutative, and Spanner pays for it with atomic clocks. One slow server in a hundred
makes most requests slow. The Job finally runs as MapReduce on sixteen machines, one of which dies.
1. The datacenter as a computer; latency numbers every programmer should know (cited, on the "cycle = second" scale).
2. Replication: single-leader, multi-leader, leaderless; synchronous against asynchronous; replication-lag anomalies.
3. **Quorums** R + W > N; sloppy quorums and hinted handoff (Dynamo 2007); probabilistically bounded staleness
   (computed).
4. Consistency models from linearizable to eventual, as a hierarchy; session guarantees.
5. **CAP** (Brewer; the Gilbert–Lynch proof), stated precisely; PACELC.
6. **CRDTs** (Shapiro et al. 2011): join-semilattices whose merge is commutative, associative and idempotent, which
   gives convergence (proved); counters, OR-sets, sequence CRDTs for collaborative editing.
7. Partitioning: hash against range; **consistent hashing** (Karger et al. 1997) with virtual nodes (load variance
   computed); rendezvous and jump hashing.
8. DHTs: Chord's fingers and O(log n) lookups; Kademlia's XOR metric.
9. Distributed transactions: 2PC and its blocking; 3PC; **Spanner** (2012): TrueTime and commit wait, animated;
   Calvin.
10. **MapReduce** (Dean & Ghemawat 2004): map, shuffle, reduce. The Job on sixteen simulated Pebbles, with a crash and
    re-execution; stragglers and backup tasks. Ledger row 15.
11. Spark's RDDs and lineage; streaming with watermarks; exactly-once via Chandy–Lamport (callback to Part 38).
12. Coordination: Chubby and ZooKeeper; leases and fencing tokens.
13. **The tail at scale** (Dean & Barroso 2013): 1 − 0.99¹⁰⁰ ≈ 63% (computed); hedged requests; two choices
    (callback to Part 20).
14. Failure at scale: correlated, gray and metastable failures; chaos engineering; post-mortems (cited). Outro.

*Computed:* PBS; CRDT convergence under random delivery orders; consistent-hashing variance; Chord hops; 2PC
blocking; Spanner's timeline; the MapReduce Job with a failure; tail amplification; hedging.
*Visuals:* the consistency hierarchy as a map; replicas merging up a lattice; the hash ring; Chord fingers; the
shuffle as colored streams; the fan-out tail.
*In practice:* Cassandra, DynamoDB, Spanner and CockroachDB, Redis Cluster, Spark; consistency choices as product decisions.
*Reading:* Kleppmann, *Designing Data-Intensive Applications*; Barroso, Hölzle & Ranganathan, *The Datacenter as a
Computer*; Saltzer & Kaashoek, *Principles of Computer System Design*; van Steen & Tanenbaum; DeCandia et al. 2007;
Corbett et al. 2012; Dean & Ghemawat 2004; Zaharia et al. 2012; Shapiro et al. 2011; Gilbert & Lynch 2002; Karger et
al. 1997; Stoica et al. 2001; Dean & Barroso 2013; Burrows 2006; Hunt et al. 2010; Bailis et al. 2012; Akidau et al.
2015.

---

## Act VIII · Building Software

### Part 40 · Software Engineering (~55)
*Story:* What one person writes in a weekend fails in different ways from what a thousand people change every day.
The discipline born at the 1968 NATO "software crisis" conference is about managing complexity. Modules hide
decisions, interfaces survive change, tests pin down behaviour, and a team's communication structure ends up as the
system's architecture. Some of this is mathematics: Brooks' n(n − 1)/2, the tails of task durations, dependency
metrics. Much of it is hard-won practice, which we test against evidence where evidence exists.
1. Hook: the 1968 NATO conference; OS/360 and Brooks' law (adding people to a late project makes it later).
2. Complexity, essential and accidental ("No Silver Bullet", 1986). **Parnas 1972**: the KWIC system decomposed two
   ways, and one change rippling through one decomposition but not the other.
3. Abstraction:
   - abstract data types (Liskov & Zilles 1974);
   - representation invariants and abstraction functions;
   - design by contract (Meyer);
   - **behavioural subtyping** (Liskov & Wing 1994).
4. Coupling and cohesion, measured on **this repository's own import graph**: cycles, layering, dependency inversion,
   instability and abstractness metrics.
5. Object-oriented design: encapsulation, polymorphism (vtables, callback to Part 15), composition over inheritance;
   SOLID stated precisely, each with a counterexample.
6. Design patterns (Gamma et al. 1994) as reusable shapes:
   - strategy, observer, visitor, adapter, decorator, factory;
   - the expression problem (Wadler 1998);
   - their functional equivalents; anti-patterns.
7. Functional design in industry: immutability; a pure core inside an imperative shell; making illegal states
   unrepresentable with algebraic data types (callback to Part 14).
8. Testing in practice:
   - the test pyramid; unit, integration and end-to-end tests;
   - test doubles (fakes, stubs, mocks);
   - **flaky tests** and their causes (order, time, concurrency; Google's statistics, cited);
   - coverage and its limits; mutation score.
9. Refactoring (Opdyke 1992; Fowler): behaviour-preserving transformations; code smells; characterization tests for
   legacy code (Feathers).
10. Technical debt (Cunningham 1992) as a debt with interest. The cost-of-a-defect curve, and how weakly the classic
    100× figure is supported (Menzies et al. 2016, cited).
11. Code review: what it catches (Bacchelli & Bird 2013); review size against detection; linters and static analysis
    in CI (Part 54).
12. Process:
    - waterfall (Royce 1970, who argued against it), iterative development, agile, Scrum and Kanban;
    - work in progress as a queue (Little's law again, callback to Part 31);
    - **the DORA metrics** (*Accelerate*).
13. **Conway's law** (1968) and the inverse Conway manoeuvre; Brooks' law with n(n − 1)/2 communication channels and
    a ramp-up model (simulated).
14. Estimation: the planning fallacy; heavy-tailed (lognormal) task durations; a Monte Carlo schedule with its tail;
    the cone of uncertainty.
15. The profession:
    - permissive against copyleft licenses;
    - the economics of open source;
    - privacy by design (data minimization, purpose limitation);
    - accessibility obligations; the ACM Code of Ethics.

    Outro.

*Computed:* this repository's import graph with its cycles and layering metrics; flakiness of an order-dependent test
suite; a Brooks' law simulation; Monte Carlo schedules; mutation testing of a Pebble toolchain module.
*Visuals:* the two KWIC decompositions with a change rippling through one; dependency graphs with cycles lit; the
communication graph's edges growing quadratically as people join; a schedule distribution and its tail.
*In practice:* how industry codebases are structured, reviewed and tested; the vocabulary of design docs and design
reviews; working on a team.
*Reading:* Brooks, *The Mythical Man-Month* (with "No Silver Bullet"); Ousterhout, *A Philosophy of Software Design*;
McConnell, *Code Complete*; Hunt & Thomas, *The Pragmatic Programmer*; Gamma, Helm, Johnson & Vlissides, *Design
Patterns*; Fowler, *Refactoring*; Feathers, *Working Effectively with Legacy Code*; Liskov & Guttag, *Program
Development in Java*; Meyer, *Object-Oriented Software Construction*; Winters, Manshreck & Wright, *Software
Engineering at Google*; Forsgren, Humble & Kim, *Accelerate*; Naur & Randell 1969; Parnas 1972; Conway 1968; Liskov &
Wing 1994.

### Part 41 · Version Control, Builds and Dependencies (~55)
*Story:* Every change to modern software passes through three machines. The version-control system is secretly a
content-addressed Merkle DAG. The build system is secretly an incremental computation over a dependency graph. The
package manager is secretly a SAT solver, because choosing versions is NP-complete. Above them, CI and deployment turn
a change into running software safely, a little at a time.
1. Hook: the 2005 BitKeeper split and git's first ten days; from RCS, CVS and SVN to distributed version control.
2. Git's object model: blobs, trees, commits, tags, all content-addressed (callback to Part 29's hashes); history as a
   Merkle DAG, with integrity for free. We build a small object store and check its hashes against real git's.
3. Refs, branches, the index and the reflog; what checkout actually does.
4. **Merging**:
   - merge bases as lowest common ancestors in the DAG (several of them, and git's recursive strategy);
   - three-way merge over Myers' diff (callback to Part 21);
   - conflicts; ort.
5. Rebase against merge; cherry-pick as applying a diff; **bisect** as binary search over history.
6. Storage: packfiles and delta compression (callback to Part 21); shallow and partial clones; monorepos at scale
   (Google, cited) against polyrepos.
7. Other models: patch theory (Darcs, Pijul) and commuting patches; CRDT-based version control (callback to Part 39).
8. Build systems:
   - Make (Feldman 1979): the dependency DAG, timestamps and how they lie;
   - topological order (callback to Part 18);
   - parallel builds as a work–span problem (callback to Part 10).
9. **Build systems à la carte** (Mokhov, Mitchell & Peyton Jones 2018):
   - schedulers × rebuilders;
   - static and dynamic dependencies; minimality and correctness;
   - early cutoff;
   - the spreadsheet as a build system.
10. Hermetic, reproducible, remote-cached builds (Bazel, Nix): content hashes as cache keys.
11. Dependencies:
    - semantic versioning;
    - **version resolution is NP-complete** (reduction from 3-SAT, on screen; Di Cosmo et al. 2006);
    - CDCL and PubGrub solvers in practice (callback to Part 26);
    - lockfiles, diamond dependencies, vendoring.
12. Supply-chain hygiene: signatures, SBOMs, SLSA (Part 55 returns to it).
13. Continuous integration: trunk-based development; **merge queues** (the probability that a batch is green, and
    bisection on failure, computed); test selection by dependency graph.
14. Continuous delivery:
    - blue/green and canary deploys, with statistical detection of a bad canary (callback to Part 44);
    - progressive rollout, feature flags, rollback;
    - expand–contract schema migrations.
15. The Job's own pipeline end to end: commit, CI, build cache, canary, rollout. Outro.

*Computed:* our object store against git's hashes; LCAs on synthetic DAGs; bisect step counts; a make-like engine with
early cutoff on a synthetic project (rebuild counts); a version solver on a reduced 3-SAT instance; merge-queue
throughput against batch size and failure rate; canary detection power.
*Visuals:* hashes changing all the way up the DAG when one blob changes; three columns converging in a three-way
merge; the build DAG lighting the minimal rebuild set; the 3-SAT gadget written as package versions.
*In practice:* git workflows, Bazel/Buck/Nix, npm/pip/cargo resolvers, CI/CD pipelines, monorepo tooling, release
engineering.
*Reading:* Chacon & Straub, *Pro Git*; Mokhov, Mitchell & Peyton Jones 2018; Feldman 1979; Dolstra 2006 (the Nix
thesis); Di Cosmo et al. 2006; Humble & Farley, *Continuous Delivery*; Winters, Manshreck & Wright ch. 16–24; Potvin &
Levenberg 2016; Beyer et al., *Site Reliability Engineering* (release engineering).

### Part 42 · The Browser and the Web (~55)
*Story:* Type a URL and press enter. Within a few hundred milliseconds, a dozen protocols and three compilers turn
bytes into pixels you can interact with. The browser is a fault-tolerant parser, a layout constraint solver, a GPU
compositor, a JIT compiler and an operating system for untrusted code. A single event loop holds it together, with
a 16 ms deadline for every frame. We build a toy browser that renders the series' own README.
1. Hook: "what happens when you type a URL", answered layer by layer (callbacks to Parts 30, 36 and 37).
2. History: Berners-Lee (1989–91), Mosaic (1993), JavaScript in ten days (1995), AJAX (2005), the living standard.
3. **HTML parsing**: the tokenizer as a state machine with error recovery (callback to Part 12), and why HTML isn't
   parsed by a grammar; the tree builder; the DOM.
4. CSS: the cascade; specificity as a lexicographic order (a, b, c); right-to-left selector matching, and why;
   inheritance.
5. **Layout**:
   - the box model and normal flow;
   - flexbox as a constrained distribution of space (the grow/shrink algorithm on screen);
   - grid;
   - line breaking: greedy against **Knuth–Plass** dynamic programming (callback to Part 19);
   - incremental relayout.
6. Rendering: paint, layers, GPU compositing (callback to Part 51); the 16.7 ms frame budget; jank;
   `requestAnimationFrame`.
7. **The event loop**: tasks, microtasks and rendering steps; run-to-completion; promises and async/await (callback to
   Part 33); why one long task freezes a page.
8. JavaScript engines: lazy parsing, bytecode, inline caches and hidden classes, the optimizing JIT and
   deoptimization, generational GC (callbacks to Part 15).
9. UI frameworks:
   - the virtual DOM, and why React's O(n) heuristic diff replaces O(n³) tree edit distance (computed);
   - keyed lists;
   - fine-grained reactivity (signals) as a dependency graph (callback to Part 41).
10. Client state: caches, service workers and offline; local-first software and CRDTs (callback to Part 39).
11. Web performance: the critical rendering path; loading priorities; **Core Web Vitals** (LCP, INP, CLS); compression
    and images; HTTP/2 and HTTP/3 in practice (callback to Part 37).
12. The browser security model: same-origin, CORS, CSP; process sandboxing and site isolation (Spectre, callback to
    Part 8); WebAssembly (callback to Part 15).
13. Accessibility: the accessibility tree, ARIA, keyboard navigation; **the WCAG contrast ratio**, derived (Part 44).
14. Mobile and native apps: the UI thread, frame deadlines, battery and radio power states (why batching requests
    saves energy, cited); cross-platform frameworks.
15. Our toy browser: an HTML-subset parser, the cascade, block and inline layout, and Part 51's rasterizer, rendering
    a page of this repository's README. Outro.

*Computed:* the toy browser; specificity orderings; Knuth–Plass against greedy line breaking on a novel's paragraph;
keyed against unkeyed list diffs; event-loop orderings; contrast ratios.
*Visuals:* the tokenizer state machine consuming characters; the DOM and CSSOM merging into the render tree; flex
items growing and shrinking; Knuth–Plass's breakpoint graph with the optimal path; a frame timeline where a long task
causes jank.
*In practice:* frontend and mobile engineering, web performance, accessibility, the engines behind Chrome, Firefox and
Safari, React/Vue/Svelte.
*Reading:* Panchekha & Harrelson, *Web Browser Engineering*; Grigorik, *High Performance Browser Networking*; Garsiel &
Irish, "How Browsers Work"; the WHATWG HTML Living Standard (parsing) and the CSS specifications (cascade, flexbox);
Knuth & Plass 1981; Haverbeke, *Eloquent JavaScript*; Flanagan, *JavaScript: The Definitive Guide*; WCAG 2.2.

### Part 43 · APIs and Services (~55)
*Story:* Once a program is split across machines, every function call becomes a message that can be lost,
duplicated, delayed or reordered (callback to Part 38). Industry's answers have real mathematics underneath:
- compatibility rules for evolving schemas;
- idempotency;
- exactly-once as at-least-once plus deduplication;
- sagas in place of distributed locks;
- backpressure.

We split the Job into services and keep its counts exact while the network loses and duplicates messages.
1. Hook: the eight fallacies of distributed computing, each matched to a real outage.
2. RPC (Birrell & Nelson 1984): stubs and marshalling; why remote is not local (Waldo et al. 1994).
3. Serialization:
   - JSON's numbers (doubles, 2⁵³, callback to Part 4);
   - **Protocol Buffers' wire format**: varints and zigzag, derived; field tags;
   - schema evolution: forward and backward compatibility as a subtyping question (callback to Part 14);
   - Avro; zero-copy formats.
4. API styles:
   - REST (Fielding 2000) and the safety and idempotency of HTTP methods;
   - offset against cursor pagination (why offsets are O(n) and skip rows under inserts, computed);
   - gRPC and streaming;
   - GraphQL, the N + 1 problem and batching.
5. **Idempotency and delivery semantics**: at-most, at-least and exactly once; exactly-once = at-least-once + dedup
   (proved in a model); idempotency keys; the two generals again.
6. API design and versioning: **Hyrum's law**; deprecation; additive changes; consumer-driven contract tests.
7. Queues and pub/sub: acknowledgements, visibility timeouts, dead-letter queues, per-key ordering.
8. Backpressure: bounded queues and load shedding; queueing between services (callback to Part 31).
9. Monolith against microservices: team autonomy against distributed complexity; bounded contexts (DDD); the
   distributed monolith; latency budgets across a call graph (callback to Part 39's tail).
10. Data across services:
    - the dual-write problem;
    - **the transactional outbox** and change data capture (Part 46);
    - **sagas** (Garcia-Molina & Salem 1987) with compensations, animated on an order–payment–shipping flow.
11. Discovery and routing: client-side load balancing, sidecars and service meshes, mTLS (callback to Part 30).
12. Authentication and authorization between services: OAuth 2.0 flows; JWTs and the `alg: none` pitfall; capability
    tokens and macaroons (Part 55).
13. Time in APIs: wall against monotonic clocks, time zones, leap seconds (callback to Part 38).
14. The Job as three services (tokenize, count, rank) on our network with loss and duplication. Its counts stay
    exact with idempotency keys and drift without them (computed). Outro.

*Computed:* varint and zigzag encoders checked against the published encoding examples; a schema-compatibility
checker; pagination anomalies under concurrent inserts; double-count rates with and without idempotency keys; sagas
under injected failures; latency budgets composed over a call graph.
*Visuals:* varint bytes with their continuation bits; a retry storm against idempotent dedup; a saga's forward steps
and compensations; a call graph with latencies accumulating along the critical path.
*In practice:* REST, gRPC and GraphQL APIs; Kafka, RabbitMQ and SQS; payment-grade idempotency; service meshes; OAuth;
backend engineering at any company.
*Reading:* Kleppmann, *Designing Data-Intensive Applications* ch. 4, 11–12; Newman, *Building Microservices*;
Richardson, *Microservices Patterns*; Evans, *Domain-Driven Design*; Hohpe & Woolf, *Enterprise Integration Patterns*;
Fielding 2000; Birrell & Nelson 1984; Waldo et al. 1994; Garcia-Molina & Salem 1987; the Protocol Buffers encoding
documentation; RFC 6749 and RFC 7519; Google's API design guide.

### Part 44 · People and Products (~55)
*Story:* Software is used by people, and both the people and the product can be measured. Fitts's law falls out of
Shannon's channel capacity. Hick's law is the entropy of a choice. Perception has thresholds, and colour has
formulas. Where intuition runs out, industry runs controlled experiments, and an A/B test checked every morning is
among the most common statistical mistakes in the world.
1. Hook: Engelbart's 1968 demo (mouse, hypertext, collaborative editing); Xerox PARC and the GUI.
2. **Fitts's law**, MT = a + b log₂(D/W + 1), derived from channel capacity (MacKenzie's form); why screen edges are
   infinitely deep targets; the steering law.
3. **Hick–Hyman**: decision time grows with the entropy of the choice (callback to *AI, Built* 1).
4. GOMS and the keystroke-level model (Card, Moran & Newell): predicting task time.
5. Perception: the 0.1 s / 1 s / 10 s thresholds; input latency; Weber–Fechner and just-noticeable differences;
   preattentive features.
6. Colour:
   - XYZ, sRGB and gamma; perceptual spaces (CIELAB, OKLab);
   - colour-blindness simulated on the series' own palette;
   - **the WCAG contrast ratio** (L₁ + 0.05)/(L₂ + 0.05), derived from relative luminance.
7. Text on screens: glyph rasterization (callback to Part 51), hinting, readability.
8. Accessibility: assistive technology, the accessibility tree, motor and cognitive accessibility, universal design.
9. Usability evaluation: Nielsen's heuristics; think-aloud studies; "five users find 85%" from 1 − (1 − p)ⁿ (Nielsen &
   Landauer 1993) and its caveats.
10. **Experiments**: the A/B test as a randomized controlled trial; the two-proportion z-test, derived; power and
    sample size (n ≈ 16σ²/δ², derived).
11. **The peeking problem**: checking daily multiplies the false-positive rate (simulated); sequential tests and
    always-valid p-values (Johari et al. 2017) fix it.
12. **CUPED** (Deng et al. 2013): regression on the pre-period cuts variance by (1 − ρ²) (derived); stratification.
13. Pitfalls at scale:
    - multiple testing and false discovery rates;
    - Simpson's paradox; novelty effects;
    - interference in marketplaces and social graphs, and cluster randomization;
    - sample-ratio-mismatch checks (χ²); Twyman's law.
14. Bandits against A/B tests (callback to *AI, Built* 26): regret against clean inference.
15. Metrics and ethics: north-star metrics; Goodhart's law (callback to *AI, Built* 31); dark patterns;
    privacy-preserving analytics. Outro.

*Computed:* Fitts and Hick regressions (on published data, cited, and on simulated pointing); colour conversions,
contrast ratios and colour-blind views of the palette; Nielsen–Landauer curves; power calculations; peeking
simulations; sequential tests; CUPED on synthetic data; SRM detection.
*Visuals:* targets shrinking and moving under the log curve; the sRGB cube sitting inside OKLab; p-value paths
wandering across 0.05 under peeking; a confidence interval shrinking under CUPED.
*In practice:* product engineering, UX research, growth and experimentation platforms, design systems,
accessibility compliance.
*Reading:* Norman, *The Design of Everyday Things*; Card, Moran & Newell, *The Psychology of Human-Computer
Interaction*; Shneiderman et al., *Designing the User Interface*; MacKenzie, *Human-Computer Interaction: An Empirical
Research Perspective*; Krug, *Don't Make Me Think*; Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments*;
Fitts 1954; Hick 1952; Hyman 1953; Nielsen & Landauer 1993; Deng et al. 2013; Johari et al. 2017; WCAG 2.2; Ottosson
2020.

---

## Act IX · Systems at Scale

### Part 45 · The Cloud (~55)
*Story:* A modern application rents its computer by the second, from a building the size of a stadium. Under the
abstraction sit:
- power and cooling budgets;
- virtual machines shrunk to microVMs;
- containers placed by a bin-packing heuristic;
- control loops that reconcile what is with what should be;
- storage that promises eleven nines by scattering erasure-coded fragments across failure domains.

The Job gets a price in dollars.
1. Hook: from owning servers to renting them; McCarthy's utility computing (1961), EC2 and S3 (2006).
2. The warehouse-scale computer: racks, power, cooling; PUE defined (values cited); failure rates at scale (callbacks
   to Parts 34 and 39).
3. Virtualization recap (callback to Part 32) and microVMs (Firecracker 2020): minimal devices, fast boots, isolation
   for serverless.
4. Containers: namespaces and cgroups (callback to Part 32); images as content-addressed layers (callback to Part 41).
5. Orchestration: Borg (Verma et al. 2015) and Kubernetes; declarative desired state and **the reconciliation loop**,
   level- against edge-triggered; etcd and Raft underneath (callback to Part 38).
6. **Scheduling as bin packing**: NP-hard (from partition); first-fit decreasing's 11/9 OPT + 6/9 (Dósa 2007, cited)
   and next-fit's 2 (proved); vector packing over CPU and memory; priorities and preemption; utilization gains
   (cited).
7. **Autoscaling as control**: a proportional controller with delay oscillates or settles (computed); capacity from
   queueing, with Erlang C derived for c servers (callback to Part 31); predictive scaling.
8. Serverless: cold-start distributions; concurrency limits; per-request billing against reserved servers
   (break-even computed from cited, dated list prices).
9. **Object storage**: S3's semantics (strong read-after-write since 2020, cited); durability from erasure coding across
   failure domains (callback to Part 28), with a Markov model of failure and repair and MTTDL derived; block against
   file against object.
10. Cloud networking: VPCs and overlays (encapsulation, callback to Part 36); managed load balancers (Part 48);
    anycast; the cost of egress.
11. Infrastructure as code: a plan is a diff between desired and actual state, applied in topological order (callbacks
    to Parts 18 and 41); drift; immutable infrastructure.
12. Multi-tenancy: noisy neighbours in caches and memory bandwidth (callback to Part 9); performance variability
    (cited); side channels.
13. Regions, zones and failure domains; placement for availability (Part 50); data residency.
14. Cost engineering: on-demand, reserved and spot pricing (spot interruptions with checkpoints, expected cost
    computed); right-sizing. The Job on autoscaled containers, in dollars (at cited, dated prices). Ledger row 16.
15. Energy and carbon: carbon-aware scheduling; the energy footprint of computing (cited). Outro.

*Computed:* a toy reconciler converging; packing heuristics against optimal solutions on small instances; autoscaler
stability with delay; Erlang C capacity; MTTDL for replication against erasure coding; spot against on-demand costs;
the Job's bill.
*Visuals:* a zoom from building to rack to server to VM to container; bins filling; a control loop overshooting and
settling; erasure-coded fragments scattered across racks surviving failures; a reconciliation diff.
*In practice:* AWS, GCP and Azure; Kubernetes; Terraform; Lambda and Firecracker; S3; platform and infrastructure
engineering; cloud cost reviews.
*Reading:* Barroso, Hölzle & Ranganathan, *The Datacenter as a Computer*; Burns, Beda & Hightower, *Kubernetes: Up and
Running*; Morris, *Infrastructure as Code*; Verma et al. 2015; Burns et al. 2016 ("Borg, Omega, and Kubernetes");
Agache et al. 2020; Armbrust et al. 2010; Jonas et al. 2019; Coffman, Garey & Johnson (the bin-packing survey); Dósa
2007; Harchol-Balter (Erlang C).

### Part 46 · Logs, Streams and Warehouses (~55)
*Story:* Every company's data ends up in two places: an append-only log that records everything as it happens, and
a column-oriented warehouse that answers questions about all of it. Between them, stream processors compute answers
continuously. The hard part is time: events arrive late, out of order and more than once. The Job becomes a live
top-twenty over a stream of novels.
1. Hook: "The Log" (Kreps 2013), the log as the unifying abstraction (callbacks to Part 35's WAL and Part 38's Raft
   log).
2. **The partitioned log** (Kafka 2011): segments, offsets, keys and partitions; consumer groups and rebalancing;
   retention and compaction; in-sync replicas (callback to Part 39).
3. Throughput engineering: sequential I/O (callback to Part 34), batching, zero-copy, the page cache.
4. Change data capture (the database's WAL as a stream, callback to Part 35); the outbox (callback to Part 43); event
   sourcing and CQRS, with state as a fold over events.
5. **The dataflow model** (Akidau et al. 2015):
   - event time against processing time;
   - tumbling, sliding and session windows;
   - watermarks and lateness; triggers and accumulation;
   - the event-time/processing-time plot, animated.
6. **Exactly-once state**: keyed state and checkpoints by asynchronous barrier snapshots (Carbone et al. 2015, a
   Chandy–Lamport descendant, callback to Part 38); idempotent and transactional sinks; exactly-once only ever holds
   end to end.
7. Streaming algorithms in production: top-k, distinct counts, quantiles with t-digest and KLL (callback to Part 20);
   windowed stream joins.
8. Lambda against Kappa; streaming as a superset of batch.
9. The warehouse: OLTP against OLAP; star and snowflake schemas; facts, dimensions and slowly changing dimensions.
10. **Columnar files**:
    - Parquet: row groups, column chunks, pages;
    - dictionary, RLE/bit-packing and delta encodings (callbacks to Parts 21 and 28);
    - statistics and predicate pushdown;
    - **Dremel's repetition and definition levels** for nested data, derived on an example.
11. Lakehouses: table formats (Iceberg, Delta) with snapshots, manifests and optimistic commits, giving ACID on object
    storage (callbacks to Parts 35 and 45); time travel.
12. MPP query engines: partitioned execution and shuffles (callback to Part 39); broadcast against shuffle hash joins
    (cost model derived); skew and salting; vectorized execution (callback to Part 35).
13. Data quality: schema evolution (callback to Part 43), data contracts, validation tests, lineage graphs.
14. Approximate and private analytics: sampling with confidence intervals, sketches in SQL, differentially private
    counts.
15. The Job as a stream: novels arriving as events, some late and some duplicated; a continuously updated top-20 with
    event-time windows and exactly-once state. Ledger row 17. Outro.

*Computed:* a partitioned-log simulator with consumer groups; a stream processor with watermarks and late data
(correctness against latency); checkpoint-and-recover with an exactly-once check; a Parquet-style encoder on the
novels' words (sizes by encoding); Dremel levels; join costs; t-digest accuracy.
*Visuals:* the event-time/processing-time plot with its watermark curve; windows sliding; barriers flowing through a
dataflow graph; a Parquet file exploded into row groups and pages; a shuffle with one hot key overloading a worker.
*In practice:* Kafka, Flink, Spark Structured Streaming, Debezium; Snowflake, BigQuery, Redshift; Parquet, Iceberg,
Delta; dbt; data engineering.
*Reading:* Kleppmann ch. 3, 10–12; Akidau, Chernyak & Lax, *Streaming Systems*; Kimball & Ross, *The Data Warehouse
Toolkit*; Kreps 2013; Kreps, Narkhede & Rao 2011; Akidau et al. 2015; Carbone et al. 2015; Melnik et al. 2010; Armbrust
et al. 2020, 2021; Abadi et al. 2013 (the design of column stores); Dunning & Ertl 2019; Karnin, Lang & Liberty 2016.

### Part 47 · Search Engines (~55)
*Story:* How do you find the ten most relevant pages among billions in a fifth of a second? The pieces:
- an inverted index turns search into merging sorted lists;
- compression keeps those lists in memory;
- a probabilistic model of relevance yields BM25;
- a random surfer yields PageRank;
- dense vectors and graph-based nearest-neighbour search now sit beside them.

We build a search engine for the thirty novels.
1. Hook: from Archie (1990) and AltaVista (1995) to Google (1998); the scale of a web index (cited).
2. Tokenizing and normalizing: Porter's stemmer; case folding; stop words. **Zipf's and Heaps' laws** fitted on the
   novels.
3. The inverted index: dictionary and postings; sort-based and single-pass in-memory construction (callback to Part
   16's external sort).
4. Boolean retrieval: merging postings; skip pointers (√n); galloping intersection (callback to Part 24); positional
   indexes for phrases.
5. **Postings compression**: gaps; variable-byte; Elias γ and δ (code lengths derived, callback to *AI, Built* 1);
   Golomb–Rice with its optimal parameter derived; SIMD block codecs (callback to Part 24).
6. **Ranking**: tf–idf and cosine similarity; the probability ranking principle (Robertson 1977); the binary
   independence model up to **BM25**, with its k₁ saturation and b length normalization derived.
7. Evaluation: precision, recall, MAP, **nDCG** (derived); test collections and pooled judgments; significance
   (callback to Part 44).
8. Top-k retrieval: **WAND** and block-max WAND (dynamic pruning with score upper bounds); tiered indexes.
9. Link analysis: PageRank as an eigenvector (callback to Part 18); HITS; link spam.
10. Crawling: the URL frontier, politeness, freshness policies, near-duplicates by SimHash (callback to Part 20).
11. Serving at scale: document- against term-partitioned indexes (callback to Part 39); replicas; fan-out and the tail
    (callback to Part 39); result and postings caches.
12. Spelling and autocomplete: noisy-channel correction with edit distance (callbacks to Parts 19 and 21); BK-trees;
    top-k completion over tries (callback to Part 17).
13. Learning to rank: pointwise, pairwise, listwise; LambdaMART (callback to *AI, Built* 6); click models and position
    bias.
14. Dense retrieval: embeddings (callback to *AI, Built* 24); **product quantization** (Jégou et al. 2011) and **HNSW**
    (Malkov & Yashunin); hybrid lexical-plus-dense retrieval; retrieval for language models (*AI, Built* 15).
15. Our engine for the novels: the index, BM25, phrases, snippets, and an evaluation on a small query set we judge
    ourselves (labelled illustrative). Outro.

*Computed:* Zipf and Heaps fits; index sizes under each code; comparison counts for intersection algorithms; BM25
against tf–idf on our judged set; WAND pruning rates; PageRank on a synthetic web; SimHash near-duplicates; PQ
distortion; HNSW recall against speed.
*Visuals:* postings lists sliding together during intersection; gap codes as bit strings; BM25's saturation curves;
WAND's pivot moving across lists; a random surfer on a graph; HNSW's descent through its layers.
*In practice:* Lucene, Elasticsearch, OpenSearch; web and e-commerce search; vector databases; retrieval-augmented
generation.
*Reading:* Manning, Raghavan & Schütze, *Introduction to Information Retrieval*; Büttcher, Clarke & Cormack,
*Information Retrieval: Implementing and Evaluating Search Engines*; Witten, Moffat & Bell, *Managing Gigabytes*;
Zobel & Moffat 2006; Robertson & Zaragoza 2009; Porter 1980; Brin & Page 1998; Kleinberg 1999; Broder et al. 2003; Ding
& Suel 2011; Charikar 2002; Jégou, Douze & Schmid 2011; Malkov & Yashunin 2018; Burges 2010.

### Part 48 · System Design I: Building Blocks (~55)
*Story:* Designing a large system means choosing and composing a small set of blocks under numbers you can estimate
on a napkin: load balancers, caches, queues, shards, replicas, indexes. Each block has mathematics of its own:
- hashing that rebalances gracefully;
- caches that avoid stampedes;
- rate limiters that are token buckets in disguise;
- IDs that sort by time without coordination;
- space-filling curves that turn maps into keys.
1. Hook: the napkin. Back-of-the-envelope estimation: QPS from daily users and peak factors, storage per year,
   bandwidth; powers of two; the latency numbers (callback to Part 39).
2. The method: functional and non-functional requirements; SLOs (Part 50); the capacity model; the data model; the API
   (callback to Part 43); the high-level design; deep dives; trade-offs; the design doc.
3. **Load balancing**:
   - L4 against L7;
   - round robin, least connections, **power of two choices** (callback to Part 20);
   - consistent hashing and **Maglev hashing** (Eisenbud et al. 2016; disruption computed);
   - health checks and outlier ejection.
4. **Caching I**:
   - where caches sit (client, CDN, proxy, application, database);
   - cache-aside, read-through, write-through, write-back;
   - eviction: LRU, LFU, W-TinyLFU's Count-Min admission (callback to Part 20);
   - hit rate against size on Zipf traffic, with **Che's approximation** derived.
5. **Caching II**: invalidation; TTLs; thundering herds; request coalescing; **probabilistic early expiration**
   (Vattani et al. 2015, derived); leases (memcache at Facebook, Nishtala et al. 2013).
6. **Rate limiting**: token bucket as a (σ, ρ) envelope (derived); leaky bucket; fixed and sliding windows (the
   approximation's error computed); GCRA; distributed limits with approximate counters.
7. Queues and asynchrony (callback to Part 43): absorbing bursts; why latency explodes as utilization nears 1
   (callback to Part 31); priorities; delayed jobs; worker pools.
8. Choosing storage: relational, key–value, document, wide-column, graph, time-series; access patterns decide;
   denormalization; indexes (callback to Part 35).
9. **Sharding** (callback to Part 39): shard keys; hot keys and the celebrity problem; resharding; local against
   global secondary indexes; cross-shard queries.
10. Replication in practice: read replicas and lag; failover; split brain and fencing tokens (callback to Part 39);
    active–active across regions and conflict resolution.
11. **Unique IDs**: UUIDv4 collisions by the birthday bound (callback to Part 17); UUIDv7 and Snowflake IDs; clock skew
    (callback to Part 38); index locality of time-ordered keys (B-trees, callback to Part 17).
12. Blobs and CDNs (callback to Part 45): chunking, content addressing, signed URLs, cache keys at the edge.
13. **Geospatial indexes**: geohash and Morton (Z-order) bit interleaving; quadtrees; S2's Hilbert-curve cells (with
    locality preservation measured); H3 hexagons; nearest-neighbour queries (callback to Part 22).
14. Real-time blocks: WebSockets against long polling; notifications; presence; search as a block (callback to Part
    47).
15. The Job as a service ("upload a book, get its top words"): estimated, designed, then load-tested in simulation,
    with p50 and p99 against QPS, with and without the cache. Outro.

*Computed:* estimation worksheets; two choices against random and round-robin assignment on uneven servers; Maglev
against ring disruption; LRU and TinyLFU hit rates on Zipf traces against Che's approximation; stampedes with and
without early expiration; token-bucket conformance; sliding-window error; ID collision probabilities; Hilbert against
Z-order locality; the Job service's load test.
*Visuals:* a napkin turning into a capacity table; requests flowing through a load balancer into queues; hit-rate
curves; a stampede at expiry, smoothed; a token bucket filling and draining; space-filling curves drawing across a
map.
*In practice:* the system design interview; NGINX, Envoy, HAProxy; Redis and Memcached; CDNs; Snowflake IDs; PostGIS,
S2, H3; backend and infrastructure design reviews.
*Reading:* Kleppmann; Xu, *System Design Interview* vols. 1–2; Burns, *Designing Distributed Systems*; Petrov,
*Database Internals*; Nishtala et al. 2013; Eisenbud et al. 2016; Einziger, Friedman & Manes 2017; Che, Tung & Wang
2002; Vattani, Chierichetti & Lowenstein 2015; Mitzenmacher 2001; Cruz 1991; RFC 9562 (UUIDs); the S2 and H3
documentation.

### Part 49 · System Design II: Case Studies (~60)
*Story:* Eight systems everyone uses, each designed from the napkin up and stress-tested in simulation:
- a URL shortener;
- a news feed;
- a chat service;
- a web crawler;
- a ride-hailing dispatcher;
- a video platform;
- a payment ledger;
- a collaborative editor.

Each turns on one hard idea, and each idea is one the series has already built. The capstone is the Job as a service
at a million books a day.
1. The method and the card of blocks (callback to Part 48).
2. **URL shortener**: the ID space (base62 length for N links, derived); hashing against counters against Snowflake
   IDs; 301 against 302 and their caching; read-heavy Zipf traffic; click analytics as a stream (callback to Part 46).
3. **News feed I**: fan-out on write against fan-out on read, with the cost model derived over a power-law follower
   graph; the celebrity problem; the hybrid (computed on a synthetic graph).
4. **News feed II**: ranking (callback to Part 47); cursor pagination (callback to Part 43); timeline caches;
   read-your-writes (callback to Part 39).
5. **Chat**: connection servers and WebSockets; per-conversation sequence numbers for ordering (callback to Part 38);
   receipts; offline sync; group fan-out; end-to-end encryption with the double ratchet, briefly (callbacks to Parts
   29–30).
6. **Web crawler** (callback to Part 47): the frontier as per-host priority queues; politeness; DNS caching; dedup by
   Bloom filters and SimHash (callback to Part 20); partitioning by host hash; the throughput for a billion pages.
7. **Ride-hailing dispatch**:
   - hexagonal geo-indexes (callback to Part 48);
   - location-update write rates;
   - batched matching as bipartite assignment (callback to Part 18) against greedy matching;
   - ETAs by contraction hierarchies (callback to Part 18);
   - surge pricing as a market.
8. **Video streaming**:
   - encoding ladders and HLS/DASH segments; CDN placement under Zipf popularity (callback to Part 45);
   - **adaptive bitrate as control**: buffer-based (Huang et al. 2014) against MPC (Yin et al. 2015), simulated with
     rebuffering.
9. **Payments**: double-entry bookkeeping as an invariant (Σ = 0, callback to Part 2); idempotency (callback to Part
   43); a payment's state machine; reconciliation with outside processors; why a ledger chooses consistency over
   availability (callback to Part 39).
10. **Collaborative editing**: operational transformation (Ellis & Gibbs 1989) against CRDTs (callback to Part 39);
    cursors and presence; convergence checked on our sequence CRDT.
11. **A Dynamo-style key–value store**, end to end: partitioning, replication, quorums, Merkle-tree anti-entropy
    (callback to Part 29), hinted handoff, simulated under failures (callbacks to Parts 38–39).
12. **A metrics pipeline**: high-cardinality time series, downsampling, retention tiers (Part 50 uses it).
13. **The Job at a million books a day**: p99, cost and cache hit rates from the simulated load test. Ledger row 18.
14. How designs fail, from post-mortems; a checklist of trade-offs (consistency, latency, cost, complexity,
    operability). Outro.

*Computed:* base62 sizing; fan-out costs on a power-law graph; ordering anomalies with and without sequence numbers;
crawler throughput and dedup accuracy; greedy against optimal dispatch; ABR simulations (rebuffer ratio against mean
bitrate); ledger invariants under concurrent retries; CRDT convergence; the key–value store under failures; the Job
service at scale.
*Visuals:* each architecture built block by block, with requests flowing through it as packets; the follower graph's
celebrities as giant nodes; an ABR buffer trace with bitrate steps; a double-entry ledger balancing; hexagons over a
city.
*In practice:* the system design interview canon, and how large consumer products are actually built.
*Reading:* Xu, *System Design Interview* vols. 1–2; Kleppmann; Burns, *Designing Distributed Systems*; DeCandia et al.
2007; Silberstein et al. 2010; Huang et al. 2014; Yin et al. 2015; Perrin & Marlinspike 2016; Ellis & Gibbs 1989;
Heydon & Najork 1999; published engineering write-ups (cited where used).

### Part 50 · Keeping It Running (~60)
*Story:* A system is only as good as its worst hour, and reliability engineering turns that into mathematics:
- availability composes in series and in parallel;
- an error budget turns reliability into a resource to spend;
- retries melt a system unless they back off with jitter;
- an overload can outlast its cause.

Observability (metrics, logs, traces, profiles) is how you find out what happened. Performance engineering is the
same discipline aimed at speed.
1. Hook: three post-mortems (the 2017 S3 typo, the 2019 regex, the 2024 endpoint update, all cited), each a lesson.
2. **Availability arithmetic**:
   - nines as downtime budgets;
   - series ∏Aᵢ against parallel 1 − ∏(1 − Aᵢ), derived and drawn as Part 3's switch circuits;
   - A = MTBF/(MTBF + MTTR);
   - correlated failures break the independence assumption.
3. SLIs, SLOs and SLAs; **error budgets**; multiwindow burn-rate alerts (thresholds derived).
4. Failure modes: fail-stop against gray failure; cascading failures; **metastable failures** (Bronson et al. 2021;
   Huang et al. 2022), where a retry-amplified overload persists after its trigger (simulated).
5. **Timeouts, retries, backoff and jitter** (full, equal and decorrelated jitter compared; Brooker 2015); retry
   budgets; hedged requests (callback to Part 39).
6. Circuit breakers, bulkheads, load shedding and admission control (CoDel for services, callback to Part 37);
   graceful degradation; backpressure (callback to Part 43).
7. Redundancy: N + 1 and N + 2; active–passive against active–active; regional evacuation; a Raft group's
   availability (callback to Part 38).
8. **Metrics**: counters, gauges, histograms; why averages lie; quantile sketches (HDR histograms; **DDSketch** and its
   relative-error guarantee, derived; callback to Part 46); cardinality.
9. **Traces**: structured logs; distributed tracing (Dapper 2010) with spans and context propagation; head against
   tail sampling; critical-path analysis of a trace (callback to Part 19's DAGs).
10. **Coordinated omission**: how load generators under-report tail latency (measured against true p99 in simulation);
    open against closed load (Schroeder et al. 2006).
11. **Profiling**:
    - sampling profilers and the binomial error of a sample count;
    - **flame graphs** (Gregg), built from a profile of our own Pebble emulator running the Job;
    - off-CPU time; eBPF (callback to Part 31).
12. Performance method: USE and RED; the roofline again (callback to Part 9 and *AI, Built* 17); capacity planning with
    queueing (callbacks to Parts 31 and 45); catching performance regressions in CI by change-point detection.
13. Incidents: on-call, incident command, communication; blameless post-mortems; the Swiss-cheese model; Cook's "How
    Complex Systems Fail".
14. **Chaos engineering** (Chaos Monkey 2011; Basiri et al. 2016): hypotheses and blast radius; fault injection on our
    Job service and Raft cluster.
15. The Job service under crashes, partitions and slow nodes, with its availability and SLO burn measured. Ledger row
    19. Outro.

*Computed:* availability compositions; burn-rate alerts on synthetic error streams; a metastable retry storm; backoff
contention with and without jitter; circuit-breaker dynamics; sketch errors; trace-sampling coverage; coordinated
omission; a flame graph of the emulator; capacity plans; chaos experiments on our services.
*Visuals:* availability as series and parallel circuits; an error budget draining; a metastable loop stuck in its bad
state; backoff timelines with and without jitter; a flame graph; a trace waterfall with its critical path lit.
*In practice:* SRE and on-call; Prometheus, Grafana, OpenTelemetry; load testing; performance engineering; incident
management.
*Reading:* Beyer, Jones, Petoff & Murphy, *Site Reliability Engineering*, and *The Site Reliability Workbook*; Nygard,
*Release It!*; Gregg, *Systems Performance* (2nd ed.) and *BPF Performance Tools*; Jain, *The Art of Computer Systems
Performance Analysis*; Harchol-Balter; Sigelman et al. 2010; Masson, Rim & Lee 2019; Bronson et al. 2021; Huang et al.
2022; Brooker 2015; Schroeder, Wierman & Harchol-Balter 2006; Cook 1998; Basiri et al. 2016.

---

## Act X · Horizons and Trust

### Part 51 · Light and Pixels (~60)
*Story:* A picture is millions of samples of light. Projecting triangles onto a screen is linear algebra plus one
division, and getting the samples right is Nyquist again. The physics of light comes down to one integral
equation, which Monte Carlo solves one bounced path at a time. Our path tracer renders the series' own scene, and
its noise falls as 1/√N.
1. Sketchpad (Sutherland 1963) to framebuffers; "a pixel is not a little square" (Smith 1995).
2. Transforms: homogeneous coordinates make translation linear; composition order; Euler angles and gimbal lock,
   quaternions and slerp (3D).
3. **Perspective projection** derived from similar triangles; the frustum squashed into the cube; NDC; the depth
   nonlinearity and z-fighting.
4. Rasterization: edge functions (Part 22's orientation test); barycentrics; **perspective-correct interpolation
   (why 1/w)**; the z-buffer (Catmull 1974). Our rasterizer.
5. Shading: Lambert's cosine law; Phong and Blinn–Phong; Gouraud against Phong.
6. Textures and **sampling**: moiré as aliasing (Nyquist, callback to Part 36); mipmaps (Williams 1983); trilinear
   and anisotropic filtering; supersampling and MSAA.
7. The GPU pipeline: vertex and fragment shaders (callback to *AI, Built* 17).
8. Ray tracing (Whitted 1980): ray–sphere and **Möller–Trumbore** intersection derived; shadows; Snell and
   Fresnel–Schlick.
9. Acceleration: BVHs with the surface-area heuristic (callback to Part 22); O(log n) per ray.
10. Radiometry: solid angle, radiance, irradiance; BRDFs (reciprocity, energy conservation); microfacets
    (Cook–Torrance, GGX).
11. **The rendering equation** (Kajiya 1986) as energy balance; its Neumann series as paths of light, summed bounce
    by bounce on screen.
12. **Path tracing**: the estimator; cosine-weighted importance sampling; Russian roulette (unbiased, proved);
    next-event estimation; **multiple importance sampling** (Veach 1997).
13. Our path tracer renders the series' scene; variance against samples; denoising.
14. Radiosity and photon mapping; real time (RTX, ReSTIR); neural rendering (callback to *AI, Built* 22).
15. Curves: **Bézier and de Casteljau**; B-splines; Catmull–Clark subdivision (*Geri's Game*); fonts as Béziers,
    including the text on this screen. Outro.

*Computed:* rasterizer and path-tracer images at increasing sample counts; variance curves; importance-sampling
gains; BVH traversal counts; mipmap comparisons; slerp against Euler paths.
*Visuals:* the frustum folding into the cube; barycentric color blends; rays bouncing in our scene; the bounce-by-
bounce Neumann sum; de Casteljau's construction.
*In practice:* game engines (Unreal, Unity), GPU pipelines (Vulkan, Metal, WebGPU), film rendering, UI rendering.
*Reading:* Pharr, Jakob & Humphreys, *Physically Based Rendering* (4th ed.); Marschner & Shirley, *Fundamentals of
Computer Graphics*; Akenine-Möller et al., *Real-Time Rendering*; Hughes et al., *Computer Graphics: Principles and
Practice*; Farin, *Curves and Surfaces for CAGD*; Kajiya 1986; Veach 1997; Whitted 1980; Cook & Torrance 1982; Catmull
1974; Sutherland 1963.

### Part 52 · Computing with Real Numbers (~55)
*Story:* In 2000 a journal named the ten algorithms that most shaped science and engineering in the 20th century.
Most of them are numerical. The organizing question is the one Part 4 left open: with rounding everywhere, which
answers can we trust? The answer separates the problem's conditioning from the algorithm's stability, and it
produced a set of algorithms that are stable, fast, and almost magical.
1. Conditioning: condition numbers for f(x) and for Ax = b (κ = ‖A‖‖A⁻¹‖), derived; stability.
2. **Backward error analysis** (Wilkinson): forward error ≤ κ × backward error.
3. Gaussian elimination as LU (2n³/3 flops); failure without pivoting on [[ε, 1], [1, 1]] (computed); partial
   pivoting, with a growth factor of 2ⁿ⁻¹ in the worst case and benign growth on average (Trefethen & Schreiber);
   Cholesky.
4. Least squares: normal equations square κ; **Householder QR** (mirrors animated) and Givens rotations; classical
   against modified Gram–Schmidt (loss of orthogonality computed).
5. The SVD as the tool of last resort (callback to *AI, Built* 3); rank and regularization.
6. Eigenvalues: Abel–Ruffini, so iteration is the only way; inverse iteration; **the QR algorithm** (Francis 1961)
   with Hessenberg reduction, shifts, deflation and its final cubic convergence (computed).
7. Krylov methods: **conjugate gradient** (Hestenes & Stiefel 1952) as optimization over Krylov spaces; the rate
   ((√κ − 1)/(√κ + 1))ᵏ; preconditioning; GMRES.
8. Sparse matrices: CSR, fill-in, orderings (minimum degree, nested dissection); the Poisson problem.
9. **Multigrid**: smoothing kills high frequencies and coarse grids handle the low ones, an O(n) solver (the error
   spectrum animated).
10. Root finding: bisection, secant, Newton, and **Newton's fractal** for z³ − 1 (computed, zoomed).
11. Approximation: Runge's phenomenon; Chebyshev points; barycentric interpolation; the Chebfun idea (Trefethen).
12. Quadrature: Gauss, adaptive, Monte Carlo.
13. ODEs: RK and step control; **stiffness** and A-stability; symplectic integrators conserve energy (leapfrog
    against RK4 over long orbits, computed).
14. Speed: BLAS levels 1, 2 and 3 and arithmetic intensity (callbacks to Part 9 and *AI, Built* 17); LAPACK;
    mixed-precision iterative refinement; HPL and the Top500. Outro.

*Computed:* pivoting failures; growth factors; orthogonality loss; QR-algorithm convergence; CG against steepest
descent; multigrid; the Newton fractal; Runge against Chebyshev; stiffness; orbit drift; BLAS timings on this
machine.
*Visuals:* Householder mirrors; subdiagonal entries fading under QR; the fractal zoom; the multigrid spectrum;
drifting orbits.
*In practice:* NumPy, SciPy and LAPACK; simulation and scientific computing; numerics in finance, engineering and ML training.
*Reading:* Trefethen & Bau, *Numerical Linear Algebra*; Golub & Van Loan, *Matrix Computations*; Higham; Demmel,
*Applied Numerical Linear Algebra*; Saad, *Iterative Methods for Sparse Linear Systems*; Briggs, Henson & McCormick, *A
Multigrid Tutorial*; Trefethen, *Approximation Theory and Approximation Practice*; Hairer, Lubich & Wanner, *Geometric
Numerical Integration*; Wilkinson, *The Algebraic Eigenvalue Problem*; Dongarra & Sullivan 2000.

### Part 53 · Quantum Computation (~60)
*Story:* Feynman asked whether a classical computer can simulate quantum physics efficiently, and suspected it
can't. A computer made of quantum parts interferes over 2ⁿ amplitudes at once. Shor used that to factor and break
Part 30's cryptography. Grover's √N is all it does for general search. Error correction, once thought impossible,
crossed its threshold in 2024. This is the one serious challenge to the extended Church–Turing thesis of Part 1.
1. Landauer (kT ln 2 per erased bit) and Bennett: reversible computation; Toffoli and Fredkin; compute, copy,
   uncompute.
2. Feynman (1982) and Deutsch (1985).
3. The qubit: amplitudes, the Born rule, the **Bloch sphere** (3D). The physics is in *Quantum Mechanics,
   Visualized*.
4. Gates as unitaries rotating the Bloch sphere; tensor products and 2ⁿ amplitudes; CNOT; Bell states and the CHSH
   game (cos²(π/8) ≈ 0.854 against the classical 3/4; callback to Part 27's MIP* = RE); **no-cloning** in three lines.
5. Circuits and universality (H, T, CNOT; Solovay–Kitaev); our state-vector simulator.
6. Interference as the resource: Deutsch, Deutsch–Jozsa, phase kickback.
7. Bernstein–Vazirani; **Simon's problem**, an oracle separation and the seed of Shor.
8. **The QFT** derived from the FFT's butterfly (callback to Part 19), with O(n²) gates for 2ⁿ points.
9. Phase estimation.
10. **Shor** (1994): order finding (Part 30's number theory), the QFT, continued fractions. Our simulator factors 15
    and 21, and the amplitude spikes at multiples of 2ⁿ/r are animated.
11. **Grover** (1996): two reflections make a rotation by 2θ; √N iterations; overshoot; optimality (BBBV 1997,
    sketched); amplitude amplification.
12. BQP's place (BPP ⊆ BQP ⊆ PP ⊆ PSPACE); no known speedup for NP-complete problems beyond Grover's; the extended
    Church–Turing thesis; supremacy claims and the classical replies (cited, carefully).
13. **Quantum error correction**: why it seemed impossible; the 3-qubit code and syndromes; Shor's 9-qubit code;
    stabilizers (Gottesman); **the surface code and the threshold** (callback to Part 28); below threshold (Google
    2024, cited) **(verify)**.
14. Simulation and chemistry; BB84 (an eavesdropper shows up as a 25% error rate); resource estimates for RSA-2048
    (Gidney 2025) **(verify)**. Outro.

*Computed:* the simulator; Bloch trajectories; Deutsch–Jozsa, BV and Simon runs; QFT against FFT; Shor on 15 and 21;
Grover's success probability against iterations; logical against physical error rates for the repetition code;
BB84.
*Visuals:* gates rotating the Bloch sphere; amplitude bars colored by phase, interfering; Grover's rotation in the
plane; Shor's peaks; a surface-code lattice lighting its syndromes.
*In practice:* quantum SDKs (Qiskit, Cirq), post-quantum migration planning, the honest state of the hardware.
*Reading:* Nielsen & Chuang, *Quantum Computation and Quantum Information*; Mermin, *Quantum Computer Science*;
Aaronson, *Quantum Computing Since Democritus*; Kitaev, Shen & Vyalyi; de Wolf's lecture notes; Preskill's Ph219
notes; Watrous, *The Theory of Quantum Information*; Feynman 1982; Deutsch 1985; Shor 1997; Grover 1996; Bennett et
al. 1997; Gottesman 1997; Fowler et al. 2012; Bennett & Brassard 1984; Landauer 1961; Bennett 1973.

### Part 54 · Proving Programs Correct (~55)
*Story:* Testing can show that bugs are present but never that they are absent, and Rice's theorem rules out
deciding correctness in general. We prove programs correct anyway: by writing the invariants ourselves, by
exhausting finite state spaces symbolically, or by approximating soundly. Verified compilers and kernels exist, and
so do the proof assistants that check their proofs.
1. The cost of bugs (Ariane 5, Therac-25, Heartbleed, cited); Dijkstra's dictum; Rice (Part 25) and the three ways
   around it.
2. Specifications; Turing's "Checking a Large Routine" (1949), the first program proof.
3. **Floyd–Hoare logic** (1967, 1969): triples and the rules (assignment by backward substitution, sequence,
   conditionals, while with its invariant); soundness and relative completeness (Cook 1978).
4. Binary search proved: the invariant, and Bloch's 2006 overflow bug; total correctness by variants and
   well-founded orders.
5. **Weakest preconditions** (Dijkstra 1975); VC generation; our VCs checked by our SAT solver (Part 26), or by z3 if
   it is installed.
6. **Separation logic** (Reynolds, O'Hearn): the frame rule; in-place list reversal proved; Infer at scale.
7. **Model checking** (Clarke, Emerson, Sifakis; the 2007 Turing Award):
   - Kripke structures; LTL and CTL over computation trees;
   - state explosion;
   - **symbolic model checking with BDDs** (callback to Part 3) and bounded model checking with SAT;
   - Peterson (Part 33) and Raft-lite (Part 38) checked.
8. **Abstract interpretation** (Cousot & Cousot 1977): Galois connections; intervals and widening, the fixpoint
   converging; Astrée on Airbus flight software (cited).
9. Types as lightweight proofs (callback to Part 14); refinement types.
10. **Proof assistants**: the LCF trusted kernel (Milner 1972); Rocq, Isabelle, Lean; a proof on screen; the
    four-color theorem, Flyspeck, the Liquid Tensor Experiment, mathlib (callback to *AI, Built* 25).
11. Verified systems: **CompCert** (Leroy; Csmith found no wrong-code bugs in its verified parts), **seL4** (2009,
    about 9k lines of C and 200k lines of proof), verified cryptography (HACL*, Fiat-Crypto), CakeML.
12. **TLA+** (Lamport): systems as state machines; an invariant checked on a protocol (Part 38); refinement.
13. Testing as science: coverage; mutation testing; property-based testing (QuickCheck 2000) with shrinking;
    coverage-guided fuzzing (Miller 1990; AFL); symbolic and concolic execution (KLEE); differential testing (Csmith).
    **Our fuzzer finds a bug planted in the Pebble compiler.**
14. Translation validation of our compiler on the Job's code; proof-carrying code (Necula 1997). Outro.

*Computed:* VCs generated and discharged for several programs; the binary-search overflow found; LTL checks of
Peterson and the dining philosophers; BDD reachability sizes; interval analysis with widening; an LCF-style kernel
for natural deduction; property tests and fuzzing of the Pebble toolchain.
*Visuals:* assertions flowing backward through code; computation trees with CTL paths lit; the interval lattice's
widening jumps; the small trusted kernel inside a large system.
*In practice:* TLA+ at AWS and Azure, static analyzers (Infer, CodeQL), fuzzing in CI (OSS-Fuzz), property-based testing, verified cryptography in browsers.
*Reading:* Huth & Ryan, *Logic in Computer Science*; Baier & Katoen, *Principles of Model Checking*; Clarke, Grumberg,
Kroening, Peled & Veith, *Model Checking*; Nipkow & Klein, *Concrete Semantics*; Pierce et al., *Software
Foundations*; Bradley & Manna, *The Calculus of Computation*; Kroening & Strichman, *Decision Procedures*; Dijkstra, *A
Discipline of Programming*; Gries, *The Science of Programming*; Lamport, *Specifying Systems*; Møller & Schwartzbach,
*Static Program Analysis*; Rival & Yi; Zeller et al., *The Fuzzing Book*; Hoare 1969; Floyd 1967; Cousot & Cousot
1977; Reynolds 2002; Leroy 2009; Klein et al. 2009; Claessen & Hughes 2000; Newcombe et al. 2015.

### Part 55 · Trusting Trust (~60; the finale)
*Story:* Security is a property of the whole tower, and every layer leaks: buffers overflow, speculation leaves
traces, DRAM rows disturb their neighbours, parsers confuse code with data. In 1984 Ken Thompson showed that even a
compiler you built yourself can hide a backdoor that its source never shows. We build his attack against our own
compiler, then catch it, and close the series by walking the tower from a NAND gate to a cluster.
1. Threat models; Saltzer & Schroeder's principles (1975).
2. Memory corruption revisited (Part 11):
   - the stack smash on Pebble;
   - canaries, W^X, ASLR (its entropy computed);
   - **return-oriented programming** (Shacham 2007), a Turing-complete chain of gadgets in our own binary;
   - CFI; CHERI.
3. Memory safety: the ~70% statistic (cited); Rust's ownership as affine types (callback to Part 14); what the borrow
   checker proves; RustBelt.
4. Hardware: Rowhammer (Part 5), Spectre and Meltdown (Part 8) and what the mitigations cost; side channels (Part
   27).
5. Authentication: password entropy and guessing; salted slow hashes (Part 29); TOTP as an HMAC over time; passkeys
   (Part 30). **Needham–Schroeder (1978) and Lowe's 1995 attack, found by our model checker** (callback to Part 54).
6. Access control: Lampson's matrix; ACLs against capabilities (the confused deputy); Bell–LaPadula; **safety is
   undecidable in the HRU model (1976)** (callback to Part 25).
7. Isolation: processes and paging (Part 32); sandboxes, site isolation, WebAssembly (Part 15); enclaves and their
   breaks.
8. The web: same origin; XSS and CSRF; **SQL injection on our own database**, fixed by parameterized queries, a parsing
   fix (callback to Part 12); PKI failures (DigiNotar).
9. Networks: amplification DDoS, BGP hijacks (Part 36), DNS (Part 37).
10. Supply chains: dependency confusion; **the xz-utils backdoor** (2024), and how a 500 ms slowdown exposed it (cited).
11. **Reflections on Trusting Trust** (Thompson 1984), built on our compiler (Part 13) with Part 25's quine trick:
    - a backdoor in `login`;
    - a compiler that inserts it when it compiles `login`;
    - and inserts itself when it compiles a compiler;
    - remove the source, and the binary keeps both.
12. **Diverse double-compiling** (Wheeler 2009) catches it, using our independent Python reference compiler.
    Reproducible builds; bootstrapping from a tiny seed (cited).
13. **The tower revisited**: the Job end to end, from NAND to cluster; the final ledger (row 20); what each layer hides
    and what leaks through.
14. Open problems across the series (Part 61 returns to them at research depth):
    - P vs NP, and whether one-way functions exist;
    - ω = 2?;
    - BB(6);
    - dynamic optimality; the UGC;
    - practical quantum advantage; verified software at scale;
    - the bridge to *AI, Built*.
15. The pebble again: Hilbert's question, and everything it led to. Outro: the series map, the problems, the final
    reading list.

*Computed:* the stack smash and ROP chain on Pebble, with and without defenses; ASLR entropy; a tiny borrow checker;
TOTP; Lowe's attack found by model checking; an HRU example; SQL injection and its fix; the trojan compiler built and
caught by DDC; the final ledger.
*Visuals:* ROP gadgets as a train of return addresses; the trojan compiler reproducing itself in a loop; **the whole
tower lit end to end, the camera rising from a NAND gate to the cluster**; the final ledger.
*In practice:* application security reviews, migrations to memory-safe languages, supply-chain security (SLSA, reproducible builds), incident response to a compromise.
*Reading:* Anderson, *Security Engineering* (3rd ed.); Bishop, *Computer Security: Art and Science*; Erickson,
*Hacking: The Art of Exploitation*; Szekeres et al. 2013 (SoK: eternal war in memory); Saltzer & Schroeder 1975;
Thompson 1984; Wheeler 2009; Shacham 2007; Abadi et al. 2005; Lampson 1974; Harrison, Ruzzo & Ullman 1976; Lowe 1996;
Kocher et al. 2019; Jung et al. 2018.

## Act XI · The Research Frontier

The degree ends at Part 55. Act XI is the first year of a PhD: the graduate breadth a qualifying exam expects, each
part built, like the rest of the series, on Pebble and the Job. It assumes the whole degree, and every part ends on
problems that are open.

### Part 56 · Spectral Graphs and Expanders (~60)
*Story:* A graph's adjacency matrix has eigenvalues, and they know things the graph's drawing hides: how fast a
random walk forgets where it started, how hard the graph is to cut, how well it spreads information. Graphs that are
sparse yet impossible to cut, expanders, turn out to be everywhere in theory, from error-correcting codes to
derandomization, and their linear algebra became, in 2022, the route to a max-flow algorithm in almost-linear time.
1. The Laplacian L = D − A; quadratic forms xᵀLx as energy; λ₂ and connectivity.
2. The Courant–Fischer theorem; Rayleigh quotients; why the second eigenvector partitions a graph (spectral
   clustering, Fiedler 1973).
3. **Cheeger's inequality**, both directions, proved on screen; the sweep cut.
4. Random walks: stationary distributions, mixing time from the spectral gap; the lazy walk; PageRank revisited (Part
   18).
5. Expanders: definitions (edge, vertex, spectral); the expander mixing lemma; Ramanujan graphs and the Alon–Boppana
   bound; existence by the probabilistic method (Part 2).
6. Explicit constructions: Margulis–Gabber–Galil; the **zig-zag product** (Reingold, Vadhan & Wigderson 2000);
   Reingold's SL = L (2005).
7. Expanders at work: expander codes (Sipser & Spielman), randomness-efficient sampling, the PCP theorem's gap
   amplification (Dinur 2006, callback to Part 27).
8. Electrical networks: effective resistance, the Laplacian as a circuit (Part 3's physics), commute times.
9. Laplacian solvers: spectral sparsification (Spielman & Srivastava), the Spielman–Teng near-linear solver (2004),
   preconditioning with low-stretch trees.
10. Electrical flows to max-flow: Christiano et al. (2011), interior-point methods; **Chen, Kyng, Liu, Peng,
    Probst Gutenberg & Sachdeva (2022)**, almost-linear max-flow (verify).
11. Frontier: high-dimensional expanders; spectral independence and the resolution of sampling conjectures; open
    problems.
12. Outro.

*Computed:* spectra of the series' graphs (the novels' word co-occurrence graph, the city grid of Part 18, the
internet of Part 36); a spectral partition against the true communities; mixing times measured against the
spectral-gap bound; Cheeger's inequality checked on random graphs; a zig-zag expander built and its λ₂ measured; a
Laplacian solved by CG with and without a sparsifier.
*Visuals:* eigenvectors drawn as vertex colours; the sweep cut moving through the Fiedler order; a random walk's
distribution flattening; the zig-zag product as a step, a cloud move, a step.
*In practice:* spectral clustering, graph partitioning for sharding (METIS), graph neural networks' spectral roots,
expander-based network topologies (Jellyfish, Xpander).
*Reading:* Spielman, *Spectral and Algebraic Graph Theory*; Hoory, Linial & Wigderson 2006 (survey); Chung,
*Spectral Graph Theory*; Vadhan, *Pseudorandomness*; Reingold, Vadhan & Wigderson 2000; Reingold 2005; Spielman & Teng
2004; Chen et al. 2022.

### Part 57 · Learning Theory (~60)
*Story:* *AI, Built* showed machines that learn. This part asks when learning is possible at all: how many examples
a learner needs, why a model with more parameters than data can still generalize, and what it means to learn while an
adversary picks the examples. The answers are theorems, and some of them are about the branch predictors of Part 7.
1. The PAC model (Valiant 1984); realizable and agnostic learning; the finite-class bound from the union bound.
2. **VC dimension**; Sauer–Shelah, proved; the fundamental theorem of PAC learning, both directions.
3. Rademacher complexity and margin bounds; why the perceptron's mistake bound (Novikoff 1962) depends on the margin,
   not the dimension (callback to Part 7).
4. Boosting: weak to strong learning (Schapire 1990); AdaBoost as a zero-sum game; multiplicative weights again
   (Part 23).
5. Online learning: the halving algorithm, the mistake-bound model, Littlestone dimension; regret and the experts
   problem; online gradient descent; online-to-batch conversion.
6. Bandits: explore and exploit; UCB, Thompson sampling; the Lai–Robbins lower bound (callback to Part 44's
   experiments).
7. The limits of learning: cryptographic hardness of learning (Kearns & Valiant); statistical-query lower bounds and
   parity (callback to Part 7's parity branch).
8. Generalization in the overparameterized regime: double descent, implicit bias of gradient descent, benign
   overfitting (callbacks to *AI, Built*).
9. Learning and compression: Occam's razor bounds, sample compression schemes, MDL (callback to Part 21).
10. Frontier: the sample-compression conjecture (compression schemes of size O(d)? Moran & Yehudayoff 2016 gave
    size exponential in d) **(verify)**; learning theory of transformers and in-context learning; open problems.
11. Outro.

*Computed:* VC bounds against measured learning curves; shattering animated; AdaBoost's margins over rounds; regret
curves for Hedge, UCB and Thompson sampling against their bounds; the perceptron's mistakes against Novikoff's bound
on Part 7's branch traces; SQ hardness of parity, measured as learning time.
*Visuals:* the shattering of point sets by half-planes; the boosting distribution re-weighting points; regret
curves bending under √T.
*In practice:* model selection and validation, online recommendation, bandit-based experimentation, ad auctions.
*Reading:* Shalev-Shwartz & Ben-David, *Understanding Machine Learning*; Mohri, Rostamizadeh & Talwalkar,
*Foundations of Machine Learning*; Kearns & Vazirani; Cesa-Bianchi & Lugosi, *Prediction, Learning, and Games*;
Lattimore & Szepesvári, *Bandit Algorithms*; Valiant 1984; Littlestone 1988; Freund & Schapire 1997; Belkin et al.
2019.

### Part 58 · Semantics (~60)
*Story:* What does a program mean? Part 14 gave types; this part gives meaning itself three ways: as steps a
machine takes, as a mathematical object a program denotes, and as the laws it obeys. Scott's answer for recursion,
fixed points of continuous functions, is the same lattice idea as Part 13's dataflow analysis; and a theorem about
all programs of a type, parametricity, writes code's properties for free.
1. Operational semantics: small-step and big-step for a language with recursion; determinism; the CEK machine
   (callback to Part 15).
2. Denotational semantics: what a program denotes; compositionality; recursion as a least fixed point.
3. **Domain theory**: complete partial orders, continuity, Kleene's fixed-point theorem (callback to Part 13's
   lattices); Scott's D∞ model of the untyped λ-calculus (1969).
4. Adequacy and full abstraction; Plotkin's PCF and parallel-or (1977); game semantics' answer (1990s).
5. Program equivalence: contextual equivalence; bisimulation; **logical relations**, and normalization of the
   simply typed λ-calculus proved with them (Tait).
6. **Parametricity**: Reynolds (1983), Wadler's *Theorems for free!* (1989), derived for map and sort.
7. Axiomatic semantics revisited (Part 54): Hoare logic proved sound against the operational semantics.
8. Effects: monads (Moggi 1991), algebraic effects and handlers; state, exceptions, nondeterminism as monads.
9. Dependent types: Martin-Löf type theory, propositions as types extended (Part 14); a proof assistant's kernel.
10. Concurrency semantics: CCS and the π-calculus; session types (callback to Part 43).
11. Frontier: mechanized semantics of real languages (CompCert's C, CakeML, WebAssembly); homotopy type theory;
    open problems.
12. Outro.

*Computed:* a small-step interpreter, a big-step interpreter and a CEK machine for the same language, agreeing on
random programs; Kleene iterates of a recursive definition converging; normalization by evaluation; free theorems
checked by property tests; bisimulation checked by our model checker (Part 54).
*Visuals:* the Kleene chain rising through a cpo; logical relations as a ladder of types; a bisimulation game
played between two transition systems.
*In practice:* language design and specification (WebAssembly's formal spec), compilers' correctness arguments,
refactoring tools, effect systems in modern languages.
*Reading:* Winskel, *The Formal Semantics of Programming Languages*; Harper, *Practical Foundations for Programming
Languages*; Pierce et al., *Software Foundations*; Scott 1970; Plotkin 1977; Reynolds 1983; Wadler 1989; Moggi 1991;
Milner, *Communicating and Mobile Systems*.

### Part 59 · Distributed Computing Theory (~60)
*Story:* Part 38 proved that consensus is impossible in one model and built Raft in another. This part is the
theory underneath: what n processes can and cannot compute when they see only their neighbours, or crash, or lie.
Some answers are lower bounds as sharp as log* n; one of them came from algebraic topology.
1. Models: synchronous and asynchronous; message passing and shared memory; crash, omission and Byzantine faults.
2. The LOCAL model: what a node knows after t rounds; **Cole–Vishkin's 3-colouring of a ring in O(log* n)**, run.
3. **Linial's lower bound** (1992): no o(log* n) algorithm; round elimination (Brandt 2019) as a proof machine.
4. Synchronous consensus: the f + 1 round lower bound; the n > 3f bound for Byzantine agreement, proved by the
   hexagon argument; authenticated agreement (Dolev–Strong).
5. Asynchronous impossibility: FLP revisited (Part 38) as a valency argument; randomized consensus (Ben-Or 1983).
6. Shared memory: registers, the consensus hierarchy (Herlihy 1991, callback to Part 33); universality.
7. **Topology**: k-set agreement is impossible (Herlihy & Shavit; Borowsky & Gafni; Saks & Zaharoglou, 1993), via
   Sperner's lemma; the asynchronous computability theorem.
8. Failure detectors (Chandra & Toueg 1996); Ω as the weakest for consensus.
9. Lower bounds in communication: the cost of Byzantine agreement (Dolev–Reischuk); recent quadratic bounds.
10. Population protocols and the theory of chemical computation.
11. Frontier: the complexity theory of locality (LCL classification); distributed graph algorithms (CONGEST); open
    problems.
12. Outro.

*Computed:* Cole–Vishkin on rings of 10⁶ nodes, rounds against log* n; round elimination steps for sinkless
orientation; the hexagon counterexample run; Ben-Or's expected rounds; Sperner colourings of subdivided triangles
checked; a population protocol computing majority.
*Visuals:* colours collapsing round by round on a ring; the hexagon of processes fooling a Byzantine protocol; a
simplex subdivided, its Sperner triangle found.
*In practice:* the guarantees behind consensus libraries, blockchains' Byzantine assumptions, gossip protocols,
self-stabilizing network protocols.
*Reading:* Lynch, *Distributed Algorithms*; Attiya & Welch, *Distributed Computing*; Herlihy, Kozlov & Rajsbaum,
*Distributed Computing through Combinatorial Topology*; Peleg, *Distributed Computing: A Locality-Sensitive Approach*;
Linial 1992; Cole & Vishkin 1986; Fischer, Lynch & Paterson 1985; Herlihy & Shavit 1999; Brandt 2019.

### Part 60 · Domain-Specific Hardware (~60)
*Story:* When Act II's free speedups ended, the industry's answer was specialization: hardware that does one kind of
work, enormously well. A matrix multiplier wired as a grid of cells passing numbers to their neighbours (H. T. Kung's
systolic array, 1978) became Google's TPU. We build one in Pebble's gate simulator, put it on the roofline, and end
with the Job in hardware.
1. The end of general-purpose scaling (callback to Part 10); Hennessy & Patterson's "new golden age" (2018 Turing
   lecture); the energy of an instruction against the energy of an operation.
2. **The roofline model** (Williams, Waterman & Patterson 2009): arithmetic intensity, derived; this machine's roofline
   measured.
3. Systolic arrays (Kung & Leiserson 1978): a matrix multiplier built from Part 4's multipliers, simulated at gate
   level and verified; weight-stationary against output-stationary dataflow.
4. The TPU (Jouppi et al. 2017): a 256 × 256 systolic array; quantization (callback to Part 4's floats); what the
   numbers in its paper mean.
5. GPUs revisited (Part 10): SIMT, tensor cores, the memory wall again.
6. Dataflow and spatial architectures; coarse-grained reconfigurable arrays; FPGAs (Part 5) as accelerators.
7. Near-memory and in-memory computing; the cost of moving a byte.
8. Sparsity and approximation: sparse accelerators, stochastic rounding, approximate computing.
9. Design methodology: high-level synthesis, Chisel and the agile hardware movement, design-space exploration;
   co-design of algorithm and hardware.
10. **The Job in hardware**: a pipelined word-hashing and counting unit built in Pebble's HDL, verified against the
    software Job; ledger row 21.
11. Frontier: accelerators for language models; wafer-scale and chiplets; open problems in hardware design
    automation.
12. Outro.

*Computed:* a gate-level systolic array multiplying matrices, cycle by cycle, against numpy; the roofline of this
machine measured; the energy per operation table (cited); the word-counting accelerator's throughput, area in gates,
and the Job's time on it.
*Visuals:* numbers flowing through the systolic grid in diagonal waves; the roofline with each kernel as a point; the
Job's accelerator as a pipeline of hash stages.
*In practice:* ML accelerators (TPU, Trainium, tensor cores), FPGA offload in data centres, video and crypto engines,
hardware design roles.
*Reading:* Hennessy & Patterson, *Computer Architecture*, 6th ed., ch. 7; Sze, Chen, Yang & Emer, *Efficient
Processing of Deep Neural Networks*; Kung & Leiserson 1978; Kung 1982; Williams, Waterman & Patterson 2009; Jouppi et
al. 2017; Hennessy & Patterson 2019 (CACM).

### Part 61 · Doing Research (~60; the coda)
*Story:* The series has quoted a thousand results. Where do they come from, and how would you make one? This part
is about method: how to measure without fooling yourself (changing the size of an environment variable can change a
program's speed by a third), how to read and review a paper, how to find a problem, and how to know whether you have
solved it. It ends on the open problems the series met, gathered on one map, and on the tower one last time.
1. What research is: a question, a method, evidence; the shape of a paper; conferences and journals in CS.
2. **Measurement bias** (Mytkowicz, Diwan, Hauswirth & Sweeney 2009), reproduced: link order and environment size
   change the Job's measured speed on this machine.
3. Statistically rigorous performance evaluation (Georges, Buytaert & Eeckhout 2007): confidence intervals, repeated
   runs, warm-up; the statistics of speedups (geometric means, and why).
4. Benchmarks and their failures; reproducibility and artifact evaluation; p-hacking in systems research.
5. Proof as research: how a conjecture becomes a theorem; counterexample search by computer; formal proof (callback
   to Parts 2, 54).
6. Reading and reviewing: the three-pass method; how to review; how to find what is not said.
7. Finding problems: Hamming's "You and Your Research" (1986); limit studies as a way to find headroom (Part 7's).
8. Writing: the structure of an argument; figures that carry the claim; the series' own conventions as a case study.
9. **The open-problems map**: P vs NP and one-way functions; ω; BB(6); dynamic optimality; the UGC; derandomization;
   circuit lower bounds; a memory model for C; practical quantum advantage; verified software at scale; each with its
   record and the part that met it.
10. The bridge to *AI, Built* and *Analysis, Built*: where the series meet.
11. The pebble, the last time: from Hilbert's question to the frontier.
12. Outro: the series map, the final reading list.

*Computed:* the measurement-bias experiment on this machine (link orders × environment sizes); bootstrap confidence
intervals for the ledger's measured rows; a counterexample search (an open conjecture's small cases, checked); the
open-problems map with each record and date.
*Visuals:* the same program's runtime jumping as an environment variable grows; confidence intervals tightening with
runs; the open-problems map as a sky over the tower.
*In practice:* research roles in industry labs, performance engineering, writing design documents and papers,
reviewing.
*Reading:* Hamming 1986; Mytkowicz et al. 2009; Georges et al. 2007; Jain, *The Art of Computer Systems Performance
Analysis*; Keshav, "How to read a paper" (2007); Pólya, *How to Solve It*; Zobel, *Writing for Computer Science*;
Aaronson, "P =? NP" (2016).

---

## 5. Phases

0. **Infrastructure:**
   - `explainer/cs/`:
     - the series constants (`SERIES_EN`, `SERIES_ZH`, `ACTS`, `PARTS`) and `series_map` for 61 parts in eleven acts;
     - `chapter_card` with the tower and the timeline, and the ledger;
     - the first instruments (`Tower`, `TapeView`, `Netlist`, `MemoryStrip`, `Datapath`); the rest are added as
       parts first need them;
     - the cards and text helpers reused from `explainer.ai` and `explainer.analysis`.
   - **Pebble's core**, which every later part depends on: `hdl.py` and the locked Pebble-32 ISA (`isa.py`,
     `emu.py`, `asm.py`), with `tests/test_cs_pebble_*.py`.
   - Tools generalized from `ai` to any bilingual series:
     - `tools/make.py` (`BILINGUAL`);
     - `tools/qa_series.py`, `tools/qa_report.py`, `tools/qa_motion.py` and `tools/qa_audio.py`, which today
       hard-code `videos/ai`;
     - `tools/package_uploads.py --series cs` with `videos/cs/cs_upload.json`.
   - `videos/cs/cs_text_zh.json` and `videos/cs/CS_ZH_GUIDE.md` (the glossary).
   - A silent en + zh smoke render of an empty chapter on Linux.
1. **Pilot: Part 1 (What Is a Computation?)**. It sets up the story and every series device: Pebble introduced, the
   tower, the timeline, the ledger's empty frame, the payoff and *In practice* cards. It exercises `TapeView` and the C
   fast path (BB(5)). It is delivered in English and Chinese, with previews and contact sheets. **Review with the
   user**, then lock the standard.
2. **Act I, Parts 2–6**, in order: proof and counting, then the hardware Pebble. **Part 6 is the second review**: the
   machine runs the Job.
3. **Roll-out in series order, Parts 7 → 61**, with the Act I Frontier retrofit (§1.1) right after Part 7. The order matters, because each part's Pebble layer rests on the ones
   before it. Acts VIII–IX run their services on Act VII's simulator. **Part 40 is the third review**, as the first
   industry part, which sets that act's tone; **Part 56 is the fourth**, as the first research-tier part. Each part
   goes through:
   - the frontier sweep;
   - locking the chapter list;
   - building its Pebble layer and tests;
   - `compute.py`;
   - English scenes, then the QA gates;
   - Chinese narration and text, then the QA gates;
   - commit and push.

## 6. Scale and risks

**Scale:**
- about 58 hours of video;
- about 8,000 narration words per part per language, roughly 490,000 per language in all;
- roughly 4–6k lines of scene code per part (what *AI, Built* took);
- Pebble and its substrate, about 30–40k lines with tests across the series.

At *AI, Built*'s pace, that is one part per one or two long sessions.

| Risk | Mitigation |
|---|---|
| Gate-level simulation is slow | bit-parallel, levelized numpy evaluation; gate level only for short runs (a paragraph of the Job, BB(3)); the emulator for the rest, bridged by co-simulation tests |
| Pebble's breadth (CPU to cloud) | every layer small and tested against an independent reference; later parts use a layer only through its API, so a layer can be rewritten without touching the scenes |
| Overlap with *AI, Built* | callback cards, not repeats (§2.3); the CS treatment goes deeper where the AI series only sketched (Turing, SAT, GPUs, floats) |
| Frontier claims and industry facts age | **(verify)** markers; dated "as of …" captions on prices, defaults and product behaviour; the frontier sweep before each part is written |
| Practice turns into opinion | each practice claim is either derived (queueing, availability, statistics), simulated on our substrate, or cited to evidence (empirical software-engineering studies, published post-mortems); folklore is labelled as such |
| Machine-dependent measurements | labelled `measured on this machine`; the narration branches on the measurement; macOS and Linux both supported |
| Educational crypto mistaken for real crypto | labelled on screen and in the code; known-answer tests only; never imported outside the series |
| No outbound network in some environments | every network and cloud experiment runs on the simulator; real-Internet and real-cloud numbers are cited, not measured |

## 7. Decisions (confirmed 2026-11-04)

1. **Name and handle**: *Computer Science, Built* (计算机科学，从零搭建), videos `cs1` … `cs61` in `videos/cs/`.
2. **Scope**: the full plan. That is fifty-five parts in ten acts, including the industry acts (VIII–IX), discrete
   mathematics (Part 2) and algorithms in practice (Part 24).
3. **Bilingual from the start**: English, then Chinese, for each part, as *AI, Built* does.
4. **The machine**: Pebble, as our own RISC-V-like ISA (cleaner encodings to draw; a comparison card covers the
   differences from RV32I).
5. **Order**: Phase 0, then the Part 1 pilot and a review, then Act I with a review at Part 6, then Parts 7–61 in
   order with reviews at Parts 40 and 56.
6. **The research tier** (the user, 2026-11-04: "this course should also include PhD stuff"): a Frontier chapter and
   a research problem in every part (§1.1), and Act XI, Parts 56–61.

## 8. Progress (updated as parts land)

| Part | State | Length |
|---|---|---|
| 1 | scenes, computations, notes and Chinese narration and on-screen text written; *Frontier* chapter and research problem added (retrofit, 2026-11-04); QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 65 min (estimate) |
| 2 | scenes, computations, notes and Chinese narration and on-screen text written; *Frontier* chapter and research problem added (retrofit, 2026-11-04); QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 69 min (estimate) |
| 3 | scenes, computations, notes and Chinese narration and on-screen text written; *Frontier* chapter and research problem added (retrofit, 2026-11-04); QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 55 min (estimate) |
| 4 | scenes, computations, notes, tests and Chinese narration and on-screen text written; *Frontier* chapter and research problem added (retrofit, 2026-11-04); QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 68 min (estimate) |
| 5 | scenes, computations, notes, tests and Chinese narration and on-screen text written; *Frontier* chapter and research problem added (retrofit, 2026-11-04); QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 55 min (estimate) |
| 6 | scenes, computations (the gate-level CPU, co-simulation, the Job's ledger row 0), notes, tests and Chinese narration and on-screen text written; *Frontier* chapter and research problem added (retrofit, 2026-11-04); QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 51 min (estimate) |
| 7 | scenes (17, including the first *Frontier* chapter), computations (the cycle-accurate pipeline, eight predictors and a limit study, the Job's ledger row 1), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 54 min (estimate) |
| 8 | scenes (17, with the *Frontier* chapter), computations (the out-of-order core and its co-simulation, the scoreboard and Tomasulo on the textbook example, Wall's limit study on the Job, memory disambiguation, the Spectre attack and its mitigations, SMT in the limit study, the Job's ledger row 2), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 68 min (estimate) |
| 9 | scenes (17, with the *Frontier* chapter), computations (a cache simulator and its analyses, this machine's latency staircase, bandwidth and matrix multiply measured, the exact LRU misses of the Job's corpus scans, the Job's ledger row 3 priced on Part 8's core), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 49 min (estimate) |
| 10 | scenes (17, with the *Frontier* chapter), computations (MESI and the store-buffering test simulated; false sharing, the litmus test with and without a fence, atomics and the Job in C with SIMD and threads measured on this machine; greedy schedules against Brent's bound, work stealing, scans, sorting networks checked by the 0–1 principle, bisection widths by exhaustive search; the Job on four Pebble cores, ledger row 4), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 64 min (estimate) |
| 11 | scenes (18, with the *Frontier* chapter), computations (Pebble's linker and loader; endianness, struct layout, a jump table, ELF objects, static and dynamic linking and ASLR measured on this machine; stack depths of factorial, Ackermann and tail calls on the emulator; five allocators on Perl's 146,336-allocation trace; Knuth's rule and Robson's bound simulated; undefined behaviour under gcc; the stack smash and four defences; the Job linked from four files), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 50 min (estimate) |
| 12 | scenes (17, with the *Frontier* chapter), computations (Thompson NFAs, the subset construction, minimization and state elimination; 2ⁿ blow-up and lazy DFAs on real text; backtracking measured in Python, Perl and grep; the Pebble language's lexer, LALR table and parser; CYK and Earley; LL(1) and LR tables checked against bison), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 51 min (estimate) |
| 13 | scenes (17, with the *Frontier* chapter), computations (our compiler pass by pass on the emulator, Part 7's pipeline and Part 8's core; dominators, SSA and liveness traces; SCCP and GVN examples; the register sweep and the chordality check; clang's LLVM IR and gcc's levels on this machine; 240 fuzzed programs; z3 rule checks; a superoptimizer; the Job's ledger row 5), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 76 min (estimate) |
| 14 | scenes (17, with the *Frontier* chapter), computations (our λ reducer under four strategies and a lazy environment machine; Church arithmetic and Y counted in β-steps; reduction graphs with confluence checked; the STLC checker, its derivations and 5,000 random terms checked for progress and preservation; termination of random untyped terms; HM inference traced on the Job in the λ-core; free theorems tested; a propositional prover with Kripke countermodels; rustc, tsc and node on this machine), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 55 min (estimate) |
| 15 | scenes (17, with the *Frontier* chapter), computations (the λ-core's bytecode compiler and reference VM under four collectors; the VM and Cheney's collector in the Pebble language, co-simulated and priced on Part 8's core for ledger row 6; reference-count traffic, lifetimes and nurseries; tri-color marking with and without barriers; a CEK machine and a tiny Prolog; CPython, V8, HotSpot, Go, gcc and node timed and traced on this machine), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 55 min (estimate) |
| 16 | scenes (18, with the *Frontier* chapter), computations (every sort counting its comparisons, with insertion, merge, heap, quick, Ford–Johnson, counting, radix, Timsort, quickselect and median of medians; decision trees; the Job v1 in the Pebble language on the emulator, an instruction model and a C event counter over the corpus for ledger row 7; repeated squaring, radix sort and `std::sort` timed on this machine), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 50 min (estimate) |
| 17 | scenes (18, with the *Frontier* chapter), computations (every structure counting its work: chaining, universal hashing, linear and double hashing, Robin Hood, cuckoo and FKS perfect hashing; plain, AVL, red–black, treap, splay, persistent trees, skip lists and B-trees; binary, pairing and Fibonacci heaps under Dijkstra; union–find; tries and rank; the Job v2 hash table in the Pebble language on the emulator, an exact instruction model, a C event counter and a C replay through Part 9's caches for ledger row 8; lookups and the Job timed natively), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 51 min (estimate) |
| 18 | scenes (18, with the *Frontier* chapter), computations (every algorithm counting its work: Euler circuits, BFS, DFS, topological sort, Tarjan and Kosaraju with 2-SAT, Dijkstra, bidirectional, A*, landmarks and contraction hierarchies, Bellman–Ford, Floyd–Warshall and Johnson, Kruskal, Prim and Borůvka, Edmonds–Karp, Gale–Shapley and the Hungarian algorithm, Held–Karp, PageRank, planar colouring), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 49 min (estimate) |
| 19 | scenes (18, with the *Frontier* chapter), computations (every paradigm counting its work: interval scheduling, Huffman, matroid greedy, Karatsuba, Strassen, DFT, FFT and NTT, an FFT multiplier and a million digits of π, closest pair, Fibonacci, edit distance and LCS, knapsack, matrix chains, optimal BSTs with Knuth's speedup, tree DP, n-queens, Dancing Links, maximum subarray four ways), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 50 min (estimate) |
| 20 | scenes (18, with the *Frontier* chapter), computations (Freivalds, Schwartz–Zippel and the Tutte matrix, fingerprints, Karger and Karger–Stein, Fermat and Miller–Rabin, random-walk SAT, balls into bins, Bloom filters, reservoir sampling, Misra–Gries and Count-Min, the Job v3 in the Pebble language emulated for ledger row 9 and swept over hash functions in C, HyperLogLog and KMV, the AMS sketch, MinHash and LSH on the novels, Ramsey colourings and Moser–Tardos, conditional expectations and RANDU), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 55 min (estimate) |
| 21 | scenes (18, with the *Frontier* chapter), computations (naive, Rabin–Karp, KMP, Boyer–Moore and Horspool counting their comparisons on the novels; Aho–Corasick over the corpus; suffix trees, the suffix array and LCP of all 25 MB; the BWT of *Moby-Dick* inverted and its contexts; the FM-index of the novels; LZ77 + Huffman, LZW and rANS against zlib, bzip2 and xz; Needleman–Wunsch and Smith–Waterman; Myers' diff on this syllabus's history; rsync and content-defined chunking; Manacher over the corpus; BWT runs of repetitive text), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 50 min (estimate) |
| 22 | scenes (17, with the *Frontier* chapter), computations (Kettner's grid and adaptive predicates; Jarvis, Graham, the monotone chain, quickhull and Chan counting their work; Bentley–Ottmann; ear clipping and Fisk's colouring; Fortune's sweep; Delaunay by insertion, by Lawson's flips and by the lifting map; the EMST; Seidel's LP and Welzl's circle; kd-trees and trapezoidal maps; distance concentration, NSW and HNSW; a ham-sandwich cut; configuration spaces, visibility graphs and an RRT; 3SUM as collinearity), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 50 min (estimate) |
| 23 | scenes (16, with the *Frontier* chapter), computations (Chvátal's LP as a 3D polytope with the simplex walk and its tableaux; a transportation problem; the dual's family of bounds, shadow prices and complementary slackness; Klee–Minty pivots under three rules, perturbed cubes and random LPs; an ellipsoid run and the central path; total unimodularity checked; knapsack branch and bound and the FPTAS; vertex and set cover against brute force; Held–Karp, the double tree, Christofides–Serdyukov, nearest neighbour and 2-opt; Goemans–Williamson against exact MAX-CUT; ski rental and paging on the Job's trace; multiplicative weights and a zero-sum game; gradient descent against Newton; random-polytope diameters against Hirsch), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 50 min (estimate) |
| 24 | scenes (17, with the *Frontier* chapter), computations (prefix sums and integral images; Fenwick and segment trees with operation counts; sparse tables, Euler-tour LCA, binary lifting and Cartesian trees; the sliding-window deque and monotonic stacks; binary search on the answer and galloping; submasks; meet in the middle and Mo's order; native C and C++ benchmarks for array against list, range structures, search layouts, branches, SIMD word finding, vectorization, hash tables, radix sort, top-k, benchmark noise and dead code; the Job engineered for ledger row 10; a learned index; ski rental with predictions), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 50 min (estimate) |
| 25 | scenes (17, with the *Frontier* chapter), computations (a Python quine and a 759-line Pebble quine run on the emulator; Sipser's PCP instance, the TM-to-PCP reduction and its accepting history, 20,000 random three-domino sets and the 206-domino instance; Jeandel and Rao's 11 Wang tiles, rectangles found and small tori refuted; Pell's equation by brute force and by continued fractions; Gödel numbers; compressors as Kolmogorov upper bounds; the halting fraction of 5,000 random three-state machines; PRIMEGAME; Collatz records; the hat's outline), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 49 min (estimate) |
| 26 | scenes (18, with the *Frontier* chapter), computations (a CDCL SAT solver tested against brute force; a 60-vertex colouring found against checked; Savitch on paths; Cook–Levin tableaux built from legal windows and solved; one formula through independent set, clique, cover, 3-colouring and subset sum, solved and mapped back; search from decision; pseudo-polynomial subset sum; a Pratt certificate; TQBF and generalized geography; the random 3-SAT phase transition and DPLL against CDCL; Schur numbers and Pythagorean colourings; exact formula sizes of all 3-input functions), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 47 min (estimate) |
| 27 | scenes (17, with the *Frontier* chapter), computations (amplification's binomial tails and Adleman's runs; the Vandermonde identity tested by Schwartz–Zippel; random restrictions of a 3-DNF against the switching lemma; equality by fingerprints; the graph non-isomorphism protocol; sum-check on a #SAT instance with an honest prover and the best cheater; zero-knowledge 3-colouring of the Petersen graph with hashed commitments, a cheater's survival and the simulator; the BLR test's exact rejection curve; random assignments against WalkSAT on MAX-3SAT; unique games under propagation; Williams's SAT-to-OV reduction run against our CDCL solver; OV and 3SUM timed; FPT vertex cover and Buss's kernel; Ryser's permanent against Bareiss; planted clique; multiplication against Pollard's rho), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 45 min (estimate) |
| 28 | scenes (16, with the *Frontier* chapter), computations (repetition exact and simulated; a picture through BSC(0.05) raw, repeated and Hamming-coded; Hamming(7,4) syndromes and exact bit-error curves; the bounds; the Golay code enumerated; GF(256) and its 30 irreducible and 16 primitive polynomials; Reed–Solomon by Berlekamp–Welch and Lagrange; a version-2 QR code identical to the `qrcode` library's, scratched three ways and decoded with a traced Berlekamp–Massey; CRC-8 burst and random detection and CRC-32 against zlib; random linear codes below and above capacity; Viterbi on the (7,5) code; a 4,800-bit (3,6) LDPC waterfall and BP traces; BEC density evolution; polarization and SC decoding; RAID-6; LT overheads; Hadamard local decoding), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 44 min (estimate) |
| 29 | scenes (18, with the *Frontier* chapter), computations (a substitution cipher on *Moby-Dick* broken by quadgram hill climbing; Vigenère's key length by the index of coincidence and its key by χ²; an Enigma I simulator against the standard test, its characteristic invariant under the plugboard, and crib placement; a two-time pad broken by crib dragging; a 17-bit LFSR recovered by Berlekamp–Massey; ChaCha20 against RFC 8439; GGM with SHA-256; Feistel distinguishers for 1–3 rounds; AES-128 from scratch against FIPS-197, traced step by step; avalanche statistics over 400 flips; our logo under ECB, CBC and CTR; Vaudenay's padding oracle; CTR malleability and the CBC-MAC splice; GCM against NIST; birthday collisions on truncated SHA-256; SHA-256 length extension; SHA3-256 against hashlib; a Merkle proof; PBKDF2 and scrypt costs; a differential attack on Heys' SPN; meet in the middle; early-exit timing; a PID-seeded key), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 58 min (estimate) |
| 30 | scenes (18, with the *Frontier* chapter), computations (Diffie–Hellman at p = 23 and in RFC 3526's 2048-bit group; Merkle's puzzles at three sizes; extended-Euclid and square-and-multiply traces; orders in Z₂₃*; 2048-bit RSA keys from our Miller–Rabin, CRT against plain decryption, malleability and OAEP; Bleichenbacher's attack on 256- and 384-bit keys with its shrinking interval; a rho walk and rho against our quadratic sieve to 34 digits; BSGS timings, Pohlig–Hellman on a smooth p − 1, index calculus; the chord-and-tangent law and the GF(97) point cloud; X25519 against RFC 7748; ECDSA against RFC 6979 and nonce-reuse key recovery; a certificate chain; a TLS 1.3-shaped handshake; period finding for 15, 21, 35; Gauss and LLL reduction, a knapsack broken; LWE noise; the NTT against schoolbook and an ML-KEM-512 K-PKE; Schnorr; Shamir sharing; cross-checked against the `cryptography` library), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 51 min (estimate) |
| 31 | scenes (17, with the *Frontier* chapter), instruments (`explainer/cs/os/`: Pebble's kernel mode with `ecall`, `eret`, CSRs, a timer and bounds; PebbleOS, 284 instructions: traps, five system calls, a pipe, round robin; schedulers, queues and real-time tests), computations (PebbleOS booting two processes; four processes, three hostile; one `getpid` traced, 78 kernel instructions; this machine's system-call, `read()`, pipe ping-pong and `fork` costs, and a 25-line shell; FCFS, SJF, SRTF, RR, MLFQ and its gaming, lottery, stride and CFS; work stealing; RMS, EDF, Liu–Layland and Mars Pathfinder; Little's law, M/M/1 against a million-job simulation, Pollaczek–Khinchine, SRPT; microsecond tail latency on 16 cores; ledger row 11, `tok | job` under PebbleOS, 2.17 s), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 55 min (estimate) |
| 32 | scenes (17, with the *Frontier* chapter), instruments (`explainer/cs/os/`: Pebble's MMU with a two-level walk, superpages, a TLB and ASIDs; PebbleOS with paging, 330 instructions, demand-zero faults; trap-and-emulate running Part 31's kernel unmodified; replacement policies, stack distances, working sets, thrashing, buddy and slab), computations (two processes at one virtual address; first-fit fragmentation; the Job's pipeline against TLB size, flushing and tagged; this machine's TLB staircase with 4 KiB and 2 MiB pages, fault, `fork` and copy-on-write costs; Belady's anomaly and OPT, LRU, FIFO, CLOCK, 2Q, ARC, LIRS on the Job's trace; four processes, two killed by faults; exits by kind under the hypervisor; the nested walk; `unshare` namespaces; TLB reach), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 55 min (estimate) |
| 33 | scenes (18, with the *Frontier* chapter), instruments (`explainer/cs/conc/`: an interleaving model checker under SC, TSO and PSO; a linearizability checker; spin locks on MESI caches; Pebble's `cas` and `amoadd`; PebbleOS threads), computations (counter++ on this machine with 1 to 4 threads; all 20 schedules of two increments and the states for k up to 4; the naive lock, Peterson and the bakery checked, Peterson broken under TSO and PSO and repaired with fences; litmus tests; TAS, TTAS, ticket and MCS simulated to 32 cores and measured here; the bounded buffer, Mesa's `if` against `while`, five philosophers, the banker's algorithm; DRF ⇒ SC; gcc hoisting a spin loop; linearizability of random histories; Treiber's ABA, tagged; consensus by test-and-set and CAS; RTM and ThreadSanitizer here; PebbleOS threads under 75 quanta), notes, tests and Chinese narration and on-screen text written; QA previews (480p, silent) reviewed; awaiting narrated master | ≈ 51 min (estimate) |
| 34–61 | planned (this document) | — |
