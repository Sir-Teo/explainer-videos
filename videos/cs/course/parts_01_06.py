"""Foundations and Act I: computation, proof, gates, arithmetic, memory, the stored-program computer (Parts 1-6)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=1, level="U", widget="beavertape",
        question="What does it mean to compute, and is there a question no machine can answer?",
        story="The part opens with Euclid's algorithm played with two piles of pebbles, and with Hilbert's 1928 "
              "demand for a procedure that decides every mathematical statement. It follows the idea of a "
              "mechanical method through Babbage's engines and Lovelace's Note G to Turing's 1936 machine: a tape, "
              "a head and a finite table. The series' simulator runs a unary adder and a palindrome checker that "
              "needs about half of n squared steps on one tape and 3n + 3 on two, and a universal machine of 14 "
              "states runs the 2-state busy beaver from its description. The lambda calculus, counter machines, "
              "Rule 110 and Life compute the same functions, which is the evidence for the Church-Turing thesis. "
              "Then the part turns: Cantor's diagonal shows there are more problems than programs, and Turing's "
              "diagonal shows that no machine decides halting. It ends with the busy beavers, all 47,176,870 steps "
              "of the 5-state champion run on screen, and with Antihydra, a 6-state machine nobody can settle.",
        handoff="The universal machine becomes the stored-program computer of Part 6, the interpreters of Part 15 "
                "and the hypervisors of Part 32. The finite control returns as the automata of Parts 5 and 12, the "
                "lambda calculus as the type theory of Part 14, and diagonalization and reductions drive Part 25, "
                "where Rice's theorem is proved. Pebble and the Job, introduced here, run through the whole series.",
        outside="School arithmetic and the ability to follow a program. No earlier part is needed.",
        objectives={
            "U": ["Trace a Turing machine from its table, step by step, and draw its space-time diagram.",
                  "Explain Cantor's diagonal argument and why it leaves most problems without a program.",
                  "State the halting problem and retell the proof with the program D run on its own text."],
            "M": ["Prove that Euclid's algorithm is correct by an invariant and terminates by a decreasing quantity.",
                  "Simulate a k-tape machine on one tape and bound the slowdown by a quadratic.",
                  "Prove that blank-tape halting is undecidable by a reduction from the halting problem."],
            "D": ["Prove that S(n) eventually exceeds every computable function.",
                  "Explain what a non-halting certificate is and how the deciders settled S(5).",
                  "State why Antihydra's halting is open and derive the 1/phi ruin probability of its random model."],
            "I": ["Recognize interpreters, emulators and virtual machines as universal machines in software.",
                  "Explain why a linter, a static analyzer or a virus scanner must approximate, citing Rice's theorem."],
        },
        results=[
            ("Lamé's bound", r"\#\text{steps of Euclid}(a,b) \le 5\cdot\#\text{digits}\bigl(\min(a,b)\bigr)"),
            ("Machines are countable", r"\#\{\text{machines with } n \text{ states}\} = (4n+4)^{2n}"),
            ("One tape against two", r"T_1(n)=\Theta(n^2), \qquad T_2(n)=3n+3 \quad\text{(palindromes)}"),
            ("The halting problem", r"\{\langle M,w\rangle : M \text{ halts on } w\} \text{ is undecidable}"),
            ("Busy beavers", r"S(2)=6,\ S(3)=21,\ S(4)=107,\ S(5)=47{,}176{,}870"),
            ("Antihydra's random model", r"q=\tfrac12+\tfrac12 q^{3} \;\Rightarrow\; q=\tfrac{\sqrt5-1}{2}=\tfrac1\varphi"),
        ],
        U=(0, 1, 2, 3, 4, 5, 7, 10, 11, 13), D=(14,), I=(15,),
        also=(("The Turing machine simulator", "explainer/cs/turing.py"), ("The lambda reducer", "explainer/cs/lam.py")),
    ),
    Part(
        n=2, level="U", widget="fifteenparity", prereq=(1,),
        question="How can you be certain that something is true for every case, or that a puzzle has no solution?",
        story="The part opens with the 15-puzzle craze of 1880 and the position with 14 and 15 swapped. Two numbers "
              "are watched through a random walk of slides, the swap parity of the sixteen squares and the blank's "
              "distance from home: they flip together, so their sum is an invariant, and a breadth-first search of "
              "the smaller puzzles reaches exactly the half of the positions it allows. From there the part "
              "supplies the mathematics the series stands on: truth tables and quantifiers, direct proof, "
              "contrapositive and contradiction, induction run as a recursive tromino tiling, structural "
              "induction, and invariants with decreasing measures. It then counts: bijections and Cantor's sizes "
              "of infinity, binomial coefficients, pigeonholes and Erdős-Szekeres, inclusion-exclusion and "
              "derangements, Catalan numbers, remainders and the Chinese remainder theorem, linearity of "
              "expectation, and the first facts about graphs. It ends at Ramsey numbers, where all 32,768 "
              "colourings of K6 are checked and the bounds on R(5,5) are still three apart.",
        handoff="Invariants and decreasing measures prove algorithms in Part 16, locks in Part 33, replicated "
                "systems in Part 39 and whole programs in Part 54. Structural induction is how Part 12 reasons "
                "about grammars and Part 14 about types. Counting and pigeonholes give the lower bounds of Part "
                "16 and the hash tables of Part 17; Bézout and the Chinese remainder theorem are the arithmetic "
                "of Parts 29 and 30; graphs carry Parts 18 and 36.",
        outside="School algebra. The epsilon-delta game of Chapter 1 is a callback to Analysis, Built, not a "
                "requirement.",
        objectives={
            "U": ["Prove a statement by induction, by contrapositive and by contradiction, and say which fits.",
                  "Find an invariant of a puzzle or a loop and use it to show a state is unreachable.",
                  "Count permutations, combinations and derangements, and compute an expectation with indicators."],
            "M": ["Prove Erdős-Szekeres by labelling each term with its longest increasing and decreasing runs.",
                  "Derive the Catalan recurrence and closed form, and give a bijection between two Catalan families.",
                  "Solve a system of congruences by the Chinese remainder theorem using Bézout coefficients."],
            "D": ["Prove R(3,3) = 6 and the bounds between the square root of 2 to the k and 4 to the k for R(k).",
                  "State the open problem of explicit Ramsey colourings and what the Paley graphs are known to give."],
            "I": ["Write a loop's invariant as an assertion and turn it into a property-based test.",
                  "Use the union bound and base rates to estimate failures across many machines and false alarms."],
        },
        results=[
            ("The puzzle's invariant", r"\operatorname{parity}(\pi) + d(\text{blank},\text{home}) \equiv 0 \pmod 2"),
            ("Erdős-Szekeres", r"n^2+1 \text{ distinct numbers} \Rightarrow \text{a monotone subsequence of } n+1"),
            ("Derangements", r"\frac{D_n}{n!}=\sum_{k=0}^{n}\frac{(-1)^k}{k!}\;\longrightarrow\;\frac1e"),
            ("Catalan numbers", r"C_{n+1}=\sum_{i=0}^{n}C_iC_{n-i},\qquad C_n=\frac{1}{n+1}\binom{2n}{n}"),
            ("Linearity of expectation", r"\mathbb{E}[\#\text{fixed points}]=\sum_{i=1}^{n}\tfrac1n=1"),
            ("Ramsey numbers", r"R(3,3)=6,\quad R(4,4)=18,\quad \sqrt2^{\,k}<R(k)<4^{k}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14), D=(15,),
    ),
    Part(
        n=3, level="U", widget="shannoncount", prereq=(2,),
        question="How do switches compute, and how many gates does a function need?",
        story="The part opens with Shannon's 1937 master's thesis: switches in series compute AND, switches in "
              "parallel compute OR, so a relay circuit is a Boolean expression and Boole's 1854 algebra simplifies "
              "it. The transistor replaces the relay, and the CMOS inverter's transfer curve, computed from "
              "square-law transistors, shows why a chain of gates restores a sloppy signal. NAND alone builds NOT, "
              "AND and OR, and so every truth table by its disjunctive normal form; an exhaustive search finds XOR "
              "in four NANDs. Karnaugh maps and Quine-McCluskey shrink the normal form, multiplexers turn a truth "
              "table into a lookup table, and decision diagrams give a canonical form whose size depends on the "
              "variable order. Then the part turns to cost: Shannon's 1949 count shows almost every function needs "
              "about 2^n / n gates, while the best bound proved for any explicit function is linear. It ends with "
              "the series' netlist simulator, the blocks Pebble needs, and the exact minimum circuits of every "
              "3-input function.",
        handoff="Gates, multiplexers and decoders build the adders of Part 4, the memories of Part 5 and Pebble "
                "itself in Part 6. The critical path decides how fast those circuits run, and Part 7's pipeline "
                "exists to shorten it; the power formula explains Part 10's turn to many cores. Decision diagrams "
                "return in Part 54, circuit lower bounds in Parts 26 and 27, reversible gates in Part 53.",
        outside="Truth tables and proof by cases from Part 2. No electronics is assumed: the transistor is "
                "treated as a voltage-controlled switch.",
        objectives={
            "U": ["Translate between a truth table, a Boolean expression and a circuit of gates.",
                  "Build NOT, AND, OR and XOR from NAND gates and explain why that makes NAND complete.",
                  "Minimize a four-variable function with a Karnaugh map and find a circuit's critical path."],
            "M": ["Apply Post's five closed classes to decide whether a set of gates is complete.",
                  "Build a reduced ordered decision diagram and show a function whose size depends exponentially on the order.",
                  "Reproduce Shannon's counting argument that almost all functions need about 2^n / n gates."],
            "D": ["Explain gate elimination and why it has only produced linear lower bounds for explicit functions.",
                  "State the Minimum Circuit Size Problem and what is known about its hardness."],
            "I": ["Describe a circuit as a netlist, simulate it bit-parallel and verify it on every input.",
                  "Explain how an FPGA's lookup table implements any small function, and what synthesis tools minimize."],
        },
        results=[
            ("NAND is complete", r"\lnot x = x\uparrow x,\quad x\land y=\lnot(x\uparrow y),\quad x\lor y=\lnot x\uparrow\lnot y"),
            ("Shannon expansion", r"f = x\,f|_{x=1} + \bar{x}\,f|_{x=0}"),
            ("Switching power", r"P \approx \alpha\,C\,V^{2} f"),
            ("Parity in two levels", r"2^{\,n-1}\ \text{product terms} \quad\text{against}\quad n-1\ \text{XOR gates}"),
            ("Shannon's count", r"\text{almost every } f:\{0,1\}^n\to\{0,1\} \text{ needs } \gtrsim \frac{2^n}{n} \text{ gates}"),
            ("The explicit gap", r"\text{best lower bound proved for an explicit } f:\ 3.1\,n \text{ gates}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 10, 13), D=(15,), I=(12,),
        also=(("The netlist simulator", "explainer/cs/pebble/hdl.py"), ("Quine-McCluskey", "explainer/cs/pebble/logic.py")),
    ),
    Part(
        n=4, level="U", widget="tinyfloat", prereq=(2, 3),
        question="How does a machine with finitely many bits add, multiply and divide, and when is its answer wrong?",
        story="The part opens with numbers that ran out: YouTube's 32-bit view counter, the Boeing 787's 248-day "
              "generator bug, and 0.1 + 0.2. Integers live on a clock of 2^n positions, and two's complement is a "
              "relabelling of that clock, so one adder serves signed and unsigned numbers. The ripple-carry adder "
              "is proved correct by induction and timed at 2n + 1 gate delays; seeing a block of bits as a "
              "function of its carry-in makes the carry operator associative, and the Kogge-Stone tree adds 64 "
              "bits in 15 delays. Multipliers become trees of carry-save adders, and division hides a table: "
              "emptying five cells of the series' SRT table reproduces the Pentium FDIV bug in miniature. Pebble's "
              "ALU is assembled and verified. Then the reals: fixed point, IEEE 754 with its doubling gaps, the "
              "rounding model, cancellation, Kahan's summation, the Patriot clock and Ariane 5, and Wilkinson's "
              "polynomial, whose roots fly apart when one coefficient moves by 2^-23. It ends with what is still "
              "open: how fast multiplication can be, and correctly rounded sin, exp and log.",
        handoff="Part 6 wires this ALU into Pebble, and Part 7 adds the multiplier and the divider to its "
                "pipeline. The parallel prefix returns in Part 10 as the scan. Overflow and integer types come "
                "back in the compiler of Part 13 and the security of Part 55; big integers and fast multiplication "
                "meet in Part 19 and drive the public-key cryptography of Part 30; rounding and conditioning "
                "return in Part 52, machine-checked arithmetic in Part 54.",
        outside="Gates, the critical path and induction from Parts 2 and 3. Newton's method is derived where it "
                "is used.",
        objectives={
            "U": ["Convert between decimal, binary and two's complement, and detect signed and unsigned overflow.",
                  "Build a ripple-carry adder from full adders and prove it correct by induction on the bits.",
                  "Decode an IEEE 754 number and explain why 0.1 + 0.2 is not 0.3."],
            "M": ["Derive the carry operator, prove it associative and compare the prefix networks' depth, size and fan-out.",
                  "Bound the error of naive, pairwise and Kahan summation with the model fl(x op y) = (x op y)(1 + delta).",
                  "Separate a problem's conditioning from an algorithm's stability, using Wilkinson's polynomial."],
            "D": ["State the known upper and lower bounds on integer multiplication and what the n log n algorithm leaves open.",
                  "Explain the table-maker's dilemma and what a correctly rounded elementary function requires."],
            "I": ["Choose between integers, fixed point, decimal and floating point for money, counters and measurements.",
                  "Explain how the FDIV table bug escaped random testing and what verification replaced it.",
                  "Compare binary16, bfloat16 and FP8 and say why machine learning traded precision for range."],
        },
        results=[
            ("Two's complement", r"-x \equiv \bar{x} + 1 \pmod{2^n}"),
            ("The carry operator", r"(g,p)\circ(g',p') = (g + p\,g',\; p\,p') \quad\text{is associative}"),
            ("Adder delay", r"t_{\text{ripple}} = 2n+1, \qquad t_{\text{prefix}} = O(\log n)"),
            ("Newton's reciprocal", r"y_{k+1}=y_k(2-d\,y_k),\qquad e_{k+1}=d\,e_k^{2},\ \ e_k=\tfrac1d-y_k"),
            ("The rounding model", r"\operatorname{fl}(x\circ y)=(x\circ y)(1+\delta),\qquad |\delta|\le u"),
            ("Conditioning and stability", r"\text{error}\;\lesssim\;\kappa\times u"),
        ],
        U=(0, 1, 2, 3, 6, 8, 9, 10, 11), D=(15,), I=(7, 13),
        also=(("The arithmetic blocks", "explainer/cs/pebble/blocks.py"),),
    ),
    Part(
        n=5, level="U", widget="latchsaddle", prereq=(3, 4),
        question="How can a circuit of gates remember, and what does remembering cost?",
        story="The part opens with two NAND gates in a loop, which hold a bit where every circuit of Part 3 "
              "forgot. Seen as voltages, the cross-coupled inverters are a dynamical system with two stable "
              "states and a saddle between them, and the time to leave the saddle grows like the logarithm of "
              "one over the starting imbalance. Latches become edge-triggered flip-flops, the clock brings setup "
              "and hold times and a top frequency, and 40,000 simulated arrivals show metastability's exponential "
              "tail and the two-flip-flop synchronizer that makes it rare. Then the machines that remember are "
              "read as mathematics: a state machine is a finite automaton, Myhill and Nerode count its necessary "
              "states, and a shift register with feedback multiplies by x over the field with two elements. The "
              "part builds Pebble's register file from 480 flip-flops, then static and dynamic memory cells. It "
              "ends with Rowhammer, where hammering one DRAM row flips bits in its neighbours, and with what a "
              "counting defence can and cannot promise.",
        handoff="Registers, the clock and the register file become Pebble in Part 6, and Part 7 slices its "
                "critical path with more registers. Static and dynamic memory are the raw material of Part 9's "
                "memory hierarchy. Finite automata are the first rung of Part 12's languages and Part 25's "
                "limits; shift registers over GF(2) return as the error-detecting codes of Part 28 and the "
                "ciphers of Part 29; Rowhammer returns with virtual memory and web security.",
        outside="Gates and unit delays from Part 3, the adder of Part 4. Chapter 2 uses a derivative and an "
                "eigenvalue, both explained on screen.",
        objectives={
            "U": ["Trace an SR latch, a D latch and a master-slave flip-flop through a waveform.",
                  "Compute a circuit's maximum clock frequency from clock-to-Q, logic and setup delays.",
                  "Design a Moore machine for a pattern and build a counter and a register from flip-flops."],
            "M": ["Linearize the cross-coupled inverters at the saddle and derive the resolution time.",
                  "Prove the Myhill-Nerode theorem and minimize a DFA by partition refinement.",
                  "Explain an LFSR as multiplication by x modulo a polynomial and say when its period is 2^n - 1."],
            "D": ["Bound the failure probability of a probabilistic Rowhammer defence with a union bound over windows.",
                  "State the Misra-Gries undercount bound and which physical assumptions a counting defence still needs."],
            "I": ["Compute a synchronizer's MTBF and explain why a single-bit synchronizer does not make a bus coherent.",
                  "Explain DRAM refresh, why Rowhammer breaks the memory abstraction, and what TRR and ECC do about it."],
        },
        results=[
            ("The clock's budget", r"f_{\max}=\frac{1}{t_{cq}+t_{\text{logic}}+t_{\text{setup}}}"),
            ("Leaving the saddle", r"t_{\text{resolve}}\approx\frac{\tau}{\lambda}\,\ln\frac{\Delta}{|\delta|}"),
            ("Synchronizer failure", r"\text{MTBF}=\frac{e^{\,t_r/\tau}}{T_0\,f_{\text{clk}}\,f_{\text{data}}}"),
            ("Myhill-Nerode", r"L \text{ regular} \iff \equiv_L \text{ has finitely many classes}"),
            ("Maximal shift registers", r"\#\{\text{primitive polynomials of degree } n\}=\frac{\varphi(2^n-1)}{n}"),
            ("Misra-Gries counters", r"\text{true count}-\text{estimate}\le\Bigl\lfloor\frac{W}{k+1}\Bigr\rfloor"),
        ],
        U=(0, 1, 3, 4, 6, 8, 9, 10, 11, 14), D=(15,), I=(12,),
        also=(("Latches, registers and state machines", "explainer/cs/pebble/seq.py"),),
    ),
    Part(
        n=6, level="U", widget="pebblesteps", prereq=(1, 3, 4, 5),
        question="How do gates, adders and registers become a machine that runs any program?",
        story="The part opens with ENIAC, programmed by plugging cables, and with the 1945 idea that replaced "
              "them: keep the instructions in memory beside the data. It designs Pebble-32's instruction set bit "
              "by bit, sixteen registers and 34 instructions in four formats, and builds the single-cycle datapath "
              "one instruction class at a time from the register file of Part 5 and the ALU of Part 4. The control "
              "unit is a 34 by 20 truth table, built as a table of product terms and as minimized logic. A "
              "two-pass assembler turns mnemonics and labels into words, and the gate-level machine runs Part 1's "
              "Euclid and 300 random programs with the same final state as the emulator. Then the part counts "
              "the cost: the iron law, the netlist's critical path, and the Job, version 0, whose linear search "
              "takes 1.069 x 10^11 cycles for thirty novels. A Turing-machine interpreter in Pebble assembly runs "
              "the busy beavers, which closes Part 1's loop. It ends by planting nine bugs in the emulator to ask "
              "how a processor is known to be right.",
        handoff="Part 7 cuts the single-cycle machine's long path into a pipeline, and Part 8 runs instructions "
                "out of order. Part 9 builds the memory hierarchy behind the loads and stores. Part 11 turns "
                "jump-and-link into a calling convention, and Part 13 writes a compiler whose output runs on "
                "Pebble. Interrupts and exceptions become an operating system in Parts 31 and 32, and the Job's "
                "ledger gains a row whenever a later part makes it faster or cheaper.",
        outside="Parts 3 to 5 for the gates, the ALU and the register file; Part 1 for Euclid and the universal "
                "machine. Programming experience in any language helps with the assembly.",
        objectives={
            "U": ["Encode and decode a Pebble-32 instruction field by field, and trace fetch, decode and execute.",
                  "Follow a load, a store, a branch and a jump through the single-cycle datapath.",
                  "Write a loop in Pebble assembly and assemble it by hand with a symbol table."],
            "M": ["Derive a control word from an instruction's needs and compare the table and minimized control units.",
                  "Compute a program's running time with the iron law and a clock period set by the critical path.",
                  "Explain why a fixed-width Pebble is finite-state and what universality needs beyond it."],
            "D": ["Estimate how many random programs are needed to catch a bug of a given rate, and name the bugs they miss.",
                  "Describe what a formal ISA specification and a verified processor prove, and what remains open."],
            "I": ["Compare Pebble-32 with RV32I and explain the design rules of a regular instruction set.",
                  "Predict the Job's cycle count from its inner loop and find where 99.7% of the time goes.",
                  "Explain memory-mapped devices, polling and why device registers must not be cached."],
        },
        results=[
            ("The iron law", r"\text{time}=\text{instructions}\times\frac{\text{cycles}}{\text{instruction}}\times\frac{\text{seconds}}{\text{cycle}}"),
            ("The R format", r"\text{word}=\text{op}\cdot2^{26}+\text{rd}\cdot2^{22}+\text{rs1}\cdot2^{18}+\text{rs2}\cdot2^{14}"),
            ("The control unit", r"34\times20 \text{ truth table}:\ 307 \text{ gates as a table},\ 205 \text{ minimized}"),
            ("The single-cycle clock", r"T \ge t_{\text{instr mem}}+t_{\text{logic}}+t_{\text{data mem}}+t_{\text{flip-flop}}"),
            ("The Job, version 0", r"1.069\times10^{11} \text{ cycles},\quad 4{,}279 \text{ per byte},\quad 99.7\% \text{ searching}"),
            ("A testing budget", r"P(\text{caught in } N)=1-(1-r)^{N}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8), D=(15,), I=(10, 14),
        also=(("The gate-level CPU", "explainer/cs/pebble/cpu.py"), ("The emulator", "explainer/cs/pebble/emu.py"),
              ("The assembler", "explainer/cs/pebble/asm.py")),
    ),
]
