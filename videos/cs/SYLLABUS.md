# Computer Science, Built: the syllabus (plan of record, draft 1)

Goal: a university computer-science degree in video. It aims to be **as comprehensive as the standard textbooks,
as technical as a graduate course, and as close to the frontier as primary sources allow**, and to tell how the
field got here alongside the mathematics. It is made in English and Chinese to the standard of *Analysis, Built* and
*AI, Built*, and renders on macOS and Linux. Each part runs **50–60 minutes**, and its content decides where in that
range it lands. Forty-two parts come to about **39 hours**.

The plan has the shape of a degree. Act I and Act II are a computer-organization and architecture sequence (Harris &
Harris, Patterson & Hennessy, Hennessy & Patterson). Act III covers systems programming, compilers and programming
languages (CS:APP, the Dragon Book, Cooper & Torczon, TAPL, SICP). Act IV is a two-semester algorithms course (CLRS,
Kleinberg & Tardos, Knuth, Motwani & Raghavan, de Berg et al., Williamson & Shmoys). Act V covers theory of
computation, complexity, coding theory and cryptography (Sipser, Arora & Barak, MacKay, Katz & Lindell, Boneh &
Shoup). Act VI covers operating systems, storage and databases (OSTEP, Herlihy & Shavit, Silberschatz et al., the Red
Book). Act VII covers networks and distributed systems (Kurose & Ross, Peterson & Davie, Lynch, Kleppmann). Act VIII
covers graphics, numerical analysis, quantum computing, formal methods and security (PBRT, Trefethen & Bau, Nielsen &
Chuang, Baier & Katoen, Anderson). Each part's **Reading** line names the textbooks, the classic papers and the
frontier papers it follows, and its reference card shows them on screen.

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
  instruction to Pebble and re-run the Job", with the expected result in the README.
- A reference card listing textbooks, the classic papers and the frontier papers.

**The history thread.**
- Every part opens with its era ("how we got here", 2–3 min), lit on the timeline strip (1800–2030).
- Every idea is credited with its people and year, its dead ends included: delay lines, Itanium, the Lisp machines,
  CODASYL, the OSI stack.
- The timeline strip gains each part's milestones. The tower strip lights the part's layer.

**Frontier sweep.** Before a part is written, its literature is checked against primary sources (papers, standards,
RFCs, vendor documentation) up to the writing date. Recent results the plan relies on (mostly from 2024 on) are
marked **(verify)** below, and must be checked against their primary sources before they go on screen. Examples: the 2025 directed-SSSP result,
optimal open addressing, Williams' square-root-space simulation, BB(6) bounds, and resource estimates for quantum
factoring.

**Numbers are real.**
- Computed numbers come from the part's `compute.py`, cached under `.cache/csN/`. Published numbers are cited.
  Schematics carry the label `schematic`, and made-up examples the label `illustrative`.
- **(CS)** Measurements of the machine that renders the video (cache latencies, branch-prediction costs,
  context-switch time, matrix-multiply throughput) are labelled `measured on this machine`. They are reported as
  measured, and the narration follows them, so the Mac build and the Linux build may say different numbers.
- **(CS)** Everything we build is checked against an independent reference (§2) before its numbers go on screen.
  Those checks live in `tests/test_cs_*.py`.
- CPU budget: ≤ 2 h per part by default, seeded and resumable (`CACHE.partial`). The named exceptions are listed per
  part.
- Scene assertions use tolerances, not exact equality.
- Narration that states a result is an f-string over the data. When a verdict depends on the data (an algorithm
  beats hardware, a predictor wins), the sentence branches on the computed result.

**Bilingual standard (as *Analysis, Built* and *AI, Built*).**
- Every narration line has its entry in `narration_zh.json`, or in the part's `zh_lines.py` template when the line is
  computed.
- Every on-screen string is in `cs_text_zh.json`, and `tools/collect_text.py --check csN` is clean.
- The glossary in `CS_ZH_GUIDE.md` grows with every new term (图灵机, 停机问题, 与非门, 流水线, 乱序执行, 缓存一致性, 虚拟内存,
  死锁, 共识, 线性一致性, …).
- Code on screen is never translated. Comments and captions are.

**Gates per part:** `tools/lecture_length.py` (fails under 50 min), `contact_sheet.py`, `dead_air.py`,
`collect_text.py --check`, `check_narration.py`, `zh_lines.py --verify`, and the part's `tests/test_cs*_*.py`.

## 2. The devices

### 2.1 Pebble, the machine we build

Pebble lives in `explainer/cs/pebble/`. It is real, tested Python, with a C fast path wherever speed matters (built
with the system `cc`, with a pure-Python fallback, per the working guide). Each layer is built in the part that
teaches it. Each layer is also checked against something that does not share its code.

| Layer | Module | Built in | Checked against |
|---|---|---|---|
| Netlists and a bit-parallel gate simulator (64 test vectors per `uint64` word, levelized evaluation, unit and real delays) | `hdl.py` | 2 | exhaustive truth tables; random vectors |
| Adders (ripple, Kogge–Stone, Brent–Kung), multipliers (array, Booth, Wallace), divider, ALU, shifter | `blocks.py` | 3 | Python integer arithmetic over all edge cases; exhaustive at 8 bits |
| Latches, flip-flops, register file, SRAM/DRAM models, FSM synthesis | `seq.py` | 4 | cycle-by-cycle reference models |
| **Pebble-32**: the ISA, the gate-level single-cycle CPU, the fast ISA emulator, the assembler | `isa.py`, `cpu.py`, `emu.py`, `asm.py` | 5 | co-simulation of gate level against the emulator on random programs; disassembly round trips |
| Pipeline (5-stage, cycle-accurate), branch predictors, out-of-order core (Tomasulo plus ROB), caches, multicore with MESI | `uarch/` | 6–9 | architectural state equals the emulator's after every program |
| Object format, linker, loader, allocator | `link.py`, `alloc.py` | 10 | relocation round trips; allocator invariants |
| The **Pebble language** (a small C-like language with functions, arrays, structs and pointers): regex engine, lexer, LL and LR parsers, type checker, SSA compiler with optimizations and register allocation | `lang/` | 11–12 | a Python reference interpreter for the language; differential testing of compiled against interpreted code |
| The λ-core (a small ML: closures, ADTs, Hindley–Milner), bytecode VM, three garbage collectors | `lang/ml/` | 13–14 | a substitution-based reducer; GC heap invariants after every collection |
| **PebbleOS**: traps, timer, processes, schedulers, MMU and paging, locks, a file system on a simulated disk | `os/` | 29–32 | invariants under randomized interrupt timing and crash points |
| A relational database: SQL parser, optimizer, executor, B+ tree, WAL and recovery | `db/` | 33 | `sqlite3` from the standard library, on the same queries and data |
| A network: links with loss and delay, Ethernet-like framing, IP routing, TCP-lite | `net/` | 34–35 | delivery and ordering invariants under seeded loss |
| Distributed systems: a deterministic event simulator, Raft, MapReduce, CRDTs, consistent hashing | `dist/` | 36–37 | safety invariants over thousands of seeded fault schedules |
| Cryptography (**educational, never for real use**, said on screen): AES, SHA-256, HMAC, RSA, ECC, a toy LWE, a TLS-like handshake | `crypto/` | 27–28 | FIPS-197 and FIPS-180 vectors, `hashlib`, `hmac`, Python's `pow` |
| A rasterizer and a path tracer | `render/` | 38 | analytic images (the white-furnace test, a lit sphere) |
| A state-vector quantum simulator | `quantum/` | 40 | closed-form states; unitarity and norm checks |
| A VC generator, an explicit and a BDD model checker, abstract interpretation, a fuzzer | `verify/` | 41 | known-answer suites |

**Pebble-32** is our own clean 32-bit RISC in the RISC-V mould. It has sixteen registers with `r0 = 0`,
byte-addressed little-endian memory, four instruction formats and about thirty instructions:
- ALU: `add sub and or xor sll srl sra slt sltu` and their immediate forms, plus `lui`;
- memory: `lw lb lbu sw sb`;
- branches: `beq bne blt bge bltu bgeu`;
- jumps: `jal jalr`.

