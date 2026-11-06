# Philosophy, Built — Part 3: All and Some

Part 3 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): first-order logic, from
Frege's notation to Lindström's theorem, and the first metaphysics it makes precise (Russell's descriptions, Skolem's
paradox, Quine's criterion). Its brick in **the Wall** is Church and Turing's theorem of 1936: validity in full
first-order logic is undecidable, only semi-decidable. Its **Price Lists** are Skolem's paradox and Plato's beard.

Every evaluation, count, proof, tableau, unifier and model on screen is computed by the Reasoner's first-order module
(`explainer/philosophy/reasoner/fol.py`: parser, Tarski satisfaction with a trace, a finite model finder, a ground
tableau that returns a countermodel from an open branch, a natural-deduction checker with the eigenvariable
conditions, unification and a given-clause resolution prover), tested in `tests/philosophy/test_fol.py`, and cached
by [`compute.py`](compute.py). The halting table in Chapter 10 is labelled illustrative.

## Build it

```bash
python -m videos.philosophy.philosophy3.compute        # every computed item (about 10 s; cached in .cache/philosophy3)
python tools/build.py philosophy3 -q l                 # 480p preview
python tools/build.py philosophy3                      # 1080p30 -> renders/philosophy3.mp4
python tools/qa_scene.py philosophy3 Tableau           # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | De Morgan's horse heads in the new notation; continuity's three quantifiers; Russell's king; the plan; the Wall's third brick. | the horse-heads tableau: closed, 29 steps, 9 branches |
| 1 | `Frege` | the *Begriffsschrift* (1879) and its two-dimensional notation; function and argument replace subject and predicate; relations as many-place functions; reception (Peano, *Principia*, Gentzen's ∀); Russell's letter (1902). | — |
| 2 | `Syntax` | terms and formulas; "first-order"; scope, binding, free variables, sentences; scope ambiguity; substitution, capture, renaming; why ∀E needs "free for"; de Bruijn indices (1972). | the capture example; ∀x∃y x≠y true at sizes 2–4, ∃y y≠y false everywhere |
| 3 | `Tarski` | Convention T (1933); object language and metalanguage; structures; the satisfaction clauses; ∀∃ and ∃∀ evaluated object by object; validity over all structures. | four people evaluated quantifier by quantifier; all 512 relations on 3 people: 343 = 7³ and 169 = 512 − 7³, entailment checked on each |
| 4 | `Express` | counting with identity; Russell's theory of descriptions (1905) and its scope ambiguity; Strawson (1950); the 256 moods inside first-order logic; "everybody loves a lover". | the counting formulas on every structure of size ≤ 4; the King of France in four worlds; 15 and 24 valid moods (agreeing with Part 1), countermodel sizes 1/2/3 = 159/81/1; the lover argument's tableau (718 steps) |
| 5 | `Proof` | Gentzen's quantifier rules and their conditions (1935); hasty generalization refused; a proof of ∃∀ ⊢ ∀∃ and the failed converse; the drinker principle and empty domains; sequents, cut elimination, and why it makes search possible. | the Reasoner's Fitch checker accepting one proof and rejecting two; the 2-object and 2-person countermodels; the drinker's 6-step tableau |
| 6 | `Tableau` | Beth and Hintikka (1955), Smullyan (1968); α, β, γ, δ; Barbara closed; an open branch read as a countermodel; the swap that grows forever. | the Barbara tree (9 steps, 3 branches); the open tree and its model a: S, P; b: P, M; the swap tableau giving up at 12 steps; the 2-person countermodel |
| 7 | `Complete` | Hilbert and Ackermann's question (1928); Gödel's completeness (1929); the consistent-set form; Henkin's proof (1949) step by step; three consequences; completeness vs incompleteness. | Henkin's construction in miniature: witness, four atoms decided, the term model checked |
| 8 | `Compact` | compactness and its one-line proof; λₙ; "finite" is inexpressible; nonstandard arithmetic (Skolem 1934) and the order type ω + ℤ·ℚ; Robinson's infinitesimals (1961). | λ₁ … λ₅ on sizes 1–6 |
| 9 | `Skolem` | Löwenheim (1915), Skolem (1920); upward and downward; the Skolem hull; Cantor's diagonal; **Price List**: Skolem's paradox (exit: relativity, Skolem 1922); Putnam's model-theoretic argument (1980). | the MUS {C, U, T, A} and its four MCSes |
| 10 | `Undecidable` | the *Entscheidungsproblem*; Church and Turing (1936); the halting diagonal; machines as sentences; semi-decidability; a sentence with only infinite models; **the Wall's third brick**; monadic logic and other decidable fragments; description logics, SNOMED CT, SMT; Trakhtenbrot (1950). | no model of the infinity axiom at sizes 1–4 (65,536 relations at size 4); smallest models of 300 random monadic sentences, never above 2² = 4 |
| 11 | `ATP` | Robinson's resolution (1965); Skolem functions; unification and the occurs check; Herbrand's theorem (1930); Robbins's problem and EQP (1996); Vampire, E, TPTP; Lean, Isabelle, Coq; hammers; AlphaProof (2024). | the most general unifier of Knows(john, x) and Knows(y, mother(y)); the occurs-check failure; a 3-step resolution refutation of the lover argument |
| 12 | `Second` | second-order induction and Dedekind's categoricity (1888); what second-order logic can say; what it loses; Quine's "set theory in sheep's clothing"; CH; Henkin semantics (1950); the Geach–Kaplan sentence and Boolos's plurals (1984). | — |
| 13 | `Lindstrom` | abstract logics; the map of extensions (Q₀, Q₁ and Keisler 1970, L_ω₁ω, second order); Lindström's theorem (1969); Quine, Shapiro (1991), Boolos and Tarski's permutation test (1966). | — |
| 14 | `Quine` | "On What There Is" (1948); Plato's beard; **Price List**: four exits (Russell–Quine, Meinong, free logic, fictional realism); the criterion of ontological commitment; indispensability; Carnap's internal and external questions (1950). | the MUS {N, A, B, E} and its four MCSes |
| 15 | `Outro` | recap; the Reasoner's second module; the Wall; problems; payoffs; references. | — |

## Sources

Books: Enderton, *A Mathematical Introduction to Logic*, ch. 2; Boolos, Burgess and Jeffrey, *Computability and
Logic* (5th ed., 2007); Smullyan, *First-Order Logic* (1968); Ebbinghaus, Flum and Thomas, *Mathematical Logic*;
Shapiro, *Foundations without Foundationalism* (1991); Sider, *Logic for Philosophy*, chs. 4–5; van Heijenoort (ed.),
*From Frege to Gödel* (1967).

Papers and texts: Frege, *Begriffsschrift* (1879); Russell, letter to Frege (16 June 1902) and "On Denoting" (Mind
1905); Löwenheim, "Über Möglichkeiten im Relativkalkül" (1915); Skolem (1920, 1922, 1934); Hilbert and Ackermann,
*Grundzüge der theoretischen Logik* (1928); Gödel, "Die Vollständigkeit der Axiome des logischen Funktionenkalküls"
(1930); Herbrand (1930); Tarski, "The Concept of Truth in Formalized Languages" (1933/1935) and "What Are Logical
Notions?" (1966, publ. 1986); Gentzen, "Untersuchungen über das logische Schließen" (1935); Church, "A Note on the
Entscheidungsproblem" (1936); Turing, "On Computable Numbers" (1936); Mal'tsev (1936); Quine, "On What There Is"
(1948), "Two Dogmas of Empiricism" (1951) and *Philosophy of Logic* (1970); Henkin, "The Completeness of the
First-Order Functional Calculus" (1949) and "Completeness in the Theory of Types" (1950); Carnap, "Empiricism,
Semantics, and Ontology" (1950); Strawson, "On Referring" (1950); Trakhtenbrot (1950); Beth (1955); Hintikka (1955);
Robinson, "A Machine-Oriented Logic Based on the Resolution Principle" (1965); A. Robinson, *Non-standard Analysis*
(1966); Lindström, "On Extensions of Elementary Logic" (Theoria 1969); Keisler (1970); de Bruijn (1972); Mortimer
(1975); van Inwagen, "Creatures of Fiction" (1977); Statman (1979); Orevkov (1979); Putnam, "Models and Reality"
(1980); Parsons, *Nonexistent Objects* (1980); Boolos, "To Be Is to Be a Value of a Variable (or to Be Some Values of
Some Variables)" (1984); McCune, "Solution of the Robbins Problem" (JAR 1997); Andréka, van Benthem and Németi (1998);
Priest, *Towards Non-Being* (2005); Gonthier (2005); Hales et al., Flyspeck (2017); DeepMind, AlphaProof (2024).

## Problems and solutions

1. **"Nobody loves everybody", twice; then "only philosophers admire Kant".** ¬∃x ∀y L(x, y), and equivalently
   ∀x ∃y ¬L(x, y): for each person there is someone they do not love. "Only philosophers admire Kant" says every
   admirer of Kant is a philosopher: ∀x (A(x, kant) → P(x)). (A common error is ∀x (P(x) → A(x, kant)), which is "all
   philosophers admire Kant".)
2. **A smallest countermodel to ∀x (P(x) ∨ Q(x)) ⊨ ∀x P(x) ∨ ∀x Q(x).** Two objects: a is P and not Q, b is Q and
   not P. Everything is P or Q, but not everything is P (b) and not everything is Q (a). One object cannot work: if it
   is P, everything is P. The Reasoner's model finder returns exactly this two-object structure.
3. **∃x Q(x) from ∀x (P(x) → Q(x)) and ∃x P(x).** 1 ∀x (P(x) → Q(x)) (premise); 2 ∃x P(x) (premise); 3 | P(a)
   (assumption, a new); 4 | P(a) → Q(a) (∀E 1); 5 | Q(a) (→E 4, 3); 6 | ∃x Q(x) (∃I 5); 7 ∃x Q(x) (∃E 2, 3–6). The new
   name is introduced at line 3; ∃E is legal because a occurs in neither premise nor in the conclusion ∃x Q(x). The
   Reasoner's `fol.check_fitch` accepts this proof.
4. **If φ has finite models of every size, it has an infinite one.** Consider {φ} ∪ {λ₂, λ₃, …}, where λₙ says
   there are at least n things. A finite part mentions only finitely many λₙ, say up to λ_N; a finite model of φ of
   size N satisfies it. By compactness the whole set has a model; it satisfies every λₙ, so it is infinite, and it
   satisfies φ.
5. **Skolemize ∀x ∃y ∀z ∃w R(x, y, z, w).** ∀x ∀z R(x, f(x), z, g(x, z)). The witness for y may depend only on the
   universal variables to its left (x); the witness for w on x and z. The result is satisfiable exactly when the
   original is (not equivalent: the Skolem functions add new symbols).
6. **(Essay) Plato's beard has four exits.** A strong answer chooses one and prices it. *Russell–Quine*: the cost is
   that proper names are not directly referential, which Kripke's *Naming and Necessity* (Part 27) attacks.
   *Meinong*: the cost is a realm of non-existent objects, and Russell's challenge: is the existent golden mountain
   existent? *Free logic*: the cost is a more complicated logic, and a decision about the truth of atomic sentences
   with empty names. *Fictional realism*: the cost is abstract artefacts, and a paraphrase for "Pegasus does not exist"
   that makes it true after all ("there is no flying horse").

## 习题与解答

1. **把"没有人爱所有人"写成两种等价形式，再写"只有哲学家欣赏康德"。** ¬∃x ∀y L(x, y)，等价地 ∀x ∃y ¬L(x, y)：对每个人，都有某个
   他不爱的人。"只有哲学家欣赏康德"是说每个欣赏康德的人都是哲学家：∀x (A(x, kant) → P(x))。（常见的错误是写成
   ∀x (P(x) → A(x, kant))，那是"所有哲学家都欣赏康德"。）
2. **∀x (P(x) ∨ Q(x)) ⊨ ∀x P(x) ∨ ∀x Q(x) 的最小反模型。** 两个对象：a 是 P 而不是 Q，b 是 Q 而不是 P。每个东西都是 P 或 Q，但并非
   每个东西都是 P（b 不是），也并非每个东西都是 Q（a 不是）。一个对象不行：如果它是 P，那么每个东西都是 P。推理机的模型搜索器给出的正是这个
   两对象结构。
3. **从 ∀x (P(x) → Q(x)) 和 ∃x P(x) 推出 ∃x Q(x)。** 1 ∀x (P(x) → Q(x))（前提）；2 ∃x P(x)（前提）；3 | P(a)（假设，a 是新名字）；
   4 | P(a) → Q(a)（∀E 1）；5 | Q(a)（→E 4, 3）；6 | ∃x Q(x)（∃I 5）；7 ∃x Q(x)（∃E 2, 3–6）。新名字在第3行引入；∃E 合法，因为 a
   既不出现在前提中，也不出现在结论 ∃x Q(x) 中。推理机的 `fol.check_fitch` 接受这个证明。
4. **如果 φ 有每一种有限大小的模型，那么它有一个无穷模型。** 考虑 {φ} ∪ {λ₂, λ₃, …}，其中 λₙ 说至少有 n 个东西。任何有限部分只提到有限
   多个 λₙ，比如到 λ_N 为止；φ 的一个大小为 N 的有限模型满足它。由紧致性，整个集合有一个模型；它满足每个 λₙ，所以是无穷的，并且它满足 φ。
5. **把 ∀x ∃y ∀z ∃w R(x, y, z, w) 斯科伦化。** ∀x ∀z R(x, f(x), z, g(x, z))。y 的见证只能依赖于它左边的全称变元（x）；w 的见证依赖于
   x 和 z。结果与原句同可满足（但不等价：斯科伦函数引入了新符号）。
6. **（论述题）柏拉图的胡子有四条出路。** 好的回答选择一条并给它标价。*罗素–蒯因*：代价是专名不是直接指称的，克里普克的《命名与必然性》
   （第27部分）攻击的正是这一点。*迈农*：代价是一个不实存对象的领域，以及罗素的诘难：实存的金山实存吗？*自由逻辑*：代价是更复杂的逻辑，以及
   必须决定含空名的原子句的真值。*虚构实在论*：代价是抽象的人造物，以及需要为"珀伽索斯不存在"找一个改写，使它终究为真（"没有会飞的马"）。
