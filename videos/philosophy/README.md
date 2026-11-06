# Philosophy, Built (哲学，从零搭建)

**Status: complete.** All forty-two parts are built, in English and Chinese, as `philosophy1` … `philosophy42` in
`videos/philosophy/`; each part's README lists its chapters, what is computed on screen, and its problems. The
chapter-by-chapter syllabus, the lecture standard every part meets and the progress table are in
[`SYLLABUS.md`](SYLLABUS.md). Shared instruments are in `explainer/philosophy/`, and the Reasoner, the library that
computes every number on screen, is in `explainer/philosophy/reasoner/` (47 modules), tested in `tests/philosophy/`.

This is a forty-two-part course in philosophy, in English and Chinese, running from the first arguments to the frontier of
research and to the places where philosophy is now engineering. It covers logic and the limits of proof, knowledge
and belief, science and causation, metaphysics and physics, language, mind and free will, and decision, ethics,
justice and democracy. It ends with fair and aligned machines. Each part is a **50–60 minute lecture** in the manner
of 3Blue1Brown: formulas derived on screen, one idea per frame drawn large, and a working toy for every central idea.
The course runs from a first-year introduction to the level of a doctoral qualifying exam, and it follows the
standard textbooks (listed part by part in the syllabus).

## The story: *Calculemus*

In 1685 Leibniz wrote that the only way to settle a dispute would be to make reasoning "as tangible as that of the
mathematicians … so that when there are disputes, we can simply say: *let us calculate*, and see who is right."

The series takes Leibniz literally. Part by part we **build the calculator**: a reasoning machine that gains a new
power in each act. It learns deduction, proof, necessity, knowledge, degrees of belief, induction, causation,
meaning, choice, cooperation, valuation and aggregation. Each time we ask three questions:

1. **What does calculation make clear?** The precise version of an ancient question, and the toy that answers it.
2. **Where does calculation stop?** Philosophy's sharpest results are impossibility theorems: Gödel, Tarski,
   Church–Turing, Bell, Kochen–Specker, Arrow, Gibbard–Satterthwaite, Sen, Lewis's triviality result, Fitch,
   Arrhenius, the fairness impossibility results, and the coordinated-attack problem. Each one marks a wall.
3. **What is the price of each way out?** When a set of plausible claims is inconsistent, every position in the
   debate is a choice of which claim to give up. The machine computes these choices exactly.

The finale returns to Leibniz. We now build calculating reasoners, and the last two parts ask what 2,500 years of
argument teach us about building them well.

## Four devices hold it together

1. **The Reasoner** (`explainer/philosophy/reasoner/`): a small, tested Python library built across the series and
   shown on screen as a toolbox that grows. It holds a SAT solver, a first-order tableau prover, a Kripke and LTL
   model checker, a dynamic-epistemic engine, a credence lab, an AGM revision engine, a structural causal model
   engine, a λ-calculus semantic parser, a decision lab, a game and tournament lab, a voting lab, a population-ethics
   calculator and a fairness auditor. Every part adds a module, and later parts reuse earlier modules on screen.
   For example, Part 39 checks a small case of Arrow's theorem with Part 2's SAT solver.
2. **The Wall** (`wall_card`, `wall_ledger`): philosophy's ledger of impossibility theorems, one row per part.
   Each row records the dream, the theorem that stops it, the year, and what the theorem forces us to give up. It
   plays the role of *Analysis, Built*'s ledger and *AI, Built*'s scoreboard.
3. **The Price List** (`price_list`): David Lewis said philosophical theories are never refuted conclusively, and
   the question is whether the price is right. For each great puzzle (mind and body, free will, the sorites,
   skepticism, personal identity, the repugnant conclusion) we state an inconsistent set of plausible claims. The
   Reasoner then enumerates its minimal correction sets, and these are exactly the possible positions. Each position
   is labeled with the philosophers who hold it and, where the 2020 PhilPapers Survey asked, the share of
   philosophers who accept it (cited). This is the Socratic elenchus run as SAT.
4. **The timeline strip** (−600 to 2030) on every chapter card, lit as the series reaches each idea, together with
   **payoff cards** ("where this comes back").

## The acts