Later parts add extensions as the series reaches them:
- `mul/div` (Part 3's multiplier, wired into the CPU in Part 6);
- `ecall/eret` and control registers (Part 29);
- a page-table MMU (Part 30);
- `cas` and `amoadd` (Parts 9 and 31).

I/O is memory-mapped: a console, the *tape* (the input stream), a timer, a disk and a network card. A card in Part 5
compares Pebble-32 with RV32I and says where it differs and why. Two speeds are documented: the gate-level CPU runs
a paragraph, and the emulator runs a novel.

### 2.2 The Job and its ledger

**The Job:** count the words in the thirty novels and list the twenty most common. The text is *AI, Built* Part 1's
reading (`BOOKS` in `ai1`'s `compute.py`: thirty Project Gutenberg novels, several million words, measured exactly
in Part 5), so `make.py` computes `ai1` first. The
ledger (`explainer.cs.ledger`, `.cache/cs*/ledger.json`) keeps one row per change. Each row records:
- what changed;
- Pebble cycles per byte of text (simulated);
- the projected time for all thirty novels at a stated clock;
- from Part 15 on, the time measured on this machine;
- memory used.

| Row | Part | What changes |
|---|---|---|
| 0 | 5 | single-cycle Pebble at gate level, hand-written assembly, words kept in an unsorted list (linear search). Projected at relay speed (the Z3's ~5 Hz), at ENIAC's, and at 1 GHz |
| 1 | 6 | 5-stage pipeline: a faster clock, CPI from the stall breakdown |
| 2 | 7 | 4-wide out-of-order core |
| 3 | 8 | realistic caches (and what the list does to them) |
| 4 | 9 | four cores, SIMD character scanning |
| 5 | 12 | the Job written in the Pebble language: `-O0` against optimized |
| 6 | 14 | the Job in the λ-core, garbage-collected: what GC costs |
| 7 | 15 | **algorithm**: sort then count, n log n |
| 8 | 16 | **algorithm**: a hash table, expected linear time. Rows 0 → 8 are set beside rows 0 → 4: the narration says which mattered more, from the data |
| 9 | 19 | Count-Min and a heap: the top twenty in kilobytes. The ledger's memory column, and the accuracy given up |
| 10 | 29 | under PebbleOS: system calls and context switches |
| 11 | 32 | the novels read from our file system |
| 12 | 33 | `SELECT word, COUNT(*) … GROUP BY word ORDER BY 2 DESC LIMIT 20` on our database: the plan it chose |
| 13 | 35 | the novels fetched over our TCP on a lossy link: bytes, round trips, time |
| 14 | 37 | MapReduce on sixteen simulated Pebbles, one of which crashes |
| 15 | 42 | the final ledger: every row, and native Python and C on this machine |

### 2.3 The tower, the timeline and the payoffs

- `explainer.cs.tower`: the stack drawn on every chapter card, with the part's layer lit. From the bottom: physics,
  switches, gates, arithmetic and memory, the ISA, the microarchitecture, machine code, languages, algorithms, the
  OS, storage and data, networks, distributed systems, applications. A side column holds the *limits*:
  computability, complexity, information. Acts V and the theory chapters light it.
- `explainer.cs.timeline`: 1800–2030. Babbage (1822, 1837), Boole (1854), Hilbert (1928), Gödel (1931), Church and
  Turing (1936), Shannon (1937, 1948, 1949), Z3 (1941), ENIAC and EDVAC (1945), the transistor (1947), the Baby
  (1948), Hamming (1950), FORTRAN (1957), the IC (1958), Dijkstra (1959), LISP (1960), Unix (1969), Codd (1970),
  Cook (1971), Diffie–Hellman (1976), RSA (1977), TCP/IP (1983), Paxos (1989), the Web (1991), Shor (1994), MapReduce
  (2004), Raft (2014), Spectre (2018), BB(5) (2024), ML-KEM (2024), and on.
- `payoff_card` ("where this comes back") and `reference_card` from `explainer.ai`. The **callbacks** to other series
  are cards, not repeats:

| Here | Elsewhere |
|---|---|
| 1 Computation, 23 Undecidable | *AI, Built* 2 (Turing, the halting problem sketched); *Analysis, Built* 1 (Cantor's diagonal) |
| 3 Arithmetic, 39 Real Numbers | *AI, Built* 4 (floats and numerics), 17 (number formats) |
| 6–9 Architecture | *AI, Built* 17 (GPUs, the roofline), 18 (collectives) |
| 15–16 Sorting, hashing | *AI, Built* 1 (bits from a comparison, Huffman) |
| 17 Graphs | *AI, Built* 2 (A*), 5 (Markov chains, PageRank's power iteration) |
| 18 FFT, DP | *Analysis, Built* 9 (the Fourier transform); *AI, Built* 7 (Viterbi), 26 (AlphaTensor) |
| 19 Randomness | *AI, Built* 3 (Johnson–Lindenstrauss), 5 (concentration, MCMC), 18 (MinHash dedup) |
| 20 Strings | *AI, Built* 1 (compression), 23 (BPE) |
| 22 Optimization | *AI, Built* 4 (Lagrange, KKT), 6 (boosting), 11 (gradient methods) |
| 24 P vs NP | *AI, Built* 2 (DPLL, CDCL, the 3-SAT phase transition) |
| 26 Codes | *AI, Built* 1 (typical sets), 7 (belief propagation) |
| 38 Graphics | *AI, Built* 22 (NeRF, Gaussian splatting) |
| 40 Quantum | *Quantum Mechanics, Visualized* and *Part 2* (the physics) |
| 41 Proofs | *AI, Built* 25 (Lean and AlphaProof) |
| 42 Trust | *AI, Built* 31 (can we trust it?) |

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
| `TreeView` | BSTs, heaps, tries, parse trees, ASTs, λ-terms; rotations, splays and reductions morph |
| `GraphView` | graphs carrying algorithm state: frontiers, distances, flows, colors, cuts |
| `ArrayView` | arrays as bars and cells; DP tables filling, with traceback |
| `Lattice` | Hasse diagrams: dataflow lattices, CRDT joins, the consistency hierarchy, complexity classes |
| `Gantt` | schedules, job pipelines, MapReduce phases, pipeline bubbles |
| `SpaceTime` | Lamport diagrams: processes, messages, logical clocks, consistent cuts |
| `SequenceDiagram` | protocols (TCP, TLS, Raft RPCs, Paxos), with loss and retransmission |
| `InterleavingTree` | thread interleavings branching; reachable bad states lit |
| `QCircuit` / `BlochSphere` / `AmpBars` | quantum circuits, states on the sphere, amplitudes colored by phase |
| `Tower` / `Ledger` | the series devices |

3D camera tours: the Boolean cube and Hamming space, the simplex walking an LP polytope (and the squashed Klee–Minty
cube), Delaunay lifted to the paraboloid, RANDU's points turning until fifteen planes appear, the Bloch sphere, rays
bouncing in our scene, the memory hierarchy as a zoom from registers to disk ("if a cycle were a second").

## 4. Part by part

Lengths are targets; the content decides. Each part lists its **story**, its chapters, what is **computed**, the
signature **visuals**, and its **reading**.

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
4. Hilbert's program, and Gödel 1931 in one picture (paid off in Part 23).
5. Turing's machine (1936): tape, head, states, transition table. Definition card. Our simulator runs an
   incrementer and a unary adder, with the tape's space–time history drawn.
6. Programming a Turing machine: palindromes, copying, binary addition, subroutines. What they cost: palindromes take
   Θ(n²) on one tape, by the crossing-sequence argument (sketched).
7. Robustness: a multitape machine simulated on a single tape with quadratic slowdown (proved by construction);
   two-way tapes and larger alphabets; nondeterminism adds no power, at an exponential cost in simulation.
8. The universal machine: encoding machines as strings, so that U simulates any M. This is the stored-program idea,
   paid off in Part 5. Small universal machines.
9. Other models with the same power:
   - the λ-calculus (Church 1936): Church numerals computing 2 + 3 on screen;
   - μ-recursive functions;
   - Minsky's two-counter machines, via the 2ᵃ3ᵇ trick;
   - Post systems;
   - Rule 110 (Cook 2004) and Conway's Life.
10. The Church–Turing thesis: what it claims and what it doesn't. The physical thesis, and the extended
    (complexity-theoretic) thesis that Part 40 challenges.
11. Diagonalization: Cantor's argument, then counting. There are countably many machines and uncountably many
    languages, so almost every problem is unsolvable.
12. The halting problem: Turing's proof, animated as an infinite table with its diagonal flipped; the paradoxical
    program.
13. Reductions: from halting to "does M ever print 1?" and "does M halt on a blank tape?". Rice's theorem as a teaser
    (proved in Part 23).
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
*Reading:* Turing 1936; Church 1936; Petzold, *The Annotated Turing*; Sipser ch. 3; Moore & Mertens, *The Nature of
Computation* ch. 7; Minsky, *Computation: Finite and Infinite Machines*; Davis, *The Universal Computer*; Aaronson,
"The Busy Beaver Frontier" (2020); bbchallenge (2024–25).

### Part 2 · Logic from Switches (~55)
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
   exponentially (computed). Part 41 uses them.
8. Circuit complexity:
   - size and depth;
   - Shannon's counting argument (1949): almost all n-input functions need ≳ 2ⁿ/n gates (proved by counting
     circuits against functions);
   - Lupanov's matching upper bound;
   - yet the best lower bound for an explicit function is about 3.1n. The gap returns in Part 25.
9. Formulas against circuits; parity needs 2ⁿ⁻¹ terms in depth two.
10. Gates take time: propagation delay, the critical path, glitches and hazards, fan-out, RC delay. Our simulator with
    unit delays shows a glitch.
11. The blocks Pebble needs, built and gate-counted: comparators, parity trees, priority encoders, a log-depth barrel
    shifter.
12. The series' hardware layer: netlists in Python, bit-parallel simulation (64 vectors per word), exhaustive
    verification of every block.
13. History: Zuse's Z1–Z3 (1938–41), Stibitz's relay calculators, Atanasoff–Berry, Colossus (1944); Moore's 1965
    paper.
14. Reversible gates (Toffoli, Fredkin) as a preview of Part 40. Outro.

*Computed:* gate counts and critical paths of every block; exhaustive checks; BDD sizes under good and bad variable
orders; Shannon's counting curves; glitch traces.
*Visuals:* relay contacts clicking into series and parallel; the CMOS inverter's transfer curve; truth table →
Boolean cube → K-map faces; a BDD collapsing as nodes merge; two towers of numbers, 2^(2ⁿ) functions against the
circuits of size s.
*Reading:* Harris & Harris, *Digital Design and Computer Architecture* ch. 1–2; Nisan & Schocken, *The Elements of
Computing Systems* ch. 1; Petzold, *Code*; Shannon 1938, 1949; Bryant 1986; Wegener, *The Complexity of Boolean
Functions*; Jukna, *Boolean Function Complexity*; Knuth, TAOCP 4A §7.1; Weste & Harris, *CMOS VLSI Design* ch. 1;
Li & Yang 2022 (3.1n).

### Part 3 · Arithmetic (~55)
*Story:* A machine has only finitely many bits, so its integers live on a clock and its reals are a sparse,
uneven ruler. The carry chain that makes addition slow becomes, seen the right way, a parallel prefix computation.
Floating point is carefully engineered, and still a wrong number can bring down a rocket.
1. Positional notation; why binary (noise margins); hexadecimal.
2. Integers mod 2ⁿ: overflow as wraparound on a clock. Two's complement as a relabeling of ℤ/2ⁿℤ, so one adder
   serves signed and unsigned. Negation = invert + 1 (proved). Sign extension.
3. Half and full adders. The ripple-carry adder, correct by induction, with delay Θ(n) measured.
4. Carry lookahead: generate and propagate. The carry operator (g, p) ∘ (g′, p′) is associative, which gives a
   parallel prefix tree. Kogge–Stone, Brent–Kung and Sklansky drawn: depth O(log n), with their size, depth and
   fan-out trade-offs. The prefix tree returns in Part 9 (scan).
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
    for Part 18).
14. Computing sin, exp and log: range reduction, minimax polynomials, CORDIC shift-and-add rotations (the HP-35).
    Outro.

*Computed:* ripple against lookahead delay over n; Wallace against array depth; a deliberately broken SRT table;
Kahan against naive summation; Wilkinson's roots; CORDIC iterations.
*Visuals:* the 2ⁿ clock; a prefix tree of carries lighting level by level; the float number line with its spacing
doubling at each power of two; the roots scattering.
*Reading:* Harris & Harris ch. 5; Parhami, *Computer Arithmetic*; Koren, *Computer Arithmetic Algorithms*; Goldberg,
"What Every Computer Scientist Should Know About Floating-Point Arithmetic" (1991); Higham, *Accuracy and Stability
of Numerical Algorithms* ch. 1–4; Muller et al., *Handbook of Floating-Point Arithmetic*; Knuth, TAOCP 2 §4.1–4.3;
Overton, *Numerical Computing with IEEE Floating Point Arithmetic*.

### Part 4 · Memory and Time (~55)
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
   n log n). The bridge to Part 11.
7. Counters and shift registers. LFSRs: maximal-length sequences from primitive polynomials over GF(2) (period
   2ⁿ − 1), with the LFSR as multiplication by x in GF(2ⁿ). Returns in CRCs (Part 26) and stream ciphers (Part 27).
8. The register file from decoders, multiplexers and flip-flops; what each extra port costs.
9. Memory arrays:
   - the 6T SRAM cell (cross-coupled inverters again), word and bit lines, sense amplifiers;
   - the 1T1C DRAM cell, destructive reads, refresh every 64 ms, row buffers;
   - why DRAM is dense and slow. Part 8 builds on this.
10. Rowhammer (2014): hammering one DRAM row flips bits in its neighbours, and the hardware abstraction leaks (Part
    42 returns to it).
11. The synchronous discipline, and why nearly everyone clocks; asynchronous circuits and the Muller C-element.
12. ROMs, PLAs, FPGAs: memory as logic; a preview of microcode.
13. History: mercury delay lines (EDSAC), Williams tubes, core memory (Forrester, Whirlwind 1953), the Intel 1103
    DRAM (1970); flash previewed for Part 32.
14. Outro.

*Computed:* the cross-coupled-inverter ODE phase portrait; a metastability histogram; Myhill–Nerode minimization;
LFSR periods for every polynomial of degree ≤ 8; the register file in the simulator.
*Visuals:* a ball rolling into one of two wells or balancing on the saddle; setup and hold windows on a waveform;
the DRAM capacitor leaking charge until refresh.
*Reading:* Harris & Harris ch. 3; Nisan & Schocken ch. 3; Sipser ch. 1; Hopcroft, Motwani & Ullman ch. 4; Jacob, Ng &
Wang, *Memory Systems*; Golomb, *Shift Register Sequences*; Kim et al. 2014 (Rowhammer); Ginosar, "Metastability and
Synchronizers" (2011).

### Part 5 · The Stored-Program Computer (~60)
*Story:* ENIAC was programmed with cables. The EDVAC report put the program in memory, alongside the data. We build
that machine, Pebble, from the gates of Parts 2–4. It runs Euclid, runs a Turing machine, and runs the Job, which
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
12. Code as data: self-modifying code in EDSAC's day, and why we forbid it later (W^X, Part 42).
13. Interrupts and exceptions previewed (Part 29).
14. The whole machine counted: Pebble's gates and critical path, against the 6502 (~3,500 transistors) and a modern
    core (cited).
15. Outro.

*Computed:* the whole CPU netlist; gate-level/emulator co-simulation on random programs; the Job v0; BB(3) on Pebble.
*Visuals:* instruction bits lighting their fields; the datapath with glowing packets; the camera zooms from the
block diagram into one NAND gate and back, the first trip down the tower.
*Reading:* Patterson & Hennessy, *Computer Organization and Design (RISC-V)* ch. 2, 4; Harris & Harris ch. 6–7;
Nisan & Schocken ch. 4–6; von Neumann 1945; Wilkes 1951; Haigh, Priestley & Rope, *ENIAC in Action*; the RISC-V
unprivileged specification.

---

## Act II · Making It Fast

### Part 6 · Pipelines (~55)
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
7. Branch prediction: static; 1-bit against 2-bit saturating counters (Part 4's FSMs); accuracy measured on the Job's
   branch trace.
8. Correlating predictors:
   - global history and gshare;
   - tournament predictors;
   - TAGE, with geometric history lengths (Seznec);
   - the perceptron predictor (Jiménez & Lin 2001), a neural network inside every CPU (callback to *AI, Built*).
9. Branch target buffers and return-address stacks.
10. Precise exceptions in a pipeline.
11. The Job's CPI on the cycle-accurate pipeline, with its stall breakdown. Ledger row 1.
12. The deep-pipeline era and its end: the Pentium 4's 31 stages, the frequency race, and the power wall (Part 9).
13. Amdahl's law, derived, with its corollaries.
14. The sorted-array puzzle, measured on this machine: why sorting data makes a branchy loop several times faster;
    branchless code and conditional moves.
15. Outro.

*Computed:* the cycle-accurate pipeline; CPI breakdowns; 1-bit, 2-bit, gshare, TAGE-lite and perceptron accuracy on
traces of the Job and other programs; sorted against unsorted branches timed on this machine.
*Visuals:* the pipeline chart with bubbles, forwarding arrows and flushes; predictor state machines flipping; the
perceptron's weights as a heatmap over branch history.
*Reading:* Patterson & Hennessy ch. 4; Hennessy & Patterson, *Computer Architecture: A Quantitative Approach* ch. 3,
App. C; Shen & Lipasti, *Modern Processor Design*; Smith 1981; Yeh & Patt 1991; McFarling 1993; Seznec & Michaud
2006; Jiménez & Lin 2001; Amdahl 1967.

### Part 7 · Out of Order (~55)
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
   out-of-order model, with a simulated cache-timing channel (Part 42 returns to it).
10. VLIW and EPIC (Itanium): the compiler-scheduled alternative and why it lost; list scheduling and software
    pipelining (Part 12).
11. RISC against CISC: the IBM 801 (Cocke), Berkeley RISC, Stanford MIPS, x86 µops, ARM, RISC-V; the 2017 Turing
    Award.
12. Simultaneous multithreading.
13. Modern cores in numbers (cited): ROB sizes, decode widths, port counts.
14. The Job on our out-of-order model. Ledger row 2.
15. Outro.

*Computed:* the out-of-order simulator (Tomasulo plus ROB) on Pebble traces; IPC against width and ROB size; the
dataflow-limit study; the Spectre toy.
*Visuals:* the CDB broadcasting tags as glowing pulses; the Job's inner-loop dataflow graph with its critical path;
the ROB as a ring buffer filling and retiring.
*Reading:* Hennessy & Patterson ch. 3; Tomasulo 1967; Thornton, *Design of a Computer: The Control Data 6600*; Smith &
Pleszkun 1985; Shen & Lipasti; Wall 1991; Patterson & Ditzel 1980; Kocher et al. 2019; Lipp et al. 2018.

### Part 8 · The Memory Hierarchy (~55)
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
11. External memory (Aggarwal & Vitter 1988): the sorting bound (N/B) log_{M/B}(N/B); B-trees (Parts 16, 33).
12. Prefetching: stride prefetchers and software prefetch.
13. DRAM in depth: banks, rows, CAS and RAS, row-buffer hits; HBM (callback to *AI, Built* 17). The TLB previewed
    (Part 30).
14. The Job with a cache model. Ledger row 3.
15. Outro.

*Computed:* a cache simulator on the Job and other traces; 3C breakdowns; this machine's latency staircase and
bandwidth; tiled matmul speedups; the pebble-game bound against simulated misses.
*Visuals:* address bits splitting; cache sets as shelves with tags; the staircase; the camera zooming down the
hierarchy on the "cycle = second" scale.
*Reading:* Hennessy & Patterson ch. 2, App. B; Bryant & O'Hallaron, *Computer Systems: A Programmer's Perspective*
ch. 6; Jacob, Ng & Wang; Drepper, "What Every Programmer Should Know About Memory" (2007); Frigo, Leiserson, Prokop &
Ramachandran 1999; Hong & Kung 1981; Aggarwal & Vitter 1988; Wulf & McKee 1995.

### Part 9 · Parallel Machines (~55)
*Story:* Around 2005 the clocks stopped getting faster, because power density had hit a wall. The way forward was
more cores. That brought new trouble: caches that disagree, memory that reorders, and programs whose speed is set by
their longest chain of dependencies. The adder's carry tree from Part 3 comes back as the core of parallel
computation.
1. The power wall: P = αCV²f; Dennard scaling (1974) and its end; fifty years of microprocessor trends (cited); dark
   silicon.
2. Multicore and shared memory; the Job split across four Pebble cores.
3. Cache coherence: the problem; snooping MSI and MESI as state machines, animated; directories; coherence misses;
   false sharing measured on this machine.
4. Memory consistency: sequential consistency (Lamport 1979); store buffers break it, as the store-buffering litmus
   test shows (both threads read 0); TSO, weak models, fences. The deep dive is Part 31.
5. Atomic instructions: test-and-set, CAS, LL/SC, fetch-and-add (Part 31 uses them).
6. SIMD and vectors: Cray-1 (1976), SSE and AVX, NEON, SVE; vectorizing the Job's character scan.
7. GPUs in one chapter: SIMT, warps, divergence (callback to *AI, Built* 17).
8. The work–span model: T₁, T∞, parallelism T₁/T∞; **Brent's theorem** T_p ≤ T₁/p + T∞ (proved); greedy
   scheduling; work stealing (Blumofe & Leiserson) and its bounds.
9. Parallel prefix (scan): Part 3's carry tree reappears. Blelloch's work-efficient scan and its uses (radix sort,
   stream compaction, lexing).
10. Sorting networks: the **0–1 principle** (proved); Batcher's bitonic sort, depth O(log² n); AKS; optimal small
    networks found by computer search (cited).
11. Amdahl against Gustafson (both derived); strong and weak scaling.
12. Models: PRAM (EREW, CREW, CRCW), BSP (Valiant 1990), LogP; message passing and MPI collectives (callback to *AI,
    Built* 18's all-reduce).
13. Interconnects: bus, crossbar, mesh, torus, hypercube, fat tree; bisection bandwidth.
14. Supercomputers from the Cray-1 to exascale (Top500, cited). Ledger row 4.
15. Outro.

*Computed:* the MESI simulation; a false-sharing benchmark on this machine; the work and span of the parallel Job;
Brent's bound against simulated greedy schedules; the 0–1 principle checked exhaustively for n ≤ 10; bitonic
networks; scan.
*Visuals:* cache lines changing color through MESI; the litmus test as two timelines; a work–span DAG with its
critical path glowing; a bitonic network's wires; the scan tree's up-sweep and down-sweep.
*Reading:* Hennessy & Patterson ch. 5; Sorin, Hill & Wood, *A Primer on Memory Consistency and Cache Coherence*;
Herlihy & Shavit ch. 1; Blelloch 1990; Blumofe & Leiserson 1999; Knuth, TAOCP 3 §5.3.4; Leighton, *Introduction to
Parallel Algorithms and Architectures*; Valiant 1990; Dennard et al. 1974; Esmaeilzadeh et al. 2011.

---

## Act III · Speaking to the Machine

### Part 10 · The Running Program (~55)
*Story:* Follow one program from source to process. Its data turns into bytes, its control flow into branches, its
function calls into a stack, its names into addresses. The linker stitches the pieces together and the loader brings
them to life. Then one unchecked copy overwrites a return address, and the program does something its author never
wrote.
1. A program's life: compiler, assembler, linker, loader, process (the tower).
2. Data in memory: bytes and words; endianness (Cohen 1980, after Swift); alignment and padding; row-major arrays;
   pointers and pointer arithmetic.
3. Control flow in machine code: conditionals, loops, and switch statements as jump tables.
4. Procedures: the call stack, activation records, calling conventions (caller- and callee-saved registers), drawn
   as recursion grows and unwinds; Ackermann's explosive stack.
5. Tail calls; stack depth; mutual recursion.
6. The heap:
   - `malloc` and `free`;
   - allocator design: free lists, boundary tags, coalescing, segregated fits, buddies;
   - fragmentation, internal and external;
   - Knuth's fifty-percent rule; Robson's worst-case bound.
7. Object files: ELF sections (.text, .data, .bss), symbol tables, strong and weak symbols.
8. Linking, step by step with Pebble's linker: symbol resolution and relocation.
9. Static against dynamic linking; position-independent code (GOT and PLT); shared libraries; interposition.
10. Loading: the address-space layout, `_start`, argv and envp.
11. Exceptional control flow previewed: exceptions, signals, setjmp and longjmp (Part 29).
12. Undefined behaviour: why it exists, and what optimizers do with it (signed overflow; a deleted null check).
13. Buffer overflows: the stack smash (the Morris worm 1988; Aleph One 1996) on our Pebble stack, overwriting the
    return address. Part 42 picks this up.
14. The Job in the Pebble language, compiled by hand in this part (automatically in Part 12): frames and heap lists.
15. Outro.

*Computed:* Pebble's linker and loader; first-fit, best-fit and segregated allocators on traces, with fragmentation;
stack-depth traces.
*Visuals:* memory as a tall strip, the stack growing down and the heap up; frames pushing and popping; relocation
arrows patching addresses; free lists as chains.
*Reading:* Bryant & O'Hallaron ch. 3, 7, 9; Levine, *Linkers and Loaders*; Wilson et al. 1995 (the allocation
survey); Knuth, TAOCP 1 §2.5; Aleph One 1996; the System V ABI.

### Part 11 · Languages and Automata (~60)
*Story:* To program a machine in sentences, we need machines that read sentences. The finite automata from Part 4
read regular languages, and a stack is what lets a machine handle nesting. The Chomsky hierarchy orders languages by
the memory needed to recognize them. A regex can also run in exponential time and take down a large part of the
web.
1. Languages as sets of strings; recognition against parsing.
2. Regular expressions (Kleene 1951); DFAs (callback to Part 4); NFAs.
3. Thompson's construction (1968): regex to NFA, simulated on sets of states in linear time.
4. The subset construction, and its exponential blow-up: the language "the n-th symbol from the end is 1" needs 2ⁿ
   states (by Myhill–Nerode).
5. Kleene's theorem: DFA to regex by state elimination.
6. The pumping lemma, with aⁿbⁿ not regular (proof animated); closure properties.
7. Backtracking engines: (a+)+b blows up exponentially; ReDoS (the 2019 Cloudflare outage, cited); Cox's argument for
   RE2; backreferences make matching NP-hard.
8. Lexing: maximal munch; the lexer for the Pebble language.
9. Context-free grammars (Chomsky 1956; BNF for ALGOL 60): derivations, parse trees, ambiguity (dangling else,
   precedence).
10. The Chomsky hierarchy, with a machine for each level: DFA, PDA, LBA, TM.
11. Pushdown automata; CFG ⇔ PDA; the CFL pumping lemma (aⁿbⁿcⁿ); Chomsky normal form.
12. CYK in O(n³) as dynamic programming (Part 18); Valiant's reduction to matrix multiplication; Earley's algorithm.
13. Top-down parsing: recursive descent; LL(1) with FIRST and FOLLOW; removing left recursion; Pratt parsing.
14. Bottom-up parsing: shift–reduce; LR(0) items and the LR automaton (Knuth 1965); SLR, LALR (yacc), LR(1);
    conflicts.
15. The Pebble language parsed: its grammar, its parser, its ASTs.
16. Undecidable questions about grammars, such as ambiguity and equivalence (Part 23). Outro.

*Computed:* our Thompson regex engine against a backtracking one (timing blow-up); subset-construction sizes; CYK
and Earley on ambiguous sentences; the LR tables for the Pebble grammar.
*Visuals:* tokens multiplying along ε-edges; states merging in the subset construction; the pumping lemma cutting a
string; parse trees growing top-down and bottom-up; the LR automaton.
*Reading:* Sipser ch. 1–2; Hopcroft, Motwani & Ullman; Aho, Lam, Sethi & Ullman, *Compilers* (the Dragon Book) ch.
2–4; Grune & Jacobs, *Parsing Techniques*; Thompson 1968; Knuth 1965; Cox 2007; Pratt 1973; Nystrom, *Crafting
Interpreters*.

### Part 12 · The Compiler (~60)
*Story:* In 1957 FORTRAN had to produce code as good as hand-written code, or nobody would use it. The compiler
turns a parse tree into a graph. On that graph, optimization becomes a fixed-point computation over lattices, and
register allocation becomes graph coloring: NP-hard in general, but solvable in polynomial time on SSA programs.
1. History: Hopper's A-0 (1952); FORTRAN (Backus 1957, eighteen person-years).
2. Front end, IR, middle end, back end: the Pebble compiler pipeline.
3. Semantic analysis: scopes, symbol tables, type checking.
4. Three-address code, basic blocks, control-flow graphs.
5. Dominators: the iterative algorithm and dominator trees; Lengauer–Tarjan mentioned.
6. SSA (Cytron et al. 1991): φ-functions at dominance frontiers; renaming; why SSA makes optimizations simple.
7. Dataflow analysis:
   - liveness, reaching definitions, available expressions;
   - monotone frameworks on lattices (Kildall 1973);
   - fixed points (Knaster–Tarski, Kleene), with the iteration converging on screen.
8. Optimizations: sparse conditional constant propagation, copy propagation, DCE, value numbering, strength
   reduction.
9. Loops: natural loops; invariant code motion; induction variables; unrolling.
10. Inlining and interprocedural analysis; alias analysis, which is undecidable in general (Rice).
11. Instruction selection: tree tiling by maximal munch and by dynamic programming.
12. Register allocation:
    - interference graphs and Chaitin's coloring (1981), NP-hard by reduction from coloring;
    - simplify and spill;
    - **SSA interference graphs are chordal** (Hack et al. 2006), so they color optimally in polynomial time;
    - linear scan.
13. Instruction scheduling: list scheduling on the dependence DAG; software pipelining (callback to Part 7).
14. The Job compiled from the Pebble language, unoptimized against optimized. Ledger row 5.
15. Correctness: Csmith's compiler bugs (Yang et al. 2011); translation validation; CompCert previewed (Part 41).
16. LLVM and MLIR; superoptimization. Outro.

*Computed:* our compiler with each pass switched on in turn: instructions and cycles on Pebble; fixpoint iterations;
coloring with spills; a chordality check on SSA interference graphs.
*Visuals:* dataflow facts flowing around the CFG as colored tokens; φs landing at dominance frontiers; the
interference graph being colored; the code shrinking pass by pass.
*Reading:* the Dragon Book; Cooper & Torczon, *Engineering a Compiler*; Appel, *Modern Compiler Implementation in
ML*; Muchnick, *Advanced Compiler Design and Implementation*; Rastello & Bouchez, *SSA-based Compiler Design*;
Nielson, Nielson & Hankin, *Principles of Program Analysis*; Cytron et al. 1991; Chaitin 1981; Kildall 1973; Hack et
al. 2006; Poletto & Sarkar 1999; Lattner & Adve 2004.

### Part 13 · Lambda and Types (~60)
*Story:* Church's λ-calculus is a whole programming language made of functions alone. Types tame it. Well-typed
programs cannot go wrong, which we prove. A type can be inferred without being written. And types turn out to be
propositions and programs to be proofs, which is the foundation of the proof assistants of Part 41.
1. λ-terms: free and bound variables, α-equivalence, capture-avoiding substitution.
2. β-reduction, normal forms, Ω = (λx.xx)(λx.xx).
3. Programming in pure λ: booleans, numerals, pairs, lists, arithmetic; the predecessor (Kleene's trick, said to have
   come to him at the dentist).
4. Recursion: the Y combinator derived; fixed points.
5. Reduction strategies: normal order, call-by-value, call-by-name, call-by-need; standardization.
6. **Church–Rosser** confluence (by parallel reduction and the diamond property, animated).
7. De Bruijn indices; environments against substitution (Part 14).
8. Why types: Milner's slogan (1978). The simply typed λ-calculus, with typing rules as inference rules and
   derivation trees on screen.
9. **Type safety = progress + preservation**, proved for a small language by induction on derivations.
10. Strong normalization of STLC (Tait's method, sketched): every well-typed term terminates, so STLC is not
    Turing-complete.
11. Hindley–Milner: algorithm W and unification (Robinson 1965), animated; let-polymorphism; the exponential worst
    case.
12. System F (Girard 1972, Reynolds 1974); parametricity and theorems for free (Wadler 1989).
13. **Curry–Howard**: implication, conjunction and disjunction as function, product and sum types; a proof as a
    program; call/cc and Peirce's law (Griffin 1990).
14. Dependent types: Π and Σ; Martin-Löf; the calculus of constructions; Lean and Rocq (Part 41).
15. Linear and affine types, and Rust's ownership and borrowing (Part 42).
16. Algebraic data types and pattern matching; subtyping and variance; gradual typing. Outro.

*Computed:* our λ reducer (β-step counts, Church arithmetic); HM inference, including the exponential let; typing
derivations generated by our checker.
*Visuals:* β-reduction rewriting a subtree; Church numerals as stacked function boxes; the Church–Rosser diamond;
unification merging nodes; the Curry–Howard dictionary.
*Reading:* Pierce, *Types and Programming Languages*; Harper, *Practical Foundations for Programming Languages*;
Barendregt, *The Lambda Calculus*; Hindley & Seldin; Sørensen & Urzyczyn, *Lectures on the Curry–Howard
Isomorphism*; Girard, Lafont & Taylor, *Proofs and Types*; Wadler 1989, 2015; Milner 1978; Damas & Milner 1982.

### Part 14 · Runtimes (~55)
*Story:* A program needs a runtime to live in. Environments make closures, continuations turn the stack into data,
and a virtual machine provides a portable instruction set. The garbage collector cleans up memory while the program
keeps running, kept correct by an invariant stated in three colors.
1. Interpreters: SICP's eval/apply.
2. Environments and closures; lexical against dynamic scope; the funarg problem (Moses 1970); closure conversion.
3. Continuations and CPS: the stack made explicit; tail calls as jumps; call/cc; exceptions and generators from
   continuations.
4. Bytecode VMs, stack against register (Lua 5); dispatch costs and threaded code; the Pebble VM.
5. Why garbage collection exists (McCarthy 1960).
6. Reference counting: cycles; deferred RC; Python's hybrid.
7. Tracing collectors:
   - mark–sweep and mark–compact;
   - Cheney's copying collector (1970), animated with its two pointers;
   - the cost model, with GC cost proportional to live data and amortized cost ~ live/(heap − live).
8. The generational hypothesis (Ungar 1984); remembered sets and write barriers.
9. Incremental and concurrent GC: the tri-color invariant (Dijkstra et al. 1978), strong and weak;
   snapshot-at-the-beginning against incremental update; pause times (Go, ZGC).
10. JITs: method against tracing; inline caches and PICs (Deutsch & Schiffman 1984; Self); hidden classes;
    speculation and deoptimization (Hölzle 1992); tiers.
11. Dynamic dispatch: vtables, interfaces, multiple dispatch.
12. Implementing exceptions: zero-cost tables against setjmp.
13. WebAssembly: a sandboxed stack machine with structured control flow, where validation is type checking.
14. Other paradigms: logic programming (Prolog as resolution and unification, callback to *AI, Built* 2), actors
    (Erlang), dataflow.
15. The Job in the λ-core, garbage-collected. Ledger row 6. Outro.

*Computed:* interpreter against VM against compiled code; mark–sweep, copying and generational collectors on
allocation traces, with their pause distributions; inline-cache hit rates.
*Visuals:* the heap as cells and arrows; the mark wavefront painting tri-color; Cheney's scan and free pointers; a
closure capturing its environment frame.
*Reading:* Abelson & Sussman, *SICP* ch. 4–5; Friedman & Wand, *Essentials of Programming Languages*; Appel,
*Compiling with Continuations*; Jones, Hosking & Moss, *The Garbage Collection Handbook*; Smith & Nair, *Virtual
Machines*; Nystrom; Ierusalimschy et al. 2005; Hölzle et al. 1991–92; Haas et al. 2017.

---

## Act IV · Algorithms

### Part 15 · Counting Steps (~60)
*Story:* The Job v0 is quadratic, and no hardware from Act II rescues it. Sorting is where computer science learned
to count steps: recursion trees, a lower bound that comes from information, and a randomized algorithm whose average
case, 2n ln n, is a small piece of calculus.
1. The ledger so far, and the question it raises: can thinking beat silicon?
2. Models of computation: the RAM and the word-RAM (w ≥ log n); the pitfalls of unit cost; cell probes; Turing time
   against RAM time (polynomially related).
3. Asymptotic notation, precisely; the growth-rate ladder on log–log axes; Stirling's formula.
4. Insertion sort: a loop-invariant proof; inversions, n(n − 1)/4 expected (derived).
5. Merge sort: the recursion tree for T(n) = 2T(n/2) + n, drawn; the substitution method.
6. The **master theorem** in its three cases, with the recursion-tree geometry; Akra–Bazzi.
7. The **comparison lower bound**: decision trees; log₂ n! = n log₂ n − n log₂ e + O(log n); each comparison gives at
   most one bit (callback to *AI, Built* 1); Ford–Johnson merge insertion for small n.
8. Heapsort; heapify in O(n) (the sum Σ h/2ʰ derived).
9. Quicksort (Hoare 1961): expected comparisons 2n ln n ≈ 1.39 n log₂ n, derived from the fact that i and j are
   compared exactly when one of them is the first pivot chosen in their range (probability 2/(j − i + 1));
   randomization; median-of-three; dual-pivot.
10. Concentration of quicksort's running time (a simulated histogram, with the tail bound).
11. Beating n log n: counting sort, radix sort, bucket sort; integer sorting on the word-RAM (Han, cited).
12. Selection: quickselect; **median of medians** (Blum, Floyd, Pratt, Rivest & Tarjan 1973), with T(n) ≤ T(n/5) +
    T(7n/10) + O(n) solved.
13. Generating functions: Fibonacci and Catalan in closed form (*Concrete Mathematics*); a glimpse of analytic
    combinatorics, with asymptotics read off singularities.
14. Amortized analysis: aggregate, accounting and potential; the dynamic array; why the growth factor 1.5 helps memory
    reuse.
15. Practice: Timsort and the 2015 bug found by formal verification (de Gouw et al.); pdqsort; stability; external
    k-way merge sort, with replacement selection's 2M runs.
16. The Job v1, sort then count. Ledger row 7. Outro.

*Computed:* comparison counts for every sort on random, sorted and adversarial input, fitted to their formulas; the
quicksort histogram; the decision-tree bound against Ford–Johnson for n ≤ 12; timings on this machine; the Job v1.
*Visuals:* bars with the invariant region lit; recursion trees summing level by level; a decision tree whose leaves
are permutations; the growth ladder as the camera pulls out.
*Reading:* Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms* (CLRS) ch. 1–9, 16; Knuth, TAOCP 3 ch. 5;
Sedgewick & Flajolet, *An Introduction to the Analysis of Algorithms*; Graham, Knuth & Patashnik, *Concrete
Mathematics*; Kleinberg & Tardos ch. 2, 5; Erickson, *Algorithms*; Flajolet & Sedgewick, *Analytic Combinatorics*;
Hoare 1962; Blum et al. 1973; de Gouw et al. 2015.

### Part 16 · Data Structures (~60)
*Story:* The Job is a dictionary problem: insert, look up, count. Hashing does it in expected constant time, if the
hash function can't be gamed. Balanced trees guarantee their time, and splay trees earn it on average. The ledger
records an order-of-magnitude drop.
1. Abstract data types against implementations; the dictionary.
2. Hashing and the birthday bound, 1 − e^{−n²/2m} (derived).
3. Chaining: expected length α; **universal hashing** (Carter & Wegman 1979), with ((ax + b) mod p) mod m proved
   universal; hash flooding (2011) and SipHash.
4. Open addressing:
   - linear probing's ½(1 + 1/(1 − α)²) (Knuth 1963, his first analysis of an algorithm), with primary clustering
     shown;
   - 5-independence suffices (Pagh, Pagh & Ružić);
   - double hashing, Robin Hood hashing, Swiss tables.
5. Cuckoo hashing (Pagh & Rodler 2001): the cuckoo graph, worst-case O(1) lookups, the ½ load threshold.
6. Optimal open addressing without reordering (Farach-Colton, Krapivin & Kuszmaul, 2024–25), which disproves Yao's
   1985 conjecture **(verify)**. Perfect hashing (FKS 1984).
7. BSTs: random BSTs have expected depth ~2 ln n, the same as quicksort (proved by the bijection).
8. Rotations; AVL trees, with height ≤ 1.44 log₂ n via Fibonacci trees; red–black trees **as 2–3–4 trees**
   (Guibas & Sedgewick 1978), morphing between the two; left-leaning red–black trees.
9. Treaps and skip lists (Pugh 1990).
10. Splay trees (Sleator & Tarjan 1985): the access lemma by potential (proved); the working-set and static
    optimality theorems; the dynamic optimality conjecture, open since 1985.
11. B-trees (Bayer & McCreight 1970): fan-out and height log_B n (Part 33).
12. Priority queues: binomial, **Fibonacci heaps** (Fredman & Tarjan 1987) with O(1) amortized decrease-key, pairing
    heaps.
13. **Union–find**: union by rank and path compression, O(m α(n)) (Tarjan 1975); Ackermann's function; the log*
    argument.
14. Tries and radix trees; rank and select; succinct structures (Part 20 builds on them).
15. Persistent structures (path copying, Okasaki); cache-friendliness (callback to Part 8).
16. The Job v2, a hash table on Pebble and natively. Ledger row 8: rows 0 → 8 against rows 0 → 4, with the verdict
    from the data. Outro.

*Computed:* probe-count distributions against Knuth's formula over α; cuckoo failure rates; BST depths; AVL
worst cases; splay amortized costs on access sequences; union–find path lengths; the Job v2.
*Visuals:* buckets filling while clusters form; rotations as smooth morphs; 2–3–4 ↔ red–black; a zig-zig splay;
a union–find forest flattening.
*Reading:* CLRS ch. 10–13, 18–19, 21; Knuth, TAOCP 3 ch. 6; Sedgewick & Wayne, *Algorithms* ch. 3; Tarjan, *Data
Structures and Network Algorithms*; Mehlhorn & Sanders, *Algorithms and Data Structures*; Okasaki, *Purely Functional
Data Structures*; Navarro, *Compact Data Structures*; Carter & Wegman 1979; Pagh & Rodler 2004; Sleator & Tarjan
1985; Fredman & Tarjan 1987.

### Part 17 · Graphs (~60)
*Story:* Euler invented the graph to walk the bridges of Königsberg. Graphs are now the shape of road maps, the
internet, compilers and markets. Dijkstra designed his algorithm in twenty minutes at a café, and in 2024–25 it was
proved universally optimal and also beaten. Flows and cuts turn out to be two faces of one theorem.
1. Königsberg (1736): Eulerian circuits by degree (proved); representations and their costs.
2. BFS: layers, unweighted shortest paths, bipartiteness.
3. DFS: discovery and finish times, the parenthesis theorem, edge classes, the white-path theorem.
4. Topological sort (DFS order; Kahn); DAGs in build systems, spreadsheets and Part 12's compiler.
5. SCCs: Kosaraju, and Tarjan's one-pass low-links (animated); the condensation; 2-SAT via SCCs.
6. Dijkstra (1956/59):
   - correctness by invariant;
   - heaps, and Fibonacci heaps for O(m + n log n);
   - the wavefront spreading over a city grid.
7. The frontier: Dijkstra is universally optimal (Haeupler et al. 2024); directed SSSP beyond the sorting barrier,
   O(m log^{2/3} n) (Duan et al. 2025) **(verify)**.
8. Negative edges: Bellman–Ford, negative cycles, arbitrage as a negative cycle in −log rates; distance-vector
   routing (Part 34).
9. All pairs: Floyd–Warshall as DP; Johnson's reweighting by potentials (proved); the min-plus product and the APSP
   conjecture (Part 25).
10. A* (callback to *AI, Built* 2), landmarks, contraction hierarchies (how a map app answers in microseconds).
11. MSTs: the cut and cycle properties (proved); Kruskal (with Part 16's union–find), Prim, Borůvka (1926, for the
    Moravian grid); randomized linear time (Karger, Klein & Tarjan).
12. **Max-flow min-cut**: Ford–Fulkerson, residual graphs, the theorem (proved), Edmonds–Karp, push–relabel; the
    almost-linear-time max flow (Chen et al. 2022).
13. Matching: bipartite matching as flow; Hall's theorem and König; the Hungarian algorithm; **Gale–Shapley** (1962,
    with stability proved) and the residency match.
14. Easy and hard: Euler tours against Hamiltonian cycles (Part 24).
15. PageRank (Brin & Page 1998) as a random surfer's stationary distribution, by power iteration (callback to *AI,
    Built* 5).
16. Planarity: Euler's V − E + F = 2; the four-color theorem (1976, verified in Coq in 2005). Outro.

*Computed:* BFS, DFS and SCC traces; Dijkstra against A* against bidirectional node counts; arbitrage detection; the
MST algorithms; Edmonds–Karp augmentations; Gale–Shapley; PageRank on a synthetic web.
*Visuals:* the Dijkstra wavefront; DFS as a thread through a maze with parenthesis intervals; flows as water in
pipes, and the min cut as a slice; proposals in stable matching.
*Reading:* CLRS ch. 20–26; Kleinberg & Tardos ch. 3, 4, 7; Tarjan; Ahuja, Magnanti & Orlin, *Network Flows*; Even,
*Graph Algorithms*; Schrijver, *Combinatorial Optimization*; Dijkstra 1959; Ford & Fulkerson 1956; Tarjan 1972; Gale &
Shapley 1962; Chen et al. 2022; Haeupler et al. 2024.

### Part 18 · The Great Paradigms (~60)
*Story:* Most good algorithms come from a handful of ideas: be greedy when an exchange argument allows it, divide
and conquer, or remember subproblems. Divide and conquer, applied to the right points (the roots of unity), gives
the most important algorithm of the century, the FFT. The same problem solved four ways closes the part.
1. Greedy: activity selection by an exchange argument; Huffman revisited (callback to *AI, Built* 1); where greedy
   fails.
2. **Matroids**: greedy is optimal exactly on matroids (Rado–Edmonds, proved); the graphic matroid is Kruskal.
3. Karatsuba (1960), which refuted Kolmogorov's n² conjecture: three products for n^{log₂ 3}; Toom–Cook.
4. Strassen (1969): seven products, derived; the history of ω from 2.81 to about 2.3713 (2024) **(verify)**;
   galactic algorithms; AlphaTensor (callback to *AI, Built* 26).
5. **The FFT, I**: coefficients against values; multiplication is pointwise on values; choosing the points as the
   roots of unity, whose squares fall onto half as many points (the centerpiece animation).
6. **The FFT, II**: Cooley–Tukey (1965, and Gauss c. 1805); the butterfly; bit reversal; the inverse by conjugation
   (orthogonality of characters, proved); O(n log n).
7. Applications: big-integer multiplication, convolution, spectra (callback to *Analysis, Built* 9);
   Schönhage–Strassen (1971); Harvey & van der Hoeven's O(n log n) (2019); the NTT over finite fields (Part 28).
8. Closest pair in the plane (the strip argument, with at most seven neighbours).
9. **Dynamic programming**: Bellman (1957) and the story of the name; memoization against tabulation; DP as
   shortest paths in a DAG.
10. Edit distance (Wagner–Fischer), with the table filling and its traceback; LCS (Part 20 takes up diff).
11. Knapsack's O(nW), and why that isn't polynomial (W is written in log W bits); subset sum (Part 24).
12. Matrix chains; optimal BSTs and Knuth's O(n²) speedup (the quadrangle inequality).
13. DP on trees and graphs: independent sets on trees; Floyd–Warshall and Bellman–Ford as DP; **Held–Karp** TSP in
    O(n²2ⁿ) against n!.
14. Viterbi and CYK as DP (callbacks to *AI, Built* 7 and Part 11); DP speedups (convex-hull trick, divide-and-conquer
    optimization).
15. Backtracking and branch-and-bound: n-queens; Sudoku as exact cover with **Dancing Links** (Knuth 2000).
16. One problem, four paradigms: maximum subarray by brute force O(n³), divide and conquer O(n log n), and Kadane's
    DP O(n). Outro.

*Computed:* the Karatsuba crossover on this machine; Strassen's operation counts; our FFT against the DFT; FFT
big-number multiplication (a million digits of π by Chudnovsky's series); edit-distance tables; Held–Karp against
brute force; Dancing Links on Sudoku.
*Visuals:* the roots of unity squaring onto half as many points; butterflies; Strassen's seven products as colored
blocks; DP tables with traceback arrows; matroid exchange.
*Reading:* CLRS ch. 4, 14–15, 30; Kleinberg & Tardos ch. 4–6; Dasgupta, Papadimitriou & Vazirani, *Algorithms* ch. 2,
5–6; Knuth, TAOCP 2 §4.3.3 and 4B; Cooley & Tukey 1965; Strassen 1969; Karatsuba & Ofman 1962; Harvey & van der
Hoeven 2021; Bellman 1957; Edmonds 1971; Alman et al. 2024.

### Part 19 · Randomness as a Resource (~55)
*Story:* A coin flip can stand in for cleverness. With one, you can check a matrix product in n², find a minimum
cut by contracting random edges, test primality in milliseconds, and count the top words of thirty novels in a few
kilobytes. Randomness has to come from somewhere, though, and some generators hide fifteen planes.
1. Las Vegas against Monte Carlo; amplification.
2. Freivalds (1977), error ≤ ½ per round (proved).
3. The **Schwartz–Zippel** lemma (proved); perfect matchings via the Tutte matrix (Lovász 1979); fingerprints.
4. **Karger's min cut** (1993): success ≥ 2/(n(n − 1)) (proved); Karger–Stein; at most C(n, 2) min cuts as a
   corollary.
5. Primality: Fermat and the Carmichael numbers; **Miller–Rabin** (error ≤ ¼); AKS (2002). Part 28 needs big
   primes.
6. Random walks: 2-SAT in O(n²) expected (gambler's ruin); Schöning's (4/3)ⁿ for 3-SAT; Reingold's SL = L (cited).
7. Balls into bins: max load log n/log log n, and with two choices log log n/log 2 (simulated).
8. Bloom filters (1970): false positives (1 − e^{−kn/m})ᵏ, optimal k = (m/n) ln 2 (derived); counting and cuckoo
   filters.
9. Streaming: reservoir sampling (proved uniform); Misra–Gries; **Count-Min** with its (ε, δ) guarantee. The Job
   in kilobytes. Ledger row 9.
10. Distinct counting: Flajolet–Martin, **HyperLogLog** (error ≈ 1.04/√m), KMV.
11. The AMS F₂ sketch (1996) from 4-wise independent signs (callback to *AI, Built* 3's Johnson–Lindenstrauss).
12. LSH (Indyk & Motwani 1998): MinHash and SimHash; near-duplicate paragraphs in the novels.
13. The probabilistic method: R(k, k) > 2^{k/2}; the Lovász local lemma and Moser–Tardos (2010).
14. Derandomization:
    - conditional expectations (MAX-CUT ≥ m/2);
    - pairwise independence;
    - expanders (Part 25);
    - where random bits come from: LCGs and **RANDU's fifteen planes** in 3D, Mersenne Twister, cryptographic PRGs
      (Part 27).
15. Outro.

*Computed:* Freivalds error rates; Karger's success rate against the bound; Miller–Rabin on Carmichael numbers;
max loads; Bloom filters against theory; Count-Min and HLL on the novels; MinHash duplicates; RANDU.
*Visuals:* a graph contracting edge by edge; bins filling with one and two choices; **RANDU's cube rotating until the
planes appear**; a Bloom bit array lighting up.
*Reading:* Motwani & Raghavan, *Randomized Algorithms*; Mitzenmacher & Upfal, *Probability and Computing*; Alon &
Spencer, *The Probabilistic Method*; Cormode & Yi, *Small Summaries for Big Data*; Muthukrishnan, *Data Streams*;
Knuth, TAOCP 2 ch. 3; Karger 1993; Flajolet et al. 2007; Alon, Matias & Szegedy 1996; Moser & Tardos 2010.

### Part 20 · Strings (~55)
*Story:* Text is the oldest data. Searching it efficiently led to automata built from patterns, then to indexes of
every suffix, then to a reversible transform that sorts a book into compressible runs and lets you search the
compressed result. Each `git diff` runs a shortest-path algorithm on a grid.
1. Matching: naive O(nm) and its worst cases.
2. Rabin–Karp: rolling hashes mod p and their collision probability.
3. **KMP** (1977): the failure function as an automaton (callback to Part 11); amortized linear time (proved).
4. Boyer–Moore: bad-character and good-suffix rules; sublinear on average (why grep is fast).
5. Aho–Corasick (1975): many patterns at once, with failure links in a trie.
6. Suffix tries and **suffix trees** (Weiner 1973; Ukkonen 1995, sketched); longest repeats; generalized trees for
   LCS.
7. **Suffix arrays** (Manber & Myers 1990): prefix doubling; SA-IS in linear time (sketched); LCP arrays (Kasai);
   O(m log n) search.
8. **The Burrows–Wheeler transform** (1994): the rotation matrix; why it clusters characters; invertibility via LF
   mapping (proved, animated); move-to-front; bzip2.
9. The **FM-index** (Ferragina & Manzini 2000): backward search in compressed space; genome aligners; the novels
   indexed.
10. Compression:
    - LZ77 and LZ78/LZW;
    - LZ is asymptotically optimal for stationary ergodic sources;
    - DEFLATE as LZ77 plus Huffman (callback to *AI, Built* 1);
    - ANS (Duda) and zstd.
11. Alignment: Needleman–Wunsch, Smith–Waterman, affine gaps, BLAST; **no O(n^{2−ε}) edit distance under SETH**
    (Backurs & Indyk 2015; Part 25).
12. **Myers' diff** (1986): the O(ND) algorithm on the edit graph (diagonals and snakes); patience diff; three-way
    merge.
13. Rolling hashes at scale: content-defined chunking; rsync (Tridgell 1996); dedup.
14. Periodicity: Fine–Wilf; Manacher; Lyndon words. Outro.

*Computed:* comparison counts for each matcher on the novels; the suffix array and BWT of a chapter; FM-index
queries; our LZ77-plus-Huffman compressor against zlib; Myers' diff on revisions of this repository's own files;
rsync chunking.
*Visuals:* the KMP automaton; the BWT's rotation matrix sorting, with its clustered last column; LF arrows walking
the text back out; snakes in the edit graph; LZ back-references as arcs over the text.
*Reading:* Gusfield, *Algorithms on Strings, Trees, and Sequences*; Crochemore, Hancart & Lecroq, *Algorithms on
Strings*; Mäkinen, Belazzougui, Cunial & Tomescu, *Genome-Scale Algorithm Design*; Navarro; Salomon & Motta,
*Handbook of Data Compression*; Knuth, Morris & Pratt 1977; Burrows & Wheeler 1994; Ferragina & Manzini 2000; Ziv &
Lempel 1977–78; Myers 1986.

### Part 21 · Geometry (~55)
*Story:* Geometry looks easy until a computer gets it wrong: a floating-point orientation test can say a point lies
on both sides of a line. Get the predicates right and beautiful structure follows. Voronoi diagrams grow as a
parabolic beach line, and every Delaunay triangulation is the shadow of a convex hull on a paraboloid.
1. The primitive: orientation as the sign of a determinant (an area). Robustness: floating-point orientation fails
   (the Kettner et al. grids, computed); Shewchuk's adaptive exact predicates.
2. Convex hulls: Jarvis O(nh), Graham O(n log n), monotone chain; the Ω(n log n) lower bound by reduction from
   sorting (proved); Chan's O(n log h) (1996); quickhull; 3D.
3. The sweep line: Bentley–Ottmann (1979), with its event queue and status structure animated.
4. Triangulating polygons: **the art gallery theorem** (Chvátal 1975; Fisk's three-coloring proof); monotone pieces;
   ear clipping.
5. Voronoi diagrams; **Fortune's sweep** (1986) and its beach line of parabolas.
6. Delaunay triangulations: the empty circle; max–min angle; Lawson flips terminate; duality with Voronoi.
7. **The lifting map**: Delaunay = the lower hull of points lifted to z = x² + y² (a 3D tour). The in-circle test as a
   4 × 4 determinant falls out of it.
8. Randomized incremental construction and backwards analysis: expected O(n log n) Delaunay.
9. Low-dimensional LP: Seidel's randomized algorithm (1991); Megiddo's linear time for fixed d.
10. Range searching: kd-trees (Bentley 1975), with O(√n + k) queries; range trees and fractional cascading;
    interval and segment trees.
11. Point location with trapezoidal maps.
12. High dimensions: the curse; LSH (callback to Part 19); graph-based ANN (HNSW).
13. Duality and arrangements; the ham-sandwich theorem.
14. Uses: configuration spaces and Minkowski sums in robot motion planning; Ruppert's meshing; BVHs (Part 38).
    Outro.

*Computed:* floating-point orientation failure maps; hull counts and timings; Bentley–Ottmann events; Fortune frames;
Delaunay via the lifting map, cross-checked against scipy's hull; kd-tree visits; Fisk's guards.
*Visuals:* the speckled failure grid near a line; Fortune's beach line; Delaunay rising onto the paraboloid; sweep
events.
*Reading:* de Berg, Cheong, van Kreveld & Overmars, *Computational Geometry: Algorithms and Applications*; Preparata &
Shamos; O'Rourke, *Computational Geometry in C*; Devadoss & O'Rourke, *Discrete and Computational Geometry*;
Edelsbrunner, *Geometry and Topology for Mesh Generation*; Shewchuk 1997; Kettner et al. 2008; Fortune 1987; Seidel
1991; Chan 1996.

### Part 22 · Optimization (~60)
*Story:* Many problems are "choose the best point of a polytope." The simplex method walks the polytope's edges.
Duality certifies the answer from the other side. When integrality makes a problem hard, LP relaxations and random
hyperplanes still get provably close. Online, without seeing the future, you can still be competitive.
1. Kantorovich (1939), Dantzig (1947), Stigler's diet; standard form; the feasible region as a 3D polytope.
2. Optima at vertices; basic feasible solutions; **simplex** walking edges (3D), with the pivot algebra.
3. **Duality**: the dual built by bounding the objective; weak and strong duality, via Farkas' lemma and a
   separating hyperplane; complementary slackness; shadow prices.
4. The Klee–Minty cube (2ⁿ pivots); smoothed analysis (Spielman & Teng 2001) explains practice.
5. Polynomial time: the ellipsoid method (Khachiyan 1979; volume shrinks by e^{−1/(2(n+1))}); separation ≡
   optimization (Grötschel, Lovász & Schrijver); interior point (Karmarkar 1984), with the central path, the log
   barrier and Newton steps (callback to *AI, Built* 4).
6. LPs for combinatorics: max-flow/min-cut duality (Part 17); **total unimodularity** gives integral vertices
   (proved for bipartite incidence matrices).
7. Integer programming: NP-hard; relaxations and integrality gaps; branch and bound; Gomory cuts; decades of solver
   speedups (Bixby, cited).
8. Approximation: vertex cover 2 by maximal matching and by LP rounding; greedy set cover H_n ≈ ln n (proved), and
   ln n hardness (Part 25).
9. TSP:
   - inapproximable in general (via Hamiltonian cycle);
   - metric TSP: double tree 2, Christofides–Serdyukov 3/2, and 3/2 − 10⁻³⁶ (Karlin, Klein & Oveis Gharan);
   - Arora's Euclidean PTAS;
   - 2-opt and LKH; Concorde's 85,900 cities (cited).
10. Knapsack FPTAS by rounding.
11. **Goemans–Williamson** MAX-CUT: vectors on a sphere, a random hyperplane, cut probability θ/π, and 0.878 =
    min 2θ/(π(1 − cos θ)) (derived); optimal under the UGC (Part 25).
12. Online algorithms: ski rental (2, and e/(e − 1) randomized); paging, where LRU is k-competitive and no
    deterministic algorithm does better (proved); randomized marking, O(log k).
13. **Multiplicative weights**: regret O(√(T log n)); one algorithm behind boosting (callback to *AI, Built* 6), von
    Neumann's minimax theorem, and fast approximate LP (Arora, Hazan & Kale).
14. Convex optimization in a page (callbacks to *AI, Built* 4 and 11). Outro.

*Computed:* our simplex on 3D examples and Klee–Minty pivot counts; ellipsoid steps; the central path; LP gaps; TSP
heuristics against exact solutions (Held–Karp for small n); GW against exact MAX-CUT for small graphs; paging ratios
on the Job's page trace; MW regret.
*Visuals:* the polytope with the simplex walk; the dual as a family of tilted planes; ellipsoids shrinking; a
hyperplane slicing a sphere of unit vectors; the squashed Klee–Minty cube.
*Reading:* Bertsimas & Tsitsiklis, *Introduction to Linear Optimization*; Chvátal, *Linear Programming*; Matoušek &
Gärtner, *Understanding and Using Linear Programming*; Schrijver, *Theory of Linear and Integer Programming*;
Williamson & Shmoys, *The Design of Approximation Algorithms*; Vazirani, *Approximation Algorithms*; Borodin &
El-Yaniv, *Online Computation and Competitive Analysis*; Applegate, Bixby, Chvátal & Cook, *The Traveling Salesman
Problem*; Boyd & Vandenberghe; Goemans & Williamson 1995; Arora, Hazan & Kale 2012; Karlin, Klein & Oveis Gharan 2021.

---

## Act V · Limits and Secrets

### Part 23 · Undecidable (~55)
*Story:* Part 1 proved that one problem can't be solved. This part finds the same impossibility in Diophantine
equations, in tilings of the plane, in Gödel's theorem and in randomness itself. A program can print its own source,
and that fact is enough to prove all of it. The busy beaver marks where provability runs out.
1. Formally: decidable, recognizable, co-recognizable; the halting set K.
2. Mapping reductions; A_TM, E_TM, EQ_TM; recognizable but undecidable; neither.
3. **Rice's theorem** (proved): every non-trivial semantic property is undecidable. What that means for compilers,
   antivirus and static analysis, and how Part 41 escapes it by approximation.
4. **The recursion theorem** (Kleene): programs that know their own code; quines in the Pebble language and in
   Python; a shorter proof of halting's undecidability.
5. Post's correspondence problem (1946), via computation histories (dominoes animated); ambiguity of CFGs (callback
   to Part 11).
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
*Reading:* Sipser ch. 4–6; Rogers, *Theory of Recursive Functions and Effective Computability*; Soare, *Turing
Computability*; Boolos, Burgess & Jeffrey, *Computability and Logic*; Li & Vitányi, *An Introduction to Kolmogorov
Complexity*; Davis 1973; Matiyasevich, *Hilbert's Tenth Problem*; Chaitin 1975; Aaronson 2020; Smith et al. 2023.

### Part 24 · P versus NP (~60)
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
8. Strong against weak NP-hardness; pseudo-polynomial algorithms (knapsack, Part 18).
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
    lives (Parts 27–28).
16. If P = NP: Gödel's letter, and the consequences. Outro.

*Computed:* our reductions, implemented and verified (a SAT instance → 3-coloring → solved → mapped back); a
Cook–Levin tableau for a tiny NTM; our CDCL solver on reduced instances; the 3-SAT phase transition with our solver;
generalized geography.
*Visuals:* the tableau grid with sliding windows; gadget graphs assembling; the reduction family tree; the five
worlds as a map; the class zoo as nested sets, zoomed.
*Reading:* Sipser ch. 7–8; Arora & Barak, *Computational Complexity: A Modern Approach* ch. 1–6; Papadimitriou,
*Computational Complexity*; Garey & Johnson, *Computers and Intractability*; Moore & Mertens ch. 4–6; Goldreich, *P,
NP, and NP-Completeness*; Cook 1971; Karp 1972; Levin 1973; Aaronson, "P =? NP" (2016); Impagliazzo 1995; Fortnow, *The
Golden Ticket*.

### Part 25 · Proofs and Randomness (~60)
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
   fooling sets and rank; streaming lower bounds (callback to Part 19).
5. Interactive proofs: graph non-isomorphism; GMR (1985), Babai's Arthur–Merlin.
6. Arithmetization and **sum-check** (Lund, Fortnow, Karloff & Nisan 1990), step by step over a finite field; #SAT ∈
   IP; **IP = PSPACE** (Shamir 1990).
7. **Zero knowledge**: Ali Baba's cave; GMW's 3-coloring protocol with commitments; simulation; Fiat–Shamir (Part 28).
8. **The PCP theorem** (AS, ALMSS 1992; Dinur 2005): checking a proof by reading O(1) bits; gap amplification.
9. Hardness of approximation: MAX-3SAT can't beat 7/8 (Håstad 2001), so a random assignment is optimal; clique
   n^{1−ε}; set cover ln n.
10. The **Unique Games Conjecture** (Khot 2002): vertex cover 2 and MAX-CUT 0.878 would be optimal (Part 22); the
    2-to-2 theorem (2018).
11. Fine-grained complexity: SETH, OV, 3SUM, APSP; edit distance (Part 20); what conditional lower bounds buy.
12. Parameterized complexity: FPT; vertex cover by bounded search trees; kernels (Buss); W[1]-hardness of clique;
    treewidth and Courcelle.
13. Counting: #P (Valiant 1979); the permanent against the determinant; Toda's theorem; approximate counting
    (Jerrum, Sinclair & Vigoda; callback to MCMC).
14. Average case and one-way functions, the bridge to Part 27. Outro.

*Computed:* Adleman's union bound in numbers; sum-check on a small #SAT instance, where a cheating prover is caught
with the computed probability; ZK 3-coloring with cheating probability (1 − 1/m)ᵏ; equality by fingerprints; random
assignments against the best found on MAX-3SAT; FPT vertex cover; permanent against determinant timings.
*Visuals:* a DNF collapsing under a random restriction; sum-check's rounds as univariate polynomials; a ZK coloring
revealing one edge; the PCP verifier sampling a few bits from a giant proof.
*Reading:* Arora & Barak ch. 7–11, 13–14, 18–22; Goldreich, *Computational Complexity: A Conceptual Perspective*;
Wigderson, *Mathematics and Computation*; Kushilevitz & Nisan, *Communication Complexity*; Jukna; Thaler, *Proofs,
Arguments, and Zero-Knowledge*; Cygan et al., *Parameterized Algorithms*; O'Donnell, *Analysis of Boolean Functions*;
Vassilevska Williams 2018 (survey); Håstad 2001; Khot 2002; Dinur 2007; Shamir 1992.

### Part 26 · Error-Correcting Codes (~55)
*Story:* In 1947 Hamming's weekend jobs kept dying on bad bits, so he taught the machine to fix them. A year later
Shannon proved that noise costs only a fixed fraction of the channel's rate, but not how to get there. It took fifty
years and several rediscoveries (Reed–Solomon, LDPC, turbo and polar codes) to reach that limit. We scratch a QR code
and get its message back.
1. Hamming at Bell Labs (1947–50); the binary symmetric channel; repetition codes.
2. Hamming distance and the Hamming cube (3D, 4D projected); d detects d − 1 errors and corrects ⌊(d − 1)/2⌋.
3. **Hamming(7,4)**: parity checks as a matrix; the syndrome names the bad bit; the Venn picture; a perfect code.
4. Bounds: Hamming (sphere packing), Singleton, Gilbert–Varshamov, on the rate–distance plane.
5. Linear codes and duality; the Golay code (Voyager, cited) and the Leech lattice, briefly.
6. Finite fields GF(p) and GF(2ᵐ) from irreducible polynomials (callback to Part 4's LFSRs); a cyclic multiplicative
   group.
7. **Reed–Solomon** (1960):
   - codewords as evaluations of polynomials, MDS by counting roots (proved);
   - erasures by Lagrange interpolation;
   - errors by **Berlekamp–Welch**, linear algebra on screen; Berlekamp–Massey;
   - CDs, QR codes, deep space, RAID-6.
8. **Our QR code**: encode a message, scratch the image, decode it back.
9. Cyclic codes and CRCs: polynomial division over GF(2) as a shift-register circuit; guarantees for burst errors;
   CRC-32 (Part 34).
10. **Shannon's channel coding theorem** (1948): BSC capacity 1 − H(p); random coding by typical sets (callback to
    *AI, Built* 1), proved; the converse via Fano.
11. Concatenated codes (Forney); convolutional codes and Viterbi (callbacks to *AI, Built* 7 and Part 18).
12. Turbo codes (1993) and the rediscovery of **LDPC** (Gallager 1962; MacKay & Neal): Tanner graphs, belief
    propagation (callback to *AI, Built* 7), density evolution, the computed waterfall.
13. **Polar codes** (Arıkan 2009): channel polarization computed and animated, with capacities splitting toward 0 and
    1; successive cancellation; 5G.
14. List decoding (Sudan, Guruswami–Sudan); locally decodable and testable codes and PCPs (Part 25).
15. Storage codes: RAID-5 and 6, LRCs (Azure), fountain and LT codes (Luby). Quantum codes previewed (Part 40).
    Outro.

*Computed:* Hamming(7,4) BER curves; the bounds; RS encode and decode of a scratched QR-like image; CRC detection
rates; random codes at small n; the LDPC waterfall; polarization.
*Visuals:* spheres around codewords in Hamming space; the Venn diagram; a polynomial through points with a corrupted
point pulled back; the polarization fan; messages flowing on a Tanner graph.
*Reading:* MacKay, *Information Theory, Inference, and Learning Algorithms*; Cover & Thomas ch. 7; Guruswami, Rudra &
Sudan, *Essential Coding Theory*; MacWilliams & Sloane; Roth, *Introduction to Coding Theory*; Richardson & Urbanke,
*Modern Coding Theory*; Lin & Costello; Hamming 1950; Reed & Solomon 1960; Gallager 1962; Berrou et al. 1993; Arıkan
2009; Shannon 1948.

### Part 27 · Secrets (~55)
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
   - **AES** (2001): SubBytes (inversion in GF(2⁸), callback to Part 26), ShiftRows, MixColumns (an MDS matrix),
     AddRoundKey;
   - the avalanche effect, where one flipped bit changes half the output.
8. Modes: **the ECB penguin** (computed on our own image); CBC and Vaudenay's padding oracle (2002); CTR.
9. Integrity: CBC-MAC and HMAC; authenticated encryption; GCM's GHASH as polynomial evaluation; ChaCha20-Poly1305.
10. Hashes:
    - the birthday bound 2^{n/2} (callback to Part 16);
    - Merkle–Damgård and length extension;
    - MD5 and SHA-1 collisions (Wang 2004; SHAttered 2017);
    - the **SHA-3 sponge**.
11. Hash applications: Merkle trees (git, certificate transparency, Part 36's blockchains); commitments; salted,
    slow, memory-hard password hashing (bcrypt, scrypt, Argon2).
12. Cryptanalysis on a toy SPN: differential (Biham & Shamir; DES's S-boxes, hardened against it in 1974) and linear
    (Matsui); meet-in-the-middle and why 2DES fails.
13. Side channels: timing (Kocher 1996) and constant-time code; power analysis; cache attacks on AES T-tables
    (callback to Parts 7–8).
14. Randomness failures: the Debian OpenSSL bug (2008); Dual_EC_DRBG. Outro.

*Computed:* frequency analysis breaking a cipher; an Enigma simulation and its cycle structures; the ECB penguin
(our own logo); AES from scratch against FIPS-197 vectors; avalanche statistics; a toy differential attack on a
4-round SPN; birthday collisions on truncated SHA-256.
*Visuals:* the penguin under ECB against noise under CBC; AES's 4 × 4 state transforming round by round; an avalanche
heatmap; rotors stepping; the sponge absorbing and squeezing.
*Reading:* Katz & Lindell, *Introduction to Modern Cryptography*; Boneh & Shoup, *A Graduate Course in Applied
Cryptography*; Goldreich, *Foundations of Cryptography* I–II; Menezes, van Oorschot & Vanstone, *Handbook of Applied
Cryptography*; Daemen & Rijmen, *The Design of Rijndael*; Ferguson, Schneier & Kohno, *Cryptography Engineering*;
Kahn, *The Codebreakers*; Singh, *The Code Book*; Shannon 1949; Heys' tutorial on linear and differential
cryptanalysis.

### Part 28 · Public Keys (~60)
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
9. Signatures and PKI: certificates, chains of trust, certificate transparency (Part 27's Merkle logs).
10. **TLS 1.3** (RFC 8446) as a sequence diagram between two simulated Pebbles: ECDHE, signatures, HKDF, AEAD;
    forward secrecy.
11. Shor's threat (Part 40), and "harvest now, decrypt later."
12. **Lattices**:
    - bases and shortest vectors; LLL (1982), animated in 2D;
    - **LWE** (Regev 2005) and worst-case to average-case reductions;
    - **ML-KEM** (FIPS 203, 2024): module-LWE with the NTT (callback to Part 18);
    - ML-DSA and SLH-DSA; Lamport one-time signatures and Merkle trees.
13. Zero knowledge in practice: Schnorr and Fiat–Shamir (Part 25); SNARKs from polynomial commitments (KZG), sketched.
14. Beyond: FHE (Gentry 2009, bootstrapping); MPC (Yao's garbled circuits; Shamir sharing, the Reed–Solomon
    polynomials again); differential privacy (callback to *AI, Built* 31). Outro.

*Computed:* extended-Euclid traces; 2048-bit RSA keys from our Miller–Rabin, checked; Pollard ρ timings as the
semiprimes grow; BSGS; the group law over ℝ and F_p; ECDSA nonce-reuse key recovery; a TLS-like transcript; LLL
breaking a toy knapsack; toy LWE and its noise; Shamir sharing.
*Visuals:* the elliptic curve's chord, third point and reflection; the F_p cloud; lattice bases reducing; LWE's
blurred lattice; the handshake.
*Reading:* Katz & Lindell ch. 9–14; Boneh & Shoup parts II–III; Hoffstein, Pipher & Silverman, *An Introduction to
Mathematical Cryptography*; Washington, *Elliptic Curves*; Silverman & Tate, *Rational Points on Elliptic Curves*;
Shoup, *A Computational Introduction to Number Theory and Algebra*; Crandall & Pomerance, *Prime Numbers*; Diffie &
Hellman 1976; Rivest, Shamir & Adleman 1978; Regev 2009; Peikert 2016; NIST FIPS 203–205 (2024); RFC 8446.

---

## Act VI · One Machine, Many Programs

### Part 29 · The Kernel (~55)
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
   callback to Part 16); EEVDF (Linux 6.6).
10. Multiprocessor scheduling: affinity, load balancing, work stealing (callback to Part 9).
11. Real time: rate-monotonic scheduling and **Liu–Layland's U ≤ n(2^{1/n} − 1) → ln 2** (1973, sketched); EDF is
    optimal; priority inversion on Mars Pathfinder (1997) and priority inheritance.
12. **Queueing theory**: Little's law L = λW (proved by areas); M/M/1's 1/(μ − λ) (derived) and its hockey stick;
    Pollaczek–Khinchine (variance matters); SRPT is optimal (Schrage 1968).
13. Kernel designs: monolithic, microkernel (Mach, L4; the Tanenbaum–Torvalds debate of 1992), exokernel, unikernel;
    seL4 (Part 41).
14. **PebbleOS boots on the emulator** and runs two processes doing the Job concurrently. Ledger row 10. Outro.

*Computed:* PebbleOS traces (traps, timer, context switches); simulations of FCFS, SJF, RR, MLFQ, stride and
CFS-lite; M/M/1 against the formula; RMS and EDF schedulability; context-switch cost on this machine.
*Visuals:* Gantt charts; the system call as a camera dive into the kernel and back; a queue's random walk under the
hockey-stick curve; the process state machine.
*Reading:* Arpaci-Dusseau & Arpaci-Dusseau, *Operating Systems: Three Easy Pieces* (OSTEP), virtualization of the
CPU; Tanenbaum & Bos, *Modern Operating Systems*; Silberschatz, Galvin & Gagne; Anderson & Dahlin, *Operating Systems:
Principles and Practice*; Cox, Kaashoek & Morris, *xv6*; Ritchie & Thompson 1974; Corbató et al. 1962; Liu & Layland
1973; Harchol-Balter, *Performance Modeling and Design of Computer Systems*; Kleinrock, *Queueing Systems*.

### Part 30 · Virtual Memory (~55)
*Story:* Every program believes it owns a huge, private, contiguous memory. None of them does. Address translation
maintains the illusion with a radix tree walked in hardware and cached in the TLB. Because memory is finite, some
page must leave, and Belady showed both which page is optimal and that adding memory can make things worse.
1. The problem: protection and relocation; Atlas (1962) invents paging.
2. Base and bounds; segmentation; external fragmentation (callback to Part 10).
3. Paging: VPN | offset split, animated; PTE bits (valid, protection, dirty, accessed).
4. Multi-level page tables as a radix-tree walk (x86-64 four and five levels); inverted and hashed tables.
5. **The TLB**, a cache for translations (callback to Part 8): reach, ASIDs, huge pages. The TLB-miss staircase is
   measured on this machine.
6. Page faults: demand paging and swapping; effective access time (why one fault per million accesses matters).
7. Replacement:
   - **Belady's OPT is optimal** (exchange argument);
   - FIFO and **Belady's anomaly** (a computed example where more frames give more faults);
   - LRU and the stack property, which rules out the anomaly (proved);
   - CLOCK and WSClock; 2Q, ARC, LIRS.
8. Working sets (Denning 1968) and thrashing; the Job's trace replayed through every policy, with miss curves
   against frames.
9. Copy-on-write fork; zero pages; mmap; shared libraries (callback to Part 10).
10. The kernel's own mapping; KPTI after Meltdown (callback to Part 7).
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
*Reading:* OSTEP (virtualization of memory); Tanenbaum & Bos ch. 3; Denning 1970; Belady 1966; Belady, Nelson &
Shedler 1969; Mattson et al. 1970; Kilburn et al. 1962; Bonwick 1994; Popek & Goldberg 1974; Adams & Agesen 2006;
Bhargava et al. 2008; Gorman, *Understanding the Linux Virtual Memory Manager*.

### Part 31 · Concurrency (~60)
*Story:* Two threads each add one to a counter, and the count goes up by one. Mutual exclusion can be built from
plain reads and writes (Peterson) until the hardware reorders them. The fix has two parts: a theory of memory
models, and a hierarchy that orders synchronization primitives by power. In that hierarchy, compare-and-swap can
implement every concurrent object.
1. Why concurrency: overlapping I/O, using cores; threads against processes.
2. **The race**: counter++ as load, add, store. Interleavings counted (C(2n, n)); the lost update found by our
   exhaustive interleaving model checker.
3. Mutual exclusion (safety, liveness, fairness): Dekker (1965); **Peterson (1981), proved by invariant**; Lamport's
   bakery (1974); the Burns–Lynch n-register lower bound.
4. Peterson breaks under TSO: the store-buffer litmus test (callback to Part 9), checked under SC and TSO models, and
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
    proved by valency (a preview of FLP in Part 36); the universality of consensus.
13. Transactional memory (Herlihy & Moss 1993; TSX's troubles).
14. Other models: CSP (Hoare 1978) and Go channels; actors and Erlang; async/await.
15. In the wild: Therac-25 and the 2003 blackout (cited); race detectors with vector clocks (Part 36).
16. PebbleOS gains a CAS mutex and threads. Outro.

*Computed:* exhaustive interleavings for counter++, Peterson and the bakery with property checks; SC against TSO
model checking; a lock benchmark (C on this machine where available, otherwise a cache-traffic simulation);
linearizability checking; the ABA scenario; dining philosophers; the banker's algorithm.
*Visuals:* interleavings branching as a tree; Peterson's state graph with the bad state unreachable; the MCS queue as
linked waiters; the consensus ladder.
*Reading:* Herlihy & Shavit, *The Art of Multiprocessor Programming*; OSTEP (concurrency); Downey, *The Little Book of
Semaphores*; Lynch, *Distributed Algorithms* ch. 10; Sorin, Hill & Wood; McKenney, *Is Parallel Programming Hard?*;
Lamport 1974, 1979; Dijkstra 1965; Hoare 1974, 1978; Herlihy 1991; Herlihy & Wing 1990; Adve & Gharachorloo 1996;
Boehm & Adve 2008; Mellor-Crummey & Scott 1991.

### Part 32 · Storage (~55)
*Story:* Memory forgets when the power goes, so data must live on spinning platters or in leaky flash. An append
that needs three writes can be cut short by a crash between any two of them. Journals, logs and copy-on-write trees
are the answers, and RAID's parity is Part 26's codes at work.
1. Persistence and the bottom of the hierarchy (callback to Part 8).
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
9. Copy-on-write (ZFS, btrfs): Merkle checksums (callback to Part 27); snapshots for free.
10. **RAID** (Patterson, Gibson & Katz 1988): levels 0/1/4/5/6 (callback to Part 26); the small-write problem; the
    chance of a second failure during rebuild (computed).
11. Reliability in the field (Schroeder & Gibson 2007, cited); latent sector errors; end-to-end checksums.
12. fsync and the illusion of durability: write caches and barriers; "fsyncgate" (2018).
13. **LSM trees** (O'Neil et al. 1996): memtables, SSTables, leveled against tiered compaction; read, write and space
    amplification (the RUM conjecture); Bloom filters per run (callback to Part 19).
14. Our file system and key-value store on PebbleOS's disk; the novels stored and read back. Ledger row 11. Outro.

*Computed:* the disk-time model; an FTL simulator; crash injection; LSM against B-tree amplification; RAID rebuild
risk; LFS cleaning.
*Visuals:* the head seeking while the platter spins; erase blocks being collected; the journal replaying after a
crash; LSM levels compacting in cascades.
*Reading:* OSTEP (persistence); McKusick et al. 1984; Rosenblum & Ousterhout 1992; Patterson, Gibson & Katz 1988;
Pillai et al. 2014; O'Neil et al. 1996; Petrov, *Database Internals* part I; Agrawal et al. 2008; Giampaolo,
*Practical File System Design*; Schroeder & Gibson 2007.

### Part 33 · Databases (~60)
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
6. Joins: nested loops, block, index, sort–merge, Grace hash. I/O costs derived (callback to Part 8's external
   memory).
7. **Selinger's optimizer** (1979): dynamic programming over join orders with interesting orders; the size of plan
   space (Catalan × n!); cardinality estimation and how independence assumptions fail.
8. Indexes: B+ trees (three levels index a billion rows); clustered against unclustered; hash and bitmap indexes;
   LSM (Part 32).
9. Transactions: ACID; schedules; **conflict serializability by precedence graphs** (a cycle means not
   serializable, proved); view serializability is NP-complete.
10. **2PL ⇒ serializable** (proved); strict 2PL; deadlock handling (wait-die, wound-wait); intention locks.
11. Optimistic concurrency and timestamps; **MVCC**; snapshot isolation and **write skew** (two doctors on call);
    serializable SI (Cahill 2008).
12. Isolation levels and their anomalies (Berenson et al. 1995; Adya 1999).
13. **Recovery**: WAL, steal/no-force; **ARIES** (Mohan 1992) with its analysis, redo and undo passes over LSNs;
    checkpoints.
14. Analytics: column stores (C-Store, MonetDB/X100, DuckDB); compression (callback to Part 20); vectorized against
    compiled execution.
15. **Our database** runs the Job's SQL on the novels and shows the plan it chose against the alternatives, with
    costs, cross-checked against `sqlite3`. Ledger row 12.
16. Beyond relational: key-value, document and graph stores; distributed transactions (Part 37). Outro.

*Computed:* join I/O against formulas; Selinger DP against exhaustive search; estimation errors under correlation; a
serializability checker; 2PL; write skew; ARIES on crashed logs; row against column scans; our database.
*Visuals:* tables transformed by algebra operators; join trees with costs; a precedence-graph cycle lighting up;
ARIES' three sweeps over the log; row against column layouts.
*Reading:* Silberschatz, Korth & Sudarshan, *Database System Concepts*; Ramakrishnan & Gehrke; Garcia-Molina, Ullman &
Widom, *Database Systems: The Complete Book*; Hellerstein & Stonebraker, *Readings in Database Systems* (the Red
Book); Gray & Reuter, *Transaction Processing*; Weikum & Vossen; Bernstein, Hadzilacos & Goodman; Abiteboul, Hull &
Vianu, *Foundations of Databases*; Codd 1970; Selinger et al. 1979; Mohan et al. 1992; Berenson et al. 1995; Adya
1999; Hellerstein, Stonebraker & Hamilton 2007.

---

## Act VII · Many Machines

### Part 34 · Networks I: Moving Bits (~55)
*Story:* The phone network reserved a wire for every call. Baran and Davies proposed cutting messages into packets
that find their own way. The Internet is that idea, organized in layers, with IP as the narrow waist. This part
derives what limits it at each layer: Shannon's capacity, ALOHA's 1/2e, the count-to-infinity problem, and BGP's
policies.
1. History: circuit switching; Baran (1964) and Davies; ARPANET (1969, "LO"); Cerf & Kahn (1974); the 1983 flag day.
2. Layering and encapsulation (headers nesting, animated); the hourglass; **the end-to-end argument** (Saltzer, Reed
   & Clark 1984); Clark's design philosophy (1988).
3. Physical layer: Nyquist and **Shannon–Hartley C = B log₂(1 + S/N)**; QAM constellations in noise; fiber and the
   speed of light; the bandwidth–delay product.
4. Link layer: framing and bit stuffing; CRC (callback to Part 26); MAC addresses.
5. Multiple access: **ALOHA, S = G e^{−2G}, max 1/(2e)** (derived); slotted 1/e; CSMA/CD and exponential backoff
   (Metcalfe 1973); Wi-Fi's CSMA/CA and hidden terminals.
6. Bridges and switches; Perlman's spanning tree (1985); VLANs.
7. IP: CIDR, NAT, IPv6; fragmentation; ICMP and traceroute's TTL trick.
8. Forwarding: longest-prefix match with tries (callback to Part 16); TCAMs; nanoseconds per packet at 400 Gb/s.
9. **Distance vector = distributed Bellman–Ford** (callback to Part 17); count-to-infinity animated; split horizon and
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
*Reading:* Kurose & Ross, *Computer Networking: A Top-Down Approach*; Peterson & Davie, *Computer Networks: A Systems
Approach*; Tanenbaum & Wetherall; Stevens, *TCP/IP Illustrated* vol. 1; Bertsekas & Gallager, *Data Networks*;
Varghese, *Network Algorithmics*; Tse & Viswanath, *Fundamentals of Wireless Communication*; Baran 1964; Cerf & Kahn
1974; Saltzer, Reed & Clark 1984; Abramson 1970; Metcalfe & Boggs 1976; Clark 1988.

### Part 35 · Networks II: Reliable Conversation (~55)
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
    migration; TLS 1.3 inside (callback to Part 28).
13. CDNs and anycast; Zipf's law of requests, fitted on the novels' words.
14. Our TCP fetching the novels over a lossy link: cwnd traces. Ledger row 13. Outro.

*Computed:* our rdt and TCP-lite under loss and reordering; utilization against window; Chiu–Jain trajectories;
sawtooth throughput against Mathis; bufferbloat delays; BBR-lite against Reno-lite; NUM by dual ascent; the Zipf fit.
*Visuals:* sequence diagrams with drops and retransmits; a window sliding over the byte stream; Chiu–Jain zig-zags
toward the fairness line; the cwnd sawtooth; queues swelling.
*Reading:* Kurose & Ross ch. 2–3; Peterson & Davie ch. 5–6; Stevens; Srikant & Ying, *Communication Networks*;
Grigorik, *High Performance Browser Networking*; Jacobson 1988; Chiu & Jain 1989; Mathis et al. 1997; Kelly, Maulloo &
Tan 1998; Cardwell et al. 2016; Langley et al. 2017; Nichols & Jacobson 2012.

### Part 36 · Distributed Systems I: Agreement (~60)
*Story:* "A distributed system is one in which the failure of a computer you didn't even know existed can render
your own computer unusable" (Lamport). With no shared clock and failures that look like slowness, even agreeing on
one bit is provably impossible in general (FLP). Paxos and Raft agree anyway, by giving up a guarantee that FLP
says no one can have. We build Raft and try to break it.
1. Partial failure, no global clock, asynchrony.
2. **The two generals** cannot agree over a lossy link (proved by induction on messages).
3. Time: NTP and its limits; **happened-before and Lamport clocks** (1978) on space–time diagrams; **vector clocks**
   characterize causality (proved); race detectors (callback to Part 31).
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
15. Checking protocols: TLA+ at Amazon (Part 41); Jepsen's findings (cited). Outro.

*Computed:* vector-clock causality; snapshots; FLP's valency explored exhaustively on a tiny protocol; Raft with
fault injection and invariant checks; the Byzantine counterexample; PBFT message counts; Nakamoto's probabilities
against Monte Carlo.
*Visuals:* space–time diagrams with clock stamps; consistent and inconsistent cuts; Raft terms and logs lining up;
configuration graphs colored by valency; a traitor sending split messages.
*Reading:* Lynch, *Distributed Algorithms*; Attiya & Welch, *Distributed Computing*; Cachin, Guerraoui & Rodrigues,
*Introduction to Reliable and Secure Distributed Programming*; van Steen & Tanenbaum, *Distributed Systems*;
Kleppmann, *Designing Data-Intensive Applications* ch. 8–9; Lamport 1978, 1998, 2001; Fischer, Lynch & Paterson 1985;
Ongaro & Ousterhout 2014; Lamport, Shostak & Pease 1982; Castro & Liskov 1999; Nakamoto 2008; Dwork, Lynch &
Stockmeyer 1988; Chandy & Lamport 1985.

### Part 37 · Distributed Systems II: Scale (~55)
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
    re-execution; stragglers and backup tasks. Ledger row 14.
11. Spark's RDDs and lineage; streaming with watermarks; exactly-once via Chandy–Lamport (callback to Part 36).
12. Coordination: Chubby and ZooKeeper; leases and fencing tokens.
13. **The tail at scale** (Dean & Barroso 2013): 1 − 0.99¹⁰⁰ ≈ 63% (computed); hedged requests; two choices
    (callback to Part 19).
14. Failure at scale: correlated, gray and metastable failures; chaos engineering; post-mortems (cited). Outro.

*Computed:* PBS; CRDT convergence under random delivery orders; consistent-hashing variance; Chord hops; 2PC
blocking; Spanner's timeline; the MapReduce Job with a failure; tail amplification; hedging.
*Visuals:* the consistency hierarchy as a map; replicas merging up a lattice; the hash ring; Chord fingers; the
shuffle as colored streams; the fan-out tail.
*Reading:* Kleppmann, *Designing Data-Intensive Applications*; Barroso, Hölzle & Ranganathan, *The Datacenter as a
Computer*; Saltzer & Kaashoek, *Principles of Computer System Design*; van Steen & Tanenbaum; DeCandia et al. 2007;
Corbett et al. 2012; Dean & Ghemawat 2004; Zaharia et al. 2012; Shapiro et al. 2011; Gilbert & Lynch 2002; Karger et
al. 1997; Stoica et al. 2001; Dean & Barroso 2013; Burrows 2006; Hunt et al. 2010; Bailis et al. 2012; Akidau et al.
2015.

---

## Act VIII · Horizons and Trust

### Part 38 · Light and Pixels (~60)
*Story:* A picture is millions of samples of light. Projecting triangles onto a screen is linear algebra plus one
division, and getting the samples right is Nyquist again. The physics of light comes down to one integral
equation, which Monte Carlo solves one bounced path at a time. Our path tracer renders the series' own scene, and
its noise falls as 1/√N.
1. Sketchpad (Sutherland 1963) to framebuffers; "a pixel is not a little square" (Smith 1995).
2. Transforms: homogeneous coordinates make translation linear; composition order; Euler angles and gimbal lock,
   quaternions and slerp (3D).
3. **Perspective projection** derived from similar triangles; the frustum squashed into the cube; NDC; the depth
   nonlinearity and z-fighting.
4. Rasterization: edge functions (Part 21's orientation test); barycentrics; **perspective-correct interpolation
   (why 1/w)**; the z-buffer (Catmull 1974). Our rasterizer.
5. Shading: Lambert's cosine law; Phong and Blinn–Phong; Gouraud against Phong.
6. Textures and **sampling**: moiré as aliasing (Nyquist, callback to Part 34); mipmaps (Williams 1983); trilinear
   and anisotropic filtering; supersampling and MSAA.
7. The GPU pipeline: vertex and fragment shaders (callback to *AI, Built* 17).
8. Ray tracing (Whitted 1980): ray–sphere and **Möller–Trumbore** intersection derived; shadows; Snell and
   Fresnel–Schlick.
9. Acceleration: BVHs with the surface-area heuristic (callback to Part 21); O(log n) per ray.
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
*Reading:* Pharr, Jakob & Humphreys, *Physically Based Rendering* (4th ed.); Marschner & Shirley, *Fundamentals of
Computer Graphics*; Akenine-Möller et al., *Real-Time Rendering*; Hughes et al., *Computer Graphics: Principles and
Practice*; Farin, *Curves and Surfaces for CAGD*; Kajiya 1986; Veach 1997; Whitted 1980; Cook & Torrance 1982; Catmull
1974; Sutherland 1963.

### Part 39 · Computing with Real Numbers (~55)
*Story:* In 2000 a journal named the ten algorithms that most shaped science and engineering in the 20th century.
Most of them are numerical. The organizing question is the one Part 3 left open: with rounding everywhere, which
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
14. Speed: BLAS levels 1, 2 and 3 and arithmetic intensity (callbacks to Part 8 and *AI, Built* 17); LAPACK;
    mixed-precision iterative refinement; HPL and the Top500. Outro.

*Computed:* pivoting failures; growth factors; orthogonality loss; QR-algorithm convergence; CG against steepest
descent; multigrid; the Newton fractal; Runge against Chebyshev; stiffness; orbit drift; BLAS timings on this
machine.
*Visuals:* Householder mirrors; subdiagonal entries fading under QR; the fractal zoom; the multigrid spectrum;
drifting orbits.
*Reading:* Trefethen & Bau, *Numerical Linear Algebra*; Golub & Van Loan, *Matrix Computations*; Higham; Demmel,
*Applied Numerical Linear Algebra*; Saad, *Iterative Methods for Sparse Linear Systems*; Briggs, Henson & McCormick, *A
Multigrid Tutorial*; Trefethen, *Approximation Theory and Approximation Practice*; Hairer, Lubich & Wanner, *Geometric
Numerical Integration*; Wilkinson, *The Algebraic Eigenvalue Problem*; Dongarra & Sullivan 2000.

### Part 40 · Quantum Computation (~60)
*Story:* Feynman asked whether a classical computer can simulate quantum physics efficiently, and suspected it
can't. A computer made of quantum parts interferes over 2ⁿ amplitudes at once. Shor used that to factor and break
Part 28's cryptography. Grover's √N is all it does for general search. Error correction, once thought impossible,
crossed its threshold in 2024. This is the one serious challenge to the extended Church–Turing thesis of Part 1.
1. Landauer (kT ln 2 per erased bit) and Bennett: reversible computation; Toffoli and Fredkin; compute, copy,
   uncompute.
2. Feynman (1982) and Deutsch (1985).
3. The qubit: amplitudes, the Born rule, the **Bloch sphere** (3D). The physics is in *Quantum Mechanics,
   Visualized*.
4. Gates as unitaries rotating the Bloch sphere; tensor products and 2ⁿ amplitudes; CNOT; Bell states; **no-cloning**
   in three lines.
5. Circuits and universality (H, T, CNOT; Solovay–Kitaev); our state-vector simulator.
6. Interference as the resource: Deutsch, Deutsch–Jozsa, phase kickback.
7. Bernstein–Vazirani; **Simon's problem**, an oracle separation and the seed of Shor.
8. **The QFT** derived from the FFT's butterfly (callback to Part 18), with O(n²) gates for 2ⁿ points.
9. Phase estimation.
10. **Shor** (1994): order finding (Part 28's number theory), the QFT, continued fractions. Our simulator factors 15
    and 21, and the amplitude spikes at multiples of 2ⁿ/r are animated.
11. **Grover** (1996): two reflections make a rotation by 2θ; √N iterations; overshoot; optimality (BBBV 1997,
    sketched); amplitude amplification.
12. BQP's place (BPP ⊆ BQP ⊆ PP ⊆ PSPACE); no known speedup for NP-complete problems beyond Grover's; the extended
    Church–Turing thesis; supremacy claims and the classical replies (cited, carefully).
13. **Quantum error correction**: why it seemed impossible; the 3-qubit code and syndromes; Shor's 9-qubit code;
    stabilizers (Gottesman); **the surface code and the threshold** (callback to Part 26); below threshold (Google
    2024, cited) **(verify)**.
14. Simulation and chemistry; BB84 (an eavesdropper shows up as a 25% error rate); resource estimates for RSA-2048
    (Gidney 2025) **(verify)**. Outro.

*Computed:* the simulator; Bloch trajectories; Deutsch–Jozsa, BV and Simon runs; QFT against FFT; Shor on 15 and 21;
Grover's success probability against iterations; logical against physical error rates for the repetition code;
BB84.
*Visuals:* gates rotating the Bloch sphere; amplitude bars colored by phase, interfering; Grover's rotation in the
plane; Shor's peaks; a surface-code lattice lighting its syndromes.
*Reading:* Nielsen & Chuang, *Quantum Computation and Quantum Information*; Mermin, *Quantum Computer Science*;
Aaronson, *Quantum Computing Since Democritus*; Kitaev, Shen & Vyalyi; de Wolf's lecture notes; Preskill's Ph219
notes; Watrous, *The Theory of Quantum Information*; Feynman 1982; Deutsch 1985; Shor 1997; Grover 1996; Bennett et
al. 1997; Gottesman 1997; Fowler et al. 2012; Bennett & Brassard 1984; Landauer 1961; Bennett 1973.

### Part 41 · Proving Programs Correct (~55)
*Story:* Testing can show that bugs are present but never that they are absent, and Rice's theorem rules out
deciding correctness in general. We prove programs correct anyway: by writing the invariants ourselves, by
exhausting finite state spaces symbolically, or by approximating soundly. Verified compilers and kernels exist, and
so do the proof assistants that check their proofs.
1. The cost of bugs (Ariane 5, Therac-25, Heartbleed, cited); Dijkstra's dictum; Rice (Part 23) and the three ways
   around it.
2. Specifications; Turing's "Checking a Large Routine" (1949), the first program proof.
3. **Floyd–Hoare logic** (1967, 1969): triples and the rules (assignment by backward substitution, sequence,
   conditionals, while with its invariant); soundness and relative completeness (Cook 1978).
4. Binary search proved: the invariant, and Bloch's 2006 overflow bug; total correctness by variants and
   well-founded orders.
5. **Weakest preconditions** (Dijkstra 1975); VC generation; our VCs checked by our SAT solver (Part 24), or by z3 if
   it is installed.
6. **Separation logic** (Reynolds, O'Hearn): the frame rule; in-place list reversal proved; Infer at scale.
7. **Model checking** (Clarke, Emerson, Sifakis; the 2007 Turing Award):
   - Kripke structures; LTL and CTL over computation trees;
   - state explosion;
   - **symbolic model checking with BDDs** (callback to Part 2) and bounded model checking with SAT;
   - Peterson (Part 31) and Raft-lite (Part 36) checked.
8. **Abstract interpretation** (Cousot & Cousot 1977): Galois connections; intervals and widening, the fixpoint
   converging; Astrée on Airbus flight software (cited).
9. Types as lightweight proofs (callback to Part 13); refinement types.
10. **Proof assistants**: the LCF trusted kernel (Milner 1972); Rocq, Isabelle, Lean; a proof on screen; the
    four-color theorem, Flyspeck, the Liquid Tensor Experiment, mathlib (callback to *AI, Built* 25).
11. Verified systems: **CompCert** (Leroy; Csmith found no wrong-code bugs in its verified parts), **seL4** (2009,
    about 9k lines of C and 200k lines of proof), verified cryptography (HACL*, Fiat-Crypto), CakeML.
12. **TLA+** (Lamport): systems as state machines; an invariant checked on a protocol (Part 36); refinement.
13. Testing as science: coverage; mutation testing; property-based testing (QuickCheck 2000) with shrinking;
    coverage-guided fuzzing (Miller 1990; AFL); symbolic and concolic execution (KLEE); differential testing (Csmith).
    **Our fuzzer finds a bug planted in the Pebble compiler.**
14. Translation validation of our compiler on the Job's code; proof-carrying code (Necula 1997). Outro.

*Computed:* VCs generated and discharged for several programs; the binary-search overflow found; LTL checks of
Peterson and the dining philosophers; BDD reachability sizes; interval analysis with widening; an LCF-style kernel
for natural deduction; property tests and fuzzing of the Pebble toolchain.
*Visuals:* assertions flowing backward through code; computation trees with CTL paths lit; the interval lattice's
widening jumps; the small trusted kernel inside a large system.
*Reading:* Huth & Ryan, *Logic in Computer Science*; Baier & Katoen, *Principles of Model Checking*; Clarke, Grumberg,
Kroening, Peled & Veith, *Model Checking*; Nipkow & Klein, *Concrete Semantics*; Pierce et al., *Software
Foundations*; Bradley & Manna, *The Calculus of Computation*; Kroening & Strichman, *Decision Procedures*; Dijkstra, *A
Discipline of Programming*; Gries, *The Science of Programming*; Lamport, *Specifying Systems*; Møller & Schwartzbach,
*Static Program Analysis*; Rival & Yi; Zeller et al., *The Fuzzing Book*; Hoare 1969; Floyd 1967; Cousot & Cousot
1977; Reynolds 2002; Leroy 2009; Klein et al. 2009; Claessen & Hughes 2000; Newcombe et al. 2015.

### Part 42 · Trusting Trust (~60; the finale)
*Story:* Security is a property of the whole tower, and every layer leaks: buffers overflow, speculation leaves
traces, DRAM rows disturb their neighbours, parsers confuse code with data. In 1984 Ken Thompson showed that even a
compiler you built yourself can hide a backdoor that its source never shows. We build his attack against our own
compiler, then catch it, and close the series by walking the tower from a NAND gate to a cluster.
1. Threat models; Saltzer & Schroeder's principles (1975).
2. Memory corruption revisited (Part 10):
   - the stack smash on Pebble;
   - canaries, W^X, ASLR (its entropy computed);
   - **return-oriented programming** (Shacham 2007), a Turing-complete chain of gadgets in our own binary;
   - CFI; CHERI.
3. Memory safety: the ~70% statistic (cited); Rust's ownership as affine types (callback to Part 13); what the borrow
   checker proves; RustBelt.
4. Hardware: Rowhammer (Part 4), Spectre and Meltdown (Part 7) and what the mitigations cost; side channels (Part
   27).
5. Authentication: password entropy and guessing; salted slow hashes (Part 27); TOTP as an HMAC over time; passkeys
   (Part 28). **Needham–Schroeder (1978) and Lowe's 1995 attack, found by our model checker** (callback to Part 41).
6. Access control: Lampson's matrix; ACLs against capabilities (the confused deputy); Bell–LaPadula; **safety is
   undecidable in the HRU model (1976)** (callback to Part 23).
7. Isolation: processes and paging (Part 30); sandboxes, site isolation, WebAssembly (Part 14); enclaves and their
   breaks.
8. The web: same origin; XSS and CSRF; **SQL injection on our own database**, fixed by parameterized queries, a parsing
   fix (callback to Part 11); PKI failures (DigiNotar).
9. Networks: amplification DDoS, BGP hijacks (Part 34), DNS (Part 35).
10. Supply chains: dependency confusion; **the xz-utils backdoor** (2024), and how a 500 ms slowdown exposed it (cited).
11. **Reflections on Trusting Trust** (Thompson 1984), built on our compiler (Part 12) with Part 23's quine trick:
    - a backdoor in `login`;
    - a compiler that inserts it when it compiles `login`;
    - and inserts itself when it compiles a compiler;
    - remove the source, and the binary keeps both.
12. **Diverse double-compiling** (Wheeler 2009) catches it, using our independent Python reference compiler.
    Reproducible builds; bootstrapping from a tiny seed (cited).
13. **The tower revisited**: the Job end to end, from NAND to cluster; the final ledger (row 15); what each layer hides
    and what leaks through.
14. Open problems across the series:
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
*Reading:* Anderson, *Security Engineering* (3rd ed.); Bishop, *Computer Security: Art and Science*; Erickson,
*Hacking: The Art of Exploitation*; Szekeres et al. 2013 (SoK: eternal war in memory); Saltzer & Schroeder 1975;
Thompson 1984; Wheeler 2009; Shacham 2007; Abadi et al. 2005; Lampson 1974; Harrison, Ruzzo & Ullman 1976; Lowe 1996;
Kocher et al. 2019; Jung et al. 2018.

---

## 5. Phases

0. **Infrastructure:**
   - `explainer/cs/`:
     - the series constants (`SERIES_EN`, `SERIES_ZH`, `ACTS`, `PARTS`) and `series_map` for 42 parts in eight acts;
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
   - Entries in `CLAUDE.md` and the top-level README.
   - A silent en + zh smoke render of an empty chapter on Linux.
1. **Pilot: Part 1 (What Is a Computation?)**. It sets up the story and every series device: Pebble introduced, the
   tower, the timeline, the ledger's empty frame, the payoff cards. It exercises `TapeView` and the C fast path
   (BB(5)). It is delivered in English and Chinese, with previews and contact sheets. **Review with the user**, then
   lock the standard.
2. **Act I, Parts 2–5**, in order: the hardware Pebble. **Part 5 is the second review**: the machine runs the Job.
3. **Roll-out in series order, Parts 6 → 42.** The order matters, because each part's Pebble layer rests on the one
   before. Each part goes through:
   - the frontier sweep;
   - locking the chapter list;
   - building its Pebble layer and tests;
   - `compute.py`;
   - English scenes, then the QA gates;
   - Chinese narration and text, then the QA gates;
   - commit and push.

## 6. Scale and risks

**Scale:**
- about 39 hours of video;
- about 8,000 narration words per part per language, roughly 340,000 per language in all;
- roughly 4–6k lines of scene code per part (what *AI, Built* took);
- Pebble itself, about 20–30k lines with its tests across the series.

At *AI, Built*'s pace, that is one part per one or two long sessions.

| Risk | Mitigation |
|---|---|
| Gate-level simulation is slow | bit-parallel, levelized numpy evaluation; gate level only for short runs (a paragraph of the Job, BB(3)); the emulator for the rest, bridged by co-simulation tests |
| Pebble's breadth (CPU to Raft) | every layer small and tested against an independent reference; later parts use a layer only through its API, so a layer can be rewritten without touching the scenes |
| Overlap with *AI, Built* | callback cards, not repeats (§2.3); the CS treatment goes deeper where the AI series only sketched (Turing, SAT, GPUs, floats) |
| Frontier claims age | **(verify)** markers; the frontier sweep before each part is written |
| Machine-dependent measurements | labelled `measured on this machine`; the narration branches on the measurement; macOS and Linux both supported |
| Educational crypto mistaken for real crypto | labelled on screen and in the code; known-answer tests only; never imported outside the series |
| No outbound network in some environments | every network experiment is simulated; real-Internet numbers are cited, not measured |

## 7. Decisions to confirm before Phase 0

1. **Name and handle**: *Computer Science, Built* (计算机科学，从零搭建), videos `cs1` … `cs42` in `videos/cs/`.
2. **Scope: 42 parts (recommended).** A shorter 36-part cut would merge Parts 6 + 7, 20 + 21, 34 + 35 and 36 + 37,
   fold 25 into 24, and fold 39 into Parts 3 and 22, at the cost of depth.
3. **Bilingual from the start** (English, then Chinese for each part, as *AI, Built* does).
4. **The machine's name and ISA**: Pebble, as our own RISC-V-like ISA rather than RV32I verbatim (cleaner encodings to
   draw; a comparison card covers the differences).
5. **Pilot**: Part 1, then Act I in order.

## 8. Progress (updated as parts land)

| Part | State | Length |
|---|---|---|
| 1–42 | planned (this document) | — |
