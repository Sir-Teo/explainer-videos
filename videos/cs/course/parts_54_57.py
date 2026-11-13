"""The end of Act X, Horizons and Trust, and the start of Act XI, the research tier: proofs of programs, trusting trust, spectral graphs, learning theory (Parts 54-57)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=54, level="U", widget="midpointwrap", prereq=(14, 25, 26, 33),
        question="If testing can only show that bugs are present, how do we prove that a program has none?",
        story="The part opens on three bugs in tested programs, Ariane 5, Therac-25 and Heartbleed, and on binary "
              "search's midpoint posed as a SAT problem over 16-bit integers: the solver finds lo = 8,997 and "
              "hi = 27,291, whose sum wraps to -29,248, and proves the repaired midpoint for every lo < hi. Rice's "
              "theorem rules out deciding correctness in general, and the part takes three ways round it. The "
              "first is to write the invariant ourselves: Turing's 1949 proof, Floyd-Hoare logic, Dijkstra's "
              "weakest preconditions, and verification conditions bit-blasted for Part 26's solver, with "
              "separation logic for pointers. The second is to exhaust a finite state space: a model checker "
              "finds the bugs planted in Peterson's lock, two-phase commit and a Raft election, and BDDs and "
              "bounded model checking push past the state explosion. The third is to approximate soundly, with "
              "intervals and widening, and with types. The part then turns to who checks the proofs: an LCF "
              "kernel of 69 lines, CompCert and seL4, TLA+. It ends with testing treated as science, a fuzzer "
              "that finds a bug planted in our own compiler and shrinks the failing program from 75 lines to 9, "
              "and the open problem of inferring invariants for loops with multiplication.",
        handoff="Part 55 asks whether the compiler itself can be trusted. Part 58 gives programs the mathematical "
                "meaning these proofs rest on, Part 59 proves the limits of distributed protocols, Part 60 checks "
                "hardware against its specification, and Part 61 treats proof as a research method.",
        outside="Propositional logic and proof by induction; two's-complement arithmetic as in Part 4.",
        objectives={
            "U": ["Write a precondition, a postcondition and a loop invariant for a short program, and check the "
                  "invariant on a run.",
                  "Push an assertion backward through assignments with the assignment axiom.",
                  "Explain why (lo + hi) >> 1 fails on machine integers and which repairs hold for which inputs."],
            "M": ["Compute weakest preconditions and the five verification conditions of a loop with an invariant "
                  "and a variant.",
                  "Compute EF and EG on a Kripke structure as least and greatest fixpoints, and read a lasso as a "
                  "liveness counterexample.",
                  "Run interval analysis on a loop with widening and narrowing, and say why the result is sound."],
            "D": ["Prove that widening reaches a post-fixpoint in at most 2n strict steps per loop head and that "
                  "narrowing stays above the least fixpoint.",
                  "State the invariant-inference problem for loops with multiplication and what a complete "
                  "procedure for a fixed class of invariants would have to show."],
            "I": ["Specify a protocol as a state machine, model-check it at a small scope and read the shortest "
                  "counterexample.",
                  "Set up differential fuzzing of a compiler and reduce a failing program by delta debugging.",
                  "Say what remains trusted in a verified system: the specification, the kernel, the hardware."],
        },
        results=[
            ("Assignment and while", r"\{Q[e/x]\}\ x:=e\ \{Q\}\qquad \frac{\{I\wedge b\}\ c\ \{I\}}"
                                     r"{\{I\}\ \text{while } b \text{ do } c\ \{I\wedge\neg b\}}"),
            ("Weakest precondition", r"\{P\}\,c\,\{Q\}\iff P\Rightarrow \operatorname{wp}(c,Q),\qquad "
                                     r"\operatorname{wp}(c_1;c_2,\,Q)=\operatorname{wp}(c_1,\operatorname{wp}(c_2,Q))"),
            ("Frame rule", r"\frac{\{P\}\ c\ \{Q\}}{\{P * R\}\ c\ \{Q * R\}}\quad "
                           r"(c \text{ modifies no variable free in } R)"),
            ("CTL by fixpoints", r"\mathrm{EF}\,q=\mu Z.\ q\vee \mathrm{EX}\,Z,\qquad "
                                 r"\mathrm{EG}\,p=\nu Z.\ p\wedge \mathrm{EX}\,Z"),
            ("Interval widening", r"[a,b]\,\nabla\,[c,d]=\bigl[\,c<a\ ?\ {-\infty}:a,\ \ d>b\ ?\ {+\infty}:b\,\bigr]"),
            ("Variable order of a BDD", r"\bigwedge_{i\le n}(x_i\leftrightarrow y_i):\quad 3n \text{ nodes interleaved},"
                                        r"\quad 3\cdot 2^n-3 \text{ separated}"),
        ],
        U=(0, 1, 2, 3, 6, 13), D=(15,), I=(11, 12, 14),
        also=(("The verifier, model checker and fuzzer", "explainer/cs/verify"),),
    ),
    Part(
        n=55, level="U", widget="passwordzipf", prereq=(11, 13, 25, 54),
        question="If a compiler can hide a backdoor that its own source never shows, what can be trusted at all?",
        story="The part opens by naming, for every layer of the tower, the leak that crosses it, from Rowhammer in "
              "the memory cells to the xz backdoor in a release tarball. It then works up the layers. Part 11's "
              "stack smash is run on Pebble under every combination of canary, W^X and ASLR, and a chain of "
              "gadgets found in our own binary prints 'pwned' with W^X fully on. Ownership types remove the "
              "memory bugs by construction, and speculation leaks what the instruction set never promised to "
              "hide. Passwords are measured in bits and in guesses, Needham-Schroeder falls to Lowe's attack "
              "under Part 54's model checker, and access control ends at an undecidable safety question. The "
              "web, the network and the supply chain each fail where code is confused with data or a promise "
              "goes unchecked. The part turns on Thompson's 1984 attack, built in three stages on our own "
              "compiler: with the trojan deleted from every source file, the trojaned binary compiles the clean "
              "source and reproduces itself bit for bit. Wheeler's diverse double-compiling catches it with a "
              "second, independent compiler. The degree ends by walking the tower once more, asking each layer "
              "what it trusts, and by listing the problems the series left open.",
        handoff="This is the end of the degree. Act XI, the research tier, begins with Part 56; Part 61 returns "
                "to each open problem listed in the Frontier chapter (P against NP, one-way functions, a memory "
                "model for C, verified software at scale) as research.",
        outside="Nothing beyond the series: the part draws on the machine, the compiler, the kernel, the network "
                "and the proofs of the parts before it.",
        objectives={
            "U": ["Write a threat model for a small system: the assets, the trust boundary, the adversary and the "
                  "attack surface.",
                  "Compute a random password's entropy and expected cracking time, and say why human-chosen "
                  "passwords fall much sooner.",
                  "Explain Thompson's three stages and why reading every source file does not find the trojan."],
            "M": ["Compute the success probability and the expected number of tries against k bits of ASLR, with "
                  "and without re-randomization.",
                  "Run diverse double-compiling by hand, X = T(c) and Z = X(c), and state the assumptions under "
                  "which Z = A shows that A corresponds to c.",
                  "Apply the Bell-LaPadula rules on a lattice of levels and categories, and find Lowe's attack on "
                  "Needham-Schroeder."],
            "D": ["Sketch the reduction from the halting problem that makes the HRU safety question undecidable.",
                  "State what an end-to-end proof for a software stack grown from an auditable seed would have to "
                  "compose, and which pieces exist only in isolation."],
            "I": ["Choose defences against memory corruption, injection and request forgery, and say what each "
                  "one leaves open.",
                  "Estimate a dependency tree's exposure, and explain what a signature, a reproducible build and "
                  "an SBOM each do and do not show.",
                  "Compute a reflection attack's amplification factor and name the filter that removes spoofing."],
        },
        results=[
            ("ASLR with k bits", r"p=2^{-k},\qquad E[\text{tries}]=2^{k}\ (\text{re-randomized}),\quad "
                                 r"\tfrac{2^{k}+1}{2}\ (\text{one sweep})"),
            ("Password guessing", r"H=L\log_2 N,\qquad E[T]=\frac{2^{H}}{2R}\quad (R \text{ guesses a second})"),
            ("Bell-LaPadula", r"s \text{ reads } o\ \Rightarrow\ \lambda(s)\ge\lambda(o),\qquad "
                              r"s \text{ writes } o\ \Rightarrow\ \lambda(s)\le\lambda(o)"),
            ("Dependency exposure", r"P(\text{no bad package among } n)=(1-p)^{n}\approx e^{-np}"),
            ("Thompson's fixpoint", r"A_{\text{trojan}}(c)=A_{\text{trojan}}\ \ne\ A_{\text{clean}}=A_{\text{clean}}(c)"
                                    r"\quad (c \text{ the clean source})"),
            ("Diverse double-compiling", r"X=T(c),\quad Z=X(c):\qquad Z=A\ \Longrightarrow\ A \text{ corresponds to } c"),
        ],
        U=(0, 1, 2, 5, 11, 13), D=(14,), I=(3, 7, 8, 9, 10),
        also=(("The trust instruments", "explainer/cs/trust"),),
    ),
    Part(
        n=56, level="D", widget="fiedlersweep", prereq=(18, 20, 27, 52),
        question="What do the eigenvalues of a graph's matrix know that its drawing hides?",
        story="The part opens on two 16-vertex rings with three neighbours at every vertex, alike in a drawing, "
              "whose second eigenvalues are 0.097 and 0.279, and reads the same number off Part 18's city grid, "
              "Part 36's internet and the word graph of a novel. The Laplacian's quadratic form is the energy of "
              "springs along the edges, and Courant-Fischer makes its second eigenvalue a relaxation of the "
              "minimum bisection. Cheeger's inequality is proved in both directions, and the sweep cut over the "
              "Fiedler vector is checked against brute force on random 12-vertex graphs. The same gap bounds how "
              "fast a lazy random walk forgets its start. Expanders are sparse graphs with a large gap: the "
              "mixing lemma, the Alon-Boppana limit, random regular graphs measured against it, and an explicit "
              "construction by the zig-zag product, which gave Reingold's SL = L. The part then turns the graph "
              "into a circuit: effective resistance, commute times, sparsifiers and Laplacian solvers, and "
              "electrical flows reweighted until they approximate a maximum flow. It ends at the almost-linear "
              "max-flow algorithm of 2022, at high-dimensional expanders, and at the small-set expansion "
              "hypothesis.",
        handoff="Part 58 meets fixed points again, in the meaning of programs. Part 59 runs algorithms on graphs "
                "where each node sees only its neighbourhood. Part 61 puts the unique games conjecture, which "
                "small-set expansion sits beside, on the map of open problems.",
        outside="Linear algebra to the spectral theorem for symmetric matrices, and Markov chains at the level of "
                "a stationary distribution.",
        objectives={
            "U": ["Write the Laplacian of a small graph and evaluate its quadratic form as a sum over edges.",
                  "Explain what a small second eigenvalue says about cutting a graph in two."],
            "M": ["Compute the conductance of a cut, and find a sweep cut from the Fiedler vector.",
                  "Bound a lazy walk's mixing time from the spectral gap, above and below.",
                  "Compute an effective resistance and predict a commute time from it."],
            "D": ["Prove both sides of Cheeger's inequality, the hard side by a random threshold cut.",
                  "Prove the expander mixing lemma, and state the Alon-Boppana bound and what the zig-zag "
                  "product preserves.",
                  "State the small-set expansion hypothesis and its relation to the unique games conjecture."],
            "I": ["Partition a graph by spectral clustering, and read a sweep curve to choose the cut.",
                  "Explain why a random regular graph is a good datacentre topology, and how a walk on an "
                  "expander saves random bits."],
        },
        results=[
            ("The Laplacian's energy", r"x^{\mathsf T}Lx=\sum_{\{i,j\}\in E}(x_i-x_j)^2,\qquad "
                                       r"\lambda_2=\min_{x\perp\mathbf 1}\frac{x^{\mathsf T}Lx}{x^{\mathsf T}x}"),
            ("Cheeger's inequality", r"\frac{\lambda_2}{2}\ \le\ \phi(G)\ \le\ \sqrt{2\lambda_2}"
                                     r"\qquad(\lambda_2 \text{ of } I-D^{-1/2}AD^{-1/2})"),
            ("Mixing of the lazy walk", r"\|p_t-\pi\|_{TV}\ \le\ \tfrac12\sqrt{1/\pi_{\min}}\,"
                                        r"\bigl(1-\tfrac{\lambda_2}{2}\bigr)^{t}"),
            ("Expander mixing lemma", r"\Bigl|e(S,T)-\frac{d\,|S|\,|T|}{n}\Bigr|\ \le\ \lambda\sqrt{|S|\,|T|},"
                                      r"\qquad \lambda\ \ge\ 2\sqrt{d-1}-o(1)"),
            ("Zig-zag product Z of G and H", r"1-\lambda_{Z}\ \ge\ (1-\lambda_H)^2\,(1-\lambda_G)"),
            ("Commute time", r"C(a,b)=2m\,R_{\text{eff}}(a,b),\qquad R_{\text{eff}}(a,b)="
                             r"(e_a-e_b)^{\mathsf T}L^{+}(e_a-e_b)"),
        ],
        U=(0, 1), I=(7,),
        also=(("The spectral instruments", "explainer/cs/spectral/spectra.py"),),
    ),
    Part(
        n=57, level="D", widget="hedgeleader", prereq=(20, 23, 29, 44),
        question="When can a machine learn from examples, and how many does it need?",
        story="The part opens on a linear model fitted to fifty noisy examples: its test error explodes when the "
              "number of features reaches fifty and then falls below every smaller model's, which no count of "
              "parameters explains. Valiant's definition makes the question exact, and a hidden rectangle is "
              "learned with (4/epsilon) ln(4/delta) examples. For infinite classes one number decides, the VC "
              "dimension: half-planes shatter three points and no four, and Sauer-Shelah turns that into a "
              "polynomial count of labellings. Margins, not dimensions, govern the perceptron, whose mistakes "
              "stay flat from a hundred dimensions to a thousand, and AdaBoost, whose test error keeps falling "
              "after the training error is zero. Against an adversary the measure is regret: Hedge keeps it "
              "under the square root of T ln N / 2 while follow the leader loses almost every round, and bandits "
              "pay a logarithm for what they do not see. The part then turns to what cannot be learned "
              "efficiently, with cryptography and with statistical queries that cannot find a parity, and "
              "returns to the opening curve through the minimum-norm interpolator. It ends with learning as "
              "compression and with Warmuth's conjecture that every class of VC dimension d has a compression "
              "scheme of size O(d).",
        handoff="Part 58 asks what programs mean and how to prove two of them the same, Part 59 what many "
                "machines can compute together, and Part 60 builds the hardware that trains and runs learned "
                "models. Part 61 asks how to measure a result honestly and returns to the bridge between this "
                "series and AI, Built.",
        outside="Probability to Hoeffding's inequality and the union bound; linear algebra to the pseudo-inverse. "
                "AI, Built shows the learners themselves.",
        objectives={
            "U": ["State what probably approximately correct means, with its epsilon and its delta.",
                  "Compute the sample size that suffices for a finite class, and learn a rectangle by the "
                  "tightest box."],
            "M": ["Find the VC dimension of a simple class by exhibiting a shattered set and proving that no "
                  "larger set is shattered.",
                  "Run the perceptron and bound its mistakes by Novikoff's argument.",
                  "Run Hedge and UCB1 by hand for a few rounds and state the regret each guarantees."],
            "D": ["Prove the Sauer-Shelah lemma, and Hedge's regret bound with Hoeffding's lemma.",
                  "Prove that a statistical query of tolerance tau is informative about at most 1/tau^2 "
                  "parities.",
                  "State the sample compression conjecture and what Moran and Yehudayoff proved."],
            "I": ["Choose a stopping round for boosting from training and test curves when labels are noisy.",
                  "Choose between explore-then-commit, UCB1 and Thompson sampling for an experiment, and say "
                  "what regret to expect.",
                  "Say why a parameter count does not predict the test error of an interpolating model."],
        },
        results=[
            ("Finite class, realizable", r"m\ \ge\ \frac{\ln|H|+\ln(1/\delta)}{\varepsilon}\ \Longrightarrow\ "
                                         r"P\bigl(L_D(h)>\varepsilon\bigr)\le\delta"),
            ("Sauer-Shelah", r"\Pi_H(m)\ \le\ \sum_{i=0}^{d}\binom{m}{i}\ \le\ \Bigl(\frac{em}{d}\Bigr)^{d}"
                             r"\quad(m\ge d)"),
            ("Novikoff's bound", r"\text{perceptron mistakes}\ \le\ \Bigl(\frac{R}{\gamma}\Bigr)^{2}"),
            ("AdaBoost's training error", r"\widehat{\operatorname{err}}(H_T)\ \le\ \exp\Bigl(-2\sum_{t=1}^{T}"
                                          r"\gamma_t^{2}\Bigr),\qquad \gamma_t=\tfrac12-\epsilon_t"),
            ("Hedge", r"\text{regret}_T\ \le\ \frac{\ln N}{\eta}+\frac{\eta T}{8}\ =\ \sqrt{\tfrac{T\ln N}{2}}"
                      r"\quad\text{at } \eta=\sqrt{8\ln N/T}"),
            ("Lai-Robbins", r"\liminf_{T\to\infty}\frac{\text{regret}_T}{\ln T}\ \ge\ \sum_{i:\Delta_i>0}"
                            r"\frac{\Delta_i}{\operatorname{KL}(\mu_i,\mu^{*})}"),
        ],
        U=(0, 1), I=(4, 6),
        also=(("The learning-theory instruments", "explainer/cs/learn/theory.py"),),
    ),
]
