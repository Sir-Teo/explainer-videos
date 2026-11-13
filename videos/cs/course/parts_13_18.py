"""Act III's compiler, types and runtimes, and the opening of Act IV, Algorithms (Parts 13-18)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=13, level="U", widget="ssacoloring", prereq=(6, 8, 12),
        question="Can a program write machine code as good as the code a person writes by hand?",
        story="The part opens on the Job's scan loop from Part 6, where the hand-written assembly advances a "
              "pointer by twelve bytes and the source indexes a table instead. FORTRAN in 1957 had to come close "
              "to hand-coded programs or nobody would have used it, and the part builds a compiler for the Pebble "
              "language under the same test. A checker resolves names, scopes, types and layouts, and the "
              "program becomes three-address code on a control-flow graph. On that graph dominators and their "
              "frontiers place the phi-functions of static single assignment, dataflow analysis becomes the "
              "search for a least fixed point on a lattice, and constant propagation, value numbering, loop "
              "transformations and inlining are measured pass by pass. Register allocation turns into graph "
              "colouring: hard in general, but strict SSA interference graphs are chordal, and the part shows the "
              "four-cycle without a chord that leaving SSA creates. Compiled at level 2 the array scan runs "
              "853,694 instructions against 827,576 for the hand-written loop and 4,466,758 unoptimized. The part "
              "ends by asking whether the compiler is right: a differential fuzzer, rewrite rules checked by an "
              "SMT solver, and a small superoptimizer that searches for short programs.",
        handoff="Part 14 proves what the type checker's promises are worth and Part 15 builds the runtimes where "
                "JIT compilers live; Parts 16 and 17 replace the Job's algorithm and this compiler carries the "
                "gain to the machine. Graph colouring returns in Part 18, Rice's theorem and NP-hardness are "
                "proved in Parts 25 and 26, CompCert's proof is Part 54, and Thompson's compiler backdoor is "
                "built into this compiler in Part 55.",
        outside="Programming in a C-like language, and graphs as vertices and edges. Sets ordered by inclusion "
                "are introduced where the lattices need them.",
        objectives={
            "U": ["Split three-address code into basic blocks, draw the control-flow graph and compute its "
                  "dominator tree.",
                  "Solve liveness on a small loop by iterating from empty sets, and build the interference graph "
                  "from the result.",
                  "Colour an interference graph by Chaitin's simplify and select, and say when a value must be "
                  "spilled."],
            "M": ["Compute dominance frontiers, place pruned phi-functions and rename along the dominator tree.",
                  "Explain why a monotone framework on a lattice of finite height converges, and when its "
                  "solution equals the meet over paths.",
                  "Derive why strict SSA interference graphs are chordal and why copies inserted on leaving SSA "
                  "can create a hole."],
            "D": ["State what the halting argument does and does not rule out for an optimizer, and what a "
                  "superoptimizer's validated candidate proves under its word model.",
                  "Reproduce the fixed-k clique-tree dynamic program for spill-everywhere on chordal graphs and "
                  "say which extensions change the problem."],
            "I": ["Choose optimization levels for a build, read the generated assembly, and measure "
                  "instructions, cycles and time as separate quantities.",
                  "Test a compiler change by differential fuzzing against a reference interpreter, and state "
                  "the language model before proving a rewrite such as (x * c) / c = x."],
        },
        results=[
            ("Dominance frontier", r"\operatorname{DF}(n)=\{\,y:\ n \text{ dom } p \text{ for some } "
                                   r"p\in\operatorname{pred}(y),\ n \text{ not sdom } y\,\}"),
            ("Liveness equations", r"\operatorname{IN}(b)=\operatorname{use}(b)\cup\bigl(\operatorname{OUT}(b)"
                                   r"\setminus\operatorname{def}(b)\bigr),\quad \operatorname{OUT}(b)="
                                   r"\bigcup_{s\in\operatorname{succ}(b)}\operatorname{IN}(s)"),
            ("Least fixed point", r"\operatorname{lfp}(f)=\bigsqcup_{k\ge 0} f^{k}(\bot)\quad"
                                  r"\text{for monotone } f \text{ on a lattice of finite height}"),
            ("Chaitin's simplify rule", r"\deg(v)<k\ \Longrightarrow\ \bigl(G \text{ is } k\text{-colourable}"
                                        r"\iff G-v \text{ is } k\text{-colourable}\bigr)"),
            ("Strict SSA interference", r"G \text{ chordal}\ \Longrightarrow\ \chi(G)=\omega(G)"
                                        r"=\text{most values live at once}"),
        ],
        U=(0, 1, 2, 3, 11), I=(13, 14), D=(15,),
        also=(("The Pebble compiler", "explainer/cs/lang/compiler"),),
    ),
    Part(
        n=14, level="U", widget="churchbeta", prereq=(1, 12, 13),
        question="How much of a programming language is left when everything but functions is taken away?",
        story="The part opens with the Job written in a lambda core with not one type annotation, and with every "
              "type inferred, and beneath it two plus three written with functions alone and rewritten by one "
              "rule to the numeral five in six steps. Church's calculus has three kinds of term and one "
              "computation rule, beta-reduction, which needs capture-avoiding substitution to be right. Booleans, "
              "numerals, pairs, Kleene's predecessor and, through the Y combinator, recursion are all encoded "
              "and counted in beta-steps: four factorial takes 10,384 of them. Strategies differ in whether "
              "they find a normal form, and Church-Rosser says they cannot disagree about which one, which the "
              "part checks on the whole reduction graph of a term. Then types: the simply typed calculus rejects "
              "stuck terms, progress and preservation are proved and run on 5,000 random terms, and the typed "
              "core always terminates, which is why Omega has no type. Hindley-Milner infers principal types by "
              "unification, System F adds polymorphism and free theorems, and under Curry-Howard a type is a "
              "proposition and a program is its proof. The part ends at dependent, linear and gradual types, "
              "with rustc and tsc on this machine supplying the error messages.",
        handoff="Part 15 gives the lambda core a runtime (environments, closures, continuations, a virtual "
                "machine and a garbage collector) and runs the Job on it. Part 25 proves the diagonal and "
                "recursion theorems used here, Part 43 puts types on the boundaries between services, Part 54 "
                "proves programs correct in Lean and Rocq, Part 55 returns to Rust, and Part 58 asks what "
                "programs mean.",
        outside="Functions as values in any programming language, and proof by induction. Part 1's lambda "
                "calculus is recalled, not assumed.",
        objectives={
            "U": ["Reduce a lambda term by hand with capture-avoiding substitution, and say whether it has a "
                  "normal form.",
                  "Write Church booleans and numerals and compute plus, times and the predecessor on them.",
                  "Type a small term in the simply typed lambda calculus by drawing its derivation tree."],
            "M": ["Prove progress and preservation for the simply typed calculus, naming the canonical-forms "
                  "and substitution lemmas.",
                  "Run Algorithm W on a let-polymorphic program, with unification and the occurs check.",
                  "Translate a propositional formula into a type and find a term for it, or a Kripke "
                  "countermodel."],
            "D": ["Sketch Tait's proof of strong normalization by logical relations and say why adding fix "
                  "ends it.",
                  "State a research question about gradual typing, polymorphic inference or cubical computation "
                  "with its model made explicit: the cast semantics, the cost model and the baseline."],
            "I": ["Explain why TypeScript accepts a covariant array write that fails at run time, and what a "
                  "sound gradual type system would charge for it.",
                  "Read rustc's ownership and borrowing errors as a linear and affine type discipline at "
                  "work."],
        },
        results=[
            ("Beta-reduction", r"(\lambda x.\,t)\,s\ \to_\beta\ t[x:=s]"),
            ("Church numerals", r"\bar n=\lambda f.\,\lambda x.\,f^{\,n}x,\qquad "
                                r"\mathrm{plus}=\lambda m\,n\,f\,x.\;m\,f\,(n\,f\,x)"),
            ("The Y combinator", r"Y=\lambda f.\,(\lambda x.\,f\,(x\,x))\,(\lambda x.\,f\,(x\,x)),\qquad "
                                 r"Y\,g=_\beta g\,(Y\,g)"),
            ("Church-Rosser", r"t\to^{*}u,\ t\to^{*}v\ \Longrightarrow\ \exists\,w:\ u\to^{*}w,\ v\to^{*}w"),
            ("Type safety", r"\vdash t:T\ \Longrightarrow\ t \text{ is a value or } t\to t',"
                            r"\ \text{ and then } \vdash t':T"),
            ("Curry-Howard", r"A\to B\ \leftrightarrow\ \text{function},\quad A\wedge B\ \leftrightarrow\ "
                             r"A\times B,\quad A\vee B\ \leftrightarrow\ A+B"),
        ],
        U=(0, 1, 2, 3, 7), I=(14,), D=(15,),
        also=(("The lambda reducer, the typed calculus and the inference engine", "explainer/cs/lang/lam"),),
    ),
    Part(
        n=15, level="U", widget="cheneycost", prereq=(11, 13, 14),
        question="Where does a program live while it runs, and who cleans up the memory it leaves behind?",
        story="The part opens on the Job's heap as it runs on the virtual machine this part builds: memory fills, "
              "the collector stops the program, keeps what is still reachable, and the program carries on. An "
              "interpreter is eval and apply; an environment captured with a function's code is a closure; and "
              "continuation-passing style turns the call stack into a value, so that a tail call is a jump. The "
              "lambda core of Part 14 is compiled to a stack bytecode with tagged words, and the virtual machine "
              "is written in the Pebble language and co-simulated with the reference machine on Pebble. Then "
              "memory: reference counting and its cycles, mark-sweep and mark-compact, and Cheney's copying "
              "collector with its scan and free pointers, whose copying work per allocated word is about "
              "L / (S - L) for live data L in a semispace S. Generations exploit short lifetimes, and a "
              "collector that runs while the program mutates the heap is kept correct by the tri-colour "
              "invariant and a write barrier. The part measures JIT tiers, inline caches, virtual dispatch and "
              "exceptions on real runtimes on this machine, assembles a WebAssembly module by hand, and runs "
              "the Job, garbage-collected, on the Pebble VM for ledger row 6.",
        handoff="Part 16 opens Act IV by changing the Job's algorithm. Part 31's kernel gives every thread its "
                "own stack and Part 32's virtual memory sits under every heap; Part 33 returns to atomics and "
                "memory barriers, the hardware relatives of the write barriers here. Part 42 opens the browser, "
                "where V8 and WebAssembly live, Parts 54 and 55 prove compilers and runtimes correct, and Part "
                "58 asks what a program means.",
        outside="Recursion and the call stack as Part 11 describes them, and pointers. The lambda core is Part "
                "14's; its types are not needed here.",
        objectives={
            "U": ["Trace eval and apply on a small expression, and show what a closure captures under lexical "
                  "scope and what dynamic scope would do instead.",
                  "Hand-compile a small function to stack bytecode and run it on paper.",
                  "Say which objects reference counting frees and which it misses, and mark a heap from its "
                  "roots."],
            "M": ["Run Cheney's algorithm on a small heap, with forwarding addresses and the scan and free "
                  "pointers, and derive the cost L / (S - L).",
                  "Convert a function to continuation-passing style and explain why proper tail calls bound the "
                  "stack.",
                  "State the strong and weak tri-colour invariants, show the move that loses an object, and say "
                  "which barrier (insertion or deletion) prevents it."],
            "D": ["State the first and second Futamura projections and what meta-tracing and partial evaluation "
                  "of interpreters do and do not guarantee.",
                  "Pose a real-time collection bound with its machine, allocation rate, roots, object sizes and "
                  "liveness limits made explicit."],
            "I": ["Size a heap from the live data and a pause or throughput target, and read a collector's log.",
                  "Explain a JIT's tiers, inline caches and deoptimization well enough to diagnose code that "
                  "stays slow after warmup.",
                  "Compare virtual dispatch and table-driven exceptions by measurement, and say what a "
                  "WebAssembly validator checks before a module runs."],
        },
        results=[
            ("A closure", r"\langle \lambda x.\,e,\ \rho\rangle\ \text{applied to } v:\quad "
                          r"\operatorname{eval}\bigl(e,\ \rho[x\mapsto v]\bigr)"),
            ("What a collector keeps", r"\text{live}\ \subseteq\ \text{reachable from the roots}\ =\ \text{kept}"),
            ("Copying cost", r"\frac{\text{words copied}}{\text{words allocated}}\ \approx\ \frac{L}{S-L}"
                             r"\qquad(L \text{ live},\ S \text{ semispace})"),
            ("Strong tri-colour invariant", r"\text{no black object points to a white object}"),
            ("Futamura projections", r"\operatorname{spec}(\mathit{int},p)=\mathit{target},\qquad "
                                     r"\operatorname{spec}(\operatorname{spec},\mathit{int})=\mathit{compiler}"),
        ],
        U=(0, 1, 2, 4, 6, 7), I=(11, 12, 13), D=(15,),
        also=(("The bytecode compiler, the reference VM and its collectors", "explainer/cs/runtime"),),
    ),
    Part(
        n=16, level="U", widget="pivotluck", prereq=(2, 6, 13),
        question="Can thinking about an algorithm beat a faster machine?",
        story="Seven ledger rows of better machines have left the Job quadratic: its cost per byte rises from "
              "about 290 cycles on 10 kB of text to 4,279 on the corpus. The part learns to count steps. It "
              "fixes what a step is (the RAM, the word-RAM, the comparison model) and what O, Omega and Theta "
              "claim, then sorts: insertion sort with its invariant and its n(n - 1)/4 inversions, merge sort "
              "with its recursion tree, and the master theorem that adds such trees up. A decision tree with "
              "n! leaves shows that no comparison sort can use fewer than lg n! comparisons, and merge "
              "insertion meets that bound up to n = 11 and misses it at 12, 30 against 29. Quicksort's expected "
              "2(n + 1)H_n - 4n comparisons follow from one observation about when two keys are compared, and "
              "10,000 runs show how tightly it concentrates; a first-element pivot on sorted input pays "
              "1,999,000 comparisons where median-of-three pays about 21,000. Counting and radix sort escape "
              "the bound by not comparing, median of medians selects in linear time, and generating functions "
              "and amortized analysis close the toolkit. The Job, sorted and then counted, makes 103 million key "
              "comparisons on the corpus where the search made 15.0 billion, and enters the ledger as row 7.",
        handoff="Part 17 replaces the sort with a hash table for ledger row 8, and Part 18's graph algorithms "
                "run on this part's heaps. Part 19 generalizes divide and conquer and adds dynamic programming, "
                "Part 20 builds the probability tools that the concentration chapter previews, Part 21 sorts the "
                "suffixes of a text, Part 26 asks which lower bounds can be proved at all, and Part 35's "
                "database sorts tables larger than memory.",
        outside="Logarithms, sums and proof by induction (Part 2). Expected values are used for quicksort and "
                "explained where they appear.",
        objectives={
            "U": ["State and use O, Omega and Theta, and rank functions by their order of growth.",
                  "Prove insertion sort correct by its loop invariant and count its comparisons through "
                  "inversions.",
                  "Solve a divide-and-conquer recurrence with a recursion tree or the master theorem, and "
                  "explain the lg n! lower bound with a decision tree."],
            "M": ["Derive quicksort's expected 2(n + 1)H_n - 4n comparisons from the probability 2/(j - i + 1) "
                  "that two keys are compared.",
                  "Analyse median of medians, T(n) <= T(n/5) + T(7n/10) + O(n), and say why groups of three "
                  "fail.",
                  "Carry out an amortized analysis of the doubling array by the aggregate, accounting and "
                  "potential methods."],
            "D": ["State what smoothed analysis measures and what a word-RAM integer-sorting bound assumes "
                  "about word width and randomness.",
                  "Explain a fine-grained hardness assumption such as SETH or 3SUM and the kind of lower bound "
                  "it yields."],
            "I": ["Choose a library sort for given data (presorted runs, small integer keys, stability, data "
                  "larger than memory) and justify the choice by counts.",
                  "Fit an instruction model to event counts, validate it on held-out inputs, and say what a "
                  "projection from it does and does not establish."],
        },
        results=[
            ("Master theorem (with one more factor log n when the two exponents tie)",
             r"T(n)=a\,T(n/b)+\Theta(n^{c})\ \Longrightarrow\ T(n)=\Theta\bigl(n^{\max(c,\,\log_b a)}\bigr)"),
            ("Comparison lower bound", r"\text{comparisons}\ \ge\ \lceil \lg n!\rceil=n\lg n-n\lg e+O(\lg n)"),
            ("Insertion sort, average", r"\mathbb{E}[\text{inversions}]=\frac{n(n-1)}{4}"),
            ("Quicksort, average", r"\mathbb{E}[C_n]=2(n+1)H_n-4n\ \approx\ 2n\ln n\ \approx\ 1.39\,n\lg n"),
            ("Heapify is linear", r"\sum_{h\ge 0}\frac{h}{2^{h}}=2\ \Longrightarrow\ \text{build-heap}=O(n)"),
            ("Median of medians", r"T(n)\le T(n/5)+T(7n/10)+O(n)\ \Longrightarrow\ T(n)=O(n)"),
        ],
        U=(0, 2, 3, 4, 5, 6, 7, 8), I=(14, 15), D=(16,),
        also=(("Every sort, with its comparison counter", "explainer/cs/algo/sorts.py"),),
    ),
    Part(
        n=17, level="U", widget="probeclusters", prereq=(2, 9, 16),
        question="Can a program look a word up in constant time, however many words it has seen?",
        story="Part 16's sorted Job made about a hundred million word comparisons, but the Job never needed its "
              "words in order: it needed a dictionary that can insert, look up and count. On this corpus that is "
              "4,609,954 lookups for 57,895 distinct words. Hashing answers in expected constant time under "
              "assumptions the part states one by one: the birthday bound says collisions come early, universal "
              "hashing chooses the function at random so that no fixed set of keys is bad, and linear probing "
              "pays Knuth's (1 + 1/(1 - a)^2)/2 probes as the load a approaches one. Cuckoo and perfect hashing "
              "buy worst-case lookups. Search trees keep order instead: a random binary search tree is "
              "quicksort in disguise, AVL and red-black trees bound the height, treaps and skip lists do it by "
              "coin flips, splay trees by amortization, and B-trees by counting block transfers. Heaps, "
              "union-find with its inverse-Ackermann bound, tries, succinct rank directories and persistence "
              "complete the catalogue, each instrumented and measured. The Job is rewritten with a hash table "
              "in the Pebble language, and a model fitted to emulator passages projects about 0.794 seconds for "
              "the next ledger row; the frontier asks how good a data structure can be.",
        handoff="Part 18's Dijkstra and Kruskal run on this part's heaps and union-find. Part 20 builds Bloom "
                "filters and sketches from universal hash families, Part 21 turns tries into suffix trees and "
                "compressed indexes, Part 33 makes hash maps and skip lists safe for many threads, Parts 34 and "
                "35 build storage engines on log-structured merge trees and B+ trees, and Part 47's search "
                "engine is an inverted index.",
        outside="Part 16's counting (O-notation, expected values, amortization) and modular arithmetic. Part "
                "9's cache hierarchy explains the timings but is not required.",
        objectives={
            "U": ["Estimate when the first collision arrives with the birthday bound, and compute expected "
                  "chain lengths at a given load.",
                  "Insert and look up by hand in a linear-probing table and in a binary search tree, and say "
                  "what sorted input does to each.",
                  "Run union by rank with path compression on a small forest."],
            "M": ["Prove that ((ax + b) mod p) mod m is a universal family and say what the proof assumes "
                  "about the keys.",
                  "Bound an AVL tree's height through Fibonacci trees, and read a red-black tree as a 2-3-4 "
                  "tree.",
                  "Prove the splay access lemma with the potential function, including the final zig's extra "
                  "one."],
            "D": ["State the dynamic optimality conjecture and what the known competitive bounds do and do not "
                  "settle.",
                  "Separate an open-addressing theorem's model (uniform probing, greedy or non-greedy insertion, "
                  "reordering) from an experiment at fixed occupancy."],
            "I": ["Choose between a hash map and an ordered map for a workload, and check the hash function's "
                  "defence against flooding by untrusted keys.",
                  "Size a B-tree's fan-out from the block size and count the block transfers of a lookup.",
                  "Benchmark complete equivalent tasks, and say what a timing alone cannot show about cache "
                  "misses."],
        },
        results=[
            ("Birthday bound", r"\Pr[\text{some collision among } n \text{ keys in } m \text{ slots}]"
                               r"\approx 1-e^{-n^{2}/2m}"),
            ("Universal hashing (a, b random, x and y distinct)",
             r"h(x)=((ax+b)\bmod p)\bmod m:\quad \Pr[h(x)=h(y)]\le \frac1m"),
            ("Linear probing at load alpha", r"\text{miss}\approx\tfrac12\Bigl(1+\frac{1}{(1-\alpha)^{2}}\Bigr),"
                                         r"\qquad \text{hit}\approx\tfrac12\Bigl(1+\frac{1}{1-\alpha}\Bigr)"),
            ("Random binary search tree", r"\mathbb{E}[\text{depth of a node}]=2\Bigl(1+\frac1n\Bigr)H_n-4"
                                          r"\ \approx\ 1.39\lg n"),
            ("AVL height", r"h<1.4405\,\lg(n+2)"),
            ("Union-find", r"m \text{ operations on } n \text{ elements cost } O\bigl(m\,\alpha(n)\bigr)"),
        ],
        U=(0, 1, 2, 3, 5, 6, 11), I=(9, 13, 14, 15), D=(16,),
        also=(("The instrumented data structures", "explainer/cs/algo/ds.py"),),
    ),
    Part(
        n=18, level="U", widget="astarweight", prereq=(2, 16, 17),
        question="What can be computed about a map, a network or a web of links once it is drawn as dots and lines?",
        story="In 1736 the citizens of Koenigsberg asked whether a walk could cross each of their seven bridges "
              "exactly once, and Euler answered by throwing away everything but which land mass each bridge "
              "joins: a circuit exists exactly when the graph is connected and every degree is even. From that "
              "abstraction the part builds the standard algorithms, each with the proof that makes its output "
              "checkable. Breadth-first search finds layers and odd cycles, depth-first search stamps intervals, "
              "and from them come topological order and strongly connected components. Dijkstra's algorithm, "
              "designed in twenty minutes at a cafe, rests on an invariant about settled vertices that one "
              "negative edge breaks; Bellman-Ford, Floyd-Warshall and Johnson's reweighting repair that. On a "
              "synthetic city, forty exact routes cost about 2,525 vertex expansions with Dijkstra, 657 with "
              "straight-line A* and 113 with a contraction hierarchy. Minimum spanning trees follow from an "
              "exchange argument, and a maximum flow is certified by a cut of the same value, 19 on the worked "
              "example. Matching, PageRank and planar colouring follow, and the gap between Euler's circuits "
              "and Hamilton's cycles is the first sight of P against NP. The last chapter states recent "
              "shortest-path and flow results with their models and dates.",
        handoff="Part 19 turns Floyd-Warshall and Held-Karp into a general method, dynamic programming. Part 20 "
                "finds minimum cuts by contracting random edges, Part 23 shows that max flow and min cut are "
                "dual linear programs, Part 26 is about Hamiltonian cycles and NP-completeness, the internet's "
                "routing in Part 36 runs Bellman-Ford and Dijkstra across routers, and Part 47's search engine "
                "ranks the web.",
        outside="Part 16's O-notation and Part 17's heaps and union-find. Proof by induction and by "
                "contradiction, as in Part 2.",
        objectives={
            "U": ["Decide whether a multigraph has an Euler circuit and construct one with Hierholzer's "
                  "algorithm.",
                  "Run BFS, DFS and Dijkstra by hand, and state the invariant that makes Dijkstra's settled "
                  "distances final.",
                  "Build a minimum spanning tree with Kruskal's or Prim's algorithm and justify each edge by "
                  "the cut property."],
            "M": ["Prove the max-flow min-cut theorem from the residual graph, and read a minimum cut off a "
                  "maximum flow.",
                  "Prove that Johnson's reweighting keeps shortest paths and makes every weight nonnegative.",
                  "Prove that Gale-Shapley ends with a stable matching, and that five colours suffice for a "
                  "planar graph by Kempe chains."],
            "D": ["State the 2024 universal-optimality result for Dijkstra and the 2025 bound beyond the "
                  "sorting barrier, each with its model: comparison-addition, real weights, distance-only "
                  "output.",
                  "Say what remains open for distance-only single-source shortest paths in O(m + n) time."],
            "I": ["Choose between Dijkstra, bidirectional search, A*, landmarks and contraction hierarchies "
                  "for a routing service, counting preprocessing and per-query work separately.",
                  "Compute PageRank by power iteration with dangling pages handled, and bound the error from "
                  "the stationarity residual, not from the last change."],
        },
        results=[
            ("Euler's theorem (connected multigraphs)", r"\text{an Euler circuit exists}\iff\text{every degree is even}"),
            ("Dijkstra's invariant", r"w\ge 0:\quad \text{when } u \text{ is settled},\ d(u)=\delta(s,u)"),
            ("A* is exact when", r"\text{priority}=d(v)+h(v),\qquad h(v)\le\delta(v,t),\quad h(t)=0"),
            ("Cut property", r"e \text{ uniquely lightest across a cut}\ \Longrightarrow\ e\in\text{every MST}"),
            ("Max-flow min-cut", r"\max_f |f|=\min_{(S,T)} c(S,T)"),
            ("PageRank (D is the rank held by dangling pages)",
             r"r_v=\frac{1-d+dD}{n}+d\sum_{u\to v}\frac{r_u}{\deg^{+}(u)}"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7, 10), I=(9, 14), D=(16,),
        also=(("The graph algorithms, each counting its work", "explainer/cs/algo/graphs.py"),),
    ),
]
