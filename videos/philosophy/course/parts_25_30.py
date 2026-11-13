"""Act V ends and Acts VI-VII open: space and time, the quantum puzzle, language, the continental tradition, mind (Parts 25-30)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=25, level="U", widget="simulslice", prereq=(24,),
        question="What are space and time: a container, a web of relations, or something built from neither?",
        story="The part opens with Augustine's remark that he knows what time is until he is asked, and with four "
              "questions: is space a thing, is its geometry a discovery or a convention, is the present special, "
              "and could the past be changed. Newton's bucket and Leibniz's shifts are checked on a universe of "
              "six bodies: every distance between bodies survives a shift, a boost and a rotation in time, yet "
              "only the last curves the water. Kant's hands, hyperbolic triangles in the Poincaré disk and "
              "Poincaré's disk world of shrinking rulers lead to Earman's principle that spacetime should have "
              "the symmetries of the laws, which picks Galilean spacetime. Special relativity then tilts the "
              "slices of simultaneity, and the Rietdijk-Putnam boost turns that into an argument from the "
              "present to the block. The turn is the hole argument: spacetime points with their own identities, "
              "determinism, and diffeomorphic models as distinct worlds cannot all be kept, which is the Wall's "
              "twenty-fifth brick. The part ends with Barbour's best matching, Deutsch's fixed points for the "
              "grandfather and knowledge paradoxes, and, labelled as speculative, a causal set whose dimension is "
              "recovered from its order alone.",
        handoff="Quantum theory on a fixed stage and what measurement does follow in Part 26; the lived present "
                "and Husserl's time-consciousness in Part 29; free will in a block universe in Part 32; the long "
                "future and its value in Parts 36 and 42.",
        outside="School geometry and algebra, including square roots; no physics beyond speed and acceleration is "
                "assumed.",
        objectives={
            "U": ["State the static and kinematic shift arguments and say why the rotating bucket is not answered "
                  "by them.",
                  "Find the boost v = t/x that makes a spacelike event simultaneous with here-now, and say why no "
                  "boost does this for a timelike event."],
            "M": ["Compute a hyperbolic triangle's area from its angles, and the measurements a disk-world "
                  "inhabitant would report for a circle.",
                  "Apply Earman's symmetry principle to Newtonian, Galilean and Leibnizian spacetime.",
                  "Solve Deutsch's consistency condition for a one-bit time-travel circuit."],
            "D": ["Set out the hole argument as an inconsistent triad and state what sophisticated "
                  "substantivalism and relationalism each give up.",
                  "State Malament's theorem on standard simultaneity and the assumption Sarkar and Stachel drop."],
            "I": ["Estimate the dimension of a sprinkled causal set from its fraction of related pairs, and say "
                  "how the estimate's error depends on the number of events."],
        },
        results=[
            ("The bucket's surface", r"z(r)=\frac{\omega^{2}r^{2}}{2g}"),
            ("Hyperbolic triangles", r"\operatorname{Area}=\pi-(\alpha+\beta+\gamma),\qquad "
                                     r"d(u,v)=\operatorname{arccosh}\Bigl(1+\frac{2\,|u-v|^{2}}{(1-|u|^{2})(1-|v|^{2})}\Bigr)"),
            ("Lorentz boost and the interval", r"t'=\gamma\,(t-vx),\quad x'=\gamma\,(x-vt),\quad "
                                               r"\gamma=\frac{1}{\sqrt{1-v^{2}}},\qquad t'^{2}-x'^{2}=t^{2}-x^{2}"),
            ("The Rietdijk-Putnam boost", r"|t|<|x|\ \Longrightarrow\ t'=0\ \text{ in the frame with } v=t/x"),
            ("Reichenbach's synchrony", r"t_{2}=t_{1}+\varepsilon\,(t_{3}-t_{1}),\quad 0<\varepsilon<1;\qquad "
                                        r"\text{Malament: only }\varepsilon=\tfrac12\text{ is definable from causal structure}"),
            ("Deutsch's consistency condition", r"\rho=\operatorname{Tr}_{1}\bigl[\,U\,(\rho_{\text{in}}\otimes\rho)\,U^{\dagger}\bigr]"),
        ],
        U=(0, 1, 2, 3, 7, 9, 10), D=(8, 11), I=(14,),
        also=(("The Reasoner's spacetime module", "explainer/philosophy/reasoner/spacetime.py"),),
    ),
    Part(
        n=26, level="U", widget="chshangles", prereq=(13, 25),
        question="What does quantum mechanics say the world is like, and which classical picture do its theorems rule out?",
        story="The part opens with Feynman's remark of 1965 that nobody understands quantum mechanics: the "
              "mathematics is clean and the predictions exact, but the textbook theory is silent about what happens "
              "when no one measures. One chapter builds the formalism on a small Hilbert-space simulator, and the "
              "measurement problem is priced as Maudlin's three claims, of which Bohm, GRW and Everett each give "
              "up one. Einstein, Podolsky and Rosen argue that the theory is incomplete; Bell's theorem answers "
              "them. The CHSH inequality is derived line by line, all 16 local deterministic strategies give "
              "|S| = 2, and the singlet reaches 2 times the square root of 2. The turn is the CHSH game: no "
              "classical strategy wins more than 3/4 of the time, the quantum strategy wins about 0.854, and the "
              "experiments from Freedman and Clauser to 2015 side with the quantum value, which is the Wall's "
              "twenty-sixth brick. GHZ, the Peres-Mermin square and Cabello's eighteen vectors are checked by "
              "brute force, PBR argues that the wavefunction is real, and Everett, Bohm and GRW are each "
              "simulated. The part ends with Wigner's friend, Frauchiger and Renner's Price List, the free will "
              "theorem and device-independent cryptography.",
        handoff="What a theory's terms refer to is taken up in Part 27; minds, machines and observers in Parts 30 "
                "and 31; free will after Kochen and Specker in Part 32; deciding in a branching world in Part 33; "
                "trust in machines that cannot be inspected in Part 41.",
        outside="Vectors, 2 x 2 matrices, complex numbers and sines and cosines; probability at the level of "
                "Part 13. No physics course is assumed.",
        objectives={
            "U": ["State the three claims of the measurement problem and say which one Bohm, GRW and Everett "
                  "each give up.",
                  "Play the CHSH game with every deterministic strategy and explain why none wins more than three "
                  "times in four."],
            "M": ["Derive the CHSH inequality from locality and predetermined outcomes, and compute the singlet's "
                  "S for given angles.",
                  "Run the GHZ argument and the Peres-Mermin square, and say why the square fails by exactly one "
                  "constraint.",
                  "Compute the decoherence of a qubit coupled to n environment qubits."],
            "D": ["State the Kochen-Specker theorem and verify Cabello's eighteen-vector parity proof.",
                  "Set out the PBR theorem and the Frauchiger-Renner argument, each with the assumptions it "
                  "needs."],
            "I": ["Name the locality, detection and freedom-of-choice loopholes and how the 2015 experiments "
                  "closed them.",
                  "Explain how a CHSH violation certifies a cryptographic key or random bits without trusting the "
                  "devices."],
        },
        results=[
            ("The Born rule", r"P(i)=|\langle i\mid\psi\rangle|^{2},\qquad "
                              r"|\psi\rangle=\cos\tfrac{\theta}{2}|0\rangle+\sin\tfrac{\theta}{2}|1\rangle"
                              r"\ \Rightarrow\ P(0)=\cos^{2}\tfrac{\theta}{2}"),
            ("The singlet's correlation", r"E(a,b)=\langle\psi^{-}|\,\sigma_{a}\otimes\sigma_{b}\,|\psi^{-}\rangle=-\cos(a-b)"),
            ("CHSH and Tsirelson", r"S=E(a,b)+E(a,b')+E(a',b)-E(a',b'),\qquad |S|\le 2\ \text{(local)},\quad "
                                   r"|S|\le 2\sqrt2\ \text{(quantum)},\quad |S|\le 4\ \text{(no-signalling)}"),
            ("The CHSH game", r"\text{win iff } a\oplus b=x\wedge y:\qquad p_{\text{classical}}\le\tfrac34,\qquad "
                              r"p_{\text{quantum}}=\cos^{2}\tfrac{\pi}{8}\approx 0.854"),
            ("GHZ", r"XXX=+1,\quad XYY=YXY=YYX=-1\ \text{ on }\ \tfrac{1}{\sqrt2}\bigl(|000\rangle+|111\rangle\bigr);"
                    r"\qquad\text{no values } x_i,y_i=\pm1 \text{ satisfy all four}"),
            ("Decoherence", r"|\rho_{01}|=\tfrac12\cos^{n}\theta\quad\text{after coupling to } n \text{ environment qubits}"),
        ],
        U=(0, 1, 2, 3, 5), D=(8, 9, 13), I=(6, 14),
        also=(("The Reasoner's quantum module", "explainer/philosophy/reasoner/quantum.py"),),
    ),
    Part(
        n=27, level="U", widget="detvenn", prereq=(3, 22),
        question="What does a word contribute to what a sentence says: the thing it stands for, or something more?",
        story="Act VI opens with Frege's observation of 1892 that 'a = a' is trivial while 'a = b' can be a "
              "discovery, although both are about one thing. After Gongsun Long's white horse, read as identity "
              "and as inclusion on a herd of six, Frege's sense and reference are computed on his own example of a "
              "triangle's medians, and Russell's theory of descriptions is evaluated in four models with both "
              "scopes of negation. Kripke's rigid names, Putnam's Twin Earth and Kaplan's character and content "
              "pull meaning out of the head and into the world and the context. The second half builds "
              "truth-conditional semantics: Tarski's Convention T, Davidson's programme and Foster's problem, "
              "Montague's typed lambda calculus, and a Heim-Kratzer parser that interprets every node of a tree. "
              "Generalized quantifiers are checked for conservativity on 256 pairs of sets, where only 'only' "
              "fails, and an Ehrenfeucht-Fraïssé game shows that 'most' is not first-order. The turn is belief "
              "reports: Lois Lane and Kripke's Pierre make Frege's puzzle a Price List, the Wall's twenty-seventh "
              "brick. The part ends with donkey sentences in dynamic predicate logic and with the parser's "
              "logical forms compiled to SQL.",
        handoff="Meaning as use, rule-following and speech acts follow in Part 28; externalism and the contents "
                "of the mind return in Parts 30 and 31; belief and knowledge from Parts 11 and 12 now have their "
                "reports; what the words of language models mean is taken up in Parts 41 and 42.",
        outside="Sets and the first-order notation of Part 3; the possible worlds of Part 22 help with rigid "
                "designation and the two-dimensional matrix.",
        objectives={
            "U": ["State Frege's puzzle and say how sense and reference, and Russell's descriptions, each "
                  "answer it.",
                  "Give Kripke's modal argument against descriptivism using a rigid name and a description that "
                  "is not rigid.",
                  "Set out the three claims about belief reports that cannot all be true and who gives up "
                  "which."],
            "M": ["Write Russell's analysis of a sentence with a definite description and evaluate both scopes "
                  "of its negation in a model.",
                  "Beta-reduce the lambda term for 'every student smokes' and interpret a tree by functional "
                  "application and quantifier raising.",
                  "Test a determiner for conservativity and monotonicity, and play the Ehrenfeucht-Fraïssé game "
                  "that separates 'most' from first-order logic."],
            "D": ["Prove that no first-order sentence defines 'most' from the Ehrenfeucht-Fraïssé theorem.",
                  "Explain the problem of logical omniscience for propositions as sets of worlds, and show that "
                  "dynamic predicate logic gives the donkey sentence its universal reading."],
            "I": ["Compile a logical form to an SQL query and check its answer against the model.",
                  "Build an inference test whose gold labels are theorems, and say what monotonicity it probes."],
        },
        results=[
            ("Russell's descriptions", r"\text{The } F \text{ is } G:\quad \exists x\,\bigl(Fx\wedge\forall y\,(Fy\to y=x)\wedge Gx\bigr)"),
            ("Rigid designation", r"\text{if } a \text{ and } b \text{ are rigid designators and } a=b,\ \text{then } \Box\,(a=b)"),
            ("Convention T", r"\text{for every sentence } s:\quad \operatorname{True}(\ulcorner s\urcorner)\leftrightarrow s"),
            ("A determiner's meaning", r"[\![\text{every}]\!]=\lambda P.\,\lambda Q.\,\forall x\,\bigl(P(x)\to Q(x)\bigr),"
                                       r"\qquad [\![\text{most}]\!](A,B)\iff |A\cap B|>|A\setminus B|"),
            ("Conservativity", r"Q(A,B)\iff Q(A,\,A\cap B);\qquad 2^{3^{n}}\ \text{of the } 2^{4^{n}} "
                               r"\text{ relations on an } n\text{-element universe}"),
            ("Donkey equivalence in DPL", r"(\exists x\,\varphi)\to\psi\ \equiv\ \forall x\,(\varphi\to\psi)"),
        ],
        U=(0, 1, 2, 3, 5, 6, 13), D=(12, 14), I=(15,),
        also=(("The Reasoner's semantics module", "explainer/philosophy/reasoner/semantics.py"),),
    ),
    Part(
        n=28, level="U", widget="rsacookies", prereq=(2, 13, 27),
        question="Is the meaning of a word its use, and can use be computed?",
        story="The part opens with Wittgenstein turning against his own picture theory: for a large class of "
              "cases, the meaning of a word is its use in the language. The Tractatus is built first, with all 16 "
              "truth functions of two propositions generated from the single operation N, and then the "
              "Investigations: the builders, language games, and family resemblance computed on six games. The "
              "turn is Kripke's plus and quus. A record of 1000 sums fits both rules and 143 rivals below 200, no "
              "fact about the speaker settles which was meant, and the sceptical solution moves meaning into a "
              "community's practice: the Wall's twenty-eighth brick. Quine's gavagai and a proxy function that "
              "keeps the truth value of all 300 sentences make reference inscrutable, and Davidson's charity "
              "picks the true translation out of six. Austin's speech acts and Grice's maxims lead to the "
              "Rational Speech Acts model, in which a listener who reasons about a speaker hears 'some' as 'some "
              "but not all'. The part ends with conventions learned in Lewis signalling games, word vectors "
              "from a small corpus, and the question whether a model trained on text alone means anything, "
              "priced as four claims and probed.",
        handoff="Meaning in a lived world follows in Part 29; minds, machines and the Chinese room in Part 30; "
                "qualia and the beetle in the box in Part 31; games, conventions and the social contract in "
                "Part 34; aligning reasoners with what is meant and not only said in Part 42.",
        outside="Truth tables (Part 2) and Bayes' rule (Part 13); logarithms for the bits a signal carries.",
        objectives={
            "U": ["State Kripke's sceptical paradox with plus and quus, and say why past use, mental images and "
                  "dispositions each fail to fix the rule.",
                  "Derive 'some but not all' from Grice's maxim of quantity, and tell an implicature from an "
                  "entailment by cancelling it."],
            "M": ["Compute the literal listener, the speaker and the pragmatic listener of the Rational Speech "
                  "Acts model for a small reference game.",
                  "Run Roth-Erev reinforcement on a Lewis signalling game and measure the bits a learned signal "
                  "carries.",
                  "Construct a proxy function that changes every reference and no truth value."],
            "D": ["Set out the four inconsistent claims about meaning in language models and the position that "
                  "gives up each.",
                  "Explain why a linear probe that succeeds shows a property is encoded, and why one that fails "
                  "may show only that the corpus does not mark it."],
            "I": ["Build a pragmatic captioner from a literal one by one step of speaker reasoning.",
                  "State Grice's maxims as requirements for an assistant and give a failure of each."],
        },
        results=[
            ("Quus", r"x\oplus y=\begin{cases}x+y & x,y<57\\ 5 & \text{otherwise}\end{cases}"),
            ("Operation N", r"N(\bar\xi)=\text{the joint denial of the } \xi\text{'s};\qquad\text{all 16 truth functions of } p,q "
                            r"\text{ arise from } p,\,q \text{ by } N"),
            ("Rational Speech Acts", r"L_{0}(s\mid u)\propto[\![u]\!](s)\,P(s),\qquad S_{1}(u\mid s)\propto "
                                     r"\exp\bigl(\alpha\,(\log L_{0}(s\mid u)-c(u))\bigr),\qquad L_{1}(s\mid u)\propto S_{1}(u\mid s)\,P(s)"),
            ("Some, not all", r"L_{1}(\text{all}\mid\text{some})=\frac{q}{n-1+q},\quad q=\frac{1}{1+n^{\alpha}}"
                              r"\qquad(n \text{ cookies, uniform prior});\qquad n=3,\ \alpha=4:\ \tfrac{1}{165}"),
            ("Information in a signal", r"I(\text{state};\text{signal})=\sum_{s,m}p(s,m)\log_{2}\frac{p(s,m)}{p(s)\,p(m)}\ \le\ \log_{2}n"),
            ("Positive PMI", r"\operatorname{PPMI}(w,c)=\max\Bigl(0,\ \log\frac{p(w,c)}{p(w)\,p(c)}\Bigr)"),
        ],
        U=(0, 1, 2, 3, 4, 7, 8, 9), D=(13, 14), I=(15,),
        also=(("The Reasoner's pragmatics module", "explainer/philosophy/reasoner/pragmatics.py"),),
    ),
    Part(
        n=29, level="U", widget="retentionfade", prereq=(27, 28),
        question="What is it to experience a world, and can what matters in it be written down as rules?",
        story="The part opens with Husserl's slogan of 1900, back to the things themselves, and with four "
              "questions about aboutness, time, world and relevance. Brentano's thesis makes intentionality the "
              "mark of the mental, and Husserl's method is shown on a cube seen from 4000 viewpoints, never more "
              "than three faces at once. The living present is built from his 1905 diagram: on all 120 orderings "
              "of five notes a knife-edge present tells 5 apart, a two-note window 20, and a fading trace all "
              "120. Heidegger's hammer and being-in-the-world lead to Dreyfus's attack on symbolic AI, and to the "
              "turn of the part, the frame problem. Frame axioms are counted against Reiter's successor-state "
              "axioms, Dennett's robots are acted out by a planner whose work grows with every irrelevant fluent, "
              "and relevance by rule becomes the Wall's twenty-ninth brick with a Price List of three claims. "
              "The second half takes the lived body with Braitenberg's vehicles, Sartre and Beauvoir, "
              "Nietzsche's eternal return tested on a reversible automaton and on Simmel's wheels, hermeneutics, "
              "Saussure and Derrida on rotated word vectors, Foucault with a gamed threshold, Habermas and the "
              "Kyoto school. It ends at Davos, with the bridges between the continental and analytic traditions.",
        handoff="Brentano's problem and the Chinese room follow in Part 30; the first person, qualia and the "
                "hard problem in Part 31; freedom in Part 32; deliberation and democracy in Part 39; "
                "normalization, gaming and fairness in Part 41; relevance and the background for machines to "
                "be aligned in Part 42.",
        outside="No mathematics beyond counting and powers. Part 28's word vectors are reused, and Part 25's "
                "block universe is the contrast for the lived present.",
        objectives={
            "U": ["State Brentano's thesis and one objection to it, and describe Husserl's epoché.",
                  "Explain with Husserl's diagram why a melody cannot be heard in a knife-edge present, and what "
                  "retention and protention add.",
                  "Describe Heidegger's ready-to-hand and present-at-hand with the hammer."],
            "M": ["Count frame axioms against successor-state axioms, and write the successor-state axiom for "
                  "a fluent in Dennett's room.",
                  "Explain why Fredkin's second-order automata are reversible and why a finite reversible world "
                  "must return, and give Simmel's counterexample for a continuous one.",
                  "Find the words a closed dictionary cannot define without leaving itself."],
            "D": ["Separate the logical frame problem from the philosophical one, and set out the three "
                  "inconsistent claims with the position that gives up each.",
                  "Show that the similarity structure of word vectors is invariant under rotation, and say what "
                  "that does and does not establish about Saussure's and Derrida's claims."],
            "I": ["Run a planner on Dennett's room and measure how its work grows with irrelevant fluents.",
                  "Simulate a threshold that people can game and report how the selected group changes, as "
                  "Goodhart's law predicts."],
        },
        results=[
            ("Brentano's thesis", r"\text{every mental phenomenon is directed at an object, and no physical phenomenon is}"),
            ("A retentional present", r"w_{i}=\sum_{\text{ages } a \text{ of note } i}\lambda^{a},\quad 0<\lambda<1:"
                                      r"\qquad n!\ \text{orderings told apart, against } n \text{ (knife-edge) and } n(n-1) \text{ (two-note window)}"),
            ("Frame axioms against successor-state axioms", r"\approx 2AF\ \text{ against }\ F:\qquad "
                r"F(\operatorname{do}(a,s))\leftrightarrow\gamma^{+}_{F}(a,s)\vee\bigl(F(s)\wedge\neg\gamma^{-}_{F}(a,s)\bigr)"),
            ("Recurrence in a reversible world", r"x_{t+1}=f(x_{t})\oplus x_{t-1}\ \text{ is invertible for every } f,\ "
                                                 r"\text{so on } n \text{ cells every state returns within } 4^{n} \text{ steps}"),
            ("Simmel's wheels", r"\text{rates } 1,\ 2,\ \tfrac{1}{\pi}:\quad \tfrac{k}{\pi}\notin\mathbb{Z}\ \text{ for every integer } k\ge 1,"
                                r"\ \text{so the three never return together}"),
            ("Difference without positive terms", r"\cos(Rx,Ry)=\cos(x,y)\quad\text{for every rotation } R"),
        ],
        U=(0, 1, 2, 3, 4, 8, 9), D=(11, 15), I=(5, 12, 13),
        also=(("The Reasoner's phenomenology module", "explainer/philosophy/reasoner/phenomenology.py"),),
    ),
    Part(
        n=30, level="U", widget="pigeonred", prereq=(27, 29),
        question="What is a mind, and could a machine have one?",
        story="The part opens with Turing's question of 1950, can machines think, and tests each theory of mind "
              "against a machine. Descartes's two substances meet Elisabeth of Bohemia's question of how they "
              "could interact; behaviourism and the identity theory fall to super-spartans and to multiple "
              "realizability. Functionalism is built: one probabilistic machine table for a pain role is "
              "realized in threshold units and in a water tank and run in lockstep for 1000 steps, and the "
              "Ramsey-Lewis definition finds exactly one occupant of the role among 1806 assignments. The "
              "imitation game, a Chinese rulebook that is perfect on a narrow test and helpless outside it, and "
              "Blockhead's table of about 10^25764 entries ask whether passing the test is enough. Supervenience "
              "is checked in its weak, strong and global forms, and the part turns on Kim's exclusion argument: "
              "a mind that is physical and yet causally its own is the Wall's thirtieth brick, priced as a "
              "tetrad, with Yablo's pigeon and proportional causes as the reply. It ends with emergence in "
              "Gosper's glider gun, Dennett's real patterns, Dretske's fuel gauge, systematicity, and a probe "
              "that reads from a network what the network does not use.",
        handoff="Qualia, zombies and the hard problem follow in Part 31; agents, causes and free will in Part "
                "32; minds that decide in Part 33; machines that decide about people in Part 41; aligned "
                "reasoners in Part 42.",
        outside="State tables of a machine and probabilities; the possible worlds of Part 22 for supervenience, "
                "and bits of information for the fuel gauge.",
        objectives={
            "U": ["Set out dualism, behaviourism, the identity theory and functionalism, each with the "
                  "objection that moved the debate on.",
                  "Describe the imitation game and the Chinese room, and state the systems and robot replies.",
                  "Estimate the size of Blockhead's table for a test of a given length."],
            "M": ["Realize a machine table in a second substrate and check the two in lockstep; write the "
                  "Ramsey sentence of a small theory and count its realizations.",
                  "Define weak, strong and global supervenience, and decide each on a small set of worlds.",
                  "Lay out Kim's exclusion argument and say which premise each of the four positions gives up."],
            "D": ["Prove that strong supervenience implies weak and global, and show by examples that weak and "
                  "global are independent.",
                  "Assess the proportionality reply to exclusion with an interventionist measure of the "
                  "difference a cause makes."],
            "I": ["Test a system for systematicity on held-out compositions of known parts.",
                  "Probe a network for a variable, remove the probe's direction, and say what the result shows "
                  "about use as against mere presence of information."],
        },
        results=[
            ("The Ramsey-Lewis definition", r"T(\text{pain},\text{calm},\dots)\ \leadsto\ \exists x_{1}\dots\exists x_{n}\,T(x_{1},\dots,x_{n});"
                                            r"\qquad\text{pain}=\text{the } x_{1} \text{ in the unique realization}"),
            ("Blockhead's table", r"27^{\,18000}\approx 10^{25764}\ \text{entries for an hour at 300 characters a minute, against } 10^{80} \text{ atoms}"),
            ("Weak and strong supervenience", r"\text{weak: } \forall w\,\forall x,y\in w\ \bigl(x\sim_{P}y\to x\sim_{M}y\bigr);\qquad "
                                              r"\text{strong: } \forall w,w'\,\forall x\in w,\,y\in w'\ \bigl(x\sim_{P}y\to x\sim_{M}y\bigr)"),
            ("Global supervenience", r"\text{worlds with the same physical distribution have the same mental distribution;}"
                                     r"\qquad\text{strong}\Rightarrow\text{weak},\ \ \text{strong}\Rightarrow\text{global}"),
            ("Kim's tetrad", r"\text{distinctness},\ \text{mental causation},\ \text{physical closure},\ \text{no systematic overdetermination}:"
                             r"\ \text{jointly inconsistent}"),
            ("A law of the glider gun", r"\text{live cells at generation } 30k\ =\ 36+5k"),
        ],
        U=(0, 1, 2, 4, 5, 6), D=(13,), I=(12,),
        also=(("The Reasoner's mind module", "explainer/philosophy/reasoner/mind.py"),),
    ),
]
