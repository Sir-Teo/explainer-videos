"""Act II, Making It Fast (Parts 7-10), and the start of Act III, Speaking to the Machine (Parts 11-12)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=7, level="U", widget="pipedepth", prereq=(5, 6),
        question="How can a processor work on five instructions at once, and what does it do when it must guess?",
        story="Part 6's single-cycle Pebble makes every instruction wait for the slowest one: 2.63 ns a cycle on "
              "the part's assumed timing budget. The iron law, time = instructions x CPI x cycle time, says where "
              "to look, and the laundry picture says how: overlap the work in five stages with registers between "
              "them, so that throughput rises while each instruction's latency does not fall. A cycle-by-cycle "
              "model of the five-stage pipeline is built and compared with the emulator, and its hazards are "
              "counted: structural ones, data ones that forwarding removes except for the bubble after a load, "
              "and control ones, where fetch must guess. The part turns on the guess. Smith's 1-bit and 2-bit "
              "counters, gshare, a tournament, a small TAGE and Jimenez and Lin's perceptron are run on the same "
              "branch traces, with a target buffer and a return stack to say where a branch goes. The Job's first "
              "chapter then runs at a CPI of about 1.2 on a 1.13 ns clock, almost twice as fast as Part 6. The "
              "part ends with what stopped deeper pipelines (power), with Amdahl's law, with the sorted-array "
              "puzzle timed on this machine, and with how far prediction can go on one trace.",
        handoff="The in-order pipeline becomes the out-of-order core of Part 8, where speculation past a predicted "
                "branch returns as Spectre; the assumed one-nanosecond memories become the caches of Part 9; the "
                "power wall and Amdahl against Gustafson return in Part 10; hiding a load-use bubble by moving an "
                "instruction returns as instruction scheduling in Part 13's compiler.",
        outside="Programming, and school algebra with one derivative for the best depth. No electronics beyond "
                "Parts 3 to 6.",
        objectives={
            "U": ["Compute a program's run time from the iron law, and explain why MIPS alone can rank two programs "
                  "the wrong way round.",
                  "Draw the pipeline chart of a short instruction sequence with forwarding, placing the load-use "
                  "bubble and the two-cycle flush after a mispredicted branch.",
                  "Trace a 1-bit and a 2-bit counter over a loop branch and count their misses."],
            "M": ["Derive the pipelined speedup (t + o)/(t/k + o), its limit 1 + t/o, and the depth that minimizes "
                  "time per instruction when a fraction b of instructions loses k - 1 cycles.",
                  "Explain what gshare, a tournament, TAGE and a perceptron each add to a table of counters, and "
                  "what a target buffer and a return stack predict.",
                  "State what a precise exception guarantees and how the pipeline delivers it."],
            "D": ["Explain why hindsight majority, an unlimited PPM predictor and a perceptron's failure on XOR "
                  "are not prediction limits, and say what each does establish.",
                  "Design a held-out evaluation of a predictor: separate training, tuning and test traces, and a "
                  "storage budget that counts every bit of state."],
            "I": ["Measure before tuning: read cycles, instructions and branch misses from hardware counters and "
                  "turn them into a CPI breakdown.",
                  "Decide when replacing a data-dependent branch by arithmetic or a conditional move pays, and "
                  "measure the extra work it does."],
        },
        results=[
            ("The iron law", r"T = N\times\text{CPI}\times t_{\text{clk}}"),
            ("Pipelined speedup", r"\frac{t+o}{t/k+o}\ \longrightarrow\ 1+\frac{t}{o}\quad(k\to\infty)"),
            ("Every cycle accounted for", r"\text{cycles}=n+4+\text{bubbles},\qquad \text{CPI}\to 1+\frac{\text{bubbles}}{n}"),
            ("The cost of branches", r"\text{CPI}=1+f_{\text{branch}}\times m_{\text{miss}}\times\text{penalty}"),
            ("The best depth", r"T(k)=\Bigl(\frac{t}{k}+o\Bigr)\bigl(1+b(k-1)\bigr),\qquad k^*=\sqrt{\frac{t(1-b)}{b\,o}}"),
            ("Amdahl's law", r"S(n)=\frac{1}{(1-p)+p/n}\ \le\ \frac{1}{1-p}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 13), D=(15,), I=(12, 14),
        also=(("Pebble's pipeline", "explainer/cs/pebble/pipe.py"), ("The branch predictors", "explainer/cs/pebble/predict.py")),
    ),
    Part(
        n=8, level="U", widget="dataflowlimit", prereq=(6, 7),
        question="Why should an instruction wait in line behind one that is stuck, and what does it cost to let it pass?",
        story="A load misses the cache, and on a machine that starts instructions in program order everything "
              "behind it waits: 81 cycles for sixteen instructions, against 70 when ready work may pass. The part "
              "first asks how fast a known path could run at all. Four trips of the Job's scan loop form a "
              "dataflow graph of 24 instructions with a longest chain of 6 cycles, and schedules with 1, 2, 4 and "
              "8 starts a cycle take 24, 12, 7 and 6. Reused register names add waits that carry no value, and "
              "renaming removes them. The mechanisms follow in historical order: the CDC 6600's scoreboard, "
              "Tomasulo's reservation stations and tags (62 against 56 cycles on the textbook example), and the "
              "reorder buffer, which retires in program order so that exceptions stay precise. A functional "
              "out-of-order core is built and checked against the emulator; on the Job's first chapter it retires "
              "1.89 instructions a cycle. The part turns on speculation: work on a mispredicted path is squashed, "
              "but a load it ran has already warmed the cache, and a bounds-check-bypass gadget in the model reads "
              "the bytes PEBBLE through that channel. It ends with the compiler-scheduled alternative (VLIW), RISC "
              "against CISC, multithreading, the Job's ledger row, and value prediction and secure speculation at "
              "the frontier.",
        handoff="Large windows meet cache misses in Part 9, and width, energy and several cores in Part 10; static "
                "scheduling and software pipelining return with the compiler in Part 13; the reordering of loads "
                "and stores returns as memory models in Parts 10 and 33; the Spectre gadget returns with threat "
                "models in Part 55.",
        outside="Programming and school algebra. The scheduling bounds use only counting.",
        objectives={
            "U": ["Draw the dataflow graph of a short instruction sequence, find its span, and schedule it with W "
                  "starts a cycle.",
                  "Tell a true dependence (read after write) from the name hazards (write after read, write after "
                  "write), and rename a sequence to remove the name hazards.",
                  "Explain in plain steps how a squashed load can still reveal a byte through the cache."],
            "M": ["Run the textbook example through a scoreboard and through Tomasulo's algorithm, cycle by cycle, "
                  "and say where each one waits.",
                  "Explain how a reorder buffer gives precise exceptions when execution is out of order, and what "
                  "a load must check about older stores whose addresses are unknown.",
                  "State the start-slot bound and Graham's bound, and say which resource model each one assumes."],
            "D": ["Say what an oracle limit study assumes (future paths, memory addresses, unlimited resources) "
                  "and why its instructions per cycle is not a hardware target.",
                  "State what a secure-speculation claim needs before it is a theorem: the attacker, the permitted "
                  "observations, the protected data and a baseline.",
                  "Evaluate a value predictor by coverage, timing and recovery cost and not by accuracy alone."],
            "I": ["Read a core's published numbers with care: which stage a width refers to, and whether a "
                  "reorder buffer counts instructions, micro-operations or fused groups.",
                  "Choose between a speculation barrier and index masking for a bounds check, and state what the "
                  "compiler and the instruction set must preserve for each to work."],
        },
        results=[
            ("The start-slot bound", r"T_W\ \ge\ \max\bigl(\lceil N/W\rceil,\ L\bigr)"),
            ("Graham's bound", r"T_G\ \le\ \frac{A}{W}+\Bigl(1-\frac{1}{W}\Bigr)L"),
            ("Renaming", r"\text{fresh name per write}\ \Rightarrow\ \text{WAR, WAW vanish; RAW remains}"),
            ("Precise state", r"\text{execute in any valid order; commit in program order}"),
            ("Penalty accounting", r"\text{CPI}=\text{CPI}_{\text{perfect}}+\frac{P}{\text{instructions per redirect}}"),
            ("Index masking", r"m=-(x<_u \text{size}),\qquad \text{load } a[x \mathbin{\&} m]"),
        ],
        U=(0, 1, 2, 7, 9, 11), D=(15,), I=(12, 13),
        also=(("The out-of-order core", "explainer/cs/pebble/ooo.py"), ("The limit study", "explainer/cs/pebble/limits.py")),
    ),
    Part(
        n=9, level="U", widget="scanthrash", prereq=(6, 7, 8),
        question="If memory is hundreds of times slower than the processor, why are programs not hundreds of times slower?",
        story="The part opens on a scale: if one processor cycle took a second, the pointer-chase times measured on "
              "this machine would stretch from seconds to minutes. Wulf and McKee's memory wall says why that "
              "matters, and locality says why it is survivable: the Job's address trace revisits a few lines again "
              "and again. A direct-mapped cache is built from an address's tag, index and offset, then given "
              "associativity and a replacement policy; misses are sorted into three kinds, and the average access "
              "time is nested across levels. The host's latency staircase and bandwidth are measured, and loop "
              "order, tiling and data layout are timed. The part turns from tuning to theory: cache-oblivious "
              "recursion needs no cache parameters, and Hong and Kung's red-blue pebble game bounds how much data "
              "a classical matrix multiply must move, a scale of n cubed over the square root of M that tiling "
              "approaches. External memory, B-trees, prefetching and the inside of a DRAM chip follow. The Job's "
              "table scans miss about 88% of the time in a 32 KiB LRU cache, yet the ledger row barely moves under "
              "the model's free prefetching, and the frontier asks how close a learned replacement policy can come "
              "to Belady's MIN.",
        handoff="Cached copies on several cores become cache coherence in Part 10; address translation and the "
                "TLB are built in Part 32; B-trees and external sorting return in Parts 17 and 35; later "
                "versions of the Job cut the searching itself instead of its cost per access.",
        outside="Programming, powers of two and logarithms. The pebble-game bound is given as a proof idea.",
        objectives={
            "U": ["Split an address into tag, index and offset for a given cache, and trace hits and misses in a "
                  "small direct-mapped or set-associative cache.",
                  "Compute an average memory access time across two levels, stating what the miss penalty includes.",
                  "Reorder a loop nest or change a data layout so that the innermost loop walks memory in order."],
            "M": ["Compute reuse (stack) distances for a trace, and read the miss ratio of every LRU capacity from "
                  "them.",
                  "Classify misses against a fully associative LRU reference, and explain why the conflict count "
                  "can come out negative.",
                  "Play the red-blue pebble game on a small graph, and state the movement bound for classical "
                  "matrix multiplication with its assumptions."],
            "D": ["State the ideal-cache and external-memory models, and say which assumptions (tall cache, "
                  "optimal replacement, no recomputation) each bound depends on.",
                  "Compare an online replacement policy with Belady's MIN under matching capacity, start state "
                  "and insertion rules, on held-out traces."],
            "I": ["Measure a machine's dependent-load latency and its sequential throughput, and say what a bend "
                  "in the staircase does and does not prove.",
                  "Decide when prefetch hints, huge pages or a structure-of-arrays layout are worth trying, and "
                  "verify the effect on a representative workload."],
        },
        results=[
            ("Address fields", r"\text{offset bits}=\log_2(\text{line}),\quad \text{index bits}=\log_2(\text{sets}),\quad \text{tag}=\text{the rest}"),
            ("Stack distance (LRU)", r"\text{hit in a } C\text{-line LRU cache}\iff 0\le d<C"),
            ("Average access time", r"\text{AMAT}=t_1+m_1\bigl(t_2+m_2\,t_3\bigr)"),
            ("Matrix multiply must move", r"\Omega\!\left(\frac{n^3}{\sqrt{M}}\right)\ \text{words (classical algorithm)}"),
            ("External sorting", r"\Theta\!\left(\frac{N}{B}\log_{M/B}\frac{N}{B}\right)\ \text{block transfers}"),
            ("Search in blocks", r"O\bigl(1+\log_B N\bigr)\ \text{transfers (B-tree, van Emde Boas layout)}"),
        ],
        U=(0, 1, 2, 3, 4, 6, 8), D=(15,), I=(7, 12, 13),
        also=(("The cache simulator", "explainer/cs/pebble/cache.py"),),
    ),
    Part(
        n=10, level="U", widget="greedybrent", prereq=(7, 8, 9),
        question="When the clock stopped getting faster, what did more cores buy, and what did they cost?",
        story="Fifty years of microprocessors on one chart: around 2005 the clock and power curves bend and a new "
              "curve, the number of cores, appears. Dynamic power is activity times capacitance times voltage "
              "squared times frequency, Dennard's scaling kept power density constant only while the voltage "
              "fell, and when it stopped falling two slower cores became a better buy than one fast one. The "
              "condition is that the work divides. The Job is cut into four shards with private tables and a "
              "partitioned merge, and the trouble of shared memory is met in order: private caches that disagree "
              "and the MESI protocol that reconciles them, false sharing measured on this machine, store buffers "
              "that let both threads of a litmus test read zero, and the atomic instructions locks are built "
              "from. SIMD and the GPU are the other answers. The part then turns to theory that fixes no "
              "machine: work and span, Brent's theorem with its proof, parallel prefix (Part 4's carry tree "
              "again), sorting networks and the 0-1 principle, Amdahl against Gustafson, PRAM, BSP and network "
              "shapes. The Job's four-core projection is about 12 seconds against 57, more than four times "
              "faster, because shorter tables mean less work. The frontier is values out of thin air, "
              "work-stealing constants and energy.",
        handoff="Locks, lock-free structures and the memory model in depth are Part 33; the Job's better "
                "algorithm is Parts 16 and 17, and a vectorized tokenizer is ledger row ten in Part 24; threads "
                "inside an operating system are Part 31; consensus between machines is Parts 38 and 59; the "
                "partitioned merge grows into MapReduce in Parts 39 and 45; specialized hardware, the answer to "
                "dark silicon, is Part 60.",
        outside="Programming with loops and arrays, logarithms, and proof by counting.",
        objectives={
            "U": ["Explain with the dynamic power formula why two cores at 80% of the clock can replace one at "
                  "full speed, and what that assumes.",
                  "Trace a cache line through MESI states for a short sequence of reads and writes by several "
                  "cores, counting invalidations.",
                  "Compute a computation's work, span and parallelism, and its speedup limits under Amdahl and "
                  "Gustafson."],
            "M": ["Prove Brent's theorem by counting complete and incomplete steps, and prove the 0-1 principle.",
                  "Enumerate the outcomes of the store-buffering test under sequential consistency and under "
                  "total store order, and place fences that forbid the relaxed outcome.",
                  "Run Blelloch's scan by hand, count its additions, and use a scan to compact an array."],
            "D": ["Explain why out-of-thin-air values are hard to forbid in a language memory model without "
                  "forbidding compiler reorderings.",
                  "State what the work-stealing bound leaves out (the constant, locality, space), and design a "
                  "simulation that measures one of them."],
            "I": ["Find and remove false sharing: pad or separate per-thread data, and confirm with a "
                  "cache-to-cache profile.",
                  "Choose between threads, SIMD and a GPU for a loop from its dependencies, branches and memory "
                  "pattern, and report strong and weak scaling separately."],
        },
        results=[
            ("Dynamic power", r"P=\alpha\,C\,V^2 f"),
            ("Brent's theorem", r"\max\Bigl(\frac{T_1}{p},\,T_\infty\Bigr)\ \le\ T_p\ \le\ \frac{T_1}{p}+T_\infty"),
            ("Scan work (n a power of two)", r"\text{Hillis-Steele: } n\log_2 n-n+1,\qquad \text{Blelloch: } 2(n-1)"),
            ("The 0-1 principle", r"\text{sorts all } 2^n \text{ inputs of 0s and 1s}\ \Rightarrow\ \text{sorts every input}"),
            ("Amdahl and Gustafson", r"S_{\text{fixed}}=\frac{1}{s+(1-s)/p},\qquad S_{\text{scaled}}=s+p\,(1-s)"),
            ("Store buffering", r"\text{SC forbids } (r_0,r_1)=(0,0);\ \text{TSO allows it}"),
        ],
        U=(0, 1, 2, 3, 9, 12), D=(15,), I=(4, 7, 8),
        also=(("Parallel algorithms and models", "explainer/cs/pebble/parallel.py"), ("The MESI simulator", "explainer/cs/pebble/coherence.py")),
    ),
    Part(
        n=11, level="U", widget="framesmash", prereq=(6,),
        question="What happens between a program's source text and a running process, and how can input become code?",
        story="The Job is rewritten as a compiler would write it: four object files with 16 holes where a name's "
              "address is not yet known, which Pebble's new linker joins into one 864-byte program that prints the "
              "same twenty words. Beside it stands a greeting program that prints 'pwned' when given 81 chosen "
              "bytes. The part follows a program's life to explain both. Data becomes bytes with an endianness, an "
              "alignment and padding; ifs, loops and a switch become branches and a jump table; calls become "
              "frames on a stack under a calling convention, traced on fact(10) and Ackermann's function. The "
              "heap is managed with free lists and boundary tags, five allocators replay a trace of 146,336 real "
              "allocations, and Knuth's fifty-percent rule is derived and set against Robson's worst case. Object "
              "files, static and dynamic linking, loading and the address space are read from this machine's own "
              "binaries. The part turns at undefined behaviour and the stack smash: an unchecked copy runs 76 "
              "bytes up the frame and overwrites the saved return address, and a canary, a no-execute stack, "
              "randomization and bounds each stop a different step. It ends with CHERI capabilities, verified "
              "compilation and what is still open about allocators.",
        handoff="The calling convention and object files are what Part 13's compiler emits; reclamation and moving "
                "collectors are built in Part 15; exceptional control flow, signals and system calls come in Part "
                "31 and pages behind the address space in Part 32; compiler correctness returns in Part 54, and "
                "the stack smash grows into code-reuse attacks in Part 55.",
        outside="Reading C at the level of structs, arrays and pointers helps; Part 6's assembly is used throughout.",
        objectives={
            "U": ["Lay out a struct with its padding, compute an array element's address, and read a word's bytes "
                  "in little-endian order.",
                  "Write a function's prologue and epilogue under Pebble's calling convention, and draw the stack "
                  "during a recursive call.",
                  "Explain step by step how an unbounded copy overwrites a return address, and what a canary and a "
                  "no-execute stack each detect."],
            "M": ["Implement first fit with splitting and coalescing, and compare allocation policies on a trace "
                  "by peak heap over peak live bytes.",
                  "Derive Knuth's fifty-percent rule from its balance argument, stating its assumptions.",
                  "Link two object files by hand: resolve the symbols, lay out the sections and patch each "
                  "relocation."],
            "D": ["State Robson's model (online, nonmoving, bounded live storage) and explain why one adversarial "
                  "replay is not a proof against every allocator.",
                  "Explain what spatial capabilities guarantee and what they leave to temporal safety, and what a "
                  "verified compiler's theorem does and does not cover."],
            "I": ["Diagnose undefined references, duplicate symbols and archive-order errors from the linker's "
                  "messages, and read a backtrace.",
                  "Use UBSan and AddressSanitizer on a failing program, and check which stack, page and "
                  "randomization defences a build actually enables."],
        },
        results=[
            ("Alignment", r"\text{offset}(f)\equiv 0 \pmod{\text{align}(f)},\qquad \text{size}\equiv 0 \pmod{\max_f \text{align}(f)}"),
            ("Row-major arrays", r"\&a[i][j]=\text{base}+(i\cdot\text{cols}+j)\cdot\text{size}"),
            ("Knuth's fifty-percent rule", r"\text{holes}\ \approx\ \tfrac12\,p\,N"),
            ("Robson's worst case", r"\text{heap}\ \propto\ M\log n,\qquad n=\frac{\text{largest block}}{\text{smallest block}}"),
            ("A buddy's address", r"\text{buddy}(a)=a\oplus\text{size}"),
            ("Relocating la on Pebble", r"\text{lui}\leftarrow\lfloor S/2^{10}\rfloor,\qquad \text{ori}\leftarrow S \bmod 2^{10}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 14), D=(16,), I=(11, 13),
        also=(("Pebble's linker and loader", "explainer/cs/pebble/link.py"), ("The heap simulator", "explainer/cs/pebble/heap.py"),
              ("The stack smash", "explainer/cs/pebble/smash.py")),
    ),
    Part(
        n=12, level="U", widget="regexblowup", prereq=(1, 5),
        question="What kind of machine can read a sentence, and why can six characters of regex stall a website?",
        story="The pattern (a+)+b, matched against a row of a's with no b, takes Python about four times longer "
              "for every two a's added, and in July 2019 a firewall rule of the same kind exhausted Cloudflare's "
              "processors for 27 minutes. The part builds the theory that explains it and that a compiler needs "
              "first. A language is a set of strings. Regular expressions and finite automata describe the same "
              "languages: Thompson's construction turns an expression into an NFA simulated on sets of states in "
              "time O(mn), the subset construction makes it deterministic at a price of up to 2 to the n states, "
              "and state elimination closes Kleene's triangle. The pumping lemma shows what no finite memory can "
              "do: match a to the n with b to the n. The part turns there. A stack supplies the missing memory, "
              "grammars turn a flat list of tokens into a tree, and the Chomsky hierarchy orders languages by the "
              "memory they need. Seven parsing algorithms follow, from CYK and Earley to LL(1), Pratt and the LR "
              "family checked against bison, and the Pebble language gets its lexer, a 79-rule grammar with a "
              "conflict-free 146-state LALR table, and a parser that reads the Job. The frontier asks how fast "
              "matching and parsing can be at all.",
        handoff="Part 13 compiles the tree the parser builds; Part 14 handles what a grammar cannot, types and "
                "declarations; CYK returns as dynamic programming in Part 19 and finite automata in Part 21's "
                "string algorithms; Part 25 proves that ambiguity is undecidable, and Part 26 explains the "
                "NP-completeness of back-references and the hypothesis behind the frontier.",
        outside="Sets, functions and proof by contradiction, as in Part 2. No formal-language background is assumed.",
        objectives={
            "U": ["Write a regular expression and a DFA for a simple language, and convert an NFA to a DFA by the "
                  "subset construction.",
                  "Use the pumping lemma to prove a language such as a^n b^n is not regular.",
                  "Write a context-free grammar for nested structure, draw parse trees, and show that a grammar "
                  "is ambiguous."],
            "M": ["Build Thompson's NFA for an expression, simulate it on sets of states, and minimize the "
                  "resulting DFA.",
                  "Compute FIRST and FOLLOW, build an LL(1) table, and construct the LR(0) items and an SLR or "
                  "LALR table for a small grammar, locating any conflict.",
                  "Fill a CYK table, and explain why the n-th-from-end language needs 2^n deterministic states."],
            "D": ["State the conditional lower bounds for regular-expression matching and context-free "
                  "recognition with their exact input models and hypotheses.",
                  "Build a DFA by Brzozowski derivatives, and explain why the residual languages give the minimal "
                  "machine only after expressions are normalized."],
            "I": ["Recognize a pattern with nested or overlapping repetition, and choose between an automaton "
                  "engine and a backtracking one by features, guarantees and limits.",
                  "Choose between a hand-written recursive-descent parser and a generated LR parser, and put "
                  "input limits and timeouts around patterns that are not trusted."],
        },
        results=[
            ("Kleene's theorem", r"\text{regular expression}\iff\text{NFA}\iff\text{DFA}"),
            ("Thompson simulation", r"O(mn)\ \text{time},\quad O(m)\ \text{active states}"),
            ("The n-th symbol from the end is 1", r"\text{NFA: } n+1 \text{ states},\qquad \text{smallest DFA: } 2^n \text{ states}"),
            ("The pumping lemma", r"s\in L,\ |s|\ge p\ \Rightarrow\ s=xyz,\ |xy|\le p,\ |y|>0,\ xy^iz\in L\ \ (i\ge 0)"),
            ("Naive backtracking on (a+)+b", r"2^{\,n-1}\ \text{ways to cut } a^n \text{ into groups}"),
            ("CYK", r"O(n^3)\ \text{for a fixed grammar in Chomsky normal form}"),
        ],
        U=(0, 1, 2, 3, 4, 6, 8, 9, 10), D=(15,), I=(7,),
        also=(("The regex engines", "explainer/cs/lang/regex.py"), ("Automata", "explainer/cs/lang/automata.py"),
              ("Grammars and parsers", "explainer/cs/lang/grammar.py")),
    ),
]