| Act | Parts | Question |
|---|---|---|
| Prologue | 1 | What is an argument, and could reasoning be calculation? |
| **I. The Machinery of Reason** | 2–5 | What follows from what? (propositional, first-order, modal and non-classical logic) |
| **II. The Limits of Reason** | 6–9 | What can't proof, computation or truth reach? (sets, Gödel and Turing, the liar, the philosophy of mathematics) |
| **III. Knowledge** | 10–14 | What can we know, and how much should we believe? (Descartes to Kant, knowledge, common knowledge, credence, revision) |
| **IV. Science** | 15–19 | How does evidence become theory? (induction, statistics, causation, theories and reality, life) |
| **V. The World** | 20–26 | What is there, and how is it put together? (ontology, identity, possible worlds, God, laws and chance, space and time, the quantum) |
| **VI. Mind and Meaning** | 27–32 | How do words and minds reach the world? (sense and reference, meaning in use, phenomenology, mind, consciousness, free will) |
| **VII. Value** | 33–40 | What should we do, together? (choice, games, ethics, population ethics, metaethics, justice, social choice, beauty) |
| **Finale** | 41–42 | What do we want from the reasoners we build? (fair machines, aligned machines) |

## The parts

| # | Part | The calculation | The wall | Built toy |
|---|---|---|---|---|
| 1 | Calculemus | syllogistic as arithmetic | Meno's paradox, Zeno | Llull's wheels, Leibniz's characteristic numbers, the 256 moods |
| 2 | The Laws of Thought | truth tables, resolution, SAT | NP-completeness (Cook–Levin) | DPLL/CDCL solver; the Price List engine |
| 3 | All and Some | first-order models and proof | undecidability (Church 1936), Lindström | tableau prover; nonstandard models |
| 4 | Necessity and Possibility | Kripke semantics | correspondence limits (Goldblatt–Thomason) | Kripke and LTL model checker; Peterson's mutex verified |
| 5 | Beyond True and False | many-valued and paraconsistent logic | the sorites | n-valued matrix evaluator; the catuṣkoṭi as FDE |
| 6 | Paradise and Paradox | ZFC, ordinals, cardinals | Russell; the independence of CH | hereditarily finite sets; the ordinal spiral |
| 7 | The Limits of Proof | arithmetization | Gödel I and II, halting, Tarski, Löb | Gödel numbering, a quine, Turing machines, Goodstein |
| 8 | The Liar | Kripke's fixed points | revenge; Curry; Yablo | Kleene-jump and revision-sequence engines |
| 9 | What Is Mathematics About? | Curry–Howard | Benacerraf's dilemmas | a proof-checking type checker; Kripke models for intuitionism |
| 10 | The Mind's Own Laws | Spinoza's geometric method | Hume's problem; Kant's antinomies | the proof graph of Spinoza's *Ethics* |
| 11 | What Is Knowledge? | safety and sensitivity in world models | Gettier; anti-luminosity | possible-worlds knowledge checker |
| 12 | Knowledge Among Many | dynamic epistemic logic | coordinated attack; Fitch | muddy children; Zollman networks |
| 13 | Degrees of Belief | Dutch books, accuracy dominance | Bertrand's paradox | credence lab on the simplex; Sleeping Beauty |
| 14 | Changing Your Mind | AGM revision, conditionals | Gärdenfors; Lewis's triviality | Grove spheres; Dung argumentation solver |
| 15 | The Problem of Induction | Bayesian confirmation, learning in the limit | grue; no free lunch; Gold | inductive-bias zoo; a small Solomonoff mixture |
| 16 | Evidence by Numbers | likelihoods, p-values, e-values | Birnbaum; Lindley | p-hacking garden; testing by betting |
| 17 | Cause | structural causal models, do-calculus | causal Markov limits | SCM engine; PC algorithm; Halpern–Pearl |
| 18 | Theories and Reality | explanation, confirmation of theories | underdetermination; meta-induction | renormalization of an Ising model |
| 19 | Life | the Price equation | levels of selection | replicator dynamics; a kin-selection lab |
| 20 | What There Is | quantifiers, mereology, description logic | the special composition question | Boolean-lattice mereology; an ALC reasoner |
| 21 | Identity and Persistence | relations of continuity | fission; Evans on vague identity | spacetime worms; a branching continuity graph |
| 22 | Possible Worlds | counterpart theory, 2D semantics | modal collapse | the two-dimensional matrix engine |
| 23 | God and the Philosophers | modal ontological proofs | Gödel's modal collapse | Gödel's proof machine-checked; branching time |
| 24 | Laws, Chance and the Arrow | best systems, typicality | Loschmidt and Zermelo; the big bad bug | Norton's dome; Kac ring; Szilard engine |
| 25 | Space and Time | spacetime structures | the hole argument | Poincaré's disk world; Minkowski diagrams; CTC fixed points |
| 26 | The Quantum Puzzle | Bell, CHSH, contextuality | Bell; Kochen–Specker; Frauchiger–Renner | CHSH game; Peres–Mermin square; Bohmian trajectories; GRW |
| 27 | Sense and Reference | Montague's λ-semantics | Frege's puzzle; Kripke's modal argument | a λ-calculus semantic parser |
| 28 | Meaning in Use | Bayesian pragmatics, signalling games | Kripkenstein; Quine's indeterminacy | Rational Speech Acts model; evolving signals; plus vs quus |
| 29 | Being and Time-Consciousness | phenomenology's structures | the frame problem | Husserl's time diagram; Saussure's relational meaning |
| 30 | Mind and Machine | functionalism, supervenience | causal exclusion; Blockhead | Turing test; Chinese room; Game of Life emergence |
| 31 | Consciousness | Φ, global workspace, free energy | the hard problem; IIT's expander objection | Φ computed on small networks; workspace ignition |
| 32 | Free Will | the consequence argument in modal logic | McKay–Johnson; self-prediction | rollback simulator; leaky accumulator for Libet |
| 33 | Rational Choice | vNM, Savage, Jeffrey | Allais; Ellsberg; Newcomb | Marschak–Machina triangle; Kelly; Newcomb predictor |
| 34 | Games and the Social Contract | Nash, Shapley, mechanisms | backward induction | Axelrod tournament; zero-determinant strategies |
| 35 | The Right and the Good | Harsanyi aggregation, universalizability | the paradox of deontology | Kant's universalizability test; moral parliament |
| 36 | Weighing Lives | population axiologies | Arrhenius; Pareto vs anonymity | Parfit's bars; exhaustive Arrhenius check |
| 37 | Is and Ought | the logic of moral language | Hume's law (Schurz); Frege–Geach | Gibbard's norm-world semantics; evolved norms |
| 38 | Justice | the original position, envy-freeness | Sen's liberal paradox | maximin vs average utility; cake cutting; Dworkin's auction |
| 39 | The Arithmetic of Democracy | voting rules, judgment aggregation | Arrow; Gibbard–Satterthwaite; List–Pettit | voting lab; Arrow checked by SAT; Condorcet's jury |
| 40 | Beauty | aesthetic measures, tuning, symmetry | Hume's standard of taste | Birkhoff's measure; the roughness curve; the 17 wallpaper groups |
| 41 | Fair Machines | fairness criteria, differential privacy, Shapley | Kleinberg–Chouldechova | fairness auditor; DP mechanisms |
| 42 | Aligning Reasoners | Goodhart, off-switch, power-seeking | the Löbian obstacle; no free lunch for preferences | off-switch game; CIRL; the final Wall |

## Standards (as *AI, Built*)

* **Every number is real.** Computed in the part's `compute.py` and cached in `.cache/philosophyN/`, or cited from a
  published source. Schematics are labeled `schematic`, made-up examples `illustrative`, and formal analogies
  `analogy`.
* **Every argument is checked.** An argument on screen is formalized, and the Reasoner checks its validity, or the
  screen states why it can't be formalized.
* **Each side gets its best case.** For every position the part presents the strongest version its defenders give,
  and it says when a question is open.
* **Bilingual.** English and Chinese narration (`narration_zh.json`), on-screen text in
  `videos/philosophy/philosophy_text_zh.json`, and terms in `PHILOSOPHY_ZH_GUIDE.md`, which builds on standard
  Chinese philosophy terminology (the 商务印书馆 translations of the classics, 李秋零's and 邓晓芒's Kant, and 冯友兰's
  history).
