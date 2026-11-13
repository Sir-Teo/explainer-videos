"""Life, and Act V, The World: ontology, identity, possible worlds, God, laws and the arrow (Parts 19-24)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=19, level="U", widget="hamiltonkin", prereq=(16, 17),
        question="What is it to be alive, and how can selection with no designer build an eye or an altruist?",
        story="The part opens with Paley's watch and Hume's objection, then reads Darwin's argument as a comparison "
              "of likelihoods: design predicts nothing until the designer is specified. Lewontin's recipe "
              "(variation, heredity, differential fitness) is run as a breeder's equation and against drift, and "
              "fitness is defended as a propensity. The Price equation is derived and checked on 500 simulated "
              "birds, and the rest of the film is read off it: Fisher's fundamental theorem, Hamilton's rule for "
              "kin, and the multilevel decomposition in which altruists lose inside every group while their share "
              "rises overall. That decomposition is the turn: the mathematics privileges no level of selection, "
              "which is the Wall's nineteenth brick. The later chapters take the concepts biology leans on "
              "(function, species, information, cooperation) and end with the definitions of life tested against "
              "seven cases and a Lenia creature the Reasoner found itself.",
        handoff="Natural kinds and species as individuals return in Part 20, gliders and ships as persisting things "
                "in Part 21, and the design argument as fine-tuning in Part 23. Organization and minds return in "
                "Part 30, evolutionary games as the social contract in Part 34, and evolved cooperation as the "
                "premise of the debunking arguments in Part 37.",
        outside="School algebra, means and covariances. The likelihood comparisons use Part 16's vocabulary.",
        objectives={
            "U": ["State Lewontin's three conditions for selection and say which one fails in a given example.",
                  "Apply Hamilton's rule to siblings, half-siblings and cousins, and compute the hawk-dove "
                  "equilibrium V/C."],
            "M": ["Derive the Price equation and obtain Fisher's theorem and Hamilton's rule from it.",
                  "Test a strategy for evolutionary stability and trace replicator dynamics on the simplex."],
            "D": ["Decompose a change in a trait into between-group and within-group Price terms, and explain why "
                  "the decomposition alone does not settle the levels-of-selection debate.",
                  "Set out the etiological and causal-role accounts of function and what each says of Swampman."],
            "I": ["Simulate drift and selection in a Wright-Fisher population and compare fixation rates with "
                  "Kimura's formula.",
                  "Run a Lenia or Life pattern and say which definitions of life it meets and which it fails."],
        },
        results=[
            ("The Price equation", r"\bar w\,\Delta\bar z=\operatorname{Cov}(w_i,z_i)+\operatorname{E}(w_i\,\Delta z_i)"),
            ("Fisher's fundamental theorem (Price form)", r"\bar w\,\Delta\bar w=\operatorname{Var}(w)"
                                                           r"\quad\text{when } z=w \text{ and transmission is faithful}"),
            ("Hamilton's rule", r"\operatorname{Cov}(w,z)=p(1-p)(rb-c),\qquad\text{so altruism spreads iff } rb>c"),
            ("Replicator dynamics and the hawk-dove ESS", r"\dot x_i=x_i\bigl((Ax)_i-x^{\top}Ax\bigr),\qquad p^{*}=V/C\ \ (C>V)"),
            ("Multilevel selection", r"\bar w\,\Delta\bar z=\operatorname{Cov}_g(W_g,Z_g)+\operatorname{E}_g\bigl[\operatorname{Cov}_{i\in g}(w_i,z_i)\bigr]"),
            ("Tit for tat resists always-defect", r"w>\frac{T-R}{T-P}"),
        ],
        U=(0, 1, 2, 9, 11, 12), D=(6,), I=(13,),
        also=(("The Reasoner's evolution module", "explainer/philosophy/reasoner/evo.py"),),
    ),
    Part(
        n=20, level="U", widget="blockfusions", prereq=(3, 6),
        question="How many things are on a table, and who decides what counts as a thing?",
        story="Act V opens with Quine's 'On What There Is': Plato's beard, and ontological commitment read off the "
              "quantifiers of a regimented sentence. Meinong's golden mountain meets Russell's theory of "
              "descriptions, and the medieval dispute over universals is rerun on property tables, where Goodman's "
              "imperfect community and companionship defeat resemblance nominalism. Mereology is then built axiom "
              "by axiom: every partial order on up to six elements is tested, and the only finite models of the "
              "classical theory turn out to be Boolean algebras with the zero removed. The turn is van Inwagen's "
              "special composition question, counted on six blocks (6 objects, 40 or 63), and the Lewis-Sider "
              "argument that any answer between never and always makes existence vague: the Wall's twentieth "
              "brick. Metaontology, grounding and the question of a bottom level follow. The part ends with "
              "ontology as engineering: an ALC tableau reasoner, OntoClean on a taxonomy, and a knowledge-graph "
              "embedding that answers every question, nonsense included.",
        handoff="The statue and its clay, and persistence, return in Part 21; possible worlds and counterparts in "
                "Part 22; whether spacetime is a thing in Part 25; entanglement and monism in Part 26; descriptions "
                "and reference in Part 27; grounding the mental in Parts 30 and 31.",
        outside="First-order quantifiers (Part 3) and the idea of a partial order. Nothing else.",
        objectives={
            "U": ["Regiment an English sentence in first-order logic and read off what it commits its speaker to.",
                  "Count the objects among a few blocks on the nihilist, contact and universalist answers."],
            "M": ["Evaluate 'the present King of France is not bald' on both scopes in a model.",
                  "Check weak supplementation, strong supplementation and unrestricted fusion on a small partial "
                  "order, and find Goodman's imperfect community in a property table."],
            "D": ["Prove that a finite model of classical extensional mereology with k atoms has exactly 2^k - 1 "
                  "elements.",
                  "Reconstruct the Lewis-Sider argument from vagueness and say which premise each moderate answer "
                  "to the composition question must give up.",
                  "Verify that a grounding relation is a strict partial order and unfold Fine's rules of ground "
                  "for a truth-functional sentence."],
            "I": ["Decide a subsumption in ALC by tableau, and read a counter-model off an open branch.",
                  "Apply OntoClean's rigidity and identity constraints to a taxonomy and name the errors."],
        },
        results=[
            ("Quine's criterion", r"\text{a theory is committed to those things its bound variables must range "
                                  r"over for it to be true}"),
            ("Russell: the F is G", r"\exists x\,\bigl(Fx\wedge\forall y\,(Fy\to y=x)\wedge Gx\bigr)"),
            ("Strong supplementation", r"y\not\le x\ \to\ \exists z\,\bigl(z\le y\wedge\neg O(z,x)\bigr),"
                                       r"\qquad O(z,x):=\exists u\,(u\le z\wedge u\le x)"),
            ("Finite models of classical mereology", r"M\cong\mathcal P(A)\setminus\{\varnothing\},\qquad |M|=2^{k}-1"
                                                     r"\quad\text{for } k \text{ atoms}"),
            ("Six blocks, three answers", r"\text{nihilism } 6,\qquad\text{contact } 40,\qquad"
                                          r"\text{universalism } 2^{6}-1=63"),
            ("Subsumption by tableau", r"C\sqsubseteq_{\mathcal T}D\iff C\sqcap\neg D\ \text{is unsatisfiable "
                                       r"with respect to }\mathcal T"),
        ],
        U=(0, 1, 2, 3, 7), D=(8, 11, 12), I=(13, 14, 15),
        also=(("The Reasoner's mereology module", "explainer/philosophy/reasoner/mereo.py"),
              ("The Reasoner's description logic", "explainer/philosophy/reasoner/dl.py")),
    ),
    Part(
        n=21, level="U", widget="parfitfade", prereq=(3, 4, 20),
        question="What makes a ship, or a person, the same one after every part of it has changed?",
        story="Three puzzles open the part: a ship rebuilt plank by plank, a teleporter, and a girl who becomes an "
              "old woman. Identity is fixed first, by two axioms (reflexivity and Leibniz's law) from which "
              "symmetry and transitivity follow, and tested on Black's spheres, where the Reasoner finds the two "
              "spheres weakly discernible. The statue and the lump, the ship of Theseus with Hobbes's second ship, "
              "and relative identity show the logic under strain; Evans's one-page proof that identity cannot be "
              "vague is model-checked and found to need rigid names. Persistence is drawn as spacetime worms, and "
              "personal identity starts from Locke's memory criterion, which Reid's brave officer breaks: memory "
              "is not transitive, though its ancestral is. Parfit's connectedness fades over a simulated life while "
              "continuity holds, and fission then gives one person two continuers: identity cannot be what "
              "matters, the Wall's twenty-first brick. The part ends with animalism, the Buddhist chariot, and "
              "minds that can be copied.",
        handoff="Counterparts and essences return in Part 22, survival after death in Part 23, identical particles "
                "in Part 26, rigid names in Part 27, minds and copies in Parts 30 and 31, and future people and "
                "the self in Part 36.",
        outside="Nothing beyond the first-order logic of Part 3; the necessity of identity uses Part 4's box.",
        objectives={
            "U": ["Tell numerical from qualitative identity and derive symmetry and transitivity from reflexivity "
                  "and Leibniz's law.",
                  "Show with Reid's officer that remembering is not transitive, and repair Locke's criterion with "
                  "the ancestral of memory.",
                  "Say what each view of the ship of Theseus counts as the original ship, and at what cost."],
            "M": ["Distinguish connectedness from continuity and compute both on a chain of memory links.",
                  "Set out the fission case as an inconsistent set and name what each exit gives up."],
            "D": ["Reconstruct Evans's argument, locate the abstraction step, and build a model with non-rigid "
                  "names in which identity statements are indeterminate.",
                  "Classify a pair of objects in a finite structure as absolutely, relatively or weakly "
                  "discernible."],
            "I": ["Explain the difference between identity and equality of records in a program or a database, "
                  "and what record linkage has to assume.",
                  "Separate what transfers from the personal-identity debate to copied model weights from what is "
                  "only analogy."],
        },
        results=[
            ("The logic of identity", r"\forall x\,(x=x),\qquad x=y\to\bigl(\varphi(x)\leftrightarrow\varphi(y)\bigr)"),
            ("The necessity of identity", r"x=y\ \to\ \Box\,(x=y)"),
            ("The identity of indiscernibles (the contested converse)", r"\forall F\,(Fx\leftrightarrow Fy)\ \to\ x=y"),
            ("Evans: no vague identity between rigidly named things", r"\nabla(a=b)\ \vdash\ \lambda x[\nabla(x=a)]\,b,"
                                                                     r"\quad \neg\lambda x[\nabla(x=a)]\,a,\quad\text{so } a\ne b"),
            ("Reid's officer", r"M(g,o)\wedge M(o,b)\wedge\neg M(g,b):\quad M \text{ is not transitive, its ancestral } M^{+} \text{ is}"),
            ("Fission", r"C(o,l)\wedge C(o,r)\wedge l\ne r\ \Rightarrow\ \text{continuity } C \text{ is not identity}"),
        ],
        U=(0, 1, 4, 9, 10, 11, 13), D=(2, 6), I=(14,),
        also=(("The Reasoner's persistence module", "explainer/philosophy/reasoner/persist.py"),),
    ),
    Part(
        n=22, level="U", widget="twodmatrix", prereq=(3, 4, 21),
        question="When we say things could have been otherwise, what are we talking about?",
        story="Part 4 gave possible worlds as a semantics; this part asks what they are. It starts with the "
              "difference between necessity de dicto and de re, Quine's mathematical cyclist evaluated on a model, "
              "and Kripke's answer: names are rigid, so the name tracks Aristotle across four worlds while the "
              "description tracks whoever taught Alexander. Rigid names make 'Hesperus is Phosphorus' necessary "
              "though known only by observation, and the standard metre contingent though known a priori. Lewis's "
              "concrete worlds and his counterpart theory are then built: the 1968 translation into first-order "
              "logic is checked against the direct semantics, and a census of small models shows the necessity of "
              "identity failing where Kripke's semantics keeps it. Ersatz worlds, alien properties and the Barcan "
              "formula follow. The turn is the two-dimensional matrix: the a priori is its diagonal, the necessary "
              "its actual row, so conceivability is no simple guide to possibility, which is the Wall's "
              "twenty-second brick. The part ends with Pierre's puzzle, Fine's essences, impossible worlds, "
              "dispositions, and possible worlds at work in counterfactual explanations and probabilistic programs.",
        handoff="The modal ontological argument uses these frames in Part 23; necessary laws and chance return in "
                "Part 24, Everett's branching worlds in Part 26, names and meaning in Parts 27 and 28, "
                "conceivability and zombies in Parts 30 and 31, and counterfactual fairness in Part 41.",
        outside="Nothing beyond Part 4's box and diamond and Part 3's quantifiers.",
        objectives={
            "U": ["Separate the de dicto from the de re reading of a modal sentence and evaluate each on a small "
                  "model.",
                  "Explain with Kripke's modal argument why a name is not short for a description.",
                  "Give an example of a necessary truth known only by experience and say why it is necessary."],
            "M": ["Fill the two-dimensional matrix of an identity sentence and classify it by its diagonal and its "
                  "actual row.",
                  "Evaluate a counterfactual by closest worlds, and a disposition claim against a fink and a mask."],
            "D": ["Translate a quantified modal sentence into counterpart theory and build a counterpart model in "
                  "which the necessity of identity fails.",
                  "State the Barcan formula, give a varying-domain countermodel, and say what necessitism and "
                  "contingentism each make of it.",
                  "Use impossible worlds to give a counterpossible a non-vacuous truth value."],
            "I": ["Find the closest worlds that flip a classifier's decision and explain why ties matter for "
                  "recourse.",
                  "Compute the probability of a query in a small ProbLog program by summing over possible worlds."],
        },
        results=[
            ("De dicto and de re", r"\Box\,\exists x\,Fx\qquad\text{against}\qquad\exists x\,\Box Fx"),
            ("Rigid names: the necessary a posteriori", r"a=b\ \to\ \Box\,(a=b)\qquad\text{for rigid } a,\,b"),
            ("Lewis's translation of possibility", r"\bigl(\Diamond\varphi(x)\bigr)^{w}=\exists v\,\exists y\,"
                                                   r"\bigl(Wv\wedge Iyv\wedge Cyx\wedge\varphi^{v}(y)\bigr)"),
            ("The Barcan formula", r"\forall x\,\Box Fx\ \to\ \Box\,\forall x\,Fx"),
            ("Two dimensions", r"S \text{ is necessary} \iff \forall v\ [\![S]\!](@,v)=1,\qquad "
                               r"S \text{ is a priori} \iff \forall w\ [\![S]\!](w,w)=1"),
            ("The distribution semantics", r"P(q)=\sum_{w\,\models\,q}\ \prod_{f\in w}p_f\prod_{f\notin w}(1-p_f)"),
        ],
        U=(0, 1, 2, 3, 4, 8), D=(5, 7, 12), I=(14,),
        also=(("The Reasoner's worlds module", "explainer/philosophy/reasoner/worlds.py"),),
    ),
    Part(
        n=23, level="U", widget="miraclewitness", prereq=(2, 4, 13, 22),
        question="Can an argument, checked line by line, establish that God exists or that God does not?",
        story="The part asks what a proof of God would need (valid, sound, not too strong, reaching the right God) "
              "and then checks each family of argument. Anselm's reductio is valid, and Gaunilo's island and Kant's "
              "thalers attack its premises. Plantinga's modal argument is valid on every S5 frame with up to three "
              "worlds, and so is its mirror image from 'possibly there is no God'. The turn is Gödel's proof, "
              "formalized in a finite higher-order modal logic: his own axioms have no model, and every model of "
              "Scott's repaired axioms has a single world, the modal collapse that is the Wall's twenty-third "
              "brick. The cosmological arguments follow, with a countermodel to Aquinas's third way and van "
              "Inwagen's collapse of the principle of sufficient reason; then fine-tuning with and without a "
              "multiverse, Pascal's wager undone by mixed strategies, and the problem of evil as a logical and then "
              "a Bayesian argument. Hume's maxim on miracles is computed against the number of independent "
              "witnesses, the sea battle is settled two ways in branching time, and the part ends with arguments "
              "from Udayana, Dharmakīrti and Avicenna.",
        handoff="The beginning of the universe and the arrow of time return in Parts 24 and 25, fatalism and "
                "freedom in Part 32, decisions with infinite stakes in Part 33, whether morality needs God in "
                "Parts 35 and 37, and value over the very long future in Parts 36 and 42.",
        outside="Bayes's rule (Part 13) and the modal systems of Part 4. No theology is assumed.",
        objectives={
            "U": ["Lay out Anselm's argument as a reductio and say which premise Gaunilo and Kant each reject.",
                  "Compute how many independent witnesses it takes to make a one-in-a-million event more probable "
                  "than not, and say why the independence matters.",
                  "State Mackie's inconsistent set and show how the free-will defence makes it consistent."],
            "M": ["Check Plantinga's argument and its mirror image on a small frame, and find a reflexive frame "
                  "on which the argument fails.",
                  "Compare the fine-tuning likelihoods for design, chance and a multiverse on the evidence that "
                  "some universe permits life and on the evidence that this one does."],
            "D": ["Derive modal collapse from Scott's axioms and explain why Gödel's original definition of "
                  "essence makes his axioms inconsistent.",
                  "Reconstruct van Inwagen's argument that the principle of sufficient reason leaves no contingent "
                  "truths, and assess Pruss's and Della Rocca's replies.",
                  "Evaluate future contingents in Prior's Peircean and Ockhamist semantics."],
            "I": ["Apply the likelihood form of Bayes's rule to testimony, with witnesses who may be copying one "
                  "another.",
                  "Recognise the inverse gambler's fallacy in an argument from a selection effect."],
        },
        results=[
            ("The modal ontological argument and its mirror", r"\Diamond\Box g\ \vdash_{\mathrm{S5}}\ \Box g,\qquad"
                                                              r"\Diamond\neg g\ \vdash_{\mathrm{S5}}\ \neg\Diamond\Box g"),
            ("Modal collapse (Sobel)", r"\text{Scott's axioms}\ \vdash\ \varphi\to\Box\varphi"),
            ("Fine-tuning as a likelihood ratio", r"\frac{P(E\mid\text{design})}{P(E\mid\text{chance})}=\frac{q}{\varepsilon}"
                                                  r"=\frac{0.5}{0.001}=500,\qquad P(E_{\text{this}}\mid\text{multiverse})=\varepsilon"),
            ("The wager with mixed strategies (Hájek)", r"\operatorname{EU}(\text{wager with probability } r)=\infty"
                                                        r"\quad\text{for every } r>0"),
            ("Miracles and k independent witnesses", r"P(M\mid k\text{ reports})=\frac{\pi h^{k}}{\pi h^{k}+(1-\pi)f^{k}}"),
            ("The sea battle, Peircean", r"F(p\vee\neg p)\ \text{is true, while}\ Fp\vee F\neg p\ \text{is not}"),
        ],
        U=(0, 1, 4, 7, 8, 9, 11), D=(3, 5, 12),
        also=(("The Reasoner's theism module", "explainer/philosophy/reasoner/theism.py"),),
    ),
    Part(
        n=24, level="U", widget="kacring", prereq=(13, 15, 22),
        question="What is a law of nature, and why does time run one way if the laws run both?",
        story="A film of colliding molecules looks the same run backwards, a film of milk mixing into coffee does "
              "not: the part asks what holds the world together. Laws come first: the regularity view and van "
              "Fraassen's two spheres, then Lewis's best system built as a contest of polynomial laws scored in "
              "bits on a falling ball, and the rival views on which laws govern. Humean chance is tested in a world "
              "of twenty coin tosses, where undermining futures carry 75% of the chance and the Principal Principle "
              "contradicts itself until the New Principle repairs it. Determinism is defined by models and broken "
              "by Norton's dome; chaos shows a deterministic system that cannot be forecast. Then the arrow: "
              "Boltzmann's counting, the H-theorem, and the objections of Loschmidt and Zermelo, all made visible "
              "in the Kac ring, which decays, recurs, reverses, and from a typical low-entropy present gains "
              "entropy toward the past as well as the future. That is the Wall's twenty-fourth brick, and the Past "
              "Hypothesis is the price of the arrow. The part ends with Maxwell's demon, Szilard's engine, "
              "Landauer's bound and reversible computing.",
        handoff="The block universe and whether time passes follow in Part 25, quantum chance and probability in a "
                "branching universe in Part 26, information and the mind in Part 30, determinism and free will in "
                "Part 32, and chance in decisions in Part 33.",
        outside="Newton's second law, logarithms and binomial counting. Part 13's credences are used for chance.",
        objectives={
            "U": ["Tell a law from an accidental regularity with van Fraassen's two spheres, and say what the "
                  "best-system account adds.",
                  "Explain with a counting argument why a gas spreads out, and why that argument alone points the "
                  "same way into the past.",
                  "Distinguish unpredictability from indeterminism using the Lorenz system and Norton's dome."],
            "M": ["Score candidate laws by two-part description length and pick the best system.",
                  "Derive the decay of the Kac ring's colour imbalance under the molecular-chaos assumption and "
                  "show where recurrence refutes it.",
                  "Compute the expected work of a Szilard engine and the erasure cost that cancels it."],
            "D": ["Derive the big bad bug from the Principal Principle in a finite Humean world and show how the "
                  "New Principle removes it.",
                  "Verify Norton's solutions of the dome and identify the Lipschitz condition whose failure "
                  "allows them."],
            "I": ["Estimate a forecast horizon from a Lyapunov exponent and an initial error.",
                  "Compute the Landauer cost of an irreversible gate and say how compute, copy and uncompute "
                  "avoids it."],
        },
        results=[
            ("The Principal Principle and the New Principle", r"Cr\bigl(A\mid \mathrm{ch}(A)=x\wedge E\bigr)=x,\qquad "
                                                              r"Cr(A\mid H\wedge T)=\mathrm{ch}(A\mid T)"),
            ("Norton's dome", r"\ddot r=\sqrt r,\qquad r(t)=\tfrac{1}{144}(t-T)^{4}\ (t\ge T),\quad r(t)=0\ (t\le T),"
                              r"\quad\text{for every } T\ge 0"),
            ("Sensitive dependence (Lorenz)", r"|\delta(t)|\approx|\delta(0)|\,e^{\lambda t},\qquad\lambda\approx 0.90"),
            ("Boltzmann's entropy", r"S=k\log W"),
            ("The Kac ring", r"\delta(t)\approx(1-2\mu)^{t}\ \text{for } t\ll N,\qquad \delta(N)=(-1)^{m}\delta(0),"
                             r"\qquad\delta(2N)=\delta(0)"),
            ("Szilard and Landauer", r"\langle W\rangle=kT\,H(x)\le kT\ln 2,\qquad E_{\text{erase}}\ge kT\ln 2"
                                     r"\ \text{per bit}"),
        ],
        U=(0, 1, 5, 7, 8, 12), D=(4, 6), I=(13,),
        also=(("The Reasoner's laws module", "explainer/philosophy/reasoner/physlaws.py"),),
    ),
]
