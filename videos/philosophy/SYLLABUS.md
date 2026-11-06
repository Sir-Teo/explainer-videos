# Philosophy, Built: the syllabus (plan of record, draft 1)

Goal: a university course in video, from first-year introduction to doctoral qualifying level, with the bridges to
industry. It aims to be **as comprehensive as the textbooks and as technical as the subject allows**, and it is told
as one story, *Calculemus* ([README](README.md)). It will be made in English and Chinese to the standard of *AI,
Built* and *Analysis, Built*. Each part runs **50–60 minutes**. Forty-two parts come to about 38 hours.

## 1. The standard every part meets

**A part is one story.** It opens with a question that a person off the street would ask, such as "do you know you
are not dreaming?" It then:

1. sharpens the question until it can be calculated;
2. builds the toy that calculates it;
3. reaches the wall (the theorem, paradox or dilemma where calculation stops);
4. lays out the price list (the positions, and what each one gives up);
5. closes with the frontier and the industry problem the question became, and sets up the next part.

**A chapter is a lecture segment of 3–4 minutes,** with 16–20 chapters per part. It runs in this order:

1. A motivating puzzle, thought experiment or historical moment, drawn: Theseus's ship, Mary's room, the trolley,
   Newcomb's boxes.
2. A definition card, in words and then in symbols.
3. The argument formalized on screen, step by step, each step with a margin reason ("rule β", "Leibniz's law",
   "conditionalization", "Jensen").
4. A computed experiment with the part's toy, which checks, refutes or measures the claim.
5. A *pause-and-predict* question or a worked example.
6. The takeaway, with a forward link (a payoff card).

**Per part:**
- An objectives card, plus theorem, definition, argument and history cards.
- One or more **Price List** puzzles, each with its inconsistent set, its minimal correction sets computed by the
  Reasoner, the holders of each position, and PhilPapers 2020 shares where the survey asked.
- One row of **the Wall**.
- A problem set: 5–6 problems, about 90 s on screen, with full solutions in the part's README in English and
  Chinese. The problems mix proofs, formalizations, toy computations and short essay prompts.
- A reference card listing the textbooks, the classic papers, the frontier papers, and the SEP entries.

**The history thread.** Every idea is credited with its people and year, and every part opens with its era (2–3
min) lit on the timeline strip. The non-Western traditions are part of the main argument wherever they contributed
to the question, and are never set apart in an appendix:
- Mohist logic and the School of Names in Parts 1 and 27;
- Nyāya inference and Dignāga's wheel of reasons in Part 15;
- the catuṣkoṭi and Jaina saptabhaṅgī in Part 5;
- Zhuangzi's butterfly in Part 11;
- Buddhist anattā and the chariot in Part 21;
- al-Ghazālī on causation in Part 17;
- Avicenna's floating man in Part 30;
- Mencius and Xunzi on human nature in Part 37;
- Confucian virtue in Part 35;
- the Yijing and Leibniz's binary in Part 1.

**Fair to every side.** Each position is given its best defense, ideally in its defenders' own words (quoted, cited).
The narration says plainly when a question is open, when a "refutation" is disputed, and when an analogy (labeled
`analogy`) is only an analogy. The narration takes no side on open normative questions. It does state the theorems.

**Numbers and claims.**
- Computed numbers come from the part's `compute.py`, cached under `.cache/philosophyN/`. The narration that states
  a result is an f-string over the cached data, and branches on it when the story depends on the outcome.
- Published numbers (survey shares, experimental results such as the 2015 loophole-free Bell tests, replication
  rates, the Moral Machine data) are cited on screen.
- Quotations are checked against a primary edition or a standard translation, and the translation is named.
- `assert`s in `compute.py` are for invariants only: the SAT solver agrees with truth tables, and the tableau prover
  agrees with model enumeration on small cases.
