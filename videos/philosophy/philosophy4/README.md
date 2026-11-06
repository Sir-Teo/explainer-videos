# Philosophy, Built — Part 4: Necessity and Possibility

Part 4 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): modal logic, from
Aristotle's sea battle and Diodorus's Master Argument to Kripke's possible worlds, the correspondence theory of
axioms and frames, completeness, bisimulation and decidability, and on to its readings as obligation, time, programs,
and the model checkers that verify chips and protocols. Its brick in **the Wall** is Goldblatt and Thomason's theorem
(1975): some modal axioms, Löb's and McKinsey's among them, correspond to no first-order condition on the frames, so
modal logic is not just first-order logic in disguise. Its **Price List** is the Master Argument: three claims that
cannot all be true, and the three ancient exits.

Every frame count, truth table, tableau, bisimulation, filtration and state graph on screen is computed by the
Reasoner's modal module (`explainer/philosophy/reasoner/modal.py`: a parser for □, ◇, the tense and deontic
operators; Kripke models and evaluation; every frame on up to four worlds with its frame conditions; the
correspondence checker; a finite model finder; the largest bisimulation and the minimal model; CTL's fixed points with
fairness; Peterson's protocol and its broken variant; a prefixed tableau for K and T), tested in
`tests/philosophy/test_modal.py`, and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy4.compute        # every computed item (about 1 min; cached in .cache/philosophy4)
python tools/build.py philosophy4 -q l                 # 480p preview
python tools/build.py philosophy4                      # 1080p30 -> renders/philosophy4.mp4
python tools/qa_scene.py philosophy4 Corr              # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | might, must, ought, always: modalities; one box with six readings (Leibniz, Hintikka 1962, von Wright 1951, Prior 1957, Gödel–Löb–Solovay, Hoare–Pratt–Pnueli); the plan; the Wall's fourth brick, previewed. | a first Kripke model evaluated |
| 1 | `Ancient` | Aristotle's sea battle (*De Interpretatione* 9); the Master Argument of Diodorus Cronus (c. 300 BCE); **Price List**: the exits of Diodorus, Cleanthes and Chrysippus; Avicenna's necessary and possible existents (c. 1020); Duns Scotus and synchronic contingency (c. 1300); Leibniz's possible worlds (*Theodicy*, 1710). | the MUS {P, I, C} and its three minimal corrections |
| 2 | `Lewis` | the paradoxes of material implication; C. I. Lewis's strict implication (1912); *Symbolic Logic* (1932) and S1–S5; the axioms K, T, 4, 5 and necessitation; the 14 modalities of S4 and 6 of S5; topology: Kuratowski's closure axioms (1922) and McKinsey and Tarski (1944): S4 is the logic of interior. | all 258 strings of up to five operators on p sorted into 14 classes (S4) and 6 (S5), on every reflexive transitive frame (389) and every equivalence frame (23) with up to 4 worlds |
| 3 | `Kripke` | Kripke (1959), with Kanger, Hintikka, Montague and Prior; frames, models and the clauses for □ and ◇; evaluation world by world; dead ends and axiom D; what the arrows mean under six readings. | ◇p, □p, □◇p and □p → p at all four worlds of a model |
| 4 | `Corr` | validity on a frame; T ⇔ reflexive and 4 ⇔ transitive, with both directions proved; D, B, 5; the table of correspondences; what correspondence means philosophically. | every frame on 3 and 4 worlds: T 64 / 4,096, D 343 / 50,625, B 64 / 1,024, 4 171 / 3,994, 5 39 / 306 valid, agreeing with the frame condition on all 512 and 65,536 frames |
| 5 | `Lob` | Löb (1955) and Solovay (1976): GL is the logic of provability; Gödel's second incompleteness theorem as a one-line instance; GL ⇔ transitive and conversely well-founded; why that is not first-order (compactness); **the Wall's fourth brick**: Goldblatt–Thomason (1975); Sahlqvist's theorem (1975). | Löb's axiom valid on exactly the strict partial orders: 3 of 16, 19 of 512, 219 of 65,536 frames |
| 6 | `Canonical` | soundness and completeness for K; maximal consistent sets as worlds; the canonical relation; the truth lemma; canonicity of T and 4; S4 and S5 complete; GL is not canonical (Segerberg 1971). | — |
| 7 | `Bisim` | bisimulation (forth and back); the invariance theorem; the largest bisimulation and the minimal model; a loop and a cycle that no formula can tell apart; the standard translation; van Benthem's theorem (1976). | the 6-world model merged into 4 classes, {0}, {1, 2}, {3, 4}, {5}; the loop ~ the 3-cycle |
| 8 | `FMP` | filtration through the subformulas; the finite model property; decidability; Ladner (1977): S5 NP-complete, K, T and S4 PSPACE-complete; the guarded fragment; prefixed tableaux. | a 12-world chain filtered to 4 worlds for □◇p → ◇□p (bound 2⁶ = 64); K's axiom closed in 8 steps; ◇p ∧ ◇q → ◇(p ∧ q) refuted by a 3-world model; □p → p open in K, closed in T |
| 9 | `QML` | Barcan Marcus (1946, 1947); the Barcan formula and its converse; constant and growing domains; Quine's objections (1953): the number of planets; *de dicto* and *de re*; the necessity of identity; Hesperus and Phosphorus; Kripke's rigid designators (1971). | the Barcan formula true with constant domains, false with growing ones |
| 10 | `Deontic` | von Wright (1951); standard deontic logic = KD; Ross's paradox (1941); Chisholm's contrary-to-duty paradox (1963); dyadic obligation (Hansson 1969, Lewis 1973). | Ross's inference valid on every serial frame up to 3 worlds; Chisholm's four versions: each inconsistent or with a redundant sentence |
| 11 | `Tense` | Prior's tense logic (1957); F, G, P, H; transitivity, no last moment, density and linearity as axioms; branching time; Peircean and Ockhamist readings of the sea battle. | four sentences evaluated on the two-history tree, Peircean and Ockhamist |
| 12 | `Temporal` | runs as paths; Pnueli (1977); X, F, G, U; safety and liveness (Alpern and Schneider 1985); CTL and model checking (Clarke and Emerson, Queille and Sifakis, 1981); fixed points; Vardi and Wolper's automata (1986), Büchi (1962). | — |
| 13 | `Peterson` | a state graph; Peterson's algorithm (1981); mutual exclusion as AG ¬(crit₀ ∧ crit₁); a broken variant and its counterexample; starvation and fairness. | Peterson: 34 states, 62 edges, mutual exclusion holds; the broken variant: 50 states and an 8-step trace to both in the critical section; endless waiting possible from 8 states without fairness, on no fair path |
| 14 | `Hoare` | Floyd (1967) and Hoare (1969) triples; the rules for assignment, sequence and loops; a loop invariant; Pratt's dynamic logic (1976). | the summation invariant checked at all 496 loop points for n = 0, …, 30 |
| 15 | `Industry` | the Pentium FDIV bug (1994) and formal verification of chips; SPIN, SLAM, TLA⁺ at Amazon, seL4 and CompCert; state explosion and its answers; Bryant's BDDs (1986). | the BDD of (x₁ ∧ y₁) ∨ … ∨ (xₙ ∧ yₙ): 2n + 2 nodes in a good order, 2ⁿ⁺¹ in a bad one, for n = 1, …, 6 |
| 16 | `Outro` | recap; the Reasoner's modal module; the Wall; problems; payoffs; references. | — |

