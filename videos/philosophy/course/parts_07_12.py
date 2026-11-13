"""Acts II and III: the limits of proof, the liar, mathematics, the moderns, knowledge (Parts 7-12)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=7, level="U", widget="beaverrun", prereq=(3, 4, 6),
        question="Can a formal system for arithmetic prove every truth, prove itself consistent, and decide every "
                 "question by machine?",
        story="In Königsberg, in September 1930, Hilbert says 'we must know, we will know', the day after Gödel has "
              "announced a theorem that says otherwise. The part builds the proof from the ground: a formal system "
              "to play by hand (MIU), Robinson's Q and Peano arithmetic axiom by axiom, the primitive recursive "
              "functions, and Master Sun's remainders, which become Gödel's β-function and let arithmetic talk "
              "about lists. Formulas become numbers, a program prints itself, and the diagonal lemma yields a "
              "sentence that says 'I am not provable'. The two incompleteness theorems follow, and the "
              "derivability conditions turn the second into a formula of the modal logic GL. The part then turns "
              "from proof to computation: Turing machines, busy beavers up to the five-state champion, the "
              "Church-Turing thesis and Rice's theorem, then independence in ordinary mathematics, Berry's paradox "
              "made exact, Tarski's theorem on truth and Löb's theorem. It ends with what the theorems do and do "
              "not say about minds, and with Gentzen's consistency proof.",
        handoff="The liar and the theories of truth built to survive it are Part 8; what mathematics is about after "
                "Gödel is Part 9. Kolmogorov complexity becomes a theory of induction in Part 15, computation "
                "meets physics in Part 26, minds and machines return in Part 30, and Löb's theorem returns in "
                "Part 42 as an obstacle for agents that must trust their own reasoning.",
        outside="School arithmetic and the idea of a proof. The modal reading of provability uses the box of Part 4.",
        objectives={
            "U": ["Derive a small sum or product in Robinson's Q, naming the axiom used at each step.",
                  "Compute the Gödel number of a short formula and decode a formula from its number.",
                  "Run a small Turing machine by hand and say why no program computes the busy beaver numbers."],
            "M": ["Code a finite list with the β-function, using the Chinese remainder theorem.",
                  "State the diagonal lemma and derive the first incompleteness theorem from it, saying where "
                  "consistency and where omega-consistency are used.",
                  "Prove Rice's theorem by reduction from the halting problem."],
            "D": ["Derive the second incompleteness theorem and Löb's theorem from the three derivability "
                  "conditions, and state Solovay's theorem relating GL to provability in PA.",
                  "Explain what Gentzen's proof assumes that PA cannot prove, and what Paris and Harrington's "
                  "theorem shows about independence in ordinary mathematics."],
            "I": ["Explain why every program analyser must sometimes answer 'I don't know' or be wrong, and how "
                  "abstraction lets a verifier live with Rice's theorem.",
                  "Assess a claim that Gödel's theorem shows something about minds, law or physics, using the "
                  "hypotheses the theorem actually has."],
        },
        results=[
            ("Gödel's β-function", r"\beta(c,d,i)=c \bmod \bigl(1+(i+1)d\bigr):\quad \text{for every } a_0,\dots,a_n "
                                   r"\text{ there are } c,d \text{ with } \beta(c,d,i)=a_i \text{ for all } i\le n"),
            ("The diagonal lemma", r"\text{for every formula } \varphi(x) \text{ there is a sentence } D \text{ with }"
                                   r"\ \mathrm{PA}\vdash D\leftrightarrow\varphi(\ulcorner D\urcorner)"),
            ("Gödel I", r"\mathrm{PA}\vdash G\leftrightarrow\neg\mathrm{Prov}(\ulcorner G\urcorner);\quad "
                        r"\mathrm{PA}\text{ consistent}\Rightarrow\mathrm{PA}\nvdash G;\quad "
                        r"\mathrm{PA}\ \omega\text{-consistent}\Rightarrow\mathrm{PA}\nvdash\neg G"),
            ("Gödel II", r"\mathrm{PA}\text{ consistent}\Rightarrow\mathrm{PA}\nvdash\mathrm{Con}(\mathrm{PA}),"
                         r"\qquad\text{in GL: }\ \neg\Box\bot\to\neg\Box\neg\Box\bot"),
            ("Löb's theorem", r"\mathrm{PA}\vdash\mathrm{Prov}(\ulcorner A\urcorner)\to A\ \Longrightarrow\ "
                              r"\mathrm{PA}\vdash A,\qquad\text{in GL: }\ \Box(\Box p\to p)\to\Box p"),
            ("Busy beavers", r"BB(2)=6,\quad BB(3)=21,\quad BB(4)=107,\quad BB(5)=47{,}176{,}870;\qquad "
                             r"BB\text{ grows faster than every computable function}"),
        ],
        U=(0, 1, 2, 5, 9, 10), D=(8, 12, 15, 17), I=(11, 16),
        also=(("The Reasoner's arithmetic module", "explainer/philosophy/reasoner/arith.py"),),
    ),
    Part(
        n=8, level="U", widget="liarstages", prereq=(2, 5, 7),
        question="Is the sentence 'this sentence is not true' true, false, neither or both?",
        story="The part is about one sentence, argued over since Eubulides, the Later Mohists and the medieval "
              "schools. Tarski isolates what the paradox needs (the T-schema, self-reference, classical logic) and "
              "answers with a hierarchy of languages, which Kripke's Nixon and Jones show does not fit how we talk. "
              "Kripke's own theory is built and run: a world of thirteen sentences that speak of each other's "
              "truth, evaluated in strong Kleene logic stage by stage until nothing changes, then every fixed "
              "point, and the sorting into grounded, ungrounded and paradoxical. The turn is revenge: add 'is not "
              "true' in the sense of false or neither and the construction has no fixed point at all. The part "
              "then tries the other exits: revision sequences in which the liar flickers for ever, Curry's "
              "paradox, which needs no negation, Yablo's staircase, and Priest's true contradictions in LP. It "
              "closes with the Price List, the axiomatic theories of truth, the old question of what truth is, "
              "and two paradoxes of knowledge and belief: the surprise exam and Moore's sentence.",
        handoff="Truth and proof in mathematics return in Part 9. The knower, Moore sentences and announcements "
                "that falsify themselves return in Part 12; gaps and degrees in Part 13; whether meaning needs "
                "truth conditions in Parts 27 and 28; agents that reason about their own reasoning in Part 42.",
        outside="Nothing beyond the truth tables of Part 2; the three values t, f, n are those of Part 5's K3.",
        objectives={
            "U": ["Derive the contradiction from the liar, the T-schema and classical logic, and say which "
                  "ingredient each of the four exits gives up.",
                  "Sort a small set of sentences about each other's truth into grounded, ungrounded and "
                  "paradoxical by tracing what each depends on."],
            "M": ["Compute the stages of Kripke's construction and all fixed points for a finite world in strong "
                  "Kleene logic.",
                  "Run a revision sequence from a given hypothesis and classify each sentence as stably true, "
                  "stably false, dependent on the start, or unstable.",
                  "Construct the revenge sentence for a gap theory and show that the jump has no fixed point "
                  "for it."],
            "D": ["Derive Curry's paradox from the T-schema, modus ponens and contraction, and explain how "
                  "strict-tolerant logic blocks it.",
                  "Compare the axiomatic theories TB, CT, KF and FS, and state what the conservativeness debate "
                  "asks of deflationism."],
            "I": ["Explain a non-terminating recursive definition as an ungrounded sentence, and say what "
                  "least-fixed-point semantics assigns to it.",
                  "Diagnose a self-referential rule or specification as grounded, underdetermined or paradoxical "
                  "before it is implemented."],
        },
        results=[
            ("The liar", r"L\leftrightarrow\neg T(\ulcorner L\urcorner)\ \text{ and }\ T(\ulcorner L\urcorner)"
                         r"\leftrightarrow L\ \text{ give }\ L\leftrightarrow\neg L,\ \text{ which no classical "
                         r"valuation satisfies}"),
            ("Kripke's jump", r"J(I)(A)=\operatorname{val}_{K3}(A, I);\qquad I\sqsubseteq I'\Rightarrow J(I)\sqsubseteq "
                              r"J(I'),\ \text{ so }\ \varnothing\sqsubseteq J(\varnothing)\sqsubseteq J^2(\varnothing)"
                              r"\sqsubseteq\cdots\ \text{ reaches a least fixed point}"),
            ("Fixed points and the T-schema", r"J(I)=I\ \Longrightarrow\ \operatorname{val}(T(\ulcorner A\urcorner),I)="
                                              r"\operatorname{val}(A,I)\ \text{ for every sentence } A"),
            ("Kripke's classification", r"\text{grounded: a value in the least fixed point;}\quad\text{paradoxical: "
                                        r"no value in any fixed point}"),
            ("Revenge", r"R:\ \text{'}R\text{ is not true' (false or neither)}:\quad n\mapsto t\mapsto f\mapsto t"
                        r"\mapsto\cdots,\ \text{ and no value of } R \text{ is a fixed point}"),
            ("Curry's paradox", r"C\leftrightarrow\bigl(T(\ulcorner C\urcorner)\to q\bigr)\ \vdash\ q\quad"
                                r"\text{for any sentence } q"),
        ],
        U=(0, 1, 2, 3, 10, 12, 14), D=(9, 13), I=(6,),
        also=(("The Reasoner's truth module", "explainer/philosophy/reasoner/truth.py"),),
    ),
    Part(
        n=9, level="U", widget="kripkeforce", prereq=(5, 6, 7),
        question="What are numbers, and how could we know anything about them?",
        story="The part opens with Russell's joke and the enslaved boy of the Meno doubling a square: mathematics is "
              "necessary, known without experiment, and applies to the world. Platonism takes its objects at face "
              "value and meets Benacerraf's dilemma: abstract objects cause nothing, so how are they known? Frege's "
              "logicism is built on a world of four objects, where sixteen concepts fall into five numbers; "
              "Frege's theorem derives arithmetic from Hume's principle, which turns out to have no finite model, "
              "and Basic Law V is its bad company. Formalism, Brouwer's intuitionism and predicativism follow, and "
              "the Curry-Howard correspondence makes the constructive reading exact: a proof is a program, the "
              "Reasoner finds programs for seven propositions and Kripke countermodels for excluded middle, "
              "Peirce's law and double negation elimination. The part turns at Benacerraf's second dilemma, that "
              "nothing settles which sets the numbers are, and structuralism's puzzle of i and minus i. It ends "
              "with the indispensability argument and Field's science without numbers, the Price List, and "
              "mathematics in practice: univalence, Lakatos, pictures that prove and lie, and proofs by machine.",
        handoff="Kant's synthetic a priori is taken up in Part 10 and Quine's web of belief in Parts 11 and 15. "
                "Abstract objects return in Part 20, identity and indiscernibility in Part 21, knowledge of "
                "possibility in Part 22, and machines that reason, and whether to trust them, in Parts 30 and 42.",
        outside="School arithmetic and geometry. The Kripke models for intuitionistic logic are those of Part 5, "
                "Cantor's theorem is from Part 6, Hilbert's program and Gentzen from Part 7.",
        objectives={
            "U": ["State Benacerraf's two dilemmas and say which one each of platonism, logicism, formalism, "
                  "intuitionism, structuralism and fictionalism is built to answer.",
                  "Sort the concepts on a small domain into Frege's numbers and explain why Hume's principle "
                  "cannot hold on a finite world.",
                  "Compute V - E + F for a polyhedron and say how Lakatos's monsters changed the theorem."],
            "M": ["Write the lambda term that proves a given intuitionistic tautology and check its type by hand.",
                  "Build a two-world Kripke model that refutes excluded middle or Peirce's law.",
                  "Recover coordinates from betweenness and congruence facts and state how unique they are."],
            "D": ["Outline the proof of Frege's theorem from Hume's principle in second-order logic and state the "
                  "bad company objection, with Boolos's question and Fine's stability criterion.",
                  "State univalence and explain in what sense it builds structuralism into a foundation."],
            "I": ["Explain what a machine-checked proof establishes, what the trusted kernel is, and what remains "
                  "to a human: reading that the statement written is the statement meant.",
                  "Read a type signature as a proposition and a program as its proof when reviewing typed code."],
        },
        results=[
            ("Hume's principle", r"\#F=\#G\ \leftrightarrow\ F\approx G\qquad(F\approx G:\ \text{the } F\text{s and "
                                 r"the } G\text{s correspond one to one})"),
            ("Frege's theorem", r"\text{second-order logic}+\text{Hume's principle}\ \vdash\ \text{the Dedekind-Peano "
                                r"axioms};\quad\text{on } n \text{ objects HP needs } n+1 \text{ numbers, so it has no "
                                r"finite model}"),
            ("Bad company", r"\text{Basic Law V: }\ \varepsilon F=\varepsilon G\leftrightarrow\forall x\,(Fx"
                            r"\leftrightarrow Gx)\ \text{ needs } 2^{|D|}\le |D|,\ \text{ impossible by Cantor's theorem}"),
            ("Curry-Howard", r"\lambda x.\,\lambda y.\,x\;:\;A\to(B\to A),\qquad \lambda p.\,\langle\operatorname{snd}p,"
                             r"\operatorname{fst}p\rangle\;:\;A\wedge B\to B\wedge A"),
            ("What has no program", r"w_0\le w_1,\ A \text{ true only at } w_1:\quad w_0\nVdash A\vee\neg A,\quad "
                                    r"w_0\nVdash\neg\neg A\to A,\quad w_0\nVdash((A\to B)\to A)\to A"),
            ("Dedekind's categoricity", r"\text{any two progressions satisfying the second-order Peano axioms are "
                                        r"isomorphic, successor matching successor}"),
        ],
        U=(0, 1, 2, 5, 9, 12, 14, 15), D=(4, 8, 13), I=(16,),
        also=(("The Reasoner's types module", "explainer/philosophy/reasoner/types.py"),
              ("The Reasoner's philosophy of mathematics module", "explainer/philosophy/reasoner/mathphil.py")),
    ),
    Part(
        n=10, level="U", widget="triangleexcess", prereq=(9,),
        question="Does knowledge come from reason or from experience, and how could we know in advance anything "
                 "that must be so?",
        story="Act III opens in the skeptical crisis of Sextus, Montaigne and Galileo's telescope. Descartes doubts "
              "everything he can, reaches the cogito, and hopes to rebuild knowledge as geometry is built; his "
              "method of normals is solved on screen. Spinoza takes the hope literally, and the Reasoner reads "
              "Part I of the Ethics as a graph of proofs: 51 items, 102 citations, no circles, a ten-step chain, "
              "and an axiom the English translation forgot to cite. Leibniz divides truths of reason from truths "
              "of fact; Locke, Berkeley and Hume answer from experience, and Hume's fork, his analysis of cause "
              "and four rules that fit eight sunrises and disagree about the ninth leave induction without a "
              "foundation. The turn is Kant's question, how synthetic judgments can be known a priori, and his "
              "answer: space, time and the categories are the mind's own forms, at the price of antinomies and "
              "unknowable things in themselves. The part ends with what became of Kant's examples (curved "
              "triangles, Eddington's eclipse, the relativized a priori), Hegel, and the empiricist trilemma.",
        handoff="What knowledge is, and Quine's web of belief, are Part 11. The problem of induction is Part 15; "
                "cause and law are Parts 17 and 24; the bundle self is Part 21; space and time after Kant are "
                "Part 25; Spinoza's freedom as understood necessity is weighed in Part 32.",
        outside="School geometry and algebra. Frege's reply to Kant on 7 + 5 = 12 is from Part 9.",
        objectives={
            "U": ["Retrace Descartes's three waves of doubt and say what the cogito does and does not establish.",
                  "Sort a judgment by Hume's fork and by Kant's grid (analytic or synthetic, a priori or a "
                  "posteriori), with a reason.",
                  "Write down two rules that fit the same past observations and disagree about tomorrow, and "
                  "explain why experience cannot choose between them."],
            "M": ["Trace what a proposition of Spinoza's Ethics rests on by following its citations back to "
                  "definitions and axioms.",
                  "Find a normal to a parabola by Descartes's double-root method, and the least-time path "
                  "across a surface, and check Snell's law there.",
                  "Set out the thesis and antithesis of Kant's first antinomy and his diagnosis of both."],
            "D": ["Reconstruct the structure of the transcendental deduction and of the second analogy, and "
                  "compare the two-world and two-aspect readings of transcendental idealism.",
                  "Assess the attempted formalizations of Hegel's dialectic and say where each stops."],
            "I": ["Compute a triangle's spherical excess and the deflection of starlight at the sun's edge, and "
                  "say what each measurement could and could not show about the geometry of space.",
                  "Distinguish the constitutive principles of a measurement framework from its empirical claims "
                  "when a theory is revised."],
        },
        results=[
            ("Spinoza's graph", r"\text{Ethics I: 8 definitions, 7 axioms, 36 propositions, 102 citations, no "
                                r"circles; the longest chain has ten steps, from D3 to P32}"),
            ("Least time and Snell's law", r"T(x)=\frac{\sqrt{(x-a_1)^2+a_2^2}}{v_1}+\frac{\sqrt{(b_1-x)^2+b_2^2}}{v_2},"
                                           r"\qquad T'(x)=0\iff\frac{\sin i}{v_1}=\frac{\sin r}{v_2}"),
            ("Hume's problem", r"\text{'the future will resemble the past' is no relation of ideas (its denial is "
                               r"conceivable), and experience supports it only by assuming it}"),
            ("Kant's question", r"\text{analytic}\Rightarrow\text{a priori};\qquad\text{how are synthetic judgments "
                                r"a priori possible: } 7+5=12,\ \text{every event has a cause?}"),
            ("Angle sum on a sphere", r"\alpha+\beta+\gamma=\pi+\frac{\text{Area}}{R^2};\qquad\text{starlight at "
                                      r"the sun's edge: }\ \delta=\frac{4GM}{c^2R}\approx 1.75''"),
            ("The empiricist trilemma", r"\text{all knowledge comes from experience; we know necessary truths; "
                                        r"experience shows only what is: jointly inconsistent, any two consistent}"),
        ],
        U=(0, 1, 5, 6, 7, 8, 9, 16), D=(11, 13, 15), I=(14,),
        also=(("The Reasoner's module for the early moderns", "explainer/philosophy/reasoner/modern.py"),),
    ),
    Part(
        n=11, level="U", widget="marginclock", prereq=(3, 4, 10),
        question="What must be added to a true belief to make it knowledge?",
        story="Ann reads the time from a working clock and Ben from one that stopped long ago at the same hour; both "
              "are right, and only one knows. Plato's Theaetetus tries three answers and the tradition settles on "
              "justified true belief, until Gettier's three pages of 1963, whose two cases the Reasoner builds as "
              "first-order models: a valid inference from a justified falsehood to a truth. Older cases "
              "(Dharmottara's mirage, Russell's clock) and the repairs follow, and Zagzebski's recipe shows that "
              "any condition short of truth can be Gettiered. Four theories are then run as checkers on the same "
              "cases: reliabilism, Nozick's tracking, safety, and Sosa's archer. The turn is Williamson: put "
              "knowledge first, and a margin for error shows that feeling cold is not luminous and that knowing "
              "does not bring knowing that you know. The part then meets the skeptic's brain in a vat with four "
              "answers and Zhuangzi's butterfly, and ends with the structure of justification, Quine's web of "
              "belief, and what experimental philosophy found when it asked people.",
        handoff="Knowledge in groups, common knowledge and testimony are Part 12. The lottery returns with degrees "
                "of belief in Part 13 and belief revision in Part 14; Quine's web in Parts 15 and 18; Putnam's "
                "externalism in Part 27; and what it would mean for a machine to know in Part 30.",
        outside="Nothing beyond Parts 3 and 4: a first-order model, and the box of modal logic read as 'knows'.",
        objectives={
            "U": ["State the justified-true-belief analysis and build a Gettier case against it in two steps: a "
                  "justified false belief, then luck that makes it true.",
                  "State the skeptic's three claims about the brain in a vat and say which one Moore, Dretske and "
                  "the contextualist each give up."],
            "M": ["Evaluate sensitivity and safety for a belief in a model of worlds ordered by similarity, and "
                  "find a case where they disagree.",
                  "Run the anti-luminosity argument on a gradual series and locate the moments that are cold but "
                  "not knowably cold.",
                  "State the generality problem for reliabilism with one belief and several process types."],
            "D": ["Prove that in a margin-for-error model each iteration of K strips one margin, so that KK "
                  "fails at the boundary, and say which frame condition KK corresponds to.",
                  "State the Bovens-Hartmann impossibility result for coherence measures and what it leaves of "
                  "coherentism."],
            "I": ["Read a cross-cultural survey of Gettier intuitions critically: the original effect, the "
                  "replications, and what either would show about the method of cases."],
        },
        results=[
            ("Justified true belief", r"S\text{ knows } p\iff p\ \wedge\ B_S\,p\ \wedge\ J_S\,p\qquad\text{(Gettier "
                                      r"1963: the right side is not sufficient)}"),
            ("Sensitivity (Nozick)", r"\neg p\ \mathrel{\Box\!\!\to}\ \neg B_S\,p:\quad\text{in the closest worlds "
                                     r"where } p \text{ is false, } S \text{ does not believe } p"),
            ("Safety (Sosa, Williamson)", r"\text{in every nearby world where } S \text{ believes } p,\ p \text{ is "
                                          r"true}"),
            ("Margin for error", r"w\models Kp\iff\forall v\,\bigl(|v-w|\le m\Rightarrow v\models p\bigr),\qquad "
                                 r"\text{so } K^n(x\le c)\ \text{holds exactly where } x\le c-nm"),
            ("Anti-luminosity", r"C(t)\to K\,C(t)\ \text{ and }\ K\,C(t)\to C(t+1)\ \text{ for all } t\ \text{ give }"
                                r"\ C(0)\to C(n)"),
            ("The skeptic's triad", r"\neg K(\neg\mathrm{BIV}),\qquad K(\text{hands})\to K(\neg\mathrm{BIV}),\qquad "
                                    r"K(\text{hands})\qquad\text{are jointly inconsistent}"),
        ],
        U=(0, 1, 2, 3, 11, 13), D=(10, 14), I=(17,),
        also=(("The Reasoner's knowledge module", "explainer/philosophy/reasoner/knowledge.py"),),
    ),
    Part(
        n=12, level="U", widget="muddyrounds", prereq=(4, 8, 11),
        question="What changes when everyone knows something, and everyone knows that everyone knows it?",
        story="Three children have been playing and two have mud on their foreheads; each sees the others and not "
              "herself. Their father says what all of them can already see, that at least one is muddy, and "
              "only then can the muddy ones work it out. The part builds the "
              "tools to explain why: Hintikka's knowledge as a box, many agents in one model with a line for "
              "each agent's ignorance, and public announcements that delete worlds, run on three cards, Cheryl's "
              "birthday and the muddy children up to eight. What the father adds is common knowledge, defined as "
              "a tower of 'everyone knows' and computed as reachability. The turn is the coordinated attack: "
              "over a channel that can lose messages each delivered messenger adds one storey to the tower and "
              "common knowledge never arrives, a theorem that distributed systems live with through quorums, "
              "timeouts and probabilistic finality. Rubinstein's email game, Aumann's agreement theorem as a "
              "dialogue, private announcements, the Russian cards and Fitch's unknowable truths follow. The "
              "part ends with knowledge from others: testimony, peer disagreement, the diversity prediction "
              "theorem behind Galton's ox, and Zollman's scientists, who find the truth more often when they "
              "talk less.",
        handoff="Degrees of belief and Bayes are Part 13, belief revision Part 14, evidence from many sources "
                "Part 16. Conventions and the social contract return in Part 34, juries and democracy in "
                "Part 39, and agreement among machines that reason in Part 42.",
        outside="Kripke models from Part 4. The last chapters use a mean, a variance and Bayes's rule.",
        objectives={
            "U": ["Solve the muddy children puzzle for any number of muddy children, and say exactly what the "
                  "father's announcement adds to what each child already knew.",
                  "Tell 'everyone knows' from common knowledge with an example where the first holds and the "
                  "second fails.",
                  "State the equal weight and steadfast views of peer disagreement and apply each to a case."],
            "M": ["Evaluate K, E and C formulas in a multi-agent S5 model and update the model by a public "
                  "announcement.",
                  "Prove that n delivered messages give n - 1 levels of mutual knowledge of the plan and never "
                  "common knowledge.",
                  "Derive Fitch's result that if every truth is knowable then every truth is known."],
            "D": ["Compute a product update with an action model for a private announcement, and state the "
                  "reduction axioms of public announcement logic.",
                  "Show by iterated best responses that almost common knowledge does not support coordination "
                  "in Rubinstein's email game, and state Monderer and Samet's common p-belief."],
            "I": ["Explain how quorum protocols and probabilistic finality reach agreement without common "
                  "knowledge, and what FLP says they cannot guarantee.",
                  "Use the diversity prediction theorem to say when averaging forecasts helps and when a shared "
                  "bias defeats it.",
                  "Describe the Zollman effect and what it suggests about how densely a research community "
                  "should share early results."],
        },
        results=[
            ("Knowledge and common knowledge", r"w\models K_i\varphi\iff\forall v\,(w\sim_i v\Rightarrow v\models"
                                               r"\varphi),\qquad C_G\varphi=\bigwedge_{k\ge1}E_G^{\,k}\varphi,"
                                               r"\quad E_G\varphi=\bigwedge_{i\in G}K_i\varphi"),
            ("The muddy children", r"\text{with } k \text{ muddy children, after the father's announcement the "
                                   r"muddy ones know in round } k \text{ and the clean ones in round } k+1"),
            ("The coordinated attack", r"\text{after } n \text{ delivered messages: } E^{\,n-1}(\text{plan}) "
                                       r"\text{ and } \neg E^{\,n}(\text{plan}),\ \text{ so } \neg C(\text{plan}) "
                                       r"\text{ for every } n"),
            ("Aumann's agreement theorem", r"\text{a common prior and common knowledge of the posteriors } "
                                           r"P(A\mid\mathcal I_1)=q_1,\ P(A\mid\mathcal I_2)=q_2\ \Longrightarrow\ "
                                           r"q_1=q_2"),
            ("Fitch's paradox", r"K(q\wedge\neg Kq)\vdash\bot,\qquad\text{so }\ \forall p\,(p\to\Diamond Kp)\ "
                                r"\vdash\ \forall p\,(p\to Kp)"),
            ("Diversity prediction theorem", r"(\bar g-\theta)^2=\frac1n\sum_i(g_i-\theta)^2-\frac1n\sum_i"
                                             r"(g_i-\bar g)^2"),
        ],
        U=(0, 2, 3, 4, 12, 13), D=(7, 9), I=(6, 14, 15),
        also=(("The Reasoner's module for knowledge among many", "explainer/philosophy/reasoner/epistemic.py"),),
    ),
]
