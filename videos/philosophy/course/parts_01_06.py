"""The prologue and Act I, The Machinery of Reason: syllogisms, propositions, quantifiers, modality, many values, sets (Parts 1-6)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=1, level="U", widget="vennmoods",
        question="Can a dispute be settled by calculation, as Leibniz hoped, and how far did the first logic get?",
        story="Around 1685 Leibniz writes down a dream: when persons dispute, let them say 'calculemus' and compute "
              "who is right. The part follows the dream from its beginnings. It opens with the unicorn syllogism, "
              "valid for the tradition and invalid for modern logic, then goes back to the first philosophers, to "
              "what an argument is, to Zeno's race (a geometric series that meets at 100/9 seconds and leaves "
              "Thomson's lamp unanswered), to the Euthyphro as a set of five claims that cannot all be kept, and to "
              "Plato's doubled square and divided line. Aristotle's syllogistic is then checked whole: each of the "
              "256 moods against all 256 arrangements of the eight Venn regions gives 15 valid moods, and 24 once "
              "every term is inhabited, which locates the unicorn dispute in the meaning of 'all'. After the "
              "Mohists, the Nyāya inference and logic in Arabic, the part turns to the first machines of reasoning: "
              "Llull's wheels, Leibniz's characteristic numbers, which reproduce exactly the 24 traditional moods, "
              "and his binary reading of the Yijing. It ends with what the syllogism cannot say: relations and "
              "stacked quantifiers.",
        handoff="The Price List of the Euthyphro becomes an engine (minimal correction sets) in Part 2; the 256 "
                "moods are recounted inside first-order logic in Part 3, where De Morgan's horse heads are proved; "
                "Strawson's truth-value gap returns in Part 5; the Nyāya inference returns with Dignāga's three "
                "marks in Part 15; Zeno's supertask is the first brick of the Wall.",
        outside="School arithmetic: fractions, divisibility, and the sum of a geometric series.",
        objectives={
            "U": ["Tell validity from soundness, and refute an invalid form by giving a counterexample.",
                  "Read a categorical sentence (A, E, I, O) as a claim about Venn regions, and test a mood by "
                  "searching for an arrangement that makes the premises true and the conclusion false.",
                  "Sum Achilles's stages as a geometric series and say what the sum does not settle about "
                  "Thomson's lamp."],
            "M": ["Explain why exactly nine moods need an inhabited term, and name the term each one needs.",
                  "Translate the four categorical forms into Leibniz's pairs of characteristic numbers and verify "
                  "Barbara by the transitivity of divisibility."],
            "D": ["State in what sense Leibniz's arithmetic is a sound and complete model of the traditional "
                  "syllogistic (Łukasiewicz 1951, Sotirov 1999), and what the search over 19,683 assignments does "
                  "and does not prove.",
                  "Give an argument that is valid and yet is none of the 256 moods, and say which expressive "
                  "resource it needs."],
            "I": ["Count Llull's combinations and write the 64 hexagrams as six-digit binary numerals, and say "
                  "what the correspondence with the Yijing does and does not show.",
                  "Lay out a disagreement as a Price List: the claims that cannot all be kept, and what each exit "
                  "gives up."],
        },
        results=[
            ("Achilles and the tortoise", r"10+1+\tfrac1{10}+\cdots=\frac{10}{1-\frac1{10}}=\frac{100}{9}\ \text{s},"
                                          r"\qquad \sum_{n\ge 1}2^{-n}=1"),
            ("Validity of a mood", r"\text{valid}\iff\text{no arrangement of the 8 Venn regions refutes it}"
                                   r"\quad(2^{8}=256)"),
            ("The count", r"4\cdot 4^{3}=256\ \text{moods},\qquad 15=4+4+4+3\ \text{valid}"),
            ("With every term inhabited", r"24=15+9=6+6+6+6\ \text{valid}"),
            ("Leibniz's numbers (1679)", r"\text{All } S \text{ are } P\iff P^{+}\mid S^{+}\ \text{and}\ P^{-}\mid S^{-}"),
            ("Llull's wheels", r"\binom{9}{2}=36,\qquad \binom{9}{3}=84,\qquad 9^{3}=729"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11), D=(12, 14), I=(13, 15),
        also=(("The Reasoner: syllogism.py", "explainer/philosophy/reasoner/syllogism.py"),),
    ),
    Part(
        n=2, level="U", widget="satdial", prereq=(1,),
        question="If an argument is built from 'and', 'or', 'not' and 'if', can a machine always say whether it is "
                 "valid, and at what price?",
        story="A knight-and-knave puzzle is settled by an eight-row table, and a 2016 computer proof colours the "
              "numbers 1 to 400 with no one-colour Pythagorean triple: the same calculation at two scales. The part "
              "builds propositional logic from Boole's algebra, where x squared equals x has the roots 0 and 1, "
              "through formulas as trees, the sixteen binary truth functions and Post's criterion for when "
              "connectives suffice. Validity becomes a truth table, which decides every question and costs 2 to the "
              "n rows. Natural deduction is shown sound and complete, so proof and truth agree. Then the search is "
              "made clever: resolution, DPLL's propagate, branch and back up, and CDCL, which learns a clause from "
              "every conflict. The turn is the price: SAT is NP-complete, random 3-SAT is hardest near 4.27 clauses "
              "per atom, and the pigeonhole formulas force exponentially long resolution proofs. The part ends by "
              "reading Socrates' elenchus as the same computation: the minimal inconsistent sets of Republic I and "
              "the minimal correction sets that restore consistency, and with them the first full Price List, the "
              "problem of evil with its six exits.",
        handoff="The Price List engine (minimal inconsistent and minimal correction sets) is used in every later "
                "part; quantifiers, which propositional logic cannot see, are Part 3; compactness returns in Parts 3 "
                "and 6; the rule of double negation divides classical from intuitionistic logic in Part 9; the "
                "problem of evil returns as an argument about probabilities in Part 23, and the SAT solver checks a case "
                "of Arrow's theorem in Part 39.",
        outside="Nothing beyond school algebra; powers of two.",
        objectives={
            "U": ["Build the truth table of a formula and use it to decide whether an argument form is valid, "
                  "giving the countermodel row when it is not.",
                  "Lay out a set of jointly inconsistent claims as a Price List: find its minimal inconsistent "
                  "subsets and every minimal set of claims whose rejection restores consistency."],
            "M": ["Prove soundness by induction on proofs, and prove completeness by extending a consistent set to "
                  "a maximal one with Lindenbaum's lemma.",
                  "Convert a formula to clauses by Tseitin's encoding and refute a clause set by resolution.",
                  "Run DPLL by hand on a small clause set: propagate, branch, back up."],
            "D": ["Sketch the Cook-Levin reduction from a machine's run to a clause set, and state Haken's lower "
                  "bound for resolution on the pigeonhole formulas and what extended resolution changes.",
                  "State the Cook-Reckhow question and its relation to NP versus coNP."],
            "I": ["Encode a dependency or scheduling problem as clauses, hand it to a SAT solver, and read the "
                  "model or the learned clauses back.",
                  "Explain what a conflict-driven solver learns from a conflict and why whatever is hard for "
                  "resolution is hard for it."],
        },
        results=[
            ("Consequence, by table", r"\Gamma\models\varphi\iff\text{no row of the } 2^{n} \text{ makes } \Gamma "
                                      r"\text{ true and } \varphi \text{ false}"),
            ("Soundness and completeness", r"\Gamma\vdash\varphi\iff\Gamma\models\varphi"),
            ("Resolution", r"\frac{C\lor p\qquad D\lor\lnot p}{C\lor D}\,,\qquad \Gamma\ \text{unsatisfiable}\iff"
                           r"\Gamma\vdash_{\mathrm{res}}\Box"),
            ("Tseitin's encoding", r"k \text{ binary connectives, } m \text{ of them } \leftrightarrow:\quad "
                                   r"3k+m+1 \text{ clauses}"),
            ("The price", r"\text{SAT is NP-complete};\qquad \text{resolution on } \mathrm{PHP}^{n+1}_{n} "
                          r"\text{ needs size } 2^{\Omega(n)}"),
            ("Reiter's duality", r"\text{MCSes}=\text{minimal hitting sets of the MUSes}"),
        ],
        U=(0, 1, 2, 4, 6, 14, 15), D=(8, 12), I=(11, 13),
        also=(("The Reasoner: prop.py", "explainer/philosophy/reasoner/prop.py"),),
    ),
    Part(
        n=3, level="U", widget="quantorder", prereq=(1, 2),
        question="What do 'all' and 'some' add to logic, and why can no machine decide which arguments that use "
                 "them are valid?",
        story="De Morgan's argument about horses' heads, which no syllogism captures, is written in Frege's notation "
              "and checked by a tableau in 29 steps. The part builds first-order logic: variables, scope and "
              "capture, then Tarski's definition of truth in a structure, run on four people and on all 512 "
              "relations among three, where 'everyone loves someone' holds in 343 and 'someone is loved by "
              "everyone' in 169. The new language counts with identity, states Russell's theory of descriptions and "
              "contains all of Aristotle's moods. Gentzen's quantifier rules and tableaux that return a "
              "countermodel from an open branch lead to Gödel's completeness theorem by Henkin's construction. "
              "Then the turn: compactness gives numbers larger than every natural number, Löwenheim and Skolem "
              "give a countable model of the theory of uncountable sets, and Church and Turing show that validity "
              "can be confirmed by calculation but not decided. The part ends by asking why this logic is the "
              "standard one: second-order logic, Lindström's theorem, and Quine's criterion of what a theory says "
              "there is.",
        handoff="The halting diagonal is proved in full and builds Gödel's incompleteness in Part 7 and Tarski's "
                "theorem on truth in Part 8; Skolem's paradox and the continuum hypothesis return with set theory in "
                "Part 6; the question of which notions are logical returns in Part 9; Quine's criterion opens the "
                "ontology of Part 20, and Russell's descriptions return in Part 27.",
        outside="The propositional logic of Part 2; no mathematics beyond the idea of a function and a set.",
        objectives={
            "U": ["Translate English sentences with 'all', 'some' and relations into first-order formulas, and show "
                  "by a small structure that the order of two quantifiers matters.",
                  "Evaluate a sentence in a finite structure by Tarski's clauses, object by object.",
                  "Write 'at least two', 'exactly one' and Russell's 'the' with identity."],
            "M": ["Build a tableau for an argument and read a countermodel off an open branch.",
                  "Prove from compactness that 'the domain is finite' is not expressible and that arithmetic has "
                  "nonstandard models.",
                  "Explain why validity is semi-decidable and why a decision procedure would decide halting."],
            "D": ["Carry out Henkin's proof of completeness: witnesses, a maximal consistent set, the term model.",
                  "State Lindström's theorem and place second-order logic, the infinitary logics and the "
                  "generalized quantifiers on the map of what each gives up."],
            "I": ["Compute a most general unifier, run the occurs check, and refute a small clause set by "
                  "resolution as an automated prover does.",
                  "Name a decidable fragment (monadic, two-variable, guarded) and say where description logics and "
                  "SMT solvers use it."],
        },
        results=[
            ("Tarski's clause for 'all'", r"\mathcal M\models\forall x\,\varphi\,[g]\iff\mathcal M\models\varphi\,"
                                          r"[g(x\mapsto a)]\ \text{for every } a\in M"),
            ("The order of quantifiers", r"\exists y\,\forall x\,L(x,y)\models\forall x\,\exists y\,L(x,y),"
                                         r"\quad\text{not conversely}"),
            ("Russell's 'the' (1905)", r"\exists x\,\bigl(K(x)\land\forall y\,(K(y)\to y=x)\land B(x)\bigr)"),
            ("Completeness (Gödel 1929)", r"\Gamma\models\varphi\iff\Gamma\vdash\varphi"),
            ("Compactness", r"\Gamma \text{ has a model}\iff\text{every finite } \Gamma_0\subseteq\Gamma \text{ has one}"),
            ("Church and Turing (1936)", r"\{\varphi:\ \models\varphi\}\ \text{is semi-decidable, not decidable}"),
        ],
        U=(0, 1, 2, 3, 4, 14), D=(7, 12, 13), I=(11,),
        also=(("The Reasoner: fol.py", "explainer/philosophy/reasoner/fol.py"),),
    ),
    Part(
        n=4, level="U", widget="frameaxioms", prereq=(2, 3),
        question="What do 'must', 'might', 'ought' and 'always' have in common, and what decides which of their "
                 "laws hold?",
        story="Aristotle asks whether it is already true that there will be a sea battle tomorrow, and Diodorus "
              "Cronus answers with the Master Argument: three claims that cannot all be true, and three ancient "
              "exits. C. I. Lewis's strict implication turns the puzzle into axiom systems, S1 to S5, with fourteen "
              "modalities in S4 and six in S5. Kripke gives them one semantics: worlds, arrows saying which worlds "
              "each world can see, and a box that means 'true in every world seen'. Then each axiom turns out to "
              "be a shape of arrows (T reflexive, 4 transitive, B symmetric, 5 euclidean, D serial), proved and "
              "checked on every frame of up to four worlds. The turn is Löb's axiom, valid exactly on the "
              "transitive frames with no infinite ascending chain, a condition no first-order sentence states: "
              "modal logic is not first-order logic in disguise. Canonical models, bisimulation and filtration "
              "give completeness, the limit of what the box can see, and decidability. The part ends with the box "
              "read as obligation, as time and as the runs of a program, and a model checker that verifies "
              "Peterson's mutual-exclusion protocol and finds the eight-step failure of a broken variant.",
        handoff="Knowledge as a modality and the debate over introspection are Parts 11 and 12; provability logic "
                "and Löb's theorem return in Part 7; possible worlds, rigid designators and essence in Part 22; "
                "branching time and foreknowledge in Part 23; the many-valued logics of Part 5 come next.",
        outside="Propositional logic (Part 2) and the idea of a relation; graphs drawn with arrows.",
        objectives={
            "U": ["Evaluate formulas with box and diamond at each world of a small Kripke model.",
                  "State the Master Argument as three jointly inconsistent claims and say which one Diodorus, "
                  "Cleanthes and Chrysippus each gave up.",
                  "Read the box as necessity, knowledge, obligation or 'always' and say what the arrows mean under "
                  "each reading."],
            "M": ["Prove both directions of a correspondence (T and reflexivity, 4 and transitivity, B and "
                  "symmetry), giving the refuting valuation when the frame lacks the property.",
                  "Compute the largest bisimulation between two models and use it to show that a property is not "
                  "modally definable.",
                  "Filter a model through the subformulas of a formula and explain why K, T, S4 and S5 are "
                  "decidable."],
            "D": ["Show by compactness that the frame condition of Löb's axiom is not first-order, and state the "
                  "Goldblatt-Thomason and Sahlqvist theorems.",
                  "Carry out the canonical-model proof of completeness for K, and say why it works for T and 4 and "
                  "fails for GL."],
            "I": ["Specify mutual exclusion and freedom from starvation in temporal logic, and explain what "
                  "fairness adds.",
                  "Read a model checker's counterexample trace, and write a loop invariant for a Hoare triple."],
        },
        results=[
            ("Kripke's clause", r"\mathcal M,w\models\Box\varphi\iff\mathcal M,v\models\varphi\ \text{for every } v "
                                r"\text{ with } wRv"),
            ("T and 4", r"\Box p\to p:\ \text{reflexive};\qquad \Box p\to\Box\Box p:\ \text{transitive}"),
            ("B, 5 and D", r"p\to\Box\Diamond p:\ \text{symmetric};\quad \Diamond p\to\Box\Diamond p:\ "
                           r"\text{euclidean};\quad \Box p\to\Diamond p:\ \text{serial}"),
            ("Löb's axiom", r"\Box(\Box p\to p)\to\Box p:\ \text{transitive, no infinite chain } w_0Rw_1R\cdots"),
            ("The Barcan formula", r"\forall x\,\Box\varphi\to\Box\,\forall x\,\varphi\quad\text{(constant domains)}"),
            ("Mutual exclusion", r"\mathrm{AG}\,\lnot(\mathrm{crit}_0\land\mathrm{crit}_1)"),
        ],
        U=(0, 1, 3, 10), D=(5, 6), I=(12, 13, 14, 15),
        also=(("The Reasoner: modal.py", "explainer/philosophy/reasoner/modal.py"),),
    ),
    Part(
        n=5, level="U", widget="heapdegrees", prereq=(2, 4),
        question="What happens to logic if a sentence may be neither true nor false, or both, or true to a degree, "
                 "and does any of it solve the paradox of the heap?",
        story="A man with no hairs is bald, one more hair never makes the difference, and so a man with a full "
              "head of hair is bald: 102 premises for 101 men, classically unsatisfiable, every one of them needed. "
              "The part builds the logics that give up 'every sentence is true or false'. Łukasiewicz, Kleene and "
              "Bochvar add a third value; K3 and LP read the same tables as a gap and as a glut and turn out to be "
              "exact duals; Belnap and Dunn's four values serve a computer told conflicting things and Nāgārjuna's "
              "four corners alike, and the Jaina count reaches seven. Paraconsistent and relevant logics refuse "
              "explosion, Gödel shows that intuitionistic logic has no finite table, and degrees of truth drive a "
              "fuzzy controller that stops a train. Then the heap returns as this part's brick in the Wall: "
              "supervaluation, degrees, epistemicism and contextualism are computed side by side, each exit from "
              "the sorites quartet has a second price, and the borderline itself turns out to have borderline "
              "cases. The part ends with logic as resources, quantum propositions where distribution fails, the "
              "question of what makes a consequence logical, and whether there is one logic or many.",
        handoff="Naive set theory and the logics that might save it are Part 6; the liar, with its gaps, gluts and "
                "revenge, is Part 8; intuitionism is Part 9; degrees of belief, which are not degrees of truth, are "
                "Part 13; vague objects and persons are Parts 20 and 21; quantum logic returns in Part 26.",
        outside="Propositional logic and the Price List of Part 2; for Chapter 13, the Kripke models of Part 4.",
        objectives={
            "U": ["Evaluate a formula in a three-valued table and say whether an inference is valid in K3 and in "
                  "LP, giving the countermodel when it is not.",
                  "State the sorites as a set of jointly inconsistent claims and say which claim each theory of "
                  "vagueness gives up.",
                  "Read Nāgārjuna's four corners and the Jaina seven predications as sets of truth values."],
            "M": ["Prove that K3 has no tautologies and that LP has no explosion, and derive the duality between "
                  "them.",
                  "Compute supervaluationist verdicts over a set of sharpenings and explain how 'there is a last "
                  "bald man' is super-true with no super-true instance.",
                  "Compute Łukasiewicz degrees along a sorites series and bound the loss of each modus ponens."],
            "D": ["Model 'definitely' as a box over sharpenings, and show why a non-transitive accessibility "
                  "relation gives higher-order vagueness and revenge.",
                  "State Tarski's permutation-invariance criterion for logical notions and the collapse argument "
                  "against logical pluralism."],
            "I": ["Write fuzzy rules with a t-norm and defuzzify them into a control signal, and say what the "
                  "controller trades between comfort and precision.",
                  "Decide whether a sequent of linear logic is provable by counting resources, and explain what "
                  "dropping contraction and weakening buys a type system."],
        },
        results=[
            ("Consequence in a matrix", r"\Gamma\models_{\mathsf M}\varphi\iff\text{designated premises never give an "
                                        r"undesignated } \varphi"),
            ("Gaps and gluts are dual", r"A\models_{\mathrm{K3}}B\iff\lnot B\models_{\mathrm{LP}}\lnot A"),
            ("What LP gives up", r"p,\ \lnot p\not\models_{\mathrm{LP}}q,\qquad p,\ p\to q"
                                 r"\not\models_{\mathrm{LP}}q\qquad(p=\tfrac12,\ q=0)"),
            ("The sorites", r"\{B_0,\ B_0\to B_1,\ \dots,\ B_{n-1}\to B_n,\ \lnot B_n\}\ \text{is minimally "
                            r"unsatisfiable}"),
            ("Degrees (Łukasiewicz)", r"v(A\to B)=\min(1,\,1-v(A)+v(B)),\quad v(B)\ge v(A)+v(A\to B)-1"),
            ("Supervaluation", r"\exists i\,(B_i\land\lnot B_{i+1})\ \text{super-true, with no super-true instance}"),
        ],
        U=(0, 1, 2, 4, 5, 10), D=(13, 16, 17), I=(9, 14),
        also=(("The Reasoner: matrix.py", "explainer/philosophy/reasoner/matrix.py"),
              ("The Reasoner: linear.py", "explainer/philosophy/reasoner/linear.py")),
    ),
    Part(
        n=6, level="U", widget="diagonalescape", prereq=(2, 3),
        question="Are there more numbers than square numbers, are some infinities larger than others, and can the "
                 "axioms of set theory settle how many real numbers there are?",
        story="Galileo pairs each number with its square and concludes that 'more' makes no sense for the infinite; "
              "Hilbert's hotel takes in one guest and then a bus when it is full; Cantor concludes that size is "
              "pairing, counts the fractions, and then flips the diagonal of any list of rows of zeros and ones to "
              "get a row the list lacks. So the reals cannot be counted, and no set can be paired with its own "
              "subsets. The part follows the paradise and its snakes: Cantor's critics, Russell's letter of 1902, "
              "which brings down Frege's system, and the axioms of Zermelo and Fraenkel that replace it. Sets are "
              "built from nothing, numbered by Ackermann's coding and stacked in the cumulative hierarchy. "
              "Ordinals count past infinity to epsilon zero, where Goodstein's sequences climb beyond reach and "
              "still return to zero, and the hydra always dies. Then the alephs, the axiom of choice with Vitali's "
              "set and the doubled ball, and the turn: Gödel's constructible universe and Cohen's forcing show that "
              "the axioms can neither prove nor refute the continuum hypothesis. The part ends with large "
              "cardinals, the Price List of the continuum (realism, provability, new axioms), and what sets are for.",
        handoff="The diagonal returns as the halting problem and Gödel's incompleteness theorems in Part 7 and as "
                "the liar in Part 8; Goodstein's theorem and epsilon zero measure the strength of arithmetic in "
                "Part 7; what numbers are, after Benacerraf, is Part 9; infinite games return in Part 34, and the "
                "infinite in space and time in Part 25.",
        outside="Fractions, binary notation and the idea of a function; the logic of Parts 2 and 3 for the axioms.",
        objectives={
            "U": ["Decide whether two infinite collections have the same size by exhibiting a pairing, and count "
                  "the fractions.",
                  "Run the diagonal argument on a given list of rows and say exactly why the new row is not on "
                  "the list.",
                  "Derive Russell's paradox from the assumption that every condition defines a set."],
            "M": ["Prove Cantor's theorem for an arbitrary set, and show how separation turns Russell's paradox "
                  "into the theorem that there is no universal set.",
                  "Compute with ordinals in Cantor normal form, and attach falling ordinals to a Goodstein "
                  "sequence to prove that it reaches zero.",
                  "State the axiom of choice, and explain the paradoxical decomposition of the free group behind "
                  "Banach and Tarski's theorem."],
            "D": ["Outline both halves of the independence of the continuum hypothesis: Gödel's constructible "
                  "universe and Cohen's generic reals meeting dense sets.",
                  "Place inaccessible cardinals and determinacy on the ladder of consistency strength, and state "
                  "the positions of Gödel, Woodin, Hamkins and Feferman on whether the hypothesis has an answer."],
            "I": ["Encode pairs, numbers and finite sets as hereditarily finite sets, and say which 'junk "
                  "theorems' depend on the encoding.",
                  "Compare set theory with type theory and category theory as a foundation for a proof assistant."],
        },
        results=[
            ("Cantor's theorem", r"f:X\to\mathcal P(X)\ \Rightarrow\ \{x\in X:\ x\notin f(x)\}\notin f[X];"
                                 r"\qquad |X|<|\mathcal P(X)|"),
            ("Russell's paradox", r"R=\{x:\ x\notin x\}\ \Longrightarrow\ \bigl(R\in R\iff R\notin R\bigr)"),
            ("Sets from nothing", r"\operatorname{code}(s)=\sum_{x\in s}2^{\operatorname{code}(x)},\qquad "
                                  r"|V_{n+1}|=2^{|V_n|}"),
            ("Ordinal arithmetic", r"1+\omega=\omega<\omega+1,\qquad 2\cdot\omega=\omega<\omega\cdot 2"),
            ("Goodstein; Kirby and Paris", r"\text{every Goodstein sequence reaches } 0;\quad \mathrm{PA} "
                                           r"\text{ cannot prove it}"),
            ("The continuum", r"\mathrm{ZFC}\nvdash 2^{\aleph_0}=\aleph_1\quad\text{and}\quad "
                              r"\mathrm{ZFC}\nvdash 2^{\aleph_0}\ne\aleph_1"),
        ],
        U=(0, 1, 2, 3, 5, 10), D=(15, 16, 17), I=(18,),
        also=(("The Reasoner: sets.py", "explainer/philosophy/reasoner/sets.py"),),
    ),
]