## Sources

Books: Hughes and Cresswell, *A New Introduction to Modal Logic* (1996); Blackburn, de Rijke and Venema, *Modal
Logic* (2001), chs. 1–4; Chellas, *Modal Logic: An Introduction* (1980); Sider, *Logic for Philosophy* (2010), chs.
6–9; Garson, *Modal Logic for Philosophers* (2nd ed., 2013); Boolos, *The Logic of Provability* (1993); Huth and
Ryan, *Logic in Computer Science* (2nd ed., 2004); Baier and Katoen, *Principles of Model Checking* (2008); Clarke,
Grumberg and Peled, *Model Checking* (1999).

Texts and papers: Aristotle, *De Interpretatione* 9; Epictetus, *Discourses* II.19; Avicenna, *The Metaphysics of
The Healing*; Duns Scotus, *Lectura* I.39; Leibniz, *Theodicy* (1710); C. I. Lewis, "Implication and the Algebra of
Logic" (Mind 1912); Lewis and Langford, *Symbolic Logic* (1932); Kuratowski (1922); Ross, "Imperatives and Logic"
(1941); McKinsey and Tarski, "The Algebra of Topology" (1944); Barcan, "A Functional Calculus of First Order Based on
Strict Implication" (JSL 1946) and "The Identity of Individuals in a Strict Functional Calculus of Second Order"
(1947); von Wright, "Deontic Logic" (Mind 1951); Quine, "Three Grades of Modal Involvement" (1953) and "Reference and
Modality" (1953); Löb, "Solution of a Problem of Leon Henkin" (JSL 1955); Prior, *Time and Modality* (1957) and
*Past, Present and Future* (1967); Kripke, "A Completeness Theorem in Modal Logic" (JSL 1959), "Semantical Analysis
of Modal Logic I" (1963) and "Identity and Necessity" (1971); Hintikka, *Knowledge and Belief* (1962); Büchi (1962);
Chisholm, "Contrary-to-Duty Imperatives and Deontic Logic" (Analysis 1963); Floyd, "Assigning Meanings to Programs"
(1967); Hoare, "An Axiomatic Basis for Computer Programming" (CACM 1969); Hansson (1969); Segerberg, *An Essay in
Classical Modal Logic* (1971); D. Lewis, *Counterfactuals* (1973); Goldblatt and Thomason, "Axiomatic Classes in
Propositional Modal Logic" (1975); Sahlqvist, "Completeness and Correspondence in the First and Second Order
Semantics for Modal Logic" (1975); van Benthem, *Modal Correspondence Theory* (1976); Solovay, "Provability
Interpretations of Modal Logic" (1976); Pratt, "Semantical Considerations on Floyd–Hoare Logic" (1976); Pnueli, "The
Temporal Logic of Programs" (FOCS 1977); Ladner, "The Computational Complexity of Provability in Systems of Modal
Propositional Logic" (SIAM J. Comput. 1977); Peterson, "Myths About the Mutual Exclusion Problem" (IPL 1981); Clarke
and Emerson (1981); Queille and Sifakis (1982); Alpern and Schneider, "Defining Liveness" (IPL 1985); Bryant,
"Graph-Based Algorithms for Boolean Function Manipulation" (IEEE Trans. Comput. 1986); Vardi and Wolper (LICS
1986); Holzmann, *The SPIN Model Checker* (2003); Ball and Rajamani, SLAM (2002); Klein et al., seL4 (SOSP 2009);
Leroy, CompCert (CACM 2009); Newcombe et al., "How Amazon Web Services Uses Formal Methods" (CACM 2015).

