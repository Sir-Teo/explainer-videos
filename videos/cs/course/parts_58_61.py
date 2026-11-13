"""Act XI, The Research Frontier, concluded: semantics, distributed computing theory, domain-specific hardware, doing research (Parts 58-61)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=58, level="D", widget="kleenefactorial", prereq=(13, 14, 15, 54),
        question="What does a program mean, and when do two programs mean the same thing?",
        story="The part opens with three meanings of factorial: as steps (the small-step interpreter rewrites "
              "fact 3 down to 6 in 18 steps), as a limit (a chain of partial functions) and as laws. One small "
              "call-by-value language with recursion is given Plotkin's small-step rules, Kahn's big-step rules "
              "and a CEK machine, and the three agree on 300 of 300 random programs. Scott and Strachey's "
              "denotational semantics then gives each construct one equation, and recursion becomes the least "
              "fixed point of a continuous functional on a complete partial order, computed as the Kleene chain "
              "whose k-th member is factorial on 0 to k - 1. Soundness and adequacy tie the steps to the "
              "mathematics by a logical relation; the turn is full abstraction, which fails for PCF because "
              "parallel-or is continuous but not sequential. The same tools decide when programs are equal "
              "(bisimulation tells a.(b + c) from a.b + a.c although their traces agree), read theorems off types "
              "(Reynolds's and Wadler's parametricity, tested on random lists, with the counterexample for sort "
              "under squaring), and prove Hoare logic sound. The part ends by stretching meaning to effects as "
              "monads and handlers, dependent types, and CCS and the pi-calculus, and at the frontier with "
              "mechanized semantics of C, ML and WebAssembly, homotopy type theory, and a memory model for C "
              "that is still open.",
        handoff="The processes of chapter 10 return as Part 59's distributed algorithms. Part 60 describes "
                "hardware as programs whose meaning must match a specification, and Part 61 treats proof as a "
                "research method and puts the memory model for C on its map of open problems. Looking back, "
                "Part 54's verification and Part 55's trusted compilers rest on the soundness proofs given here.",
        outside="Proof by induction on derivations, partial orders and least upper bounds; some experience "
                "with a functional language helps.",
        objectives={
            "U": ["Evaluate a small program by the small-step rules, naming the search or reduction rule used at "
                  "each step.",
                  "Compute the first Kleene iterates of the factorial functional and say on which inputs each is "
                  "defined."],
            "M": ["Prove that small-step evaluation is deterministic, by induction on derivations.",
                  "Prove Kleene's fixed-point theorem, and show that the factorial functional is continuous and "
                  "that its least fixed point is factorial.",
                  "Derive the free theorem for a function of type forall a. [a] -> [a] from the relational "
                  "reading of types."],
            "D": ["Prove adequacy for a language with fix by a logical relation, handling fix through the Kleene "
                  "chain and admissibility.",
                  "Explain with parallel-or why Scott's model is not fully abstract for PCF, and what game "
                  "semantics changes.",
                  "State the out-of-thin-air problem and what an accepted relaxed-memory semantics for C would "
                  "have to forbid, permit and compile to."],
            "I": ["Test two implementations of a language against each other on random terminating programs, "
                  "and say what agreement does and does not show.",
                  "Use a free theorem as a property test or a fusion rule, and say where seq, run-time type "
                  "tests and general recursion weaken it."],
        },
        results=[
            ("Kleene's fixed-point theorem", r"\operatorname{fix}F=\bigsqcup_{k\ge 0}F^{k}(\bot)"
                                             r"\quad\text{for continuous }F\text{ on a cpo}"),
            ("Soundness and adequacy", r"e\to^{*}v\ \Rightarrow\ [\![e]\!]=[\![v]\!],\qquad"
                                       r"[\![e]\!]=n\ \Rightarrow\ e\to^{*}n"),
            ("Bisimilarity is finer than traces", r"a.(b+c)\ \not\sim\ a.b+a.c,\qquad"
                                                  r"\text{both have traces }\{\varepsilon,a,ab,ac\}"),
            ("A free theorem", r"r:\forall a.\,[a]\to[a]\ \ \Rightarrow\ \ "
                               r"\operatorname{map}f\circ r=r\circ\operatorname{map}f"),
            ("Soundness of Hoare logic", r"\vdash\{P\}\,c\,\{Q\}\ \ \Rightarrow\ \ \models\{P\}\,c\,\{Q\}"),
            ("Monad laws, left unit", r"\operatorname{return}a\ \mathbin{>\!\!>\!\!=}\ k\;=\;k\,a"),
        ],
        U=(0, 1, 2), D=(11,), I=(8,),
        also=(("The semantics instruments", "explainer/cs/semantics/meaning.py"),),
    ),
    Part(
        n=59, level="D", widget="colevishkinring", prereq=(33, 38, 39),
        question="What can n processes compute when each sees only its neighbours, or may crash, or may lie?",
        story="A million processes on a ring, each knowing only its own identifier and its successor's, must "
              "3-colour themselves, and Cole and Vishkin's bit-position trick does it in seven rounds: a million "
              "colours, then 38, 12, 8, 6, 5, 4 and 3. Linial's lower bound shows that about log* n rounds are "
              "needed by any algorithm, through a speed-up lemma on neighbourhood graphs. The part then turns "
              "from locality to agreement. FloodSet is checked against every input and crash pattern, and f "
              "crashes are shown to need f + 1 rounds; the hexagon of Fischer, Lynch and Merritt, run against a "
              "two-round majority protocol, shows that three processes cannot survive one liar. Under asynchrony "
              "the FLP proof is given for three processes and Ben-Or's coins get around it, at a cost in phases "
              "that roughly doubles with every two processes. Shared memory brings Herlihy's consensus hierarchy, "
              "and the turn of the part is topological: one round of immediate snapshots subdivides a simplex, "
              "and Sperner's lemma makes k-set agreement impossible. Failure detectors, the Dolev-Reischuk "
              "message bound and population protocols follow, and the part ends on the classification of "
              "locally checkable problems.",
        handoff="Part 60's accelerators are networks of cells that pass values to their neighbours, the same "
                "picture as the LOCAL model. Part 61 asks how to choose an open problem and how to measure "
                "honestly. Looking back, this is the theory under Part 38's consensus, Part 39's replication "
                "and the protocols Part 54 checked.",
        outside="Graphs and colourings, logarithms and binary notation, proof by contradiction; no topology is "
                "assumed.",
        objectives={
            "U": ["Run one round of Cole and Vishkin's rule on a short ring by hand, and explain why neighbours "
                  "still differ afterwards.",
                  "Compute log* n, and tell crash, omission and Byzantine faults and synchronous and asynchronous "
                  "models apart."],
            "M": ["Prove that b-bit colours shrink to 1 + ceil(log2 b) bits in a round, and bound the rounds by "
                  "log* n plus a constant.",
                  "Prove that f crashes need f + 1 synchronous rounds, and that Byzantine agreement without "
                  "signatures needs n > 3f, by the hexagon argument.",
                  "State Sperner's lemma and use it to show that three processes cannot solve wait-free 2-set "
                  "agreement."],
            "D": ["Prove Linial's speed-up lemma on neighbourhood graphs and derive the bound t >= (log* n)/2 - 1.",
                  "State the asynchronous computability theorem, and explain why the subdivision after r rounds "
                  "of immediate snapshots has no holes.",
                  "State the classification of locally checkable labellings on rings, and name a gap on general "
                  "graphs that is still open."],
            "I": ["Read a consensus library's fault assumptions (crash or Byzantine, n > 2f or n > 3f, timing) "
                  "and say which theorem each one answers.",
                  "Compare PBFT's and HotStuff's messages per view against the Dolev-Reischuk bound, and say "
                  "what phi accrual and SWIM failure detectors trade."],
        },
        results=[
            ("Cole and Vishkin's step", r"c_v\ \leftarrow\ 2i+\operatorname{bit}_i(c_v),\qquad "
                                        r"i=\min\{j:\operatorname{bit}_j(c_v)\ne\operatorname{bit}_j(c_{s(v)})\}"),
            ("Linial's lower bound", r"\chi(B_k)\le c\ \Rightarrow\ \chi(B_{k-1})\le 2^{c},\qquad "
                                     r"t\ \ge\ \tfrac12\log^{*}n-1"),
            ("Synchronous agreement", r"f\text{ crashes: } f+1\text{ rounds};\qquad "
                                      r"f\text{ liars, no signatures: } n>3f"),
            ("Sperner's lemma", r"\#\{\text{rainbow triangles}\}\ \equiv\ 1\pmod 2"),
            ("Dolev and Reischuk", r"\text{Byzantine agreement costs }\Omega(n+f^{2})\text{ messages}"),
            ("Exact majority", r"\#A-\#B\ \text{ is invariant under }\ A+B\to a+b"),
        ],
        U=(0, 1, 2), D=(11,), I=(8, 9),
        also=(("The distributed-theory instruments", "explainer/cs/disttheory/theory.py"),),
    ),
    Part(
        n=60, level="D", widget="systolicwave", prereq=(4, 9, 10, 52),
        question="When a general-purpose processor stops getting faster, what does hardware built for one kind of "
                 "work buy, and what does it cost?",
        story="The part opens on a table of energies at 45 nm: an 8-bit add costs 0.03 pJ and a 64-bit read from "
              "DRAM as much as 90,000 of them, so a processor that spends 10 pJ fetching an instruction to do a "
              "0.1 pJ add is at most 1% useful. The roofline model is derived from two inequalities and this "
              "machine's two roofs are measured, with each kernel placed under them. Then H. T. Kung's systolic "
              "array is built from Part 4's multipliers and simulated gate by gate: the operands of a matrix "
              "product meet in cell (i, j) at cycle i + j + k, so the product crosses an N by N grid as a "
              "diagonal wave in 3N - 2 cycles, exact against NumPy. Which number stays put decides utilization: "
              "a third for one output-stationary product, above 80% for a long weight-stationary stream. The "
              "same grid at 256 by 256 with 8-bit numbers is Google's first TPU, and its paper's 92 TOPS is "
              "recomputed. The part goes on through GPUs and tensor cores, spatial machines, computing near "
              "memory, sparsity and approximation, and how hardware is designed, and then turns the Job itself "
              "into a four-stage circuit that counts one byte every cycle: ledger row 21, the thirty novels in "
              "about 31 ms. It ends on accelerators for language models, where decoding one token at batch 1 "
              "uses 0.3% of the peak.",
        handoff="Part 61 asks how a number such as this machine's roofline should be measured and reported, "
                "gathers this part's open problems with the others on one map, and reads the ledger, with its "
                "twenty-first row from this part's circuit, one last time. The roofline also meets AI, Built "
                "Part 17 on Part 61's bridges.",
        outside="Matrix multiplication, binary arithmetic and logarithmic axes; the gates, adders and "
                "registers come from Parts 3 to 5.",
        objectives={
            "U": ["Compute a kernel's arithmetic intensity from its flops and its compulsory bytes, and place it "
                  "under a roofline.",
                  "Trace a 2 by 2 systolic product cycle by cycle and say when each cell is busy."],
            "M": ["Derive the roofline bound from T >= F/P and T >= Q/beta, and find the ridge point.",
                  "Derive the 3N - 2 cycles of an output-stationary grid and the utilizations N/(3N - 2) and "
                  "M/(M + 3N - 2).",
                  "Derive that stochastic rounding is unbiased with variance at most a quarter of the step "
                  "squared, and bound the accumulator width an int8 product needs."],
            "D": ["State Hong and Kung's red-blue pebble game and what an I/O lower bound for a grid of cells "
                  "with local memories would have to show.",
                  "Explain why decoding a language model at batch 1 sits far below the ridge, and compare the "
                  "remedies by what they change in the roofline."],
            "I": ["Read an accelerator paper's headline number (cells times operations times clock) and say "
                  "whether its workloads are compute-bound or memory-bound.",
                  "Quantize a matrix product or a linear classifier to int8 and report the error and the "
                  "change in answers.",
                  "Size a direct-mapped counting table from the expected number of words that find their slot "
                  "taken, m(1 - exp(-n/m))."],
        },
        results=[
            ("The roofline", r"\frac{F}{T}\ \le\ \min\bigl(P,\ I\beta\bigr),\qquad I=\frac{F}{Q}"),
            ("When operands meet", r"A_{ik}\text{ and }B_{kj}\text{ meet in cell }(i,j)\text{ at cycle }i+j+k"),
            ("Cycles and utilization", r"3N-2\ \text{cycles},\qquad \frac{N}{3N-2}\to\frac13,\qquad "
                                       r"\frac{M}{M+3N-2}\to 1"),
            ("Amdahl, for an accelerator", r"S=\frac{1}{(1-f)+f/s}\ \le\ \frac{1}{1-f}"),
            ("The TPU's matrix unit", r"256^{2}\times 2\times 700\ \text{MHz}=9.18\times 10^{13}\ \text{ops/s}"),
            ("Stochastic rounding", r"\mathbb{E}\,[r(x)]=x,\qquad \operatorname{Var}\,r(x)\le\tfrac{\Delta^{2}}{4}"),
        ],
        U=(0, 1, 2, 3), D=(12,), I=(5, 6, 7, 10, 11),
        also=(("The hardware instruments", "explainer/cs/hw"),),
    ),
    Part(
        n=61, level="D", widget="noiseonlyspread", prereq=(2, 7, 54, 60),
        question="Where do the results this series quoted come from, and how would you make one without fooling "
                 "yourself?",
        story="One C program, compiled once, is timed while an unused environment variable grows from nothing to "
              "4 KiB, and its median time moves by up to 7%. Mytkowicz, Diwan, Hauswirth and Sweeney showed in "
              "2009 that such changes move where the stack begins and can decide which compiler setting looks "
              "faster. The part rebuilds their experiment and turns on its own result: 4,000 noise-only "
              "experiments typically spread 10%, and 89% of them exceed the 6.7% observed, because Linux already "
              "starts the stack at a random address on every run. So the medians moved, and nothing shows that "
              "the environment moved them. From there the part is method: thirty runs of the Job with a "
              "bootstrap interval, why speedups are averaged geometrically, how benchmarks become targets and "
              "analyses fork, and what a computer search proves (Goldbach to 2,000,000, Euler's conjecture "
              "refuted by one line of integers, Polya's by a failure at 906,150,257). It practises reading in "
              "three passes, reviewing an invented paper, choosing a problem with Hamming and Polya, and writing "
              "an argument whose figures carry the claim. It ends on the eleven open problems the series met, "
              "drawn as a sky over the tower, on seven bridges to AI, Built and Analysis, Built, and on the "
              "ledger's 22 rows, from 281 seconds to 31.5 milliseconds.",
        handoff="This is the last part: nothing follows it in this series. Its bridges lead out to AI, Built "
                "(gradient descent, generalization, the roofline, typical sets) and to Analysis, Built "
                "(computable numbers, Fourier, convergence), and its map sends each open problem back to "
                "the part that met it, from Part 26's P versus NP to Part 54's verified software.",
        outside="Means, medians and the idea of a confidence interval; the rest is the series itself.",
        objectives={
            "U": ["Explain why one timing of a program is not a result, and report repeated runs with a median "
                  "and an interval.",
                  "Read a paper in three passes and say what its claim, its evidence and its baseline are."],
            "M": ["Compute a percentile bootstrap interval for a mean time, and predict how its width changes "
                  "with four times the runs.",
                  "Show that the geometric mean of speedup ratios does not depend on the reference machine, "
                  "while the arithmetic mean can favour either side.",
                  "Compute the chance that at least one of twenty null comparisons passes a 5% test."],
            "D": ["Design a noise-only control for a measured effect, and state what a spread inside the noise "
                  "does and does not show.",
                  "Say what a finite computer search proves about a conjecture and what it cannot, with "
                  "Goldbach, Euler's sum of powers and Polya as the cases.",
                  "Choose an open problem from the map, state its record, and name a special case small "
                  "enough to attack."],
            "I": ["Run a performance comparison with interleaved runs, randomized setup and a stated number of "
                  "runs, and report the totals for a fixed workload.",
                  "Review a systems paper: summary, strengths, weaknesses, questions, and what is not said "
                  "about runs, baselines and limitations."],
        },
        results=[
            ("Where a local lands", r"\text{address}=16\,\bigl\lfloor (T-e-c)/16\bigr\rfloor+k"),
            ("An interval for the mean", r"\bar x\ \pm\ 1.96\,\frac{s}{\sqrt n}:\qquad 4n\ \text{runs halve the width}"),
            ("Averaging speedups", r"\Bigl(\prod_{i=1}^{n}\frac{a_i}{b_i}\Bigr)^{1/n}"
                                   r"=\frac{\operatorname{GM}(a_i/r_i)}{\operatorname{GM}(b_i/r_i)}"),
            ("Forking paths", r"P(\text{a false alarm in 20 tests})=1-0.95^{20}\approx 0.64"),
            ("Euler refuted (Lander, Parkin)", r"27^{5}+84^{5}+110^{5}+133^{5}=144^{5}"),
            ("One descent step", r"f\bigl(x-\tfrac{f'(x)}{L}\bigr)\ \le\ f(x)-\frac{f'(x)^{2}}{2L}"
                                 r"\quad\text{if } f''\le L"),
        ],
        U=(0, 1, 3, 6, 11), D=(9,), I=(2, 4, 8),
        also=(("The research instruments", "explainer/cs/research/method.py"),),
    ),
]