- CPU budget: at most 1 h per part by default. Most toys are exact and fast. The named exceptions (Part 15's
  Solomonoff mixture, Part 31's Φ sweeps, Part 34's tournaments, Part 26's Bohmian ensembles) get up to 6 h, are
  resumable, and are seeded.

**Frontier sweep.** Before a part is written, its literature is checked up to the writing date: the SEP entry and its
bibliography, PhilPapers, arXiv (for the formal parts), and the leading journals (*Mind*, *Noûs*, *Phil Review*,
*JPhil*, *PPR*, *Phil Studies*, *JPL*, *RSL*, *BJPS*, *Phil Sci*, *Ethics*, *PPA*, *Synthese*, *Erkenntnis*). Any
result newer than mid-2026 is verified against its primary source before it goes on screen.

**Visual standard** (3Blue1Brown manner). The base is the AI series' `viz.py`: continuity over cuts, in-place
derivations, colour as meaning, a narrating camera, and live quantities. The new instruments are below.

| Instrument | What it shows |
|---|---|
| `ArgumentMap` | premises flowing into a conclusion. Each inference edge lights green (valid) or red (invalid, with the countermodel opening beside it), and an attacked premise cracks. |
| `PriceList` | an inconsistent set as a ring of claims. Each minimal correction set rotates into the light as a position, with its philosophers and survey bar. |
| `WorldGraph` | Kripke models: worlds as glowing nodes, accessibility as arrows, and valuations as coloured facets. Updates cut worlds away (muddy children), and bisimulations pair nodes. |
| `SpheresView` | Lewis and Grove sphere systems, nested around a world. Counterfactuals and revisions find the closest antecedent world. |
| `Simplex` | the probability simplex in 2D and 3D: credences as points, Dutch-book separating planes, Brier projections, replicator flows, the Machina triangle with indifference lines. |
| `TruthTable` / `ProofTree` / `Tableau` | truth tables that fill column by column, natural-deduction trees that grow, tableaux that branch and close with ✗. |
| `Lattice` | Hasse diagrams (FOUR, bilattices, mereological sums, the Lindenbaum algebra), with joins and meets as animated paths. |
| `CausalDAG` | structural models. Interventions cut arrows with scissors, and back-door paths light up. |
| `SpacetimeView` | Minkowski diagrams with tilting simultaneity slices, worldtubes for persistence, and branching worms for fission and many worlds. |
| `Tournament` | strategy zoos playing round-robin, with a population share river (stacked areas) over generations. |
| `VoteLab` | ballots as coloured permutations, the Condorcet cycle as a rotating triangle, the pivotal-voter sweep. |
| `ParfitBars` | populations as rectangles, width as population and height as welfare, sliding toward the repugnant conclusion. |
| 3D camera tours | ordinal towers to ε₀, the cumulative hierarchy V as a widening cone, the Bloch sphere, the 3-simplex of credences. |

**Bilingual standard (as *AI, Built*).**
- Every narration line has its `narration_zh.json` entry, and each part has a `zh_lines.py` for computed lines.
- Every on-screen string is in `philosophy_text_zh.json`, and `tools/collect_text.py --check philosophyN` is clean.
- `PHILOSOPHY_ZH_GUIDE.md` is the glossary. It uses standard Chinese philosophical terms, such as 先验/超验 for
  *transcendental*/*transcendent* (following 李秋零's Kant), 意向性 for *intentionality*, 随附性 for
  *supervenience*, and 可能世界 for *possible world*. For classical Chinese texts we quote the original and gloss it.

**Gates per part:** `tools/lecture_length.py` (50–60 min), `contact_sheet.py`, `dead_air.py`, `collect_text.py
--check`, `check_narration.py`, and the Reasoner's own test suite (`tests/philosophy/`).

## 2. The canon: what the course follows

The degree reads like the standard reading lists of a strong undergraduate and doctoral program. Each part's
reference card names its own sources; these are the spines.

**Logic and foundations:**
- Enderton, *A Mathematical Introduction to Logic*;
- Boolos, Burgess and Jeffrey, *Computability and Logic*;
- Sider, *Logic for Philosophy*;
- Priest, *An Introduction to Non-Classical Logic*;
- Hughes and Cresswell, *A New Introduction to Modal Logic*;
- Blackburn, de Rijke and Venema, *Modal Logic*;
- van Dalen, *Logic and Structure*;
- Smith, *An Introduction to Gödel's Theorems*;
- Kunen, *Set Theory*;
- Shapiro, *Thinking about Mathematics*;
- Linnebo, *Philosophy of Mathematics*;
- Hamkins, *Lectures on the Philosophy of Mathematics*;
- Beall and Restall, *Logical Pluralism*.

**Epistemology:**
- Pritchard, *What Is This Thing Called Knowledge?*;
- Williamson, *Knowledge and Its Limits*;
- Fagin, Halpern, Moses and Vardi, *Reasoning About Knowledge*;
- van Ditmarsch, van der Hoek and Kooi, *Dynamic Epistemic Logic*;
- Titelbaum, *Fundamentals of Bayesian Epistemology*;
- Pettigrew, *Accuracy and the Laws of Credence*;
- Halpern, *Reasoning about Uncertainty*;
- Gärdenfors, *Knowledge in Flux*;
- Goldman and O'Connor (SEP), *Social Epistemology*.

**Science:**
- Godfrey-Smith, *Theory and Reality*;
- Curd, Cover and Pincock (eds.), *Philosophy of Science: The Central Issues*;
- Howson and Urbach, *Scientific Reasoning*;
- Earman, *Bayes or Bust?*;
- Kelly, *The Logic of Reliable Inquiry*;
- Pearl, *Causality*;
- Spirtes, Glymour and Scheines, *Causation, Prediction, and Search*;
- Woodward, *Making Things Happen*;
- Mayo, *Statistical Inference as Severe Testing*;
- Sober, *Philosophy of Biology*;
- Okasha, *Evolution and the Levels of Selection*.

**Metaphysics and physics:**
- Loux and Crisp, *Metaphysics: A Contemporary Introduction*;
- van Inwagen, *Metaphysics*;
- Sider, *Writing the Book of the World*;
- Lewis, *On the Plurality of Worlds* and *Counterfactuals*;
- Kripke, *Naming and Necessity*;
- Williamson, *Modal Logic as Metaphysics*;
- Paul and Hall, *Causation: A User's Guide*;
- Maudlin, *Philosophy of Physics: Space and Time* and *Quantum Theory*;
- Albert, *Quantum Mechanics and Experience* and *Time and Chance*;
- Earman, *A Primer on Determinism* and *World Enough and Space-Time*;
- Bell, *Speakable and Unspeakable*;
- Wallace, *The Emergent Multiverse*;
- Oppy, *Arguing about Gods*.

**Language and mind:**
- Lycan, *Philosophy of Language*;
- Heim and Kratzer, *Semantics in Generative Grammar*;
- Gamut, *Logic, Language, and Meaning*;
- Lewis, *Convention*;
- Skyrms, *Signals*;
- Kim, *Philosophy of Mind*;
- Chalmers, *The Conscious Mind*;
- Dennett, *Consciousness Explained*;
- Seth, *Being You*;
- Clark, *Surfing Uncertainty*;
- Moran, *Introduction to Phenomenology*;
- Dreyfus, *What Computers Still Can't Do*;
- Kane (ed.), *The Oxford Handbook of Free Will*.

**Value:**
- Peterson, *An Introduction to Decision Theory*;
- Joyce, *The Foundations of Causal Decision Theory*;
- Buchak, *Risk and Rationality*;
- Osborne and Rubinstein, *A Course in Game Theory*;
- Skyrms, *Evolution of the Social Contract*;
- Kagan, *Normative Ethics*;
- Shafer-Landau, *The Fundamentals of Ethics*;
- Parfit, *Reasons and Persons*;
- Broome, *Weighing Goods*;
- MacAskill, Bykvist and Ord, *Moral Uncertainty*;
- Miller, *Contemporary Metaethics*;
- Kymlicka, *Contemporary Political Philosophy*;
- Rawls, *A Theory of Justice*;
- Sen, *Collective Choice and Social Welfare*;
- Gaertner, *A Primer in Social Choice Theory*;
- Brandt et al. (eds.), *Handbook of Computational Social Choice*;
- List and Pettit, *Group Agency*;
- Gaut and Lopes (eds.), *The Routledge Companion to Aesthetics*.

**History:**
- Kenny, *A New History of Western Philosophy*;
- Copleston, *A History of Philosophy*;
- 冯友兰, 《中国哲学简史》;
- Graham, *Disputers of the Tao*;
- Ganeri, *Indian Logic: A Reader*;
- Matilal, *The Character of Logic in India*;
- Garfield, *The Fundamental Wisdom of the Middle Way*;
- Adamson, *A History of Philosophy without Any Gaps*.

**Industry and AI:**
- Russell and Norvig, *Artificial Intelligence: A Modern Approach*;
- Barocas, Hardt and Narayanan, *Fairness and Machine Learning*;
- Dwork and Roth, *The Algorithmic Foundations of Differential Privacy*;
- Russell, *Human Compatible*;
- Baier and Katoen, *Principles of Model Checking*;
- Baader et al., *The Description Logic Handbook*;
- Nisan et al., *Algorithmic Game Theory*.

## 3. Part by part

Length targets are estimates, and the content decides. *Built* lists the toys (Reasoner modules) a part adds.
*Wall* is its row of the impossibility ledger. *Price List* names its inconsistent sets. *Frontier and industry* lists
the open research and the places where the question is now engineering.

### Prologue

#### Part 1 · Calculemus (~55 min): what an argument is, and the dream of calculating it
1. Cold open: Leibniz, 1685, "calculemus"; and a dispute settled by a computer on screen.
2. The Axial Age: Thales, Confucius, the Buddha, Socrates, and the move from myth to argument. This chapter has
   the timeline strip's first lights.
3. Arguments: premises, conclusion, validity, soundness; form vs content. The first `ArgumentMap`.
4. Parmenides and Zeno: the dichotomy and Achilles. The sum Σ2⁻ⁿ = 1 resolves the arithmetic; the supertask
   question it leaves (Thomson's lamp) does not resolve.
5. Socrates' elenchus: get an interlocutor to accept p₁ … pₙ, then show that they are jointly inconsistent. The
   *Euthyphro* dilemma is shown as an inconsistent set. This is the first Price List.
6. Plato's *Meno*: the slave boy doubles the square (the √2 diagonal, drawn). Meno's paradox of inquiry, and
   recollection as Plato's answer.
7. Plato's divided line and the cave, as a picture of levels of knowledge.
8. Aristotle's syllogistic: the four forms A, E, I, O and the square of opposition. Existential import is the
   modern fix (shown as Venn diagrams).
9. The 256 moods: we enumerate them all and find the 24 valid ones (15 unconditionally valid, plus 9 with
   existential import), checked by Venn regions and by brute-force models.
10. Stoic and Mohist logic: Chrysippus's five indemonstrables; the Mohist canons and the School of Names ("a white
    horse is not a horse", read as identity vs predication).
11. Indian logic's five-membered inference (Nyāya): thesis, reason, example, application, conclusion.
12. Ramon Llull's *Ars Magna* (1305): concentric wheels generating every combination. Built as rotating circles.
13. Leibniz's characteristic numbers (1679): concepts as primes. With *man* = 6 = 2 × 3 (*animal* × *rational*),
    "every A is B" becomes "B divides A". Built and tested on all the valid moods, with the cases where it fails.
14. Leibniz and the Yijing (1703): the Fuxi ordering of the hexagrams read as binary 0–63.
15. Why the dream needed two thousand more years: what Aristotle's logic cannot express (relations, "every horse's
    head is an animal's head", De Morgan's challenge).
16. The plan of the series: the Reasoner, the Wall, the Price List; the series map.
17. Recap and Problems.

*Built:* the syllogism engine (all 256 moods, exactly); Llull's wheels; Leibniz's prime encoding; the first Price
List (*Euthyphro*).
*Wall:* Zeno and the supertask problem. Meno's paradox, dissolved only by an account of inquiry.
*Visuals:* Achilles's gap shrinking on a zooming number line; the square of opposition rotating into Venn regions;
Llull's wheels turning; 64 hexagrams flipping into binary.
*References:* Kenny vol. 1; Plato *Euthyphro*, *Meno*, *Republic* VI–VII; Aristotle *Prior Analytics*; Łukasiewicz,
*Aristotle's Syllogistic*; Graham, *Later Mohist Logic*; Ganeri; Leibniz, *Elements of a Calculus* (1679),
*Explication de l'arithmétique binaire* (1703).

### Act I · The Machinery of Reason

#### Part 2 · The Laws of Thought (~55): propositional logic and SAT
1. Boole's *Laws of Thought* (1854): algebra of classes, x² = x.
2. Syntax: formulas as trees; connectives; truth functions. Every n-ary function is expressible, and Post's
   functional completeness theorem says which sets of connectives suffice ({NAND} does).
3. Semantics: valuations; tautology, satisfiability, consequence ⊨. Truth tables filled live.
4. Normal forms: CNF and DNF, with Tseitin's linear-size transformation.
5. Natural deduction (Gentzen 1935): introduction and elimination rules; proof trees for contraposition and
   Peirce's law.
6. Soundness, proved by induction on proofs.
7. Completeness via maximal consistent sets (Lindenbaum's lemma).
8. Compactness as a corollary; it returns in Parts 3 and 6.
9. Resolution (Robinson 1965), with refutation completeness sketched.
10. DPLL and CDCL: unit propagation, clause learning, the implication graph. Built and run live.
11. Cook–Levin: SAT is NP-complete. The cost of calculation (the Wall).
12. Pigeonhole formulas need exponential-size resolution proofs (Haken 1985); measured with our solver.
13. Industry: SAT/SMT at work, including hardware verification, AWS Zelkova (verifying access policies), package
    managers, and the Boolean Pythagorean triples proof (Heule, Kullmann and Marek 2016; a 200 TB certificate).
14. The elenchus as SAT: minimal unsatisfiable subsets (MUS) and minimal correction sets (MCS), with their hitting-set
    duality proved. This is **the Price List engine**.
15. First full Price List: the problem of evil as an inconsistent quartet (God is omnipotent, omniscient and wholly
    good; there is evil). The MCSs are the positions; Part 23 returns to it.
16. What propositional logic can't say (quantifiers), leading to Part 3.
17. Recap and Problems.

*Built:* `reasoner.prop` (parser, truth tables, a natural-deduction checker, Tseitin, DPLL/CDCL, MUS/MCS
enumeration via MARCO). Tested against brute force.
*Wall:* NP-completeness; exponential lower bounds for resolution.
*Visuals:* the formula tree evaluating bottom-up; CDCL's implication graph with a learned clause cutting it; the
MUS/MCS hitting-set duality as a bipartite light-up.
*References:* Enderton ch. 1; van Dalen chs. 1–2; Sider ch. 2; Biere et al., *Handbook of Satisfiability*;
Liffiton and Sakallah 2008.

#### Part 3 · All and Some (~55): first-order logic
1. Frege's *Begriffsschrift* (1879), drawn in Frege's own two-dimensional notation and then translated.
2. Syntax: terms, formulas, free and bound variables, substitution and capture.
3. Tarski's semantics (1933): structures, assignments, satisfaction. A finite structure is evaluated live.
4. Expressive power: "there are at least n", relations, definite descriptions (Russell 1905, previewing Part 27).
5. Proof: the sequent calculus; cut elimination (sketch); the subformula property.
6. The completeness theorem (Gödel 1929), by Henkin's construction step by step: witnesses and the term model.
7. Compactness, and its surprises: non-standard models of arithmetic (an infinite element beyond every n).
8. Löwenheim–Skolem: countable models; Skolem's paradox (a countable model of "there are uncountable sets").
9. Undecidability: Church and Turing 1936 (full proof in Part 7); semi-decidability; decidable fragments (monadic,
   Bernays–Schönfinkel).
10. Tableau proving: building a countermodel when a proof fails. Built.
11. Automated theorem proving: the Robbins conjecture proved by EQP (1996); Vampire and E; the TPTP library.
12. Second-order logic: categoricity of arithmetic, at the cost of completeness; Henkin vs full semantics; Boolos's
    plural interpretation.
13. Lindström's theorem (1969): FOL is the strongest logic with compactness and Löwenheim–Skolem (statement and
    meaning).
14. Logic and ontology, previewing Part 20: Quine's "to be is to be the value of a bound variable".
15. Recap and Problems.

*Built:* `reasoner.fol` (finite model checker, tableau prover with countermodel extraction, a small model finder).
*Wall:* the undecidability of validity; Lindström's characterization (the cost of power is losing compactness).
*Visuals:* Henkin's term model assembling itself; the non-standard model as ℕ followed by copies of ℤ; a tableau
branching and closing.
*References:* Enderton ch. 2; Boolos–Burgess–Jeffrey chs. 9–14, 18–19; Ebbinghaus, Flum and Thomas; Shapiro,
*Foundations without Foundationalism*.

#### Part 4 · Necessity and Possibility (~55): modal logics
1. Aristotle's sea battle and Diodorus's master argument: modality as an old problem.
2. C. I. Lewis's strict implication (1912) and the systems S1–S5.
3. Kripke semantics (1959–63): frames, models, □ and ◇. `WorldGraph` is introduced.
4. Correspondence: T ↔ reflexive, 4 ↔ transitive, B ↔ symmetric, 5 ↔ Euclidean. Each is proved, then checked
   exhaustively on all frames of up to 4 worlds.
5. Sahlqvist's theorem (statement), and Löb's axiom as a non-first-order frame condition (Goldblatt–Thomason).
6. Completeness via canonical models.
7. Bisimulation: what modal logic cannot distinguish; van Benthem's theorem (modal logic is the bisimulation-
   invariant fragment of FOL).
8. Decidability and the finite model property; filtrations.
9. Quantified modal logic: the Barcan formula; constant vs varying domains; Kripke's rigid designators (Part 22).
10. Deontic logic: SDL, Ross's paradox, Chisholm's contrary-to-duty paradox (shown to be inconsistent in SDL by the
    Reasoner).
11. Tense logic: Prior's tense logic; Ockhamist vs Peircean branching time (Part 23 returns to it).
12. Temporal logic for machines: LTL and CTL (Pnueli 1977; Clarke, Emerson and Sifakis). Automata-theoretic model
    checking.
13. Built: an LTL model checker verifying Peterson's mutual-exclusion algorithm, then finding the bug in a broken
    variant and showing the counterexample trace.
14. Dynamic logic and Hoare logic: programs as modalities; {P} C {Q}.
15. Industry: model checking in chip design (Intel after the 1994 FDIV bug), TLA+ at Amazon (Newcombe et al. 2015),
    SPIN and NuSMV.
16. Recap and Problems.

*Built:* `reasoner.modal` (Kripke model checker, frame-property enumerator, bisimulation minimizer, LTL to Büchi,
explicit-state model checking).
*Wall:* correspondence limits (some modal axioms have no first-order frame condition); Chisholm's paradox for SDL.
*Visuals:* frames morphing as an axiom is imposed; two bisimilar models collapsing into one; the Peterson state
graph lighting up its reachable states and the bug trace.
*References:* Hughes and Cresswell; Blackburn, de Rijke and Venema chs. 1–4; Sider ch. 6; Baier and Katoen;
McNamara (SEP), "Deontic Logic".

#### Part 5 · Beyond True and False (~55): non-classical logics and vagueness
1. Why leave classical logic: future contingents, vagueness, the liar, inconsistent databases, quantum
   propositions.
2. Logical matrices: Kleene's K3, Łukasiewicz Ł3, Priest's LP. Their designated values and the consequences they
   give.
3. Belnap and Dunn's FDE: four values, *told true* and *told false*; the lattice FOUR; bilattices.
4. The catuṣkoṭi (Nāgārjuna): true, false, both, neither, mapped onto FDE (Priest 2010); the "fifth corner".
5. Jaina saptabhaṅgī: seven predications and their formal reconstructions.
6. Paraconsistency: explosion (ex falso) fails in LP; inconsistency-tolerant databases.
7. Relevance logic: the paradoxes of material implication; Routley–Meyer ternary semantics (sketch).
8. Intuitionistic logic, previewing Part 9: no excluded middle, BHK.
9. Fuzzy logic: t-norms (Gödel, product, Łukasiewicz); industrial fuzzy control (the Sendai subway 1987).
10. The sorites: the paradox, stated formally; the Reasoner shows that the premises are classically inconsistent.
11. Theories of vagueness: supervaluationism (Fine 1975); degree theories; epistemicism (Williamson 1994, sharp but
    unknowable cutoffs); contextualism. The sorites Price List.
12. Higher-order vagueness.
13. Substructural logics: linear logic as a logic of resources (Girard 1987); the resource interpretation.
14. Quantum logic: Birkhoff–von Neumann (1936); distributivity fails on the lattice of subspaces (shown with
    polarizers); Putnam's "Is logic empirical?" (Part 26 returns to it).
15. What is logical consequence? Tarski (1936); Etchemendy's critique; the logical constants as permutation-invariant
    operators (Tarski–Sher).
16. Logical pluralism (Beall and Restall) vs monism; anti-exceptionalism about logic (Williamson, Hjortland).
17. Recap and Problems.

*Built:* `reasoner.matrix` (any finite-valued logic from its tables, consequence checked by enumeration); a sorites
engine with supervaluation and degree semantics side by side.
*Wall:* the sorites; revenge for every theory of vagueness (higher-order vagueness).
*Price List:* the sorites quartet (tolerance; bivalence; classical logic; that there is a bald man and a non-bald
man).
*Visuals:* FOUR's lattice with values flowing through ∧ and ∨; a 100-man sorites with the supervaluation's
"penumbra" shaded; subspaces in 3D showing distributivity fail.
*References:* Priest, *Introduction to Non-Classical Logic* (2nd ed.); Williamson, *Vagueness*; Keefe and Smith
(eds.), *Vagueness: A Reader*; Beall and Restall; Priest, *The Fifth Corner of Four*.

### Act II · The Limits of Reason

#### Part 6 · Paradise and Paradox (~55): sets and the infinite
1. Galileo's paradox (squares vs naturals); Hilbert's hotel; Aristotle's potential vs actual infinite.
2. Cantor: bijections; ℚ countable; the diagonal; Cantor's theorem |X| < |𝒫(X)|, with the proof drawn.
3. Frege's Basic Law V and Russell's letter (1902). The paradox derived in four lines; Frege's reply.
4. The responses: Russell's types; Zermelo 1908; Zermelo–Fraenkel axioms, each with the paradox it blocks or the
   object it builds.
5. The iterative conception: the cumulative hierarchy V_α as a widening cone, toured in 3D (Boolos 1971).
6. Ordinals: von Neumann's construction; ω, ω + 1, ω·2, ω², ω^ω, ε₀ (the ordinal spiral); transfinite induction.
7. Cardinals: ℵ numbers; cardinal arithmetic; cofinality (sketch).
8. The axiom of choice: Zorn and well-ordering; Banach–Tarski (the free-group paradox drawn on the hyperbolic Cayley
   graph); Vitali's non-measurable set.
9. Is choice true? The debate, and the dependent and countable choice alternatives.
10. The continuum hypothesis: Gödel's L (1938, consistency); Cohen's forcing (1963, independence), sketched with
    Boolean-valued models and generic filters drawn as paths through a tree of conditions.
11. Large cardinals: inaccessible, measurable, the consistency-strength ladder; determinacy (Martin–Steel, Woodin).
12. The philosophy: Gödel's realism ("the meaning is determinate; CH has an answer"); Hamkins's multiverse (2012);
    Woodin's Ultimate L; Maddy's naturalism and "Believing the Axioms".
13. What sets are for: set theory as the foundation, and its rivals (categories, types; Part 9).
14. Built: hereditarily finite sets as nested boxes and Ackermann's coding (n ↔ HF set); the ordinal comparator to
    ε₀ (Cantor normal form).
15. Recap and Problems.

*Built:* `reasoner.sets` (HF sets, Ackermann coding, ordinal arithmetic in Cantor normal form).
*Wall:* Russell's paradox (naive comprehension is inconsistent); the independence of CH from ZFC.
*Visuals:* the diagonal sweeping a table; V as a cone with L inside it; the ordinal spiral; the Banach–Tarski
free-group tree splitting.
*References:* Kunen; Enderton, *Elements of Set Theory*; Potter, *Set Theory and Its Philosophy*; Maddy 1988 (JSL);
Hamkins 2012 (RSL); Koellner (SEP), "The Continuum Hypothesis".

#### Part 7 · The Limits of Proof (~60): Gödel, Turing, Tarski, Löb
1. Hilbert's program (1921–28): finitary consistency proofs; the Entscheidungsproblem.
2. Robinson's Q and Peano arithmetic, axiom by axiom.
3. Representability: primitive recursive functions, Σ₁ formulas, β-function coding (sketch).
4. Gödel numbering: a formula becomes a number. Built: it encodes and decodes a proof, live.
5. The diagonal lemma, with the quine as its program-level twin. Built: a Python quine and a self-describing
   sentence.
6. The first incompleteness theorem: G ↔ ¬Prov(⌜G⌝), proved; Rosser's improvement.
7. The second incompleteness theorem: Con(PA) is unprovable in PA; the Hilbert–Bernays derivability conditions.
8. Turing machines (1936): built, with a busy-beaver champion running on screen.
9. The halting problem by diagonalization; Rice's theorem; the Church–Turing thesis (and what it does and doesn't
   say).
10. Busy beavers: BB(4) = 107 steps; BB(5) = 47,176,870, proved by the bbchallenge collaboration in Coq (2024).
    BB(n) eventually escapes ZFC (Yedidia and Aaronson 2016; later improvements).
11. Natural independence: Goodstein's theorem (sequences computed; they reach astronomical sizes and then return to
    0), Kirby–Paris 1982, Paris–Harrington.
12. Chaitin's Ω and incompleteness from information (the Berry paradox formalized).
13. Tarski's undefinability of truth (1933/36), proved from the diagonal lemma (bridge to Part 8).
14. Löb's theorem (1955) and provability logic GL; Solovay's completeness (1976). GL is checked on finite
    irreflexive transitive trees with `reasoner.modal`.
15. Consequences claimed and contested: Lucas–Penrose on minds vs machines and the standard replies (Benacerraf,
    Feferman, Shapiro); Franzén's catalogue of misuses.
16. Proof theory's answer: Gentzen's consistency proof of PA by induction to ε₀ (Part 6's spiral); ordinal analysis.
17. Recap and Problems.

*Built:* `reasoner.arith` (Gödel numbering, a PA proof checker on a fragment, quines, a Turing-machine simulator,
Goodstein sequences, small busy beavers).
*Wall:* Gödel I and II; the halting problem; Tarski; Löb.
*Visuals:* the diagonal lemma as a loop of mirrors; the Turing tape; a Goodstein base-bump tower growing and then
collapsing; GL's frames as finite trees.
*References:* Smith, *An Introduction to Gödel's Theorems*; Boolos–Burgess–Jeffrey chs. 15–18; Boolos, *The Logic of
Provability*; Franzén, *Gödel's Theorem: An Incomplete Guide*; Aaronson, "The Busy Beaver Frontier" (2020).

#### Part 8 · The Liar (~55): truth and paradox
1. Epimenides and Eubulides; the medieval *insolubilia* (Buridan, Bradwardine).
2. Tarski's T-schema and Convention T; the object language vs metalanguage hierarchy.
3. The semantic paradoxes: Grelling, Berry, Richard. Priest's inclosure schema unifies them with Russell and
   Burali-Forti.
4. Kripke (1975): the strong Kleene jump on a language with its own truth predicate. Built: the least fixed point
   computed by iteration; grounded vs ungrounded sentences (the truth-teller vs the liar).
5. Fixed points beyond the least: intrinsic, maximal; the liar is undefined in all of them.
6. Revenge: "this sentence is not true in the fixed point."
7. Revision theory (Gupta and Belnap 1993). Built: revision sequences; the liar oscillates, the truth-teller
   stabilizes on its starting value.
8. Curry's paradox: no negation needed; why it threatens paraconsistent answers.
9. Yablo's paradox (1993): an infinite sequence with no self-reference? The debate (Priest, Cook).
10. Dialetheism: the liar is both true and false (Priest); LP as its logic.
11. Axiomatic theories of truth: TB, CT, KF, FS; their proof-theoretic strength (Halbach).
12. Theories of truth: correspondence, coherence, pragmatist, identity; deflationism (Ramsey, Quine's
    disquotation, Horwich's minimalism) and the conservativeness debate (Shapiro, Ketland).
13. The surprise-exam paradox, formalized in epistemic logic (Kaplan and Montague 1960; Chow 1998).
14. Moore's paradox ("it's raining but I don't believe it") previews Part 12.
15. Recap and Problems.

*Built:* `reasoner.truth` (a toy language with T; Kleene jump iteration; revision sequences).
*Wall:* Tarski's undefinability; revenge for every consistent account.
*Price List:* the liar set (classical logic; the T-schema; self-reference; consistency).
*Visuals:* the extension of T growing stage by stage like a crystal; the liar flickering in revision; Yablo's
infinite staircase.
*References:* Kripke 1975 (JPhil); Gupta and Belnap, *The Revision Theory of Truth*; Field, *Saving Truth from
Paradox*; Halbach, *Axiomatic Theories of Truth*; Priest, *In Contradiction*; Beall, Glanzberg and Ripley, *Formal
Theories of Truth*.

#### Part 9 · What Is Mathematics About? (~55): the philosophy of mathematics
1. The puzzle: mathematics is necessary, a priori and applicable. How?
2. Platonism (Frege, Gödel) and Benacerraf's epistemological dilemma (1973): causal access to abstract objects.
3. Logicism: Frege's *Grundlagen* (1884) and the Julius Caesar problem.
4. Frege's theorem: Hume's principle plus second-order logic gives the Peano axioms. Key steps on screen;
   neo-logicism (Wright and Hale); the bad company objection.
5. Formalism: Hilbert's program after Gödel (Part 7); game formalism.
6. Intuitionism: Brouwer, choice sequences; BHK; the weak counterexample (does π contain 1000 consecutive 9s?).
7. Kripke semantics for intuitionistic logic: excluded middle fails at a two-node model. Built and drawn.
8. Curry–Howard: propositions as types, proofs as programs. Built: a small typed λ-calculus checker that accepts
   proofs of A → (B → A) and rejects Peirce's law.
9. Predicativism: Poincaré and Weyl; Feferman's predicative analysis; the vicious-circle principle.
10. Structuralism: Benacerraf's "What Numbers Could Not Be" (1965), with Zermelo's vs von Neumann's 2;
    ante rem (Shapiro), eliminative, modal (Hellman).
11. Indispensability (Quine and Putnam) vs fictionalism (Field's *Science without Numbers*, 1980); easy road
    nominalism.
12. Reverse mathematics: the Big Five subsystems (RCA₀, WKL₀, ACA₀, ATR₀, Π¹₁-CA₀); which theorems need which axioms.
13. Homotopy type theory and univalence (2013): equivalent structures are equal; structuralism built into a
    foundation.
14. Mathematical practice: proof as explanation; visual proofs (and the times when diagrams mislead).
15. Industry and frontier: Lean and Mathlib; the Liquid Tensor Experiment (2022); Tao's formalization projects; AI
    provers (AlphaProof 2024, IMO results cited). What a machine-checked proof shows.
16. Recap and Problems.

*Built:* `reasoner.types` (a simply typed λ-calculus checker; intuitionistic Kripke models).
*Wall:* Benacerraf's two dilemmas (epistemic access; identification).
*Price List:* the Benacerraf–Field puzzle (mathematical truths are objective; they are about abstract objects; we
know them; knowledge requires a reliable connection to its objects).
*Visuals:* the Curry–Howard dictionary with proof trees morphing into programs; Zermelo's and von Neumann's 2 as
nested boxes; a two-node Kripke frame refusing p ∨ ¬p.
*References:* Shapiro, *Thinking about Mathematics*; Linnebo; Benacerraf and Putnam (eds.); Hamkins, *Lectures*;
Simpson, *Subsystems of Second Order Arithmetic*; the HoTT Book; Avigad, "Mathematics and the formal turn" (2024).

### Act III · Knowledge

#### Part 10 · The Mind's Own Laws (~55): Descartes to Kant
1. The new science and the crisis of certainty (Galileo, Montaigne's skepticism, the Pyrrhonist modes of Sextus).
2. Descartes's method of doubt: the senses, the dream, the demon; the cogito; the clear-and-distinct rule; the
   Cartesian circle.
3. Descartes the geometer: coordinates as the calculus of space (the method that inspired the hope).
4. Spinoza's *Ethics* "in geometrical order". Built: the proof dependency graph of Part I (definitions, axioms, 36
   propositions), with its longest chains and its unused axioms computed.
5. Leibniz: the principle of sufficient reason, monads, truths of reason vs of fact (finite vs infinite analysis),
   and the best of all possible worlds as an optimization (bridge to Part 23).
6. Locke: ideas, primary and secondary qualities, Molyneux's problem (and the 2011 test with newly sighted patients,
   Held et al., cited).
7. Berkeley: *esse est percipi*; the master argument.
8. Hume: impressions and ideas; the missing shade of blue; relations of ideas vs matters of fact (Hume's fork).
9. Hume on causation: constant conjunction and habit (previews Parts 15 and 17); the self as a bundle (previews
   Part 21).
10. Kant's question: how are synthetic a priori judgments possible? The analytic/synthetic × a priori/a posteriori
    grid, filled in.
11. 7 + 5 = 12 and Euclid's geometry as Kant's examples; the transcendental aesthetic.
12. The table of judgments and the categories; the transcendental deduction (structure of the argument).
13. The antinomies: the first antinomy's thesis and antithesis both "proved" (finite vs infinite world); Kant's
    diagnosis.
14. Transcendental idealism: two-world vs two-aspect readings (Allison).
15. What happened to Kant's examples: non-Euclidean geometry (Part 25), Frege's analyticity of arithmetic (Part 9),
    and Reichenbach's relativized a priori and Friedman's dynamics of reason.
16. Hegel's dialectic, briefly and honestly, with the formal reconstructions attempted and their limits.
17. Recap and Problems.

*Built:* the Spinoza proof graph (hand-encoded from Curley's translation, checked for cycles and dangling
references).
*Wall:* Hume's problem (no demonstrative or probable argument for induction); Kant's antinomies (reason contradicts
itself when it goes beyond experience).
*Price List:* the empiricist trilemma (all knowledge comes from experience; we know necessary truths; experience
shows only what is, not what must be).
*Visuals:* Spinoza's Ethics as a glowing DAG; Kant's 2×2 grid with examples sliding between cells; the antinomy as
two proofs racing side by side.
*References:* Descartes, *Meditations*; Spinoza, *Ethics* (Curley trans.); Leibniz, *Monadology*; Locke, *Essay*;
Berkeley, *Principles*; Hume, *Enquiry*; Kant, *Critique of Pure Reason* (Guyer and Wood trans.; 李秋零 译); Gardner,
*Kant and the Critique of Pure Reason*; Allison, *Kant's Transcendental Idealism*.

#### Part 11 · What Is Knowledge? (~55)
1. Plato's *Theaetetus*: knowledge as justified true belief.
2. Gettier (1963): Smith's coins and the Ford case. Built as a world model; the Reasoner checks that every JTB
   condition holds and that the subject still lacks knowledge.
3. Repairs: no false lemmas; defeasibility; Zagzebski's recipe showing that Gettier cases are inescapable for
   any "JTB + X" with fallible X.
4. Reliabilism (Goldman 1979): process reliability; the generality problem.
5. Sensitivity (Nozick 1981): if p were false, S wouldn't believe p. Evaluated in a `SpheresView` of nearby worlds.
6. Safety (Sosa, Williamson): in nearby worlds where S believes p, p. Built: the safety and sensitivity checkers
   disagree on a computed case (the "I am not a brain in a vat" belief).
7. Virtue epistemology (Sosa's archer: accurate, adroit, apt).
8. Knowledge-first (Williamson 2000): E = K; the anti-luminosity argument with its margin-for-error principle,
   formalized and computed on a gradual series (cold to warm).
9. The KK principle and its failure under margin-for-error (computed).
10. Skepticism: the brain in a vat; the closure argument; the Price List (I don't know I'm not a BIV; if I know I
    have hands, I know I'm not a BIV; I know I have hands).
11. Answers: Moore's proof; Dretske's denial of closure; contextualism (DeRose, Lewis's "Elusive Knowledge");
    subject-sensitive invariantism; Putnam's semantic externalism argument against the BIV.
12. Zhuangzi's butterfly dream and the Pyrrhonists: skepticism as tranquility.
13. The structure of justification: Agrippa's trilemma; foundationalism, coherentism (with Bayesian coherence
    measures and Olsson's impossibility result), and infinitism (Klein).
14. Internalism vs externalism; the new evil demon problem.
15. The a priori and Quine's "Two Dogmas" (1951): the web of belief, holism, and revision even of logic.
16. Experimental philosophy: Gettier intuitions across cultures (Weinberg, Nichols and Stich 2001; the large
    replications of Machery et al. 2017; cited).
17. Recap and Problems.

*Built:* `reasoner.knowledge` (world models with similarity, sensitivity and safety checkers, margin-for-error
series).
*Wall:* Gettier (no fallibilist analysis escapes); anti-luminosity.
*Price List:* skepticism's closure triad; the regress trilemma.
*Visuals:* the Gettier world with a lucky arrow hitting the target; nested spheres sliding outward for sensitivity
and inward for safety; the margin-for-error ladder.
*References:* Pritchard; Williamson, *Knowledge and Its Limits*; Nozick, *Philosophical Explanations* ch. 3;
Sosa, *A Virtue Epistemology*; DeRose, *The Case for Contextualism*; Olsson, *Against Coherence*.

#### Part 12 · Knowledge Among Many (~55): epistemic logic, common knowledge, social epistemology
1. Hintikka's *Knowledge and Belief* (1962): K as □ over epistemic alternatives; S5 and its critics (negative
   introspection).
2. Multi-agent Kripke models. `WorldGraph` with one colour per agent.
3. Muddy children: public announcement logic; the n-cube of worlds cut down round by round. Built and run to n = 8.
4. Common knowledge: Lewis (1969), Aumann (1976); defined as the transitive closure; why "everyone knows" ≠
   common knowledge.
5. The coordinated-attack problem: common knowledge is unattainable over unreliable channels (Halpern and Moses 1990;
   the proof drawn as an induction over messages).
6. Industry: distributed systems; the two generals; Byzantine agreement; FLP impossibility (1985); how Paxos and
   Raft live with it.
7. Rubinstein's email game (1989): almost-common knowledge doesn't coordinate.
8. Aumann's agreement theorem: rational agents with common priors cannot agree to disagree (proof on a finite
   partition model, computed). The no-trade theorem (Milgrom–Stokey).
9. Dynamic epistemic logic: action models (Baltag, Moss and Solecki); private announcements; lies.
10. Moore sentences and unsuccessful updates; Fitch's paradox of knowability (if all truths are knowable, all
    truths are known), derived in KT plus a knowability modality.
11. Testimony: reductionism (Hume) vs anti-reductionism (Reid, Coady).
12. Peer disagreement: equal weight (Elga), steadfastness, total evidence (Kelly); the Bayesian treatment.
13. The wisdom of crowds: Galton's ox (1907), the diversity prediction theorem (proved: crowd error = average error −
    diversity).
14. Networks of inquiry: the Zollman effect (2007). Built: bandit-playing scientists on networks; less connected
    networks converge on the truth more reliably but more slowly (computed with seeds and spreads). Echo chambers
    vs epistemic bubbles (Nguyen).
15. Recap and Problems.

*Built:* `reasoner.del` (multi-agent S5 models, public and private announcements, action-model products, common
knowledge); the Zollman simulator.
*Wall:* coordinated attack (no common knowledge over lossy channels); Fitch.
*Visuals:* the muddy-children cube losing vertices each round; message chains that never reach common knowledge;
belief rivers on networks.
*References:* Fagin, Halpern, Moses and Vardi; van Ditmarsch, van der Hoek and Kooi; Aumann 1976; Zollman 2007
(Phil Sci); Lackey and Christensen (eds.), *The Epistemology of Disagreement*; Goldman, *Knowledge in a Social World*.

#### Part 13 · Degrees of Belief (~60): Bayesian epistemology
1. From all-or-nothing to degrees: Ramsey's "Truth and Probability" (1926); de Finetti (1937).
2. Kolmogorov's axioms; credences as points on the simplex (`Simplex`).
3. The Dutch book theorem: incoherent credences can be exploited by a sure-loss book. The proof is a separating
   hyperplane drawn on the simplex. Built: an LP finds the book for any incoherent credence.
4. Accuracy: the Brier score; Joyce's accuracy-dominance argument (1998). Projecting an incoherent point onto the
   simplex dominates it in every world (Predd et al. 2009), drawn in 2D and 3D.
5. Proper scoring rules: Brier, logarithmic, spherical; the characterization (Savage, Schervish). Industry:
   forecasting, calibration, superforecasters (Tetlock), Metaculus; we compute Brier and log scores of synthetic
   forecasters.
6. Conditionalization and the diachronic Dutch book (Lewis/Teller); Jeffrey conditionalization.
7. The problem of the priors: subjective vs objective Bayesianism; MaxEnt (Jaynes).
8. The principle of indifference and Bertrand's paradox: three "random chords" give 1/2, 1/3 and 1/4, all simulated;
   van Fraassen's cube factory; Jaynes's invariance answer and its limits.
9. Chance and credence: Lewis's Principal Principle (Part 24 returns with the "big bad bug").
10. Imprecise credences: credal sets; dilation, computed; the arguments for and against (Elga 2010).
11. The lottery and preface paradoxes; the Lockean thesis; Leitgeb's stability theory of belief (2017), with stable
    sets computed.
12. Self-locating belief: Sleeping Beauty (Elga 2000; Lewis 2001). Simulated, with the long-run frequencies, the
    bets each answer wins, and the double-halfer view.
13. Anthropic reasoning: SSA vs SIA; the Doomsday argument; the presumptuous philosopher; fine-tuning and observation
    selection (Bostrom), all computed on toy universes.
14. Bayesian brains and Bayesian machines: what the formal framework promises and what it can't compute
    (complexity of exact inference).
15. Recap and Problems.

*Built:* `reasoner.credence` (coherence checking, the Dutch-book LP, Brier projection, scoring rules, conditioning,
credal sets, Sleeping Beauty and anthropic simulators).
*Wall:* Bertrand's paradox (indifference is not well-defined); the lottery paradox (no simple bridge from credence to
belief).
*Price List:* the lottery triad (rational belief is closed under conjunction; high credence suffices for belief;
don't believe what you know to be false).
*Visuals:* the 3-simplex in 3D with incoherent points and their projections; Bertrand's three chord ensembles;
Sleeping Beauty's branching week.
*References:* Titelbaum; Pettigrew; Joyce 1998 (Phil Sci); Hájek (SEP), "Interpretations of Probability"; Leitgeb,
*The Stability of Belief*; Bostrom, *Anthropic Bias*.

#### Part 14 · Changing Your Mind (~55): belief revision, conditionals, defeasible reasoning
1. Revision vs update vs contraction; the recovery debate.
2. The AGM postulates (Alchourrón, Gärdenfors and Makinson 1985), one per card.
3. Partial meet contraction and the representation theorem; Grove's spheres (1988). Built and drawn as
   `SpheresView`.
4. The Levi and Harper identities; entrenchment.
5. Iterated revision: Darwiche–Pearl postulates; ranking functions (Spohn), computed.
6. Conditionals: the material conditional's paradoxes; the Ramsey test.
7. Gärdenfors's impossibility theorem (1986): the Ramsey test and AGM can't coexist (non-trivially). Statement and
   the Reasoner's check on a small belief set.
8. Stalnaker and Lewis semantics for counterfactuals: the closest antecedent worlds; the limit assumption;
   conditional excluded middle.
9. Indicatives vs counterfactuals: the Oswald–Kennedy pair.
10. Adams's thesis P(A → C) = P(C | A); Lewis's triviality result (1976), proved on screen; Bradley and Hájek's
    extensions. Built: a search shows that no non-trivial model satisfies the thesis.
11. McGee's counterexample to modus ponens (1985).
12. Non-monotonic reasoning: Tweety; default logic (Reiter 1980); circumscription (McCarthy).
13. KLM preferential models and System P; rational closure.
14. Argumentation frameworks (Dung 1995): attacks; grounded, preferred and stable extensions. Built; and industry
    uses in legal reasoning, multi-agent negotiation and LLM argument mining.
15. Recap and Problems.

*Built:* `reasoner.revision` (AGM via spheres, Spohn ranks, Darwiche–Pearl); `reasoner.cond` (Stalnaker and Lewis
models, triviality search); `reasoner.argue` (Dung extensions).
*Wall:* Gärdenfors's impossibility; Lewis's triviality.
*Price List:* the triviality cluster (Adams's thesis; conditional probability; conditionals express propositions;
non-triviality).
*Visuals:* spheres shrinking to the most plausible A-worlds; the triviality proof as probability mass sliding until
the model collapses; argumentation graphs coloured by labelling.
*References:* Gärdenfors, *Knowledge in Flux*; Hansson, *A Textbook of Belief Dynamics*; Lewis, *Counterfactuals*;
Bennett, *A Philosophical Guide to Conditionals*; Edgington (SEP), "Indicative Conditionals"; Baroni et al.,
*Handbook of Formal Argumentation*.

### Act IV · Science

#### Part 15 · The Problem of Induction (~60)
1. Hume's problem restated: the circle in any inductive justification of induction.
2. Laplace's rule of succession and the sunrise problem, computed; what the prior assumes.
3. Indian inference: vyāpti (invariable concomitance) and Dignāga's wheel of reasons (hetucakra), a 3×3 grid of
   which only two reasons are good, drawn and checked.
4. Hempel's ravens (1945): the equivalence condition and Nicod's criterion. The Bayesian answer, computed: a white
   shoe confirms "all ravens are black", by an amount of order 10⁻⁶ in a realistic model.
5. Confirmation measures: difference, ratio, likelihood ratio, Kemeny–Oppenheim. Fitelson's comparison of which
   measures satisfy which desiderata.
6. The problem of old evidence (Glymour 1980): Mercury's perihelion and GR.
7. Goodman's new riddle (1955): grue; projectibility and entrenchment.
8. Grue in a neural network. Built: train small models on emeralds observed before t and show which extrapolation
   each architecture projects. Inductive bias is projectibility.
9. Popper: falsification and corroboration; the asymmetry; Duhem–Quine holism.
10. Merging of opinions: Blackwell–Dubins (1962); Bayesian convergence computed for disagreeing priors; when
    convergence fails (non-absolutely-continuous priors).
11. Formal learning theory: identification in the limit (Gold 1967) and Gold's theorem (no learner identifies all
    regular languages from positive data), proved; Putnam's diagonal argument against Carnap.
12. Kelly's Ockham efficiency theorem: Ockham's razor as minimizing retractions.
13. Solomonoff induction: Kolmogorov complexity; the universal prior; the convergence theorem; incomputability.
    Built: a Solomonoff mixture over a small program language predicting bit sequences.
14. MDL and two-part codes; the link to Part 1 of *AI, Built* (compression is prediction).
15. No free lunch (Wolpert 1996): averaged over all problems no learner beats another. Hume's problem in machine
    learning, and the answers (the world is not uniformly random; priors).
16. Reichenbach's pragmatic vindication: if any method succeeds, the straight rule does.
17. Recap and Problems.

*Built:* `reasoner.induction` (confirmation measures, Bayesian convergence, Gold-style learners, a Solomonoff
mixture over a toy language, the grue experiment).
*Wall:* Hume; Goodman; no free lunch; Gold.
*Price List:* the paradox of the ravens (Nicod's criterion; the equivalence condition; the white shoe doesn't
confirm).
*Visuals:* two posteriors merging toward a point; the hetucakra grid; grue and green branching on the timeline; the
retraction staircase of Ockham's learner.
*References:* Howson and Urbach; Earman, *Bayes or Bust?*; Goodman, *Fact, Fiction, and Forecast*; Kelly; Li and
Vitányi, *An Introduction to Kolmogorov Complexity*; Sterkenburg 2016 (Phil Sci); Henderson (SEP), "The Problem of
Induction".

#### Part 16 · Evidence by Numbers (~55): the philosophy of statistics
1. Three schools: Fisher's significance, Neyman–Pearson's error control, Bayes; the 1930s feuds.
2. The p-value defined and the six common misreadings, each refuted by simulation (the ASA statement 2016).
3. The base-rate fallacy: a medical test with 1% prevalence, drawn as a population grid.
4. Ioannidis (2005): positive predictive value from power, α and prior odds, computed across fields.
5. The garden of forking paths. Built: a p-hacking simulator that turns pure noise into "significant" results.
   The replication crisis numbers (Open Science Collaboration 2015) are cited.
6. Optional stopping: a frequentist test breaks, while Bayesian posteriors and the likelihood principle don't.
   Computed.
7. The likelihood principle; Birnbaum's theorem (1962), that sufficiency plus conditionality imply it, stated and
   proved. Mayo's challenge (2014) and the debate.
8. Lindley's paradox, computed: p < 0.05 while the Bayes factor favors the null.
9. Bayes factors, priors on hypotheses, and the sensitivity to the prior.
10. Severe testing (Mayo): severity curves computed.
11. Simpson's paradox: the Berkeley admissions data (Bickel, Hammel and O'Connell 1975; cited) and the causal
    reading (previews Part 17).
12. The reference class problem (Hájek).
13. Industry: A/B testing; the peeking problem; sequential tests.
14. Testing by betting: e-values and test martingales (Shafer and Vovk; Grünwald, de Heide and Koolen; Ramdas et al.)
    with Ville's inequality proved; anytime-valid inference, computed. The philosophy of evidence as betting gains.
15. Model selection: AIC as an estimate of predictive accuracy (Forster and Sober 1994) vs BIC.
16. Recap and Problems.

*Built:* `reasoner.stats` (p-hacking garden, PPV calculator, Lindley's paradox, e-values and betting martingales).
*Wall:* Birnbaum's theorem (respect sufficiency and conditionality, and you must accept the likelihood principle);
Lindley's paradox.
*Visuals:* the population grid of true and false positives; a p-value random walk crossing 0.05 under the null; a
betting wealth curve climbing under the alternative.
*References:* Royall, *Statistical Evidence*; Mayo, *Statistical Inference as Severe Testing*; Sober, *Evidence and
Evolution* ch. 1; Shafer and Vovk, *Game-Theoretic Foundations for Probability and Finance*; Ramdas et al. 2023
(Stat Sci), "Game-theoretic statistics and safe anytime-valid inference".

#### Part 17 · Cause (~60)
1. Hume's two definitions; al-Ghazālī's occasionalism eight centuries earlier (the cotton and the fire).
2. Mill's methods; Mackie's INUS conditions.
3. Lewis's counterfactual analysis (1973) and its dependence chains; early and late preemption; trumping;
   overdetermination (Suzy and Billy's rocks, drawn).
4. Probabilistic causation (Suppes, Cartwright) and Simpson's paradox again.
5. Russell's "On the Notion of Cause" (1913): no causes in fundamental physics? Answers from interventionism.
6. Interventionism (Woodward 2003): invariance under intervention.
7. Structural causal models (Pearl): equations, graphs, d-separation. Built: the SCM engine.
8. The do-operator; the back-door and front-door criteria, each proved and checked by simulation.
9. The do-calculus's three rules; completeness (Shpitser and Pearl, Huang and Valtorta 2006).
10. Pearl's ladder: association, intervention, counterfactuals; twin networks; the probabilities of necessity and
    sufficiency.
11. Actual causation: Halpern–Pearl (2005, 2015). Built and run on the classic cases (preemption, double prevention,
    bogus prevention), with where the definition still disagrees with intuition.
12. The causal Markov condition and faithfulness; Reichenbach's common cause principle (and its failure in quantum
    correlations, previewing Part 26).
13. Causal discovery: the PC algorithm (built), recovering a DAG from data up to its Markov equivalence class; FCI
    with latent variables.
14. Potential outcomes (Rubin) and their relation to SCMs; RCTs; instrumental variables; difference in
    differences.
15. Industry: causal inference in tech (uplift modelling, experimentation platforms); LLMs and causal reasoning
    benchmarks (frontier, cited).
16. Causation and the mind: Kim's exclusion argument (previews Part 30).
17. Recap and Problems.

*Built:* `reasoner.causal` (SCMs, do, counterfactuals, Halpern–Pearl, PC).
*Wall:* underdetermination of causal structure by observational data (Markov equivalence); the counterexamples that
every analysis of actual causation faces.
*Price List:* the preemption cluster (counterfactual dependence is necessary; Suzy's throw caused the breaking;
Billy's would have; transitivity).
*Visuals:* `CausalDAG` with scissors cutting arrows for do(x); back-door paths glowing; the PC algorithm removing
edges round by round.
*References:* Pearl, *Causality*; Spirtes, Glymour and Scheines; Woodward; Halpern, *Actual Causality*; Paul and
Hall; Hernán and Robins, *Causal Inference: What If*.

#### Part 18 · Theories and Reality (~55): explanation, change and realism
1. The Vienna Circle; verificationism and its self-refutation problem.
2. Hempel's deductive-nomological model (1948); its counterexamples (the flagpole, the hexed salt); statistical
   relevance (Salmon).
3. Unification (Friedman, Kitcher); mechanisms (Machamer, Darden and Craver); the causal-mechanical view.
4. Kuhn (1962): paradigms, normal science, revolutions, incommensurability; a toy model of anomaly accumulation.
5. Lakatos's research programmes; Feyerabend's anarchism; Laudan's problem solving.
6. Underdetermination: empirically equivalent theories (Newton's absolute velocity); Duhem–Quine revisited.
7. The no-miracles argument (Putnam 1975) and the base-rate fallacy objection (Magnus and Callender 2004),
   computed with Part 13's credence lab.
8. The pessimistic meta-induction (Laudan 1981): the list of successful false theories.
9. Structural realism (Worrall 1989): Fresnel's equations survive into Maxwell's. Epistemic vs ontic (Ladyman).
10. Constructive empiricism (van Fraassen 1980); the observable/unobservable line.
11. Reduction: Nagel's bridge laws; multiple realizability.
12. Emergence and universality: why the Ising model and the liquid–gas critical point share exponents. Built: block-
    spin renormalization of a 2D Ising model on screen, with the flow to the fixed point (Batterman's argument).
13. Models and idealization: the frictionless plane; minimal models; simulations as experiments.
14. The demarcation problem revisited (Popper, Laudan's obituary, the new demarcation literature).
15. Values in science: the argument from inductive risk (Rudner 1953; Douglas).
16. AI scientists: automated discovery (BACON, 1978; modern AI-driven discovery claims, cited). What counts as
    explanation from a black box.
17. Recap and Problems.

*Built:* `reasoner.science` (the Ising coarse-graining; no-miracles Bayes; Kuhnian anomaly toy, labeled `analogy`).
*Wall:* underdetermination; the pessimistic meta-induction.
*Price List:* the realism trilemma (success is evidence of truth; past successful theories were false; we have no
privileged position).
*Visuals:* the flagpole and its shadow swapped; Ising spins coarse-graining in blocks; the theory family tree from
Fresnel to Maxwell with structure preserved.
*References:* Godfrey-Smith; Salmon, *Four Decades of Scientific Explanation*; Kuhn, *Structure*; van Fraassen, *The
Scientific Image*; Psillos, *Scientific Realism*; Batterman, *The Devil in the Details*; Douglas, *Science, Policy,
and the Value-Free Ideal*.

#### Part 19 · Life (~55): the philosophy of biology
1. Darwin's argument as an inference to the best explanation; Paley's watch.
2. Natural selection's recipe: variation, heredity, differential fitness (Lewontin 1970).
3. Fitness: the propensity interpretation; the tautology objection; the Price equation derived on screen.
4. Replicator dynamics on the simplex; evolutionarily stable strategies (Maynard Smith and Price 1973), with the
   hawk–dove game.
5. Kin selection: Hamilton's rule rb > c derived from the Price equation.
6. Levels of selection: group selection, multilevel selection as a Price decomposition; Simpson's paradox again.
   The debate (Okasha; Nowak, Tarnita and Wilson 2010 vs 100+ authors 2011).
7. Genes, organisms, extended phenotypes; Dawkins vs Gould; the replicator/interactor distinction (Hull).
8. Function: etiological (Wright, Millikan) vs causal-role (Cummins); teleology without design.
9. Species: the species problem and its many concepts; cladistics.
10. Information in biology: the genetic code as a code? (Maynard Smith 2000; Godfrey-Smith's skepticism); Shannon vs
    teleosemantic information.
11. Evolution and cooperation: the bridge to Part 34 (Axelrod) and Part 37 (debunking).
12. What is life? Definitions and their failures; autopoiesis; Schrödinger's *What Is Life?*.
13. Artificial life: Lenia (Chan 2019), with continuous creatures rendered live; open-ended evolution.
14. Recap and Problems.

*Built:* `reasoner.evo` (the Price equation, replicator dynamics, Hamilton's rule simulations, Lenia).
*Wall:* the levels-of-selection question (no level is privileged by the mathematics alone).
*Visuals:* replicator flows on the simplex; the Price equation's covariance term as a tilted cloud; Lenia
creatures gliding.
*References:* Sober, *The Nature of Selection* and *Philosophy of Biology*; Okasha, *Evolution and the Levels of
Selection*; Godfrey-Smith, *Darwinian Populations and Natural Selection*; Sterelny and Griffiths, *Sex and Death*.

### Act V · The World

#### Part 20 · What There Is (~55): ontology
1. Quine's "On What There Is" (1948): Plato's beard; ontological commitment as quantification.
2. Meinong's jungle and Russell's escape (previews Part 27).
3. Universals vs nominalism: Plato, Aristotle, the medieval debate (Ockham's razor), Armstrong's universals,
   tropes.
4. Resemblance nominalism and Goodman's imperfect community and companionship problems, shown on toy property
   tables.
5. Abstract objects: the way-of-abstraction criteria and their failure.
6. Mereology: classical extensional mereology, axiom by axiom. Built: finite models are complete Boolean algebras
   with the bottom removed (proved and enumerated).
7. The special composition question (van Inwagen 1990): nihilism, universalism, organicism.
8. Composition as identity; the argument from vagueness for universalism (Lewis, Sider).
9. Metaontology: Carnap's internal and external questions; quantifier variance (Hirsch); Sider's structure.
10. Grounding (Fine, Schaffer, Rosen): a strict partial order; metaphysical explanation; priority monism.
11. Fundamentality and the well-foundedness question (is there a bottom level?).
12. Formal ontology as engineering: description logics. Built: an ALC tableau reasoner.
13. Industry: OWL and the semantic web; the Gene Ontology, SNOMED CT, Basic Formal Ontology. Philosophical mistakes
    in real ontologies (OntoClean's rigidity and identity criteria; Guarino and Welty).
14. Knowledge graphs and LLMs: what an embedding commits to.
15. Recap and Problems.

*Built:* `reasoner.mereo` (finite mereology models); `reasoner.dl` (ALC with TBox and ABox; subsumption).
*Wall:* the special composition question; quantifier variance's challenge to "what really exists".
*Price List:* the problem of the many (Unger, Geach): many candidates for "the cloud"; one cloud; parity; clouds
exist.
*Visuals:* Hasse diagrams of mereological sums; nested description-logic concepts as regions; a grounding DAG.
*References:* Loux and Crisp; van Inwagen, *Material Beings*; Simons, *Parts*; Varzi (SEP), "Mereology"; Chalmers,
Manley and Wasserman (eds.), *Metametaphysics*; Baader et al., *The Description Logic Handbook*.

#### Part 21 · Identity and Persistence (~55)
1. Identity: reflexivity and Leibniz's law; the indiscernibility of identicals vs the identity of indiscernibles.
2. Black's two spheres (1952); weak discernibility and quantum particles (Saunders 2006; Muller and Saunders).
3. Coincidence: the statue and the lump; the debate between pluralists and monists.
4. The Ship of Theseus with Hobbes's twist: the two-ship problem, drawn.
5. Relative identity (Geach) and sortals.
6. Evans's argument (1978): there is no vague identity, proved in a modal logic of definiteness.
7. Persistence: endurance vs perdurance (worms) vs stage theory. `SpacetimeView` worldtubes.
8. Temporary intrinsics (Lewis): the bent and straight problem.
9. Personal identity: Locke's memory criterion; Reid's brave officer (transitivity fails), made a relation on screen.
10. Psychological continuity vs connectedness; Parfit's teletransporter.
11. Fission: branching worms; "identity is not what matters" (Parfit 1971).
12. Animalism (Olson); the thinking-animal problem.
13. Buddhist anattā: the chariot in the *Milindapañha*; the bundle theory and Hume.
14. Copies and uploads: brain emulation; and the modern case of model weights run as many simultaneous instances.
    Which properties of the personal-identity debate transfer (labeled `analogy` where they don't).
15. Recap and Problems.

*Built:* `reasoner.persist` (continuity graphs; transitive closure vs identity; branching checks).
*Wall:* fission (no account preserves transitivity of identity and the importance of continuity); Evans on vague
identity.
*Price List:* the fission set (I survive teleportation; identity is transitive; fission's branches are not
identical to each other; each branch has an equal claim).
*Visuals:* the ship's planks migrating plank by plank; spacetime worms splitting; Reid's officer as a chain of
memory links with the end-to-end link missing.
*References:* Noonan and Curtis (SEP), "Identity"; Sider, *Four-Dimensionalism*; Parfit, *Reasons and Persons*
Part III; Olson, *The Human Animal*; Siderits, *Buddhism as Philosophy*.

#### Part 22 · Possible Worlds (~55): modal metaphysics
1. De re vs de dicto; Quine's mathematical cyclist.
2. Kripke's *Naming and Necessity* (1970): rigid designation; the modal argument against descriptivism.
3. The necessary a posteriori: water = H₂O; Hesperus = Phosphorus; the contingent a priori (the standard metre).
4. Lewis's modal realism (1986): concrete worlds; the incredulous stare; the argument from utility.
5. Counterpart theory: translating quantified modal logic into counterpart theory (Lewis 1968), and what it
   validates or not (necessity of identity fails). Built: the translator, checked on test formulas.
6. Ersatzism: Plantinga's states of affairs, Stalnaker's actualism; the problem of alien properties.
7. Necessitism vs contingentism (Williamson 2013): the Barcan formula's metaphysics.
8. Modal epistemology: conceivability and possibility (Yablo, Gendler and Hawthorne).
9. Two-dimensional semantics (Chalmers, Jackson): primary and secondary intensions. Built: the 2D matrix engine on
   the water/XYZ case. The bridge to Part 31's zombie argument.
10. Essence: Fine's "Essence and Modality" (1994): Socrates and {Socrates}; essence is not modal.
11. Hyperintensionality: impossible worlds (Nolan, Berto); counterpossibles ("if Hobbes had squared the circle …").
12. Dispositions and their conditional analysis; finks and masks.
13. Recap and Problems.

*Built:* `reasoner.worlds` (counterpart translation; 2D matrices; impossible-world models).
*Wall:* the Kripkean necessary a posteriori splits conceivability from possibility; Fine's counterexamples to modal
accounts of essence.
*Price List:* Kripke's puzzle about belief (Pierre and Londres).
*Visuals:* worlds as islands with counterpart bridges; the 2D matrix filling cell by cell; impossible worlds drawn
outside the possible.
*References:* Kripke, *Naming and Necessity*; Lewis, *On the Plurality of Worlds*; Williamson, *Modal Logic as
Metaphysics*; Chalmers 2006 ("The Foundations of Two-Dimensional Semantics"); Menzel (SEP), "Possible Worlds"; Berto
and Jago, *Impossible Worlds*.

#### Part 23 · God and the Philosophers (~55): the philosophy of religion
1. Anselm's ontological argument (1078); Gaunilo's island; Kant's "existence is not a predicate".
2. Plantinga's modal ontological argument in S5, proved valid by the Reasoner; the possibility premise and its
   mirror image ("possibly God does not exist").
3. Gödel's ontological proof (published 1987). Built: formalized in higher-order modal logic and checked; it
   reproduces the known result (Benzmüller and Woltzenlogel Paleo 2014) that Gödel's original axioms are
   inconsistent and that Scott's variant implies modal collapse (□(p ↔ □p)).
4. Cosmological arguments: Aquinas's five ways; Leibniz's PSR argument; the Kalam (al-Ghazālī; Craig) and the
   infinity premises (callback to Part 6's Hilbert hotel).
5. The PSR and van Inwagen's modal collapse argument against it.
6. Design and fine-tuning: the likelihood argument (Sober); the multiverse reply and the inverse gambler's fallacy
   (Hacking 1987; White 2000), all computed on a toy model.
7. Pascal's wager: decision theory with infinite utility; many gods; Hájek's mixed-strategy objection (2003),
   computed.
8. The logical problem of evil (Mackie 1955) and Plantinga's free-will defense: consistency shown with a model.
9. The evidential problem (Rowe 1979) as a Bayesian argument; skeptical theism.
10. Hume on miracles (1748): a Bayesian formalization (Earman's "Hume's Abject Failure", and the replies).
11. Divine foreknowledge and free will: Boethius's eternity; Ockhamism. Prior's branching-time logic: Ockhamist vs
    Peircean semantics, built; Aristotle's sea battle resolved in each.
12. Religious epistemology: reformed epistemology (Plantinga), religious experience, religious disagreement.
13. Non-theistic traditions: Buddhist arguments against a creator (Dharmakīrti); the Dao as non-agential ground.
14. Recap and Problems.

*Built:* `reasoner.hol` (a small higher-order modal logic, enough for Gödel's proof); `reasoner.branching`
(Ockhamist and Peircean semantics).
*Wall:* modal collapse in Gödel's and Scott's systems; the symmetry of the modal ontological argument.
*Price List:* the problem of evil (from Part 2), with each theodicy as a correction set.
*Visuals:* S5 worlds where God exists in one and therefore all; the modal collapse proof lighting every □;
branching time with Ockhamist "thin red line" vs Peircean all-branches truth.
*References:* Oppy, *Arguing about Gods*; Plantinga, *The Nature of Necessity*; Sobel, *Logic and Theism*;
Benzmüller and Woltzenlogel Paleo 2014 (ECAI); Hájek (SEP), "Pascal's Wager"; Earman, *Hume's Abject Failure*;
Øhrstrøm and Hasle, *Temporal Logic: From Ancient Ideas to Artificial Intelligence*.

#### Part 24 · Laws, Chance and the Arrow (~60)
1. What is a law? The regularity view and accidental generalizations (gold spheres vs uranium spheres).
2. Lewis's best-system account: strength vs simplicity; the Mentaculus (Albert and Loewer).
3. Armstrong, Dretske and Tooley: necessitation between universals; the inference problem.
4. Dispositional essentialism (Bird); primitivism (Maudlin).
5. Chance: Lewis's Principal Principle; undermining futures and the "big bad bug", derived; the New Principle (Hall,
   Lewis 1994).
6. Determinism (Earman): Laplace's demon; definitions by models.
7. Norton's dome (2003): Newtonian mechanics with non-unique solutions, r(t) = (1/144)(t − T)⁴, computed and
   animated for several T.
8. Chaos: sensitive dependence, the Lorenz attractor; Lyapunov exponents computed; unpredictability ≠
   indeterminism.
9. Statistical mechanics: Boltzmann entropy S = k log W; macrostates as cells of phase space.
10. The H-theorem; Loschmidt's reversibility objection; Zermelo's recurrence objection.
11. The Kac ring (1959). Built: a reversible, recurrent toy model whose "entropy" still rises toward equilibrium for
    almost all initial conditions. Typicality explains the arrow.
12. The Past Hypothesis (Albert 2000): a low-entropy beginning; Boltzmann brains and the case against
    fluctuation cosmology.
13. Maxwell's demon and Szilard's engine (1929); Landauer's principle (kT ln 2 per erased bit) derived, with its
    experimental tests (Bérut et al. 2012, cited); Bennett's exorcism.
14. Industry: reversible computing and the energy cost of erasure; the thermodynamics of computation.
15. Other arrows: the causal, the epistemic (records), the radiative; are they the thermodynamic arrow?
16. Recap and Problems.

*Built:* `reasoner.physics.laws` (best-system toy: candidate laws scored for simplicity and strength on generated
data; Norton's dome solutions; Lorenz Lyapunov exponents; the Kac ring; Szilard's engine).
*Wall:* Loschmidt and Zermelo (no time-symmetric dynamics gives the arrow alone); the big bad bug.
*Price List:* the arrow of time (dynamics are time-symmetric; entropy increases; the increase is lawlike; no special
initial condition).
*Visuals:* the dome with balls rolling off at different T; the Kac ring's balls flipping on markers and the
entropy curve rising then recurring; phase-space cells for macrostates.
*References:* Lewis 1994 ("Humean Supervenience Debugged"); Armstrong, *What Is a Law of Nature?*; Earman, *A Primer
on Determinism*; Albert, *Time and Chance*; Loewer, *Laws of Nature and Chance* (2023); Sklar, *Physics and Chance*;
Leff and Rex (eds.), *Maxwell's Demon 2*.

#### Part 25 · Space and Time (~60)
1. Newton's bucket (1687) and absolute space.
2. The Leibniz–Clarke correspondence: static and kinematic shift arguments; the principle of the identity of
   indiscernibles applied to the universe.
3. Kant's incongruent counterparts (1768): left and right hands; a Möbius strip turns one into the other.
4. Non-Euclidean geometry: Gauss, Bolyai and Lobachevsky; the Poincaré disk drawn with its geodesics; Gauss's
   triangle measurement.
5. Conventionalism: Poincaré's disk world (temperature that shrinks rulers); Reichenbach's universal forces.
6. Spacetime structures: Aristotelian, Galilean, Newtonian, neo-Newtonian (Maudlin's diagrams), each with what it
   keeps.
7. Special relativity: the Minkowski diagram; the relativity of simultaneity as a tilting slice in `SpacetimeView`.
8. The conventionality of simultaneity: Reichenbach's ε; Malament's theorem (1977).
9. McTaggart (1908): A-series and B-series; the argument for the unreality of time.
10. Presentism, eternalism, the growing block, the moving spotlight.
11. The Rietdijk–Putnam argument: special relativity against presentism; the presentist replies.
12. General relativity: curvature; the hole argument (Einstein 1913; Earman and Norton 1987). Diffeomorphism
    invariance drawn as a deformation inside a hole.
13. Sophisticated substantivalism; Leibniz equivalence; relationalism revived (Barbour).
14. Time travel: Gödel's rotating universe (1949); Lewis's "Paradoxes of Time Travel" (1976); the grandfather
    paradox; Novikov's self-consistency; Deutsch's CTC model, whose fixed points are computed for a toy
    circuit.
15. Quantum gravity and the emergence of spacetime (holography, ER=EPR), shown schematically and labeled as
    speculative.
16. Recap and Problems.

*Built:* `reasoner.physics.spacetime` (Poincaré disk geometry; Minkowski diagram engine; Deutsch CTC fixed-point
solver).
*Wall:* the hole argument (substantivalism seems to imply indeterminism); Malament vs Reichenbach.
*Price List:* the hole-argument cluster (spacetime points are real; GR is deterministic; diffeomorphic models
differ).
*Visuals:* the bucket's water surface curving; the Möbius strip flipping a hand; Poincaré's world with shrinking
rulers; simultaneity slices rotating; the hole deformation.
*References:* Maudlin, *Philosophy of Physics: Space and Time*; Earman, *World Enough and Space-Time*; Huggett (ed.),
*Space from Zeno to Einstein*; Dainton, *Time and Space*; Norton (SEP), "The Hole Argument"; Arntzenius, *Space, Time,
and Stuff*.

#### Part 26 · The Quantum Puzzle (~60)
1. The formalism in one chapter: states as vectors, measurement as projection, the Born rule (callback to the
   repository's *Quantum Mechanics* videos).
2. The measurement problem: Maudlin's trilemma (1995), with its three claims and the three ways out.
3. EPR (1935): the argument for completeness, formalized.
4. Bell (1964): local hidden variables imply |S| ≤ 2 (CHSH, derived step by step); quantum mechanics gives 2√2
   (Tsirelson's bound, derived).
5. The CHSH game. Built: all 16 deterministic local strategies are enumerated (the maximum is 3/4), and the quantum
   strategy is simulated (cos²(π/8) ≈ 0.854).
6. Experiments: Aspect (1982); the 2015 loophole-free tests (Hensen et al., Giustina et al., Shalm et al.); the
   2022 Nobel prize (all cited). What locality, freedom of settings and realism mean.
7. GHZ: Bell without inequalities (a contradiction with certainty).
8. Kochen–Specker and the Peres–Mermin square. Built: all 2⁹ assignments are checked and none works.
   Contextuality.
9. The PBR theorem (2012): the wavefunction is ontic (given its assumptions).
10. Many worlds (Everett 1957): decoherence, branching; the probability problem; the Deutsch–Wallace decision-theoretic
    derivation of the Born rule (bridge to Part 33).
11. Bohmian mechanics. Built: the guidance equation integrated for the double slit, with the famous trajectories
    computed; non-locality made explicit.
12. GRW spontaneous collapse (1986). Built: collapse simulation with the GRW rate parameters; tests (CSL bounds,
    cited).
13. QBism and relational quantum mechanics.
14. Wigner's friend and Frauchiger–Renner (2018): the no-go theorem's assumptions, each set as a Price List
    claim.
15. The free will theorem (Conway and Kochen 2006), previewing Part 32.
16. Industry: quantum computing and its interpretation-neutrality; Bell tests in quantum cryptography (device-
    independent QKD).
17. Recap and Problems.

*Built:* `reasoner.quantum` (small Hilbert-space simulator; CHSH enumeration; Peres–Mermin search; Bohmian
integrator; GRW collapse).
*Wall:* Bell (no local hidden variables); Kochen–Specker (no non-contextual values); Frauchiger–Renner.
*Price List:* Maudlin's measurement triad (the wavefunction is complete; it always evolves by Schrödinger's
equation; measurements have definite outcomes).
*Visuals:* the CHSH correlation curve with the classical bound as a dashed hexagon edge; Bohmian trajectories
fanning through two slits; the Peres–Mermin square refusing to fill.
*References:* Maudlin, *Philosophy of Physics: Quantum Theory*; Albert, *Quantum Mechanics and Experience*; Bell,
*Speakable and Unspeakable*; Wallace, *The Emergent Multiverse*; Dürr, Goldstein and Zanghì, *Quantum Physics without
Quantum Philosophy*; Myrvold (SEP), "Philosophical Issues in Quantum Theory".

### Act VI · Mind and Meaning

#### Part 27 · Sense and Reference (~55)
1. The School of Names: Gongsun Long's white horse dialogue as a puzzle about reference and predication.
2. Frege's puzzle (1892): a = a vs a = b; sense (Sinn) and reference (Bedeutung); Frege's compositionality.
3. Russell's theory of descriptions (1905): "the present king of France is bald", formalized; the scope ambiguity
   of negation, shown as two trees.
4. Strawson's presupposition; Donnellan's referential vs attributive uses.
5. Kripke's modal, epistemic and semantic arguments against descriptivism; the Gödel/Schmidt case; the causal-
   historical picture.
6. Putnam's Twin Earth (1975): "meanings ain't in the head"; semantic externalism; Burge's arthritis.
7. Kaplan's indexicals: character and content; "I am here now" is a priori but contingent.
8. Tarski–Davidson: truth-conditional semantics; a T-theory for a toy language.
9. Montague (1970): "English as a formal language". λ-calculus, types e and t.
10. Built: a Heim–Kratzer semantic parser. The tree of a sentence is computed with λ-terms beta-reducing up to a
    truth value in a model.
11. Generalized quantifiers (Barwise and Cooper 1981): conservativity; "most" is not first-order definable, proved
    by the Reasoner with an Ehrenfeucht–Fraïssé game on finite models.
12. Intensional semantics: propositions as sets of worlds; the problem of logical omniscience.
13. Belief reports and opacity: Frege's answer, Russellianism (Salmon, Soames), hidden indexicals.
14. Dynamic semantics: donkey sentences ("every farmer who owns a donkey beats it"); DRT and dynamic predicate logic
    (meaning as context change), built as a small example.
15. Industry: formal semantics in NLP (semantic parsing to SQL and logical forms); where LLMs succeed and fail on
    scope and quantifiers (benchmarks cited).
16. Recap and Problems.

*Built:* `reasoner.semantics` (typed λ-calculus over a model; a Heim–Kratzer fragment; generalized quantifiers; EF
games; a DPL fragment).
*Wall:* Frege's puzzle and the failure of substitution in belief contexts; the inexpressibility of "most" in FOL.
*Price List:* Frege's puzzle (names have only referents; co-referential names are substitutable; Lois believes
Superman flies but not that Clark flies).
*Visuals:* the syntax tree with λ-terms flowing upward; scope trees rotating; two models in an EF game with pebbles.
*References:* Lycan; Heim and Kratzer; Gamut; Kripke; Kaplan, "Demonstratives"; Barwise and Cooper 1981; Kamp and
Reyle, *From Discourse to Logic*.

#### Part 28 · Meaning in Use (~55)
1. Wittgenstein's *Tractatus* (1921): the picture theory; truth tables invented (callback to Part 2).
2. The *Investigations* (1953): meaning as use; language games; family resemblance.
3. Rule-following (Kripke's *Wittgenstein on Rules and Private Language*, 1982): plus vs quus, built. Every finite
   record of use fits both; the skeptical paradox and its "solution".
4. The private language argument.
5. Quine's radical translation (1960): gavagai; the indeterminacy of translation and the inscrutability of
   reference (proxy functions).
6. Davidson's radical interpretation; the principle of charity; truth and meaning together.
7. Speech acts: Austin's performatives; Searle's taxonomy.
8. Grice: the cooperative principle and the maxims; conversational implicature; cancellability.
9. Scalar implicature: "some" → "not all".
10. The Rational Speech Acts model (Frank and Goodman 2012). Built: a literal listener, a pragmatic speaker and a
    pragmatic listener as recursive Bayesian reasoning; it derives "some, not all" and reference games.
11. Lewis's *Convention* (1969) and signalling games; Skyrms's evolution of meaning. Built: Roth–Erev
    reinforcement learning on a 2×2 and a 3×3 signalling game; with seeds and spreads, how often perfect signalling
    emerges vs partial pooling equilibria.
12. Structuralism's relational meaning (Saussure; Harris's distributional hypothesis) and word vectors (callback to
    *AI, Built* Part 3).
13. Do LLMs mean anything? The octopus argument (Bender and Koller 2020); the symbol grounding problem (Harnad 1990);
    replies (Piantadosi and Hill; Mollo and Millière 2023 on vector grounding); inferentialism (Brandom).
14. A probe on the AI series' novels model (`explainer.ai.novels`): what it represents about referents in its
    training stories, and what that does and doesn't show.
15. Recap and Problems.

*Built:* `reasoner.pragmatics` (RSA; signalling games; plus vs quus).
*Wall:* Kripkenstein (no fact about past use fixes a rule); Quine's indeterminacy.
*Price List:* the grounding question (meaning requires reference; reference requires causal contact; text-only
models have none; LLM outputs are meaningful).
*Visuals:* the RSA listener and speaker as alternating matrices sharpening; signalling-game urns filling; plus and
quus diverging only past 57.
*References:* Wittgenstein; Kripke 1982; Quine, *Word and Object*; Davidson, *Inquiries into Truth and
Interpretation*; Grice, *Studies in the Way of Words*; Goodman and Frank 2016 (TiCS); Skyrms, *Signals*; Bender and
Koller 2020 (ACL).

#### Part 29 · Being and Time-Consciousness (~55): phenomenology, existentialism, hermeneutics
1. Brentano's thesis: intentionality as the mark of the mental (previews Part 30).
2. Husserl: the phenomenological reduction (epoché); noesis and noema; eidetic variation (shown as variation over a
   parameter space, labeled `analogy`).
3. Husserl's analysis of time-consciousness: retention, primal impression, protention. His own diagram (1905)
   animated.
4. Heidegger's *Being and Time* (1927): being-in-the-world; ready-to-hand vs present-at-hand; the hammer.
5. Dreyfus's *What Computers Can't Do* (1972): the phenomenological critique of symbolic AI; what deep learning
   answered and what it didn't.
6. The frame problem (McCarthy and Hayes 1969): the logical version and Dennett's robot; solutions in logic
   (successor-state axioms) and the philosophical residue.
7. Merleau-Ponty: the body schema; embodied, embedded, enactive, extended cognition (4E).
8. Sartre: existence precedes essence; bad faith. Beauvoir: *The Second Sex*; situated freedom.
9. Kierkegaard and Nietzsche: the individual, value creation, eternal recurrence as a thought experiment.
10. Hermeneutics: Gadamer's fusion of horizons; the hermeneutic circle (part ↔ whole), with an iteration toy
    labeled `analogy`.
11. Structuralism and post-structuralism: Saussure's differential meaning; Derrida's différance, carefully stated
    and with the critiques.
12. Foucault: power/knowledge; the panopticon; the datafied subject.
13. The Frankfurt school and Habermas: communicative rationality; the ideal speech situation (previews Part 39).
14. Kyoto school (Nishida's basho) and the dialogue with Buddhism.
15. The analytic–continental divide and its bridges (Dreyfus–McDowell debate, phenomenology and cognitive science:
    neurophenomenology, Varela).
16. Recap and Problems.

*Built:* Husserl's time diagram; a successor-state axiom planner showing the frame problem solved and not solved;
Saussure on embeddings (the meaning of a word is invariant under rotations of the whole space, computed with
Procrustes).
*Wall:* the frame problem (relevance is not formalizable in general, according to its critics).
*Visuals:* Husserl's retention diagonal; the hammer withdrawing into use; the hermeneutic circle as a spiral.
*References:* Moran, *Introduction to Phenomenology*; Zahavi, *Husserl's Phenomenology*; Dreyfus, *Being-in-the-World*
and *What Computers Still Can't Do*; Shanahan (SEP), "The Frame Problem"; Gallagher and Zahavi, *The
Phenomenological Mind*; Varela, Thompson and Rosch, *The Embodied Mind*.

#### Part 30 · Mind and Machine (~55)
1. Descartes's dualism and Elisabeth of Bohemia's interaction problem (1643); Avicenna's floating man.
2. Behaviorism (Ryle's ghost in the machine); the identity theory (Place, Smart).
3. Functionalism: Putnam's multiple realizability (1967); machine-table states. Built: one probabilistic automaton
   "pain role" realized in two substrates, with behavior identical by construction.
4. Turing's 1950 paper: the imitation game, and his nine objections answered one by one.
5. Searle's Chinese room (1980); the systems, robot and brain-simulator replies. Built: a rulebook that passes a
   narrow test.
6. Block's Blockhead (1981): a lookup table that passes the test. Its size is computed (for a 1-hour conversation it
   exceeds the atoms of the universe by many orders), so intelligence is about how, not just what.
7. Block's China brain; absent qualia.
8. Supervenience: weak, strong and global, defined modally and checked on toy world sets.
9. Kim's causal exclusion argument (1998), formalized; the overdetermination and autonomy replies.
10. Emergence: weak vs strong. Built: Conway's Life with gliders and guns; weak emergence and simulation-only
    derivability (Bedau).
11. Eliminativism (Churchlands): folk psychology as a theory.
12. Intentionality naturalized: Dretske's information-theoretic content (mutual information, from Part 1 of the AI
    series); Millikan's teleosemantics; Fodor's asymmetric dependence.
13. The language of thought (Fodor 1975) vs connectionism; the systematicity challenge (Fodor and Pylyshyn 1988) and
    neural networks' answers (compositional generalization benchmarks, cited).
14. The extended mind (Clark and Chalmers 1998): Otto's notebook; parity principle; the phone and the LLM.
15. Representation in interpretability: what makes a direction in activation space a representation (Shea's
    *Representation in Cognitive Science*; linear probes and their limits, callback to *AI, Built* Part 30).
16. Recap and Problems.

*Built:* `reasoner.mind` (multiply realized automata; supervenience checker; Life; Blockhead's size).
*Wall:* causal exclusion; the Chinese room's dilemma for functionalism (contested; both sides shown).
*Price List:* the mind–body tetrad (the mental is not physical; mental events cause physical ones; the physical
is causally closed; no systematic overdetermination).
*Visuals:* two automata in different materials running in lockstep; the exclusion argument as an arrow being
pre-empted; a Life glider gun firing.
*References:* Kim, *Philosophy of Mind*; Turing 1950; Searle 1980 (BBS) with commentaries; Block 1981 (Phil Rev);
Kim, *Mind in a Physical World*; Bedau 1997; Shea, *Representation in Cognitive Science*.

#### Part 31 · Consciousness (~60)
1. Nagel's bat (1974): what it is like.
2. The hard problem (Chalmers 1995) vs the easy problems.
3. Jackson's Mary (1982); the ability hypothesis (Lewis, Nemirow) and the acquaintance reply.
4. Zombies: the conceivability argument formalized via two-dimensional semantics (callback to Part 22).
5. The explanatory gap (Levine); the phenomenal concept strategy.
6. Illusionism (Frankish, Dennett); the meta-problem (Chalmers 2018).
7. Panpsychism and the combination problem; Russellian monism.
8. Global workspace theory (Baars; Dehaene). Built: a toy workspace network with ignition (non-linear broadcast above
   a threshold), reproducing a masking curve.
9. Higher-order theories (Rosenthal, Lau).
10. Integrated information theory (Tononi; IIT 4.0, 2023). Built: Φ computed exhaustively for small logic-gate
    networks, using a simplified measure that is labeled as such.
11. Aaronson's expander objection (2014), computed: a simple grid or expander can reach high Φ with no plausible
    experience.
12. Predictive processing and the free-energy principle (Friston; Clark): variational free energy (callback to the AI
    series' ELBO). Built: a toy active-inference agent.
13. The adversarial collaboration of IIT vs GNWT (Cogitate, published 2025; results cited), and the 2023 open letter
    controversy over IIT.
14. Animal consciousness: the Cambridge (2012) and New York (2024) declarations; markers.
15. AI consciousness: indicator properties derived from the theories (Butlin, Long et al. 2023); LLM self-reports and
    why they are weak evidence; AI moral patienthood under uncertainty (Long, Sebo et al. 2024).
16. Recap and Problems.

*Built:* `reasoner.consciousness` (workspace ignition; small-system Φ; active inference).
*Wall:* the hard problem (a priori entailment from physical to phenomenal truths seems to fail); IIT's
counterexamples.
*Price List:* the zombie argument (zombies are conceivable; conceivability entails possibility; possibility of
zombies refutes physicalism; physicalism).
*Visuals:* the workspace lighting up on ignition; Φ's cut search over bipartitions; the 2D zombie matrix.
*References:* Chalmers, *The Conscious Mind* and *The Character of Consciousness*; Dennett; Seth, *Being You*;
Dehaene, *Consciousness and the Brain*; Albantakis et al. 2023 (IIT 4.0); Butlin, Long et al. 2023 (arXiv); Frankish
(ed.), *Illusionism*.

#### Part 32 · Free Will (~55)
1. The dilemma: determinism undermines freedom; indeterminism makes it luck.
2. Aristotle and the Stoics: Chrysippus's cylinder; the lazy argument.
3. The consequence argument (van Inwagen 1983) formalized with the N operator: rules α and β.
4. McKay and Johnson (1996): rule β is invalid, shown on a Kripke model built by the Reasoner. The repaired
   versions and the debate.
5. Frankfurt cases (1969): the principle of alternative possibilities; flickers of freedom.
6. Compatibilism: hierarchical desires (Frankfurt); reasons-responsiveness (Fischer and Ravizza).
7. Libertarianism: agent causation, event-causal views (Kane). The luck objection and van Inwagen's rollback
   argument. Built: a rollback simulator shows that replays converge to frequencies.
8. Hard incompatibilism (Pereboom); Galen Strawson's basic argument as a regress.
9. P. F. Strawson's "Freedom and Resentment" (1962): reactive attitudes.
10. Libet (1983): the readiness potential. Schurger, Sitt and Dehaene (2012): a leaky stochastic accumulator
    reproduces it. Built: the accumulator generates RPs from noise.
11. Predictability and self-prediction: MacKay's argument; a diagonal proof that no agent can, in general, act on a
    prediction of itself. Newcomb's predictor previews Part 33.
12. The free will theorem (Conway and Kochen) and what it does and doesn't show.
13. Moral luck (Nagel, Williams): resultant, circumstantial, constitutive.
14. Responsibility for artificial agents: responsibility gaps (Matthias 2004) and who answers for what (previews
    Part 41).
15. Recap and Problems.

*Built:* `reasoner.freewill` (the N-operator model checker for rule β; rollback; leaky accumulator; self-prediction
diagonal).
*Wall:* the McKay–Johnson countermodel (but stronger rules survive); the self-prediction diagonal.
*Price List:* the free will tetrad (some acts are free; free acts require alternative possibilities; determinism
rules out alternatives; determinism or randomness holds), with the PhilPapers 2020 shares.
*Visuals:* rollback replays fanning out from one moment; the accumulator crossing threshold; the Frankfurt
intervener hovering unseen.
*References:* Kane (ed.), *Oxford Handbook of Free Will*; van Inwagen, *An Essay on Free Will*; Fischer, Kane,
Pereboom and Vargas, *Four Views on Free Will*; McKenna and Pereboom, *Free Will: A Contemporary Introduction*;
Schurger et al. 2012 (PNAS).

### Act VII · Value

#### Part 33 · Rational Choice (~60): decision theory
1. Preferences: completeness, transitivity; the money pump, built.
2. Expected utility: Bernoulli and the St Petersburg paradox (1738); log utility; Menger's super-St Petersburg.
3. The von Neumann–Morgenstern theorem: the axioms and the construction of u; proof sketch. Indifference curves are
   parallel lines in the Marschak–Machina triangle (`Simplex`).
4. The Allais paradox (1953): the fanning-out in the triangle, drawn; Kahneman and Tversky's data (cited).
5. Savage (1954): acts, states, consequences; the sure-thing principle; subjective probability from preference.
6. Ellsberg (1961): ambiguity aversion; maxmin EU (Gilboa and Schmeidler 1989).
7. Risk-weighted EU (Buchak 2013): r(p) over the decumulative distribution; Allais accommodated.
8. Prospect theory: value function and probability weighting; industry and behavioral economics.
9. The Kelly criterion: maximize E[log wealth], derived; simulated growth vs ruin; how industry uses it in betting,
   portfolio sizing and fractional Kelly.
10. The Pasadena game (Nover and Hájek 2004): expectation undefined.
11. Newcomb's problem (Nozick 1969). Built: a predictor with accuracy p; one-box and two-box payoffs computed.
12. Evidential vs causal decision theory: Jeffrey's desirability; Lewis and Joyce's causal expected utility via
    imaging; the smoking lesion; death in Damascus; ratifiability.
13. Functional decision theory (Yudkowsky and Soares 2017), transparent Newcomb, Parfit's hitchhiker; and the
    critiques.
14. Dynamic choice: sequential consistency; Ulysses and the sirens; resolute vs sophisticated choice (McClennen).
15. The value of information: Good's theorem (1967), proved: free information never hurts an EU maximizer; when it
    fails (non-EU agents, Buchak; Newcomb-like cases).
16. The two-envelope paradox: the hidden improper prior, computed.
17. Recap and Problems.

*Built:* `reasoner.decision` (EU and RDU calculators; Machina triangle; Kelly simulator; Newcomb predictor; EDT vs
CDT engine on decision graphs; value-of-information checker).
*Wall:* Allais and Ellsberg (no EU representation of common preferences); Newcomb (EDT and CDT disagree, each with
counterexamples).
*Price List:* the Newcomb cluster (dominance; maximize expected value; the predictor is reliable; the box contents
are fixed), with PhilPapers 2020 shares.
*Visuals:* parallel indifference lines in the triangle vs fanned Allais lines; Kelly wealth paths fanning on a log
scale; the Newcomb boxes with the predictor's record.
*References:* Peterson; Savage, *The Foundations of Statistics*; Jeffrey, *The Logic of Decision*; Joyce, *The
Foundations of Causal Decision Theory*; Buchak, *Risk and Rationality*; Gilboa, *Theory of Decision under
Uncertainty*; Ahmed, *Evidence, Decision and Causality*.

#### Part 34 · Games and the Social Contract (~60)
1. Hobbes's state of nature as a prisoner's dilemma; the Leviathan as a mechanism.
2. Nash equilibrium: definition; existence via Kakutani, sketched with best-response correspondences crossing.
3. The prisoner's dilemma and the tragedy of the commons; Ostrom's commons governance (and her design principles).
4. Rousseau's stag hunt: payoff vs risk dominance; equilibrium selection.
5. Backward induction and the centipede game; the paradox (Binmore, Bicchieri, Aumann 1995 on common knowledge of
   rationality).
6. Correlated equilibrium (Aumann 1974); conventions and traffic lights.
7. The iterated prisoner's dilemma and Axelrod's tournaments (1980). Built: a strategy zoo (TFT, Grim, Pavlov,
   Joss, Random, generous TFT …) rerun with noise; results with seeds.
8. Press and Dyson (2012): zero-determinant strategies, derived and played; the evolutionary response (Stewart and
   Plotkin).
9. Evolutionary game theory (callback to Part 19): replicator dynamics for the iterated PD; cooperation's rise and
   collapse.
10. Skyrms's *Evolution of the Social Contract*: the Nash demand game; basins of attraction of fair division,
    computed.
11. Bargaining: Nash's axioms and solution, derived; Kalai–Smorodinsky; Rubinstein's alternating offers.
12. Cooperative games: the core; the Shapley value from its axioms, with uniqueness proved. Industry: SHAP in
    ML explanation (and its limits; callback in Part 41).
13. Mechanism design: the revelation principle; Vickrey and VCG truthfulness, proved; Myerson's optimal auction.
14. Industry: ad auctions (GSP vs VCG), spectrum auctions, kidney exchange (Roth), school choice (Gale–Shapley
    deferred acceptance, built, with its stability and strategy-proofness for proposers).
15. Recap and Problems.

*Built:* `reasoner.games` (equilibria of bimatrix games via support enumeration; tournaments; ZD strategies;
replicators; Shapley; VCG; Gale–Shapley).
*Wall:* the PD (individual rationality leads to a collectively worse outcome); the paradox of backward induction.
*Visuals:* the tournament as a population river; Kakutani's correspondences crossing; Skyrms's basins on a simplex;
the deferred-acceptance proposals rippling.
*References:* Osborne and Rubinstein; Binmore, *Game Theory and the Social Contract*; Skyrms, *Evolution of the
Social Contract* and *The Stag Hunt*; Axelrod, *The Evolution of Cooperation*; Nisan et al., *Algorithmic Game
Theory*; Roth, *Who Gets What — and Why*.

#### Part 35 · The Right and the Good (~60): normative ethics
1. Three questions: what is good, what is right, what kind of person to be.
2. Consequentialism: Bentham's felicific calculus; Mill's higher pleasures; Sidgwick's *Methods*.
3. Theories of welfare: hedonism, desire satisfaction, objective lists; Nozick's experience machine.
4. Harsanyi's aggregation theorem (1955): vNM individuals + Pareto + vNM society ⇒ a weighted sum of utilities;
   proof sketch, with the geometry of utility possibility sets.
5. Interpersonal comparisons; Harsanyi vs Diamond's fairness objection (1967).
6. Distribution: utilitarianism vs prioritarianism vs egalitarianism; Parfit's levelling-down objection; Gini and
   Atkinson computed.
7. Kant: the formulas of the categorical imperative.
8. Universalizability as a consistency test. Built: a toy world where maxims are universalized and checked for
   contradiction in conception (the lying promise collapses) and in will; the known counterexamples (the
   "false positives") are run too.
9. Agent-relative constraints and the paradox of deontology (Scheffler); consequentializing (Portmore, Dreier).
10. The trolley problem (Foot 1967; Thomson 1985): switch, footbridge, loop; the doctrine of double effect; the Moral
    Machine data (Awad et al. 2018, cited).
11. Contractualism (Scanlon): reasonable rejection; the aggregation problem (Transmitter Room) and partial
    aggregation.
12. Virtue ethics: Aristotle's mean, eudaimonia, practical wisdom; Confucian ren and li; Mencius's four sprouts;
    situationism's challenge (Doris; Harman).
13. Care ethics (Gilligan, Noddings).
14. Moral uncertainty: maximizing expected choiceworthiness; intertheoretic comparisons; variance normalization; the
    moral parliament. Built and run on test cases.
15. Recap and Problems.

*Built:* `reasoner.ethics` (aggregators; inequality measures; universalizability tester; trolley variants; moral-
uncertainty aggregators).
*Wall:* the paradox of deontology; Harsanyi's theorem (Pareto plus rationality forces utilitarian form).
*Price List:* the trolley cluster (minimize deaths; don't use a person as a mere means; switch is permissible;
footbridge isn't), with PhilPapers 2020 shares on the trolley questions.
*Visuals:* utility possibility frontiers with weighted-sum lines; the Kantian toy world collapsing under
universalized lying; the trolley tracks with a vote tally.
*References:* Kagan, *Normative Ethics*; Shafer-Landau; Sidgwick; Kant, *Groundwork*; Parfit, *On What Matters*;
Scanlon, *What We Owe to Each Other*; Hursthouse, *On Virtue Ethics*; MacAskill, Bykvist and Ord, *Moral Uncertainty*;
Van Norden, *Introduction to Classical Chinese Philosophy*.

#### Part 36 · Weighing Lives (~55): population ethics and the far future
1. Parfit's question: which outcomes are better when different people exist?
2. Total, average, critical-level, and variable-value views, each a formula.
3. The repugnant conclusion. `ParfitBars`, with A and Z drawn.
4. The mere addition paradox: A, A+, B−, B, step by step.
5. Arrhenius's impossibility theorems (2000): six plausible conditions, no axiology satisfies all. Built: an
   exhaustive check over small populations finds the violation for each candidate view.
6. The asymmetry; person-affecting views; the non-identity problem.
7. Discounting the future: the Ramsey formula r = δ + ηg, derived; Stern vs Nordhaus; the social cost of carbon
   (published values cited).
8. Longtermism (Greaves and MacAskill 2021) and existential risk; estimates as estimates (cited, labeled).
9. Fanaticism and Pascal's mugging; Wilkinson's defense of fanaticism; Beckstead and Thomas's trilemma.
10. Infinite ethics: Pareto and anonymity are incompatible for infinite utility streams (Diamond 1965; Basu and
    Mitra 2003), proved; overtaking criteria.
11. Effective altruism: QALYs and DALYs; cost-effectiveness analysis; the critiques (Srinivasan; Crary).
12. Industry: cost–benefit analysis, the value of a statistical life (published figures cited), health technology
    assessment.
13. Recap and Problems.

*Built:* `reasoner.population` (axiology library; Arrhenius condition checker; discounting; infinite stream
comparisons).
*Wall:* Arrhenius; Pareto vs anonymity for infinite populations.
*Price List:* the repugnant conclusion set (mere addition doesn't make things worse; non-anti-egalitarianism;
transitivity; A is better than Z).
*Visuals:* Parfit's bars widening and lowering; the mere-addition staircase; infinite streams as sequences of bars
fading right.
*References:* Parfit, *Reasons and Persons* Part IV; Arrhenius, *Population Ethics* (draft) and 2000 (Econ & Phil);
Greaves 2017 (Phil Compass), "Population axiology"; Broome, *Weighing Lives*; Stern Review; Askell, *Pareto Principles
in Infinite Ethics*.

#### Part 37 · Is and Ought (~55): metaethics
1. Hume's law (1739): no ought from is. Prior's counterexamples (1960); Schurz's theorem (1997) on the is–ought gap in
   alethic-deontic logic, stated and checked on small models.
2. Moore's open-question argument (1903); the naturalistic fallacy; the paradox of analysis.
3. Moral realism: non-naturalism (Parfit, Enoch, Shafer-Landau); Cornell realism (Boyd, Brink); the supervenience
   challenge (Blackburn).
4. Error theory (Mackie 1977): queerness; the companions-in-guilt reply (epistemic normativity).
5. Expressivism: Ayer, Stevenson, Blackburn's quasi-realism.
6. The Frege–Geach problem: "if lying is wrong, then getting your brother to lie is wrong" in a valid modus ponens.
7. Gibbard's norm-world pairs (1990, 2003). Built: a semantics of factual-normative worlds that makes the inference
   valid; Schroeder's critique (*Being For*, 2008) and the negation problem.
8. Relativism and moral disagreement; Harman; the moral twin earth argument (Horgan and Timmons).
9. Constructivism: Rawls's Kantian constructivism, Korsgaard, Street.
10. Evolutionary debunking: Street's Darwinian dilemma (2006). Built: norms evolving under fitness payoffs
    track fitness, not any independent truth, in a toy model labeled `analogy`. The third-factor replies.
11. Moral psychology: Haidt's social intuitionist model; moral foundations (data cited); Greene's dual process; the
    trolley fMRI debate.
12. Mencius vs Xunzi: human nature good (性善) or bad (性恶), with the sprouts vs the craftsman as two learning
    theories.
13. Reflective equilibrium (Goodman, Rawls): coherence between principles and judgments. Built: as an optimization
    that drops the fewest weighted commitments (MaxSAT with the Part 2 solver).
14. Moral progress: what it would mean, on each metaethical view.
15. Recap and Problems.

*Built:* `reasoner.deontic` (alethic-deontic models; Schurz's gap checker); `reasoner.expressivism` (norm-world
pairs); reflective equilibrium as weighted MaxSAT.
*Wall:* Schurz's is–ought theorem; Frege–Geach for simple expressivism.
*Price List:* Mackie's triad (moral claims purport to state objective facts; there are no such facts; some moral
claims are true), with PhilPapers 2020 shares on moral realism.
*Visuals:* the is–ought gap as a wall in a two-layer model; norm-world pairs eliminated by a conditional;
reflective equilibrium as a constraint network relaxing.
*References:* Miller, *Contemporary Metaethics*; Gibbard, *Thinking How to Live*; Schroeder, *Being For* and
*Noncognitivism in Ethics*; Mackie, *Ethics*; Street 2006 (Phil Studies); Schurz, *The Is-Ought Problem*; Ivanhoe and
Van Norden (eds.), *Readings in Classical Chinese Philosophy*.

#### Part 38 · Justice (~55): political philosophy
1. Plato's *Republic* and Thrasymachus: is justice the interest of the stronger?
2. The social contract: Hobbes, Locke, Rousseau (callback to Part 34's games).
3. Rawls's *A Theory of Justice* (1971): the original position, the veil of ignorance, the two principles and their
   lexical order.
4. Maximin vs average utility (Harsanyi 1975): the debate, computed. The choice behind the veil under each rule
   across many distributions, and what risk attitude each assumes.
5. The difference principle, drawn on a production possibility frontier.
6. Nozick's *Anarchy, State, and Utopia* (1974): entitlement theory; Wilt Chamberlain, run as a toy economy.
7. Luck egalitarianism (Dworkin, Cohen, Arneson). Dworkin's auction and envy-free allocations. Built: competitive
   equilibrium from equal incomes (Varian 1974), envy-freeness checked.
8. Capabilities (Sen, Nussbaum).
9. Sen's liberal paradox (1970): the impossibility of a Paretian liberal, proved; Lady Chatterley's Lover.
10. Liberty: Berlin's two concepts; republican freedom as non-domination (Pettit).
11. Fair division: cut-and-choose; Selfridge–Conway for three (drawn); bounded envy-free cake cutting (Aziz and
    Mackenzie 2016). Industry: rent division (Spliddit).
12. Communitarians (Sandel, MacIntyre, Walzer) and the Confucian alternative (role ethics; meritocracy debates, Bai
    Tongdong; Chan).
13. Global justice: Singer's drowning child (1972); Pogge; the cosmopolitan vs statist debate.
14. Justice and AI: distributive questions about automation and compute; the Rawlsian case for alignment
    principles chosen behind a veil (Gabriel 2020), as a preview of Parts 41–42.
15. Recap and Problems.

*Built:* `reasoner.justice` (veil-of-ignorance choice rules; envy-free equilibrium; Selfridge–Conway; Sen's
paradox checker).
*Wall:* Sen's liberal paradox.
*Price List:* Nozick's Wilt cluster (D1 is just; voluntary transfers from a just distribution preserve justice;
D2 arises by voluntary transfers; D2 is unjust).
*Visuals:* the veil sliding over a population; the difference principle on a frontier; the cake being cut and
trimmed in Selfridge–Conway.
*References:* Kymlicka; Rawls; Nozick; Dworkin, *Sovereign Virtue*; Sen, *The Idea of Justice*; Brams and Taylor,
*Fair Division*; Pettit, *Republicanism*; Bai, *Against Political Equality*.

#### Part 39 · The Arithmetic of Democracy (~60): social choice
1. Condorcet's paradox (1785): a cycle from three transitive voters; the rotating triangle.
2. The probability of a Condorcet cycle under impartial culture: Guilbaud's limit (≈ 8.77% for three alternatives),
   derived and checked by simulation; how it grows with the number of alternatives.
3. Borda vs Condorcet; the voting rules zoo (plurality, IRV, approval, Copeland, Kemeny, Schulze, Borda), with the
   same profile giving different winners.
4. May's theorem (1952): majority rule characterized, proved.
5. Arrow's theorem (1951): the conditions; Geanakoplos's pivotal voter proof drawn as a sweep.
6. Arrow by computer: the 2-voter, 3-alternative case encoded as SAT and proved unsatisfiable by the Part 2 solver
   (after Tang and Lin 2009), with the MUS shown.
7. Gibbard–Satterthwaite (1973–75): manipulability; computer-found manipulations of each rule.
8. Computational resistance: manipulation is NP-hard for some rules (Bartholdi, Tovey and Trick 1989); Kemeny is
   NP-hard.
9. Domain restrictions: single-peaked preferences; Black's median voter theorem, proved; Hotelling–Downs.
10. Cardinal voting: range, majority judgment (Balinski and Laraki); quadratic voting (Lalley and Weyl), with
    industry uses (Gitcoin; Colorado legislature, cited).
11. The Condorcet jury theorem, computed; its correlated-voter failures; epistemic democracy.
12. Diversity trumps ability (Hong and Page 2004), rebuilt; Thompson's critique (2014) checked.
13. Judgment aggregation: the doctrinal paradox; the discursive dilemma; List and Pettit's impossibility (2002);
    premise-based vs conclusion-based procedures.
14. Apportionment: the Alabama paradox (1880 census figures, cited) and Balinski–Young (1982).
15. Deliberative democracy (Habermas, Fishkin's polls) and liquid democracy.
16. Social choice for AI: RLHF aggregates annotators' comparisons; Bradley–Terry fitting implicitly behaves like the
    Borda count (Siththaranjan, Laidlaw and Hadfield-Menell 2023), demonstrated; Conitzer et al. 2024; collective
    constitutions (Anthropic and CIP 2023, cited).
17. Recap and Problems.

*Built:* `reasoner.vote` (profiles, rules, Condorcet cycles, impartial-culture simulation, SAT encodings of Arrow and
Gibbard–Satterthwaite cases, juries, judgment aggregation, apportionment).
*Wall:* Arrow; Gibbard–Satterthwaite; List–Pettit.
*Price List:* Arrow's set itself (unrestricted domain; Pareto; IIA; non-dictatorship; transitivity), with each
escape as a correction set and its real-world rule.
*Visuals:* `VoteLab` permutation ballots; the cycle triangle; the pivotal voter moving down the line; single-peaked
curves stacked over a left–right axis.
*References:* Arrow, *Social Choice and Individual Values*; Sen, *Collective Choice and Social Welfare*; Gaertner;
Brandt et al. (eds.); List and Pettit, *Group Agency*; Saari, *Chaotic Elections!*; Balinski and Young, *Fair
Representation*; Conitzer et al. 2024 (ICML position paper).

#### Part 40 · Beauty (~55): aesthetics
1. Plato's beauty and Aristotle's *Poetics* (mimesis, catharsis).
2. Hume's "Of the Standard of Taste" (1757): the true judges; read as a convergence claim and simulated as the
   wisdom of a crowd of critics (labeled `analogy`).
3. Kant's *Critique of Judgment*: disinterested pleasure; subjective universality; purposiveness without purpose;
   the sublime.
4. Pythagorean consonance: ratios 2:1, 3:2, 4:3; the Pythagorean comma 3¹²/2¹⁹ computed; equal temperament.
5. Helmholtz and Plomp–Levelt: sensory roughness. Built: the dissonance curve of harmonic timbres, with consonant
   intervals at its minima; Sethares's tuned timbres.
6. Symmetry: the 17 wallpaper groups, generated and classified (Fedorov 1891; the Alhambra).
7. Birkhoff's *Aesthetic Measure* (1933): M = O/C, computed on polygons; why it fails.
8. Information aesthetics: Bense, Moles; Berlyne's inverted U; Schmidhuber's compression-progress theory.
9. The golden ratio: the claims, tested (computed and cited); what survives.
10. What is art? Family resemblance (Weitz), the institutional theory (Dickie), Danto's artworld and Warhol's Brillo
    boxes.
11. Forgery and authenticity (Goodman; van Meegeren).
12. Mathematical beauty: Hardy's *Apology*; proofs as beautiful; the fMRI study (Zeki et al. 2014, cited).
13. Chinese aesthetics: Xie He's six principles of painting; 意境; Zhuangzi's Cook Ding as skill and flow.
14. AI art: authorship, copyright (US Copyright Office guidance; Thaler v. Perlmutter, cited), and whether a model's
    image can be art.
15. Recap and Problems.

*Built:* `reasoner.aesthetics` (tuning and roughness; wallpaper group generator and classifier; Birkhoff's measure;
compression-based "interestingness").
*Wall:* Hume's problem of taste (no rule settles disagreement, yet some judgments are better).
*Price List:* the paradox of taste (de gustibus non est disputandum; some art is better than other art; judgments
of beauty are based on feeling).
*Visuals:* the dissonance curve with consonant dips lighting up; wallpaper patterns tiling and their symmetry
elements flashing; the Pythagorean spiral of fifths not closing.
*References:* Gaut and Lopes (eds.); Kant, *Critique of the Power of Judgment*; Hume, *Of the Standard of Taste*;
Sethares, *Tuning, Timbre, Spectrum, Scale*; Conway, Burgiel and Goodman-Strauss, *The Symmetries of Things*; Danto,
*The Transfiguration of the Commonplace*; 李泽厚，《美的历程》.

### Finale · The Reasoners We Build

#### Part 41 · Fair Machines (~55): algorithmic fairness, privacy, explanation, responsibility
1. The COMPAS controversy (ProPublica 2016; Northpointe's response; cited) as the motivating case.
2. Fairness criteria: demographic parity, equalized odds, equal opportunity, calibration (sufficiency); as
   independence relations (Barocas, Hardt and Narayanan).
3. The impossibility results: Kleinberg, Mullainathan and Raghavan (2016); Chouldechova (2017), proved on screen.
   Built: a fairness auditor on synthetic data shows that with unequal base rates, no non-trivial classifier meets
   all three.
4. Which criterion is right? Equality of opportunity (Rawls, Roemer) and the philosophical readings of each metric
   (Hellman; Long).
5. Individual fairness: Dwork et al. (2012): "treat similar individuals similarly" as a Lipschitz condition.
6. Counterfactual fairness (Kusner et al. 2017) with Part 17's SCM engine; path-specific effects; the problem of
   "causal effects of race" (Kohler-Hausmann).
7. Discrimination: disparate treatment vs impact; statistical discrimination; what makes discrimination wrong
   (Hellman, Eidelson).
8. Privacy: the failures of anonymization (Netflix Prize de-anonymization, 2008; cited); differential privacy
   (Dwork, McSherry, Nissim and Smith 2006). Built: Laplace mechanism and composition; DP as a philosophical
   definition of privacy and its critics (contextual integrity, Nissenbaum).
9. Explanation: Shapley values and SHAP (callback to Part 34) and their limits; counterfactual explanations (Wachter,
   Mittelstadt and Russell 2017); the "right to explanation" debate (GDPR, EU AI Act; cited).
10. Opacity and trust: epistemic dependence on black boxes; the computational reliabilism view (Durán and Formanek).
11. Responsibility gaps (from Part 32): many hands; accountability structures in industry (model cards, audits,
    incident reporting).
12. Industry: fairness in lending, hiring and medicine (cited cases); how audits are actually done.
13. Recap and Problems.

*Built:* `reasoner.fairness` (criteria; impossibility demonstrations; counterfactual fairness via SCMs); `reasoner.dp`
(Laplace and exponential mechanisms; composition accounting).
*Wall:* Kleinberg–Chouldechova (calibration and balance can't both hold with unequal base rates).
*Price List:* the fairness trilemma, with each correction set paired with the institutions that chose it.
*Visuals:* score distributions sliding apart with their thresholds; the confusion-matrix tiles recoloring as the
threshold moves; the Laplace noise curve widening as ε shrinks.
*References:* Barocas, Hardt and Narayanan; Kleinberg et al. 2016 (ITCS 2017); Chouldechova 2017 (Big Data);
Dwork and Roth; Hellman, "Measuring Algorithmic Fairness" (2020); Nissenbaum, *Privacy in Context*.

#### Part 42 · Aligning Reasoners (~60): the finale
1. Wiener (1960): "we had better be quite sure that the purpose put into the machine is the purpose which we really
   desire." King Midas and the series' question: we have built calculating reasoners; what do we want them to
   calculate?
2. Goodhart's law: Manheim and Garrabrant's four variants (2018). Built: the regressional case computed
   (optimizing a noisy proxy, true utility falls off at high optimization pressure).
3. Specification gaming (cited catalogue); reward hacking in RL.
4. Value learning: inverse reinforcement learning; Armstrong and Mindermann's no free lunch for preferences (2018),
   that planner and reward can't be separated without assumptions. This is Hume's is–ought gap (Part 37) as a
   theorem about learning.
5. Cooperative inverse reinforcement learning (Hadfield-Menell et al. 2016).
6. The off-switch game (Hadfield-Menell et al. 2017). Built and solved: uncertainty about the objective gives an
   incentive to defer; overconfidence removes it.
7. Instrumental convergence: Omohundro, Bostrom; Turner et al.'s power-seeking theorems (2021), computed on small MDPs.
8. Embedded agency: Löb's theorem (callback to Part 7) and the Löbian obstacle to self-trusting agents; logical
   induction (Garrabrant et al. 2016), stated.
9. Corrigibility, myopia and the alignment problem as decision theory (callback to Part 33's Newcomb debates).
10. Whose values? Social choice for alignment (callback to Part 39); contractualist and Rawlsian proposals (Gabriel
    2020); moral uncertainty (Part 35) in a model's constitution; reflective equilibrium (Part 37) as a process.
11. Honesty, deception and the epistemology of model reports (callback to Parts 12 and 31): what would it mean to
    know that a model believes what it says?
12. Moral status of AI systems under uncertainty (callback to Part 31).
13. The Wall, complete: every row from Parts 1–42, read as one lesson about where calculation must hand over to
    judgment.
14. The Price List of the series: which philosophical bets the field of AI is already making, explicitly or not.
15. Back to Leibniz: calculemus, what it achieved, and what it never will.
16. Recap, the series map, and what to read next.

*Built:* `reasoner.alignment` (Goodhart toys; IRL ambiguity; off-switch game; power-seeking measures on MDPs).
*Wall:* no free lunch for preferences; the Löbian obstacle; and the full ledger.
*Price List:* the alignment cluster (we can specify what we want; optimization pressure is safe for a correct
specification; proxies are all we can specify; strong optimizers are coming).
*Visuals:* the proxy-vs-true utility curve bending over; the off-switch game tree with deference regions; the
complete Wall rising row by row; Leibniz's calculator in the last frame.
*References:* Russell, *Human Compatible*; Christian, *The Alignment Problem*; Gabriel 2020 (Minds & Machines);
Hadfield-Menell et al. 2016, 2017; Turner et al. 2021 (NeurIPS); Armstrong and Mindermann 2018 (NeurIPS); Demski and
Garrabrant 2019, *Embedded Agency*.

## 4. Phases

0. **Infrastructure** (one session):
   - the `videos/philosophy/` package (`__init__.py`), `philosophy_text_zh.json`, `philosophy_upload.json`,
     `PHILOSOPHY_ZH_GUIDE.md`, `LECTURE_GUIDE.md`;
   - `explainer/philosophy/` with `ACTS`, `PARTS`, the −600 to 2030 timeline (with a compressed scale before 1500),
     `chapter_card`, `series_map`, `wall_card` and `wall_ledger`, `price_list`, `payoff_card`, `reference_card`; the
     lecture cards are reused from `explainer.ai.lecture`;
   - the visual instruments (`ArgumentMap`, `PriceList`, `WorldGraph`, `SpheresView`, `Simplex`, `TruthTable`,
     `ProofTree`, `Tableau`, `Lattice`, `CausalDAG`, `SpacetimeView`, `Tournament`, `VoteLab`, `ParfitBars`);
   - the Reasoner's core (`reasoner.prop` with MUS/MCS, `reasoner.fol`, `reasoner.modal`) with `tests/philosophy/`;
   - tooling: add `philosophy` to `tools/make.py`'s `BILINGUAL`; the QA tools that hard-code `ai` take a series
     argument; top-level README and CLAUDE.md entries.
1. **Pilot: Part 2 (The Laws of Thought).** It builds the SAT engine and the Price List that every later part uses,
   exercises the main instruments, and has a natural Wall. Delivered in English and Chinese, with previews and
   contact sheets. **Review with the user**, then lock the standard.
2. **Part 1 (Calculemus)**, which needs the devices to exist in order to introduce them.
3. **Roll-out in series order, Parts 3 → 42.** Each part goes through:
   - the frontier sweep, and a check of quotations and translations;
   - locking the chapter list;
   - the Reasoner module and its tests, then `compute.py`;
   - English scenes, then the QA gates;
   - Chinese narration and text, then the QA gates;
   - commit and push.

Scale: about 38 hours of video, about 230k narration words per language, roughly 4–6k lines of scene code per part,
and a Reasoner library of perhaps 20–30k lines with its tests. Expect one part per one or two long sessions.

## 5. Progress (updated as parts land)

| Part | State | Length |
|---|---|---|
| — | plan of record (this document) | — |
| 1 · Calculemus | scenes, English and Chinese narration and text, QA | ~50 min |
| 2 · The Laws of Thought | scenes, English and Chinese narration and text, QA | ~58 min |
| 3 · All and Some | scenes, English and Chinese narration and text, QA | ~65 min |
| 4 · Necessity and Possibility | scenes, English and Chinese narration and text, QA | ~50 min |
| 5 · Beyond True and False | scenes, English and Chinese narration and text, QA | ~59 min |
| 6 · Paradise and Paradox | scenes, English and Chinese narration and text, QA | ~51 min |
| 7 · The Limits of Proof | scenes, English and Chinese narration and text, QA | ~54 min |
| 8 · The Liar | scenes, English and Chinese narration and text, QA | ~49 min |
| 9 · What Is Mathematics About? | scenes, English and Chinese narration and text, QA | ~63 min |
| 10 · The Mind's Own Laws | scenes, English and Chinese narration and text, QA | ~50 min |