## Problems and solutions

1. **B, p → □◇p, is valid on exactly the symmetric frames.** *If the frame is symmetric:* suppose p is true at w,
   and w R v. By symmetry v R w, so v sees a p-world, and ◇p is true at v. That holds for every v that w sees, so
   □◇p is true at w. *If the frame is not symmetric:* some w R v without v R w. Make p true at w only. Then p is true
   at w, but v sees no p-world (the only one is w, which v does not see), so ◇p fails at v, and □◇p fails at w. The
   Reasoner's correspondence checker agrees on all 16, 512 and 65,536 frames with 2, 3 and 4 worlds.
2. **In S5, ◇□p → □p is valid; axiom 5 does the work.** Axiom 5 is ◇q → □◇q. Put q = ¬p and contrapose:
   ¬□◇¬p → ¬◇¬p, and since ◇¬ is ¬□ and □¬ is ¬◇, this is ◇□p → □p. So it holds in every logic containing 5, on
   every euclidean frame; T and 4 are not needed. Semantically: if w sees v where □p holds, and w R u, then by the
   euclidean condition v R u, so p holds at u. The Reasoner finds ◇□p → □p valid on exactly the euclidean frames:
   7 of 16 with two worlds and 39 of 512 with three, the same frames as axiom 5.
3. **A smallest frame on which □p → □□p fails has two worlds.** On one world, both possible relations (empty and a
   loop) are transitive, so 4 is valid. On two worlds, take 0 R 1 and 1 R 0, with no loops, and make p true at 0
   only. At world 1, □p is true (the only world it sees is 0, where p holds), but □□p is false: 1 sees 0, which sees
   1, where p fails. The Reasoner finds exactly three two-world frames on which 4 fails, each containing this
   two-cycle with at most one loop.
4. **Bisimilar models, one with a cycle and one without.** Take M, one world with a loop, and N, the infinite chain
   0 → 1 → 2 → …, with the same atoms true everywhere in both. The relation that links M's world with every world of
   N is a bisimulation: every move on either side is matched by a move on the other, to a linked world with the same
   atoms. They are not isomorphic (one world versus infinitely many). No finite model without a cycle would do: in a
   finite acyclic model every path has at most n steps, so □ⁿ⁺¹⊥ is true at every world, while ◇ⁿ⁺¹⊤ is true at the
   loop.
5. **Two specifications in LTL.** "The light is never green in both directions": G ¬(green_NS ∧ green_EW), a safety
   property (a finite trace can refute it). "Every request is eventually granted": G (request → F grant), a liveness
   property (only an infinite run can refute it).
