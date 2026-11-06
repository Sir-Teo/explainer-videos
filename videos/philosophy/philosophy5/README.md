# Philosophy, Built — Part 5: Beyond True and False

Part 5 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): the logics that give up
"every sentence is true or false". Logical matrices and the three-valued logics of Łukasiewicz, Kleene and Bochvar;
gaps (K3) and gluts (LP) and their duality; Belnap and Dunn's four values, read both as a computer's state of
information and as Nāgārjuna's catuṣkoṭi, with Priest's fifth value; the Jaina seven predications; paraconsistency
and classical recapture; relevance; Gödel's theorem that intuitionistic logic has no finite matrix; degrees of truth
and a fuzzy train controller; the sorites and four theories of vagueness computed side by side; higher-order
vagueness as a modal logic; linear logic as a logic of resources; quantum logic; what makes a consequence logical;
and logical pluralism. Its brick in **the Wall** is the sorites: tolerance, bivalence and classical logic cannot all
be kept. Its **Price List** is the sorites quartet.

Every table, consequence, countermodel, verdict and proof on screen is computed by the Reasoner's two new modules:
`explainer/philosophy/reasoner/matrix.py` (any finite matrix: K3, LP, Ł3, G3, RM3, B3, FDE and Priest's FDE with a
fifth value; consequence by enumeration with countermodels; minimally inconsistent LP; FOUR's two lattice orders;
Gödel's n-valued chains; t-norms and their residua; a Mamdani fuzzy controller and a train simulation; the sorites
classically, by supervaluation, by degrees and with Williamson's margin for error, and five theories against the
quartet; the lattice of subspaces; permutation-invariant relations and quantifiers) and
`explainer/philosophy/reasoner/linear.py` (intuitionistic linear logic without exponentials, decided by cut-free proof
search). Higher-order vagueness reuses Part 4's modal module. All are tested in `tests/philosophy/test_matrix.py` and
cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy5.compute        # every computed item (about 10 s; cached in .cache/philosophy5)
python tools/build.py philosophy5 -q l                 # 480p preview
python tools/build.py philosophy5                      # 1080p30 -> renders/philosophy5.mp4
python tools/qa_scene.py philosophy5 Superval          # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | five pressures on two values (the future, vagueness, paradox, inconsistent data, physics); the bald man; the plan; the Wall's fifth brick, previewed. | the 102 premises for 101 men: classically unsatisfiable, every one needed |
| 1 | `Matrices` | Łukasiewicz (1920) and the future; his tables; Kleene (1938) and partial functions; the one cell where they differ; Bochvar (1938) and the infectious "meaningless"; SQL's NULL; logical matrices (Łukasiewicz–Tarski 1930), designated values, consequence; Łoś–Suszko (1958). | the tables of Ł3, K3 and B3; 3ⁿ rows |
| 2 | `Gaps` | K3 and LP: the same tables, opposite designated sets; Asenjo (1966), Priest (1979); why K3 has no tautologies and LP no explosion; modus ponens fails in LP; the duality theorem; a gap between "valid in both" and FDE. | six inferences in CL, K3, LP, Ł3, FDE with countermodels; the duality on all 144 pairs of 12 formulas; p ∧ ¬p ⊨ q ∨ ¬q valid in K3 and LP, refuted in FDE |
| 3 | `Four` | Dunn (1976) and Belnap (1977): values as (told true, told false); Belnap's computer; FOUR's truth and information orders; consensus and gullibility; bilattices (Ginsberg 1988, Fitting 1991); FDE contains K3, LP and classical logic; first-degree entailment (Anderson–Belnap 1975). | eight queries to a database with a conflict (o ∨ l = T); ∧ and ∨ as the truth lattice's meet and join on all 16 pairs; no FDE tautologies |
| 4 | `Corners` | the catuṣkoṭi in the early sutras and Nāgārjuna (c. 150); the unanswered questions; Priest (2010): the corners are FDE's values; the fifth value, emptiness; MMK I.1 (Garfield's translation); three readings (Priest and Garfield 2003; prasaṅga; Robinson 1957, Jayatilleke 1963). | five inferences in FDE and FDE with E; p ⊨ p ∨ q fails (q = E) |
| 5 | `Jaina` | Mahāvīra and anekāntavāda; the blind men and the elephant; syādvāda and the saptabhaṅgī (Kundakunda, Samantabhadra, Mallisena 1292); why seven (Priest 2008, Ganeri 2002); the jar. | the seven nonempty subsets of three values, in the traditional order |
| 6 | `Paracon` | the proof of explosion (William of Soissons; Lewis–Langford 1932) and the step LP refuses; Jaśkowski (1948), da Costa (1963), Priest (1979); paraconsistency vs dialetheism; minimally inconsistent LP (Priest 1991) and classical recapture; candidates for true contradictions; Lewis (1982), Quine (1970), *In Contradiction* (1987). | each step of the explosion proof in LP (DS fails: p = ½, q = 0); five arguments in classical logic, LP and LPₘ |
| 7 | `Relevance` | the paradoxes of implication; Anderson and Belnap's *Entailment*; variable sharing (Belnap 1960); Sobociński's RM3 (1952) and its limits; Routley–Meyer ternary semantics (1972–73) and the Routley star; naive set theory in relevant logic (Brady), inconsistent mathematics (Mortensen 1995). | six formulas in classical logic and RM3 with countermodels; RM3 still proves (p ∧ ¬p) → (q ∨ ¬q) |
| 8 | `Intuition` | Brouwer (1908) against excluded middle; BHK (Heyting 1930, Kolmogorov 1932); Heyting's three values; Gödel (1932): no finite matrix; Kripke's semantics for intuitionistic logic (1965). | LEM and ¬¬p ⊨ p fail in G3, p ⊨ ¬¬p holds; Gödel's Dₙ valid in n values and refuted in n + 1, for n = 2, 3, 4; six formulas at two stages of knowledge |
| 9 | `Fuzzy` | Zadeh (1965); the Gödel, product and Łukasiewicz t-norms; residuation; Hájek's BL (1998); the Sendai subway (1987); a Mamdani controller; comfort vs speed. | the three t-norms as heat maps, residuation on a grid; nine rules at 120 m and 15 m/s (two fire, brake 0.47); two simulated stops from 600 m: error +1.4 m vs −0.8 m, worst jerk 0.8 vs 4.8 m/s³ |
| 10 | `Sorites` | Eubulides (4th c. BCE); Chrysippus's silence; the bald man formalized; a minimal inconsistent set; vagueness everywhere; the law's lines; Wright (1975) on tolerance; **the Wall's fifth brick**. | 7 premises for 6 men and 102 for 101: unsatisfiable, each premise needed (CDCL) |
| 11 | `Superval` | penumbra and sharpenings; supertruth (Mehlberg 1958, Fine 1975); the verdicts; a true existential with no true instance; excluded middle without bivalence; Williamson's objections; degree theories and the decay of modus ponens; artificial precision. | 21 men, penumbra 7–12, 7 sharpenings: statuses of B, the conditionals and LEM; "there is a last bald man" super-true, no witness; Łukasiewicz degrees on 101 men, every conditional ≥ 0.975, the guarantee used up by man 70 |
| 12 | `Epistemic` | epistemicism (Sorensen 1988, Williamson 1994) and the margin for error; contextualism (Kamp 1981, Raffman 1994, Graff Fara 2000, Shapiro 2006); **Price List**: the sorites quartet (Williamson; Fine, Machina, Smith; Hyde, Cobreros–Égré–Ripley–van Rooij; Unger); each theory's second price. | the 6 unknowable men nearest a cutoff (margin 3); the MUS {T, E, B, L} and its four corrections; five theories in their own semantics against the four claims |
| 13 | `Higher` | the edges of the penumbra; "definitely"; a modal model of sharpenings (reflexive, symmetric, not transitive: T without 4); each level its own borderline; no definite borderline case; revenge; Sainsbury (1990). | B, DB, DDB and "borderline" for 21 men at 8 sharpenings, via Part 4's modal module |
| 14 | `Linear` | Gentzen's structural rules; Girard (1987); ⊸, ⊗, &, ⊕; the vending machine; a proof spending each dollar once; the substructural landscape (relevance, Grišin 1974 and Zardini 2011, Lambek 1958, ST; Rust, session types, no-cloning). | six sequents, linear vs classical; the 7-node proof for two dollars; contraction and weakening refuted, exchange holds |
| 15 | `Quantum` | Birkhoff and von Neumann (1936); propositions as subspaces; distributivity fails for three polarizations; three polarizers (Malus's law); Putnam (1968), Dummett (1976). | p ∧ (q ∨ r) has dimension 1, (p ∧ q) ∨ (p ∧ r) dimension 0; 0 vs ⅛ of the light through crossed polarizers |
| 16 | `Consequence` | Bolzano (1837) and Tarski (1936); the logical constants; Etchemendy (1990); Tarski's permutation invariance (1966), Sher (1991), Feferman (1999); tonk (Prior 1960), conservativeness (Belnap 1962), harmony (Prawitz, Dummett). | the 4 invariant relations among 512 on three things; invariant quantifiers 4, 8, 16, 32 of 4, 16, 256, 65,536 on 1–4 things |
| 17 | `Pluralism` | Carnap's tolerance (1934); Quine (1970); Beall and Restall (2006) and the Generalized Tarski Thesis; the collapse argument (Priest, Read 2006); anti-exceptionalism (Williamson 2017, Hjortland 2017). | each logic's strength: 6, 3, 3, 4, 0 of Chapter 2's six inferences |
| 18 | `Outro` | recap; the Reasoner's matrix and linear modules; the Wall; problems; payoffs; references. | — |

## Sources

Books: Priest, *An Introduction to Non-Classical Logic: From If to Is* (2nd ed., 2008); Williamson, *Vagueness*
(1994); Keefe and Smith (eds.), *Vagueness: A Reader* (1996); Beall and Restall, *Logical Pluralism* (2006);
Restall, *An Introduction to Substructural Logics* (2000); Hájek, *Metamathematics of Fuzzy Logic* (1998); Priest,
*In Contradiction* (1987, 2nd ed. 2006) and *The Fifth Corner of Four* (2018); Anderson and Belnap, *Entailment*, vol.
I (1975); Malinowski, *Many-Valued Logics* (1993); Garfield, *The Fundamental Wisdom of the Middle Way* (1995);
Shapiro, *Vagueness in Context* (2006); Sher, *The Bounds of Logic* (1991); Etchemendy, *The Concept of Logical
Consequence* (1990).

Papers and texts: Łukasiewicz, "O logice trójwartościowej" (1920); Post, "Introduction to a general theory of
elementary propositions" (1921); Łukasiewicz and Tarski, "Untersuchungen über den Aussagenkalkül" (1930); Gödel, "Zum
intuitionistischen Aussagenkalkül" (1932); Kolmogorov, "Zur Deutung der intuitionistischen Logik" (1932); Carnap, *Logische
Syntax der Sprache* (1934); Tarski, "On the concept of logical consequence" (1936) and "What are logical notions?"
(1966, publ. 1986); Birkhoff and von Neumann, "The logic of quantum mechanics" (1936); Bochvar (1938); Kleene, "On
notation for ordinal numbers" (1938); Jaśkowski, "Rachunek zdań dla systemów dedukcyjnych sprzecznych" (1948);
Sobociński (1952); Mehlberg, *The Reach of Science* (1958); Łoś and Suszko, "Remarks on sentential logics" (1958);
Belnap, "Entailment and relevance" (1960) and "Tonk, plonk and plink" (1962); Prior, "The runabout inference-ticket"
(1960); da Costa (1963); Kripke, "Semantical analysis of intuitionistic logic I" (1965); Zadeh, "Fuzzy sets" (1965);
Asenjo, "A calculus of antinomies" (1966); Putnam, "Is logic empirical?" (1968); Quine, *Philosophy of Logic*
(1970); Routley and Meyer, "The semantics of entailment" (1972–73); Fine, "Vagueness, truth and logic" (1975); Wright,
"On the coherence of vague predicates" (1975); Dunn, "Intuitive semantics for first-degree entailments and 'coupled
trees'" (1976); Dummett, "Is logic empirical?" (1976); Machina, "Truth, belief and vagueness" (1976); Belnap, "How a
computer should think" and "A useful four-valued logic" (1977); Priest, "The logic of paradox" (1979) and "Minimally
inconsistent LP" (1991); Unger, "There are no ordinary things" (1979); Kamp, "The paradox of the heap" (1981); Lewis,
"Logic for equivocators" (1982); Yasunobu and Miyamoto, "Automatic train operation system by predictive fuzzy control"
(1985); Girard, "Linear logic" (1987); Sorensen, *Blindspots* (1988); Ginsberg, "Multivalued logics" (1988);
Sainsbury, "Concepts without boundaries" (1990); Fitting, "Bilattices and the semantics of logic programming" (1991);
Wright, "Is higher order vagueness coherent?" (1992); Raffman, "Vagueness without paradox" (1994); Mortensen,
*Inconsistent Mathematics* (1995); Hyde, "From heaps and gaps to heaps of gluts" (1997); Williamson, "On the
structure of higher-order vagueness" (1999); Feferman, "Logic, logics, and logicism" (1999); Graff, "Shifting sands"
(2000); Ganeri, "Jaina logic and the philosophical basis of pluralism" (2002); Garfield and Priest, "Nāgārjuna and
the limits of thought" (2003); Read, "Monism: the one true logic" (2006); Brady, *Universal Logic* (2006); Priest,
"Jaina logic: a contemporary perspective" (2008) and "The logic of the catuṣkoṭi" (2010); Smith, *Vagueness and
Degrees of Truth* (2008); Zardini, "Truth without contra(di)ction" (2011); Cobreros, Égré, Ripley and van Rooij,
"Tolerant, classical, strict" (2012); Williamson, "Semantic paradoxes and abductive methodology" (2017); Hjortland,
"Anti-exceptionalism about logic" (2017).

## Problems and solutions

1. **K3 has no tautologies, and LP has exactly the classical ones.** *K3:* give every atom the value ½. Each
   connective sends halves to a half (¬½ = ½, ½ ∧ ½ = ½ ∨ ½ = ½, ½ → ½ = max(½, ½) = ½), so by induction every
   formula takes ½, which K3 does not designate. *LP:* an LP tautology is true on the valuations that use only 0 and
   1, where LP's tables are classical, so it is a classical tautology. Conversely, Kleene's tables are *regular*:
   replacing a ½ in the input by 0 or 1 never changes an output that was already 0 or 1. So if some LP valuation gave
   a classical tautology the value 0, sharpening every ½ to 0 or 1 would give a classical valuation that also gives
   it 0, which is impossible. So it never takes 0 in LP, and LP designates the other two values.
2. **(p → q) ∨ (q → p).** Not a K3 tautology: with p = q = ½, both disjuncts are ½ → ½ = ½. A tautology of Ł3 and of
   G3: in both, a → b = 1 whenever a ≤ b, and the values form a chain, so one of p ≤ q or q ≤ p holds and one
   disjunct is 1. (It is classically valid but not intuitionistically: it is the axiom that turns intuitionistic
   logic into Gödel–Dummett logic LC, the logic of all linear Kripke frames.) The Reasoner confirms all three.
3. **Belnap's computer, p = B, q = N.** ¬B = B, so p ∧ ¬p = B ∧ B = B; then B ∨ N is the join of B and N in the truth
   order, which is T. So (p ∧ ¬p) ∨ q = T. And p ∨ q = T, so ¬(p ∨ q) = F.
4. **A ⊗ B ⊢ A & B and A & B ⊢ A ⊗ B.** The first: &R needs A ⊗ B ⊢ A and A ⊗ B ⊢ B, and after ⊗L the first is
   A, B ⊢ A, which needs *weakening* to discard B. The second: ⊗R must split the hypotheses between A and B, but there
   is only one hypothesis, A & B; you would need two copies of it, which is *contraction*. The Reasoner's prover finds
   neither, and both are classically valid (with ∧ for both ⊗ and &).
5. **Men 0–4, with 0 and 1 clearly bald and 3 and 4 clearly not.** The admissible sharpenings put the cutoff after
   man 1 or after man 2. B₁ → B₂ is false on the first and true on the second: not super-true. B₂ ∨ ¬B₂ is true on
   both: super-true, though neither disjunct is. ∃i (Bᵢ ∧ ¬Bᵢ₊₁) is true on both (witness 1 on the first, 2 on the
   second): super-true, with no super-true instance. The Reasoner's `supervaluate` gives I, T, T.
6. **(Essay) An exit from the sorites quartet, and its second price.** A strong answer chooses an exit and names both
   prices, using Chapter 12's table. *Epistemicism* keeps classical logic and bivalence; its price is a sharp fact
   that no use of the word fixes visibly, and the burden of showing that use fixes it invisibly (Williamson's margin
   for error explains our ignorance, not the fact). *Supervaluationism* gives up bivalence, and also tolerance as a
   universal truth, and says "there is a last bald man" with no man who is it. *Degree theory* keeps tolerance only as
   "nearly true", and buys a precise number for every vague sentence (artificial precision). *Glut and
   non-transitive logics* keep tolerance and pay in logic: modus ponens (LP) or the chaining of valid steps (ST).
   *Nihilism* keeps the logic and loses the bald men, and with them almost everything we say. Each must then say what
   it does about higher-order vagueness (Chapter 13).

## 习题与解答

1. **K3没有重言式，而LP的重言式恰好是经典重言式。** *K3：* 给每个原子赋值½。每个联结词都把½送到½（¬½ = ½，½ ∧ ½ = ½ ∨ ½ = ½，
   ½ → ½ = max(½, ½) = ½），所以由归纳，每个公式都取值½，而K3不指定它。*LP：* 一个LP重言式在只用0和1的赋值上为真，而在那里LP的真值表
   就是经典的，所以它是经典重言式。反过来，克莱尼的真值表是*正则的*：把输入中的一个½换成0或1，从不改变一个本来就是0或1的输出。所以，如果
   某个LP赋值让一个经典重言式取值0，把每个½精确化为0或1，就会得到一个也让它取值0的经典赋值，这不可能。所以它在LP中从不取值0，而LP指定
   另外两个值。
2. **(p → q) ∨ (q → p)。** 不是K3的重言式：取p = q = ½，两个析取支都是½ → ½ = ½。它是Ł3和G3的重言式：在两者中，只要a ≤ b，就有
   a → b = 1，而这些值构成一条链，所以p ≤ q或q ≤ p必有一个成立，有一个析取支为1。（它经典有效，但不是直觉主义有效的：正是这条公理把
   直觉主义逻辑变成哥德尔–达米特逻辑LC，即所有线性克里普克框架的逻辑。）推理机确认了这三个结论。
3. **贝尔纳普的计算机，p = B，q = N。** ¬B = B，所以p ∧ ¬p = B ∧ B = B；而B ∨ N是B和N在真值序中的并，即T。所以(p ∧ ¬p) ∨ q = T。
   又p ∨ q = T，所以¬(p ∨ q) = F。
4. **A ⊗ B ⊢ A & B与A & B ⊢ A ⊗ B。** 第一个：&R需要A ⊗ B ⊢ A和A ⊗ B ⊢ B，而经过⊗L之后，前者是A, B ⊢ A，需要*弱化*来丢掉B。
   第二个：⊗R必须把假设分给A和B，但只有一个假设A & B；你需要它的两个副本，这就是*收缩*。推理机的证明器两个都找不到，而两者在经典逻辑中
   都有效（⊗和&都读作∧）。
5. **第0–4个人，0和1显然秃，3和4显然不秃。** 容许的精确化把分界放在第1个人之后，或第2个人之后。B₁ → B₂在前者上为假，在后者上为真：
   不是超真的。B₂ ∨ ¬B₂在两者上都为真：超真，尽管两个析取支都不是。∃i (Bᵢ ∧ ¬Bᵢ₊₁)在两者上都为真（前者的见证是1，后者是2）：超真，却
   没有超真的实例。推理机的`supervaluate`给出I、T、T。
6. **（论述题）谷堆四元组的一条出路，以及它的第二个代价。** 好的回答选择一条出路，并用第12章的表说出两个代价。*认知主义*保留经典逻辑和
   二值原则；它的代价是一个锐利的事实，没有任何对这个词的使用能明显地确定它，于是它承担着证明“使用不可见地确定了它”的负担（威廉森的误差
   余地解释的是我们的无知，而不是那个事实）。*超赋值主义*放弃二值原则，也放弃了作为全称真理的容忍，并且说“存在最后一个秃子”，却没有哪个人
   是他。*程度论*只把容忍保留为“接近真”，并为每个模糊句子买来一个精确的数（人为的精确）。*过剩逻辑与非传递逻辑*保留容忍，用逻辑来付账：
   肯定前件式（LP），或者有效步骤的串联（ST）。*虚无论*保留逻辑，失去了秃子，也随之失去了我们所说的几乎一切。每种理论接着都必须说明它怎样
   处理高阶模糊（第13章）。
