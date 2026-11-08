# Philosophy, Built — Part 2: The Laws of Thought

Part 2 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): propositional logic, built
and run. It is the first act's foundation, and the source of two devices the series uses throughout: the Reasoner's
SAT solver and the **Price List** (Socrates' elenchus as minimal correction sets). Its brick in **the Wall** is the
price of calculation: SAT is NP-complete, and resolution proofs of the pigeonhole principle are exponentially long.

Every table, proof, search and count on screen is computed by the Reasoner (`explainer/philosophy/reasoner/prop.py`,
tested against brute force in `tests/philosophy/test_prop.py`) and cached by [`compute.py`](compute.py). Published
facts (the 2016 Pythagorean-triples proof, the Pentium bug, Zelkova, the 2020 PhilPapers survey) are cited on
screen. Schematics are labelled `schematic`.

## Build it

```bash
python -m videos.philosophy.philosophy2.compute        # every computed item (about 30 s; cached in .cache/philosophy2)
python tools/build.py philosophy2 -q l                 # 480p preview
python tools/build.py philosophy2                      # 1080p30 -> renders/philosophy2.mp4
python tools/qa_scene.py philosophy2 CDCL              # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Leibniz's *calculemus*; Smullyan's knights and knaves settled by a table; the Boolean Pythagorean triples (Heule, Kullmann and Marek 2016); the plan; the Wall and the Price List introduced. | the 8-row table and its one surviving row; 1 … 400 two-coloured with no one-colour triple (294 triples) by our CDCL solver |
| 1 | `Boole` | Chrysippus's five indemonstrables; Philo vs Diodorus on 'if'; Boole's algebra of classes; x² = x has the roots 0 and 1; the principle of contradiction derived; Jevons's logic piano (1869). | Jevons's method on "iron is a metal; every metal is an element": 8 combinations, 4 struck, the conclusion read off |
| 2 | `Syntax` | the grammar of formulas; parse trees and evaluation from the leaves; unique readability; the 16 binary truth functions; three demands single out Philo's conditional. | the 16 truth tables; the filter 16 → 4 → 2 → 1 |
| 3 | `Post` | DNF, so {¬, ∧, ∨} is complete; De Morgan; Sheffer's nand (and Peirce's, 1880); XOR from four nand gates; Post's five classes and criterion (1941). | the nand identities on all rows; the four-gate circuit swept; Post's table; completeness of 12 sets cross-checked by closure |
| 4 | `Semantics` | valuation, tautology, satisfiability, ⊨; Peirce's law by table; six argument forms and their countermodels; Post and Wittgenstein (1921): a decision procedure; its 2ⁿ cost. | Peirce's table; the verdicts; table time for 20 … 100 atoms; this machine's Python rows per second |
| 5 | `Normal` | CNF from the false rows; clauses and DIMACS; the 2ⁿ blowup of distribution; Tseitin's linear encoding (1968); Horn clauses and forward chaining; 2-SAT and 3-SAT. | distribution vs Tseitin clause counts for n = 1 … 12; a forward-chaining run, checked by entailment |
| 6 | `Deduction` | Jaśkowski and Gentzen; introduction and elimination rules; Fitch's boxes; modus tollens proved; the checker rejects a misuse of a closed subproof; Peirce's law and excluded middle need ¬¬E: the intuitionist divide (Part 9). | four proofs checked by the Reasoner; the broken one rejected with its message |
| 7 | `Soundness` | ⊢ and ⊨; soundness by induction on proofs; each rule's condition a tautology; an unsound rule's countermodel; consistency as a corollary. | the ten rule conditions checked; the countermodel |
| 8 | `Completeness` | completeness (Bernays 1918, Post 1921, Gödel 1929); the contrapositive strategy; Lindenbaum's lemma run; the truth lemma; compactness and de Bruijn–Erdős (1951). | 14 steps of Lindenbaum's construction and the valuation it decides; a properly coloured map (schematic) |
| 9 | `Resolution` | the resolution rule and its soundness by cases; refutation; Davis–Putnam (1960), Robinson (1965); the island refuted; refutation completeness. | the island's 10 clauses and a 5-step refutation; resolution's growth on pigeonhole formulas |
| 10 | `DPLL` | propagate, branch, back up (Davis, Logemann and Loveland 1962); a recorded search; reductio, done systematically. | the search tree (6 nodes, 2 conflicts) and its model; narration generated from the run |
| 11 | `CDCL` | GRASP (1996) and Chaff (2001); the implication graph; first-UIP learning; the backjump; CDCL as resolution (Pipatsrisawat and Darwiche 2011). | a recorded run: one conflict, the learned clause ¬a, the finish; DPLL vs CDCL decisions on random 3-SAT, n = 20 … 60, 7 seeds |
| 12 | `Cost` | P and NP; Cook–Levin (1971, 1973) by the tableau; the pigeonhole principle and Haken (1985); extended resolution (Cook 1976); Cook–Reckhow (1979); **the Wall's second brick**. | resolution (3 → 586,005 clauses) and CDCL (up to 1,608 conflicts) on PHP(n+1, n), n ≤ 7 |
| 13 | `Industry` | the Pentium FDIV bug (1994) and bounded model checking (1999); Zelkova and SMT at AWS; package installation; Schur 5, Keller 7; Appel–Haken (1976) and Tymoczko (1979) on computer proofs. | a dependency problem solved by the Reasoner |
| 14 | `Elenchus` | *Republic* I: Cephalus and Polemarchus; minimal unsatisfiable subsets; minimal correction sets; Reiter's hitting-set duality (1987); **the Price List engine**. | 128 subsets checked: 2 MUSes, 12 MCSes, duality verified |
| 15 | `Evil` | Epicurus, Hume's Philo, Mackie (1955); **the first Price List**: six claims, six positions (atheism, process theology, open theism, dystheism, evil as illusion, the free-will defense); what propositional logic cannot see. | the MUS (all six) and the six MCSes; the Socrates syllogism's countermodel |
| 16 | `Outro` | recap; the Reasoner's first module; the Wall; problems; payoffs; references. | — |

## Sources

Books: Enderton, *A Mathematical Introduction to Logic*, ch. 1; van Dalen, *Logic and Structure*, chs. 1–2; Sider,
*Logic for Philosophy*, ch. 2; Biere, Heule, van Maaren and Walsh (eds.), *Handbook of Satisfiability* (2nd ed.,
2021); Kneale and Kneale, *The Development of Logic*.

Papers and texts: Diogenes Laertius VII.80 and Sextus Empiricus, *Outlines* II.157 (the indemonstrables) and
*Against the Mathematicians* I.309 (Callimachus); Boole, *An Investigation of the Laws of Thought* (1854); Jevons,
"On the Mechanical Performance of Logical Inference" (Phil. Trans. 1870); Sheffer (1913); Post, "Introduction to a
General Theory of Elementary Propositions" (1921) and *The Two-Valued Iterative Systems of Mathematical Logic* (1941);
Bernays (1926); Gentzen, "Untersuchungen über das logische Schließen" (1935); Jaśkowski (1934); Fitch, *Symbolic
Logic* (1952); Tseitin (1968); Davis and Putnam (1960); Davis, Logemann and Loveland (1962); Robinson (1965); Cook
(1971, 1976); Levin (1973); Cook and Reckhow (1979); Haken (1985); Marques-Silva and Sakallah (1996, 1999);
Moskewicz et al. (2001); Pipatsrisawat and Darwiche (2011); Dowling and Gallier (1984); Aspvall, Plass and Tarjan
(1979); de Bruijn and Erdős (1951); Biere, Cimatti, Clarke and Zhu (1999); Backes et al. (2018); Rungta (CAV 2022);
Mancinelli et al. (2006); Heule, Kullmann and Marek (2016); Heule (2017); Brakensiek, Heule, Mackey and Narváez
(2020); Appel and Haken (1977); Tymoczko (J. Phil. 1979); Reiter (1987); Liffiton and Sakallah (2008); Plato,
*Republic* I 331c–335e (trans. Jowett); Hume, *Dialogues Concerning Natural Religion* X (1779); Mackie, "Evil and
Omnipotence" (Mind 1955); Plantinga, *God, Freedom, and Evil* (1974); Hick, *Evil and the God of Love* (1966);
Smullyan, *What Is the Name of This Book?* (1978); Bourget and Chalmers, "Philosophers on Philosophy: The 2020
PhilPapers Survey" (Phil. Imprint 2023).

## Problems and solutions

1. **Show that {→, ⊥} is functionally complete. Is {∨, →}?** ¬p ≡ p → ⊥ and p ∨ q ≡ ¬p → q ≡ (p → ⊥) → q, and
   {¬, ∨} is complete (De Morgan turns DNF into ¬ and ∨). By Post's criterion: → lies outside "keeps F" (F → F is
   T), outside "self-dual", "monotone" and "affine"; ⊥ lies outside "keeps T". {∨, →} is not complete: both keep T
   (each is true when all its inputs are), so everything built from them is true when every atom is, and ¬p is not.
2. **A Fitch proof of (p → q) → ((q → r) → (p → r)).** 1 | p → q (assumption); 2 | | q → r (assumption); 3 | | |
   p (assumption); 4 | | | q (→E 1, 3); 5 | | | r (→E 2, 4); 6 | | p → r (→I 3–5); 7 | (q → r) → (p → r) (→I
   2–6); 8 (p → q) → ((q → r) → (p → r)) (→I 1–7). The Reasoner's checker accepts it.
3. **Tseitin's clause count.** Our encoding gives each binary connective a fresh atom: three clauses for ∧, ∨ or →,
   four for ↔, and negations cost nothing (they flip a literal's sign). With k binary connectives of which m are ↔,
   that is 3(k − m) + 4m + 1 = 3k + m + 1 clauses, the 1 being the clause asserting the whole formula.
4. **The second island.** A ↔ ¬B and B ↔ (A ↔ C). If B is a knight, A and C are of the same kind; A's claim "B is a
   knave" is false, so A is a knave, so C is a knave. If B is a knave, A and C differ; A's claim is true, so A is a
   knight, so C is a knave. Two solutions (the Reasoner finds exactly these): nothing follows about A or B
   separately, but C is a knave either way.
5. **Every minimal correction set meets every minimal unsatisfiable subset.** Let M be an MCS and S an MUS, and
   suppose M ∩ S = ∅. Then S lies inside the complement of M, which is a maximal *satisfiable* subset; so S is
   satisfiable, contradicting its unsatisfiability. (The other half: a minimal hitting set H of the MUSes leaves a
   complement containing no MUS, hence satisfiable, and minimality of H makes it maximal.)
6. **(Essay) Another exit in *Republic* I.** Two good candidates. (a) Deny o: what is *owed* is what is *fitting*
   or *due*, so returning weapons to a madman is not owing anything; Polemarchus takes a version of this when he
   reinterprets Simonides, and much later Aristotle's account of justice as giving each what is due follows it. (b)
   Deny H: harming the wicked by punishment may make them better, not worse, a view Socrates himself defends in the
   *Gorgias*. A strong essay states the claim it rejects, the cost of rejecting it, and why that cost is lower than
   rejecting a definition.

## 习题与解答

1. **证明 {→, ⊥} 是函数完全的。{∨, →} 呢？** ¬p ≡ p → ⊥，p ∨ q ≡ ¬p → q ≡ (p → ⊥) → q；而 {¬, ∨} 是完全的（德摩根律把析取范式改写成只用
   ¬ 和 ∨）。用波斯特判据：→ 不在"保F"类中（F → F 为 T），也不在"自对偶""单调""仿射"类中；⊥ 不在"保T"类中。{∨, →} 不完全：两者都"保T"
   （所有输入为真时输出为真），所以由它们构造的一切公式在所有原子为真时都为真，而 ¬p 不是这样。
2. **(p → q) → ((q → r) → (p → r)) 的菲奇式证明。** 1 | p → q（假设）；2 | | q → r（假设）；3 | | | p（假设）；4 | | | q（→E 1, 3）；
   5 | | | r（→E 2, 4）；6 | | p → r（→I 3–5）；7 | (q → r) → (p → r)（→I 2–6）；8 (p → q) → ((q → r) → (p → r))（→I 1–7）。
   推理机的检查器接受这个证明。
3. **采廷编码的子句数。** 每个二元联结词得到一个新原子：∧、∨、→ 各三个子句，↔ 四个子句；否定不增加子句（只翻转文字的符号）。若共有 k 个二元
   联结词，其中 m 个是 ↔，子句数为 3(k − m) + 4m + 1 = 3k + m + 1，最后的 1 是断言整个公式为真的那个子句。
4. **第二座岛。** A ↔ ¬B，B ↔ (A ↔ C)。若 B 是骑士，则 A 与 C 同类；A 说"B 是无赖"为假，所以 A 是无赖，从而 C 也是无赖。若 B 是无赖，则 A 与 C
   不同类；A 的话为真，所以 A 是骑士，从而 C 是无赖。共两组解（推理机找到的正是这两组）：A 和 B 各自是什么无法确定，但无论哪种情况，C 都是无赖。
5. **每个极小修正集都与每个极小不可满足子集相交。** 设 M 是极小修正集，S 是极小不可满足子集，假设 M ∩ S = ∅。那么 S 包含在 M 的补集中，而这个补集
   是一个极大可满足子集，所以 S 可满足，与 S 不可满足矛盾。（另一半：所有极小不可满足子集的一个极小碰集 H，其补集不含任何极小不可满足子集，因而可
   满足；H 的极小性保证这个补集是极大的。）
6. **（论述题）《理想国》第一卷的另一条出路。** 两个好的候选：(a) 否认 o：所"欠"的是"应得的、恰当的"，因此把武器还给疯子并不是在还所欠之物；
   玻勒马霍斯重新解释西蒙尼德斯时走的正是这条路，后来亚里士多德把正义理解为"给每个人以其所应得"，也延续了这一思路。(b) 否认 H：用惩罚去伤害恶人，
   可能使他们变好而不是变坏，苏格拉底本人在《高尔吉亚篇》中就为这一观点辩护。一篇好的论述应当说明它拒绝哪个主张、拒绝的代价是什么，以及为什么
   这个代价比放弃一个定义更低。