6. **(Essay) The Master Argument has three exits.** A strong answer chooses one and prices it. *Diodorus* (reject C:
   the possible is what is or will be true): the cost is a near-determinism in which nothing that never happens was
   ever possible, and possibility becomes a fact about time. *Cleanthes* (reject P: some past truths are not
   necessary): the cost is that the past is not fixed, unless "necessary" is read as unpreventable only for genuine
   past events and not for "soft facts" about the past that depend on the future, the line taken by Ockham and, in
   Part 23, by the debate over foreknowledge. *Chrysippus* (reject I: the impossible can follow from the possible):
   the cost is that "possible" is no longer closed under entailment, so it cannot be "true in some world", and the
   Kripke semantics of this part must be given up or reinterpreted. Each choice is a theory of what "possible" means.

## 习题与解答

1. **B，即 p → □◇p，恰好在对称框架上有效。** *若框架是对称的：* 设 p 在 w 上为真，且 w R v。由对称性 v R w，所以 v 能看到一个
   p 世界，◇p 在 v 上为真。这对 w 看到的每个 v 都成立，所以 □◇p 在 w 上为真。*若框架不是对称的：* 有某个 w R v 而没有 v R w。只让 p
   在 w 上为真。那么 p 在 w 上为真，但 v 看不到任何 p 世界（唯一的 p 世界是 w，而 v 看不到它），所以 ◇p 在 v 上为假，□◇p 在 w 上为假。
   推理机的对应检查器在 2、3、4 个世界的全部 16、512 和 65,536 个框架上都与此一致。
2. **在 S5 中，◇□p → □p 有效；起作用的是公理 5。** 公理 5 是 ◇q → □◇q。令 q = ¬p 并取逆否：¬□◇¬p → ¬◇¬p，由于 ◇¬ 就是 ¬□，
   □¬ 就是 ¬◇，这正是 ◇□p → □p。所以它在任何包含 5 的逻辑中成立，在每个欧几里得框架上有效；不需要 T 和 4。从语义上看：若 w 看到一个
   □p 成立的 v，且 w R u，则由欧几里得条件 v R u，所以 p 在 u 上成立。推理机发现 ◇□p → □p 恰好在欧几里得框架上有效：两个世界时 16 个中
   有 7 个，三个世界时 512 个中有 39 个，与公理 5 的框架完全相同。
3. **使 □p → □□p 不成立的最小框架有两个世界。** 只有一个世界时，两种可能的关系（空关系和一个自环）都是传递的，所以 4 有效。两个世界时，
   取 0 R 1 和 1 R 0，没有自环，只让 p 在 0 上为真。在世界 1 上，□p 为真（它唯一看到的世界是 0，p 在那里成立），但 □□p 为假：1 看到 0，
   0 看到 1，而 p 在 1 上不成立。推理机找到恰好三个使 4 不成立的两世界框架，每个都包含这个二元环，至多再加一个自环。
4. **两个互模拟的模型，一个有环，一个无环。** 取 M 为一个带自环的世界，N 为无穷链 0 → 1 → 2 → …，两者处处有相同的原子为真。把 M 的
   世界与 N 的每个世界相连的关系是一个互模拟：任一方的每一步都能被另一方的一步匹配，到达一个相连的、原子相同的世界。它们不同构（一个世界对
   无穷多个）。任何无环的有限模型都不行：在有限无环模型中每条路径至多 n 步，所以 □ⁿ⁺¹⊥ 在每个世界上为真，而 ◇ⁿ⁺¹⊤ 在自环世界上为真。
5. **两个 LTL 规约。** "信号灯从不在两个方向同时为绿"：G ¬(green_NS ∧ green_EW)，这是安全性质（一条有限轨迹就能驳倒它）。"每个请求
   最终都会被批准"：G (request → F grant)，这是活性性质（只有无穷的运行才能驳倒它）。
6. **（论述题）主论证有三条出路。** 好的回答选择一条并给它标价。*狄奥多罗斯*（拒绝 C：可能的就是现在或将来为真的）：代价是一种近乎决定论
   的立场，从不发生的事从来都不可能，可能性变成了关于时间的事实。*克莱安西斯*（拒绝 P：有些关于过去的真理不是必然的）：代价是过去并不固定，
   除非把"必然"理解为只对真正的过去事件不可阻止，而不包括依赖于未来的、关于过去的"软事实"，这是奥卡姆的路线，也是第23部分关于预知的争论
   所采取的路线。*克吕西波*（拒绝 I：不可能的可以从可能的推出）：代价是"可能"不再在蕴涵下封闭，因此它不能是"在某个世界中为真"，本部分的
   克里普克语义学就必须放弃或重新解释。每一种选择都是一种关于"可能"意味着什么的理论。
