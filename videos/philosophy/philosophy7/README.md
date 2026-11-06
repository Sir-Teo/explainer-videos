# Philosophy, Built — Part 7: The Limits of Proof

Part 7 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): Gödel, Turing, Tarski and Löb.
Hilbert's program and a formal system to play (MIU); Robinson's Q and Peano arithmetic, axiom by axiom, and their
nonstandard models; primitive recursion and Ackermann's function; the Chinese remainder theorem, from Master Sun to
Gödel's β-function; Gödel numbering; quines, Quine's sentence and the diagonal lemma; the first incompleteness theorem,
Rosser's sentence, the truth of G and Hilbert's tenth problem; the second theorem, the derivability conditions and the
logic GL; Turing machines and busy beavers to BB(5); the Church–Turing thesis and Rice's theorem; Ramsey,
Paris–Harrington and natural independence; Berry's paradox, Chaitin and Ω; Tarski's undefinability of truth and the
definability of partial truth; Löb's theorem and the fixed points of provability logic; Lucas, Penrose and Gödel's
disjunction; Gentzen's consistency proof, ordinal analysis and reverse mathematics. Its brick in **the Wall** is
"Gödel": incompleteness, undecidability, undefinability and Löb, one diagonal argument. Its **Price List** is minds and
machines: mechanism, knowledge of our own consistency, and consistency itself.

Every derivation, code, number, run and check on screen is computed by the Reasoner's arithmetic module
(`explainer/philosophy/reasoner/arith.py`: Robinson's Q as a rewriting system, primitive recursive combinators and
Ackermann's function, the Chinese remainder theorem and Gödel's β-function, Gödel numbering both ways, a quine and the
diagonal sentence checked, Hofstadter's MIU, a Turing-machine simulator fast enough for the five-state champion, an
exhaustive two-state busy beaver search, R(3,3) by brute force, shortest names in a toy language, a truth predicate for
bounded sentences, and provability logic on every finite GL frame), tested in `tests/philosophy/test_arith.py` and
cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy7.compute        # every computed item (about ten seconds; cached in .cache/philosophy7)
python tools/build.py philosophy7 -q l                 # 480p preview
python tools/build.py philosophy7                      # 1080p30 -> renders/philosophy7.mp4
python tools/qa_scene.py philosophy7 Beavers           # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Königsberg, 7–8 September 1930: Gödel's announcement and Hilbert's "we must know"; Hilbert's three wishes and who took each; the plan. | — |
| 1 | `Program` | formalism and metamathematics (Hilbert, Bernays, Ackermann; the *Entscheidungsproblem*, 1928); Hofstadter's MIU (1979); the mod-3 invariant: a proof *about* a system. | MIU's theorems to depth 3 as a tree; 1,730 theorems within seven steps, none of them MU |
| 2 | `Arith` | Robinson's Q (1950), axiom by axiom; Q computes; Q cannot prove ∀x (0 + x = x); induction (Dedekind 1888, Peano 1889) and PA; nonstandard models (Skolem 1934), Tennenbaum (1959). | 2 + 2 = 4 in three steps and 2 × 2 = 4 in nine, each step an axiom of Q |
| 3 | `Recursion` | the five combinators; primitive recursion; Ackermann (1928) and Péter; the diagonal against the primitive recursive functions; representability and Σ₁-completeness. | add, mul, exp, pred, fact as combinator trees, with sizes and values; A(m, n) for m ≤ 3, A(4, 1) = 65,533, A(4, 2) with 19,729 digits |
| 4 | `Beta` | why recursion needs lists; Sunzi's problem (c. 400) and Qin Jiushao (1247): the Chinese remainder theorem; Gödel's β-function. | 23 found by sieving; the list 2, 3, 5 coded as c = 5,482,512, d = 120, and decoded |
| 5 | `Numbering` | codes for symbols; a formula as a product of prime powers; decoding by factoring; proofs as numbers; Form, Prf, Prov. | ⌜0 = 0⌝ = 2²¹·3¹⁵·5²¹; ∀x(x + 0 = x) decoded from its 115-digit number; a two-line proof's number has about 10⁶⁸ digits |
| 6 | `Diagonal` | the regress of naive self-reference; quines and Kleene's recursion theorem (1938); Quine's sentence (1962); the diagonal lemma (Gödel 1931, Carnap 1934), proved. | a Python quine run and compared; Quine's sentence and a Gödel-style sentence checked to refer to themselves |
| 7 | `First` | G ↔ ¬Prov(⌜G⌝); the proof, with ω-consistency; Rosser (1936); G is true; Hilbert's tenth problem and MRDP (1970). | — |
| 8 | `Second` | Con(PA); PA ⊢ Con → G; Gödel II; the derivability conditions (Hilbert–Bernays 1939, Löb 1955); GL; **the Wall's seventh brick**. | ¬□⊥ → ¬□¬□⊥ on all 242 finite GL frames with up to four worlds |
| 9 | `Turing` | Turing's analysis of the human computer (1936); Church, Post; a two-state machine run; space–time diagrams; the universal machine. | the two-state champion step by step; Brady's four-state machine, all 107 steps |
| 10 | `Beavers` | Radó's busy beaver (1962); why BB is uncomputable; the champions; bbchallenge (2024); cryptids, Goldbach and Riemann machines; Yedidia–Aaronson (2016) and the ZFC frontier. | all 20,736 two-state machines run: 9,784 halt, at most 6 steps and 4 ones; the champions for 2–5 states, with BB(5) = 47,176,870 and 4,098 ones |
| 11 | `Thesis` | the convergence of definitions; the Church–Turing thesis; what it does not say (Gandy 1980, Shor 1994); Rice's theorem (1953). | — |
| 12 | `Ramsey` | Ramsey (1930) and R(3,3) = 6; Paris–Harrington (1977); Kruskal and TREE(3) (Friedman); the graph minor theorem. | all 1,024 colourings of K₅ (12 without a one-coloured triangle) and all 32,768 of K₆ (none) |
| 13 | `Berry` | Berry's paradox (Russell 1906); a toy language and its shortest names; Kolmogorov complexity; Chaitin's theorem (1974); Ω (1975) and Franzén's caution. | the shortest names of 1–300; the least numbers with no name of 3, 5, 7 symbols: 19, 92, 239 |
| 14 | `Tarski` | the undefinability of truth (1933); partial truth predicates; truth and proof apart. | four bounded sentences decided by the Reasoner's Δ₀ truth predicate |
| 15 | `Lob` | Henkin's question (1952); Löb's theorem (1955) in nine lines; Gödel II as a corollary; the fixed points of GL (de Jongh, Sambin), Solovay (1976). | Gödel's and Henkin's fixed points and their uniqueness, on all 242 finite GL frames |
| 16 | `Minds` | Lucas (1961) and Penrose (1989, 1994); **Price List**: minds and machines (Benacerraf 1967, Putnam, Feferman; Turing 1947); Gödel's disjunction (1951); Franzén's misuses (2005). | the MUS {M, K, C} and its three corrections |
| 17 | `Gentzen` | Gentzen's consistency proof (1936) and its ε₀; ordinal analysis; reverse mathematics and the Big Five (Friedman, Simpson); what became of Hilbert's program. | — |
| 18 | `Outro` | recap; the Reasoner's arithmetic module; the Wall; problems; payoffs; references. | — |

## Sources

Books: Smith, *An Introduction to Gödel's Theorems* (2nd ed., 2013); Boolos, Burgess and Jeffrey, *Computability and
Logic* (5th ed., 2007), chs. 15–18; Boolos, *The Logic of Provability* (1993); Franzén, *Gödel's Theorem: An Incomplete
Guide to Its Use and Abuse* (2005); Hofstadter, *Gödel, Escher, Bach* (1979); Simpson, *Subsystems of Second Order
Arithmetic* (1999); Li and Vitányi, *An Introduction to Kolmogorov Complexity and Its Applications* (3rd ed., 2008);
Kaye, *Models of Peano Arithmetic* (1991); Davis (ed.), *The Undecidable* (1965).

Papers and texts: *Sunzi Suanjing* (c. 400); Qin Jiushao, *Shushu Jiuzhang* (1247); Dedekind (1888); Peano (1889);
Hilbert, "Mathematical problems" (1900), "On the infinite" (1926) and the Königsberg address (1930); Russell (1906);
Hilbert and Ackermann (1928); Ackermann (1928); Ramsey (1930); Gödel (1931; Gibbs lecture 1951); Tarski (1933);
Carnap (1934); Skolem (1934); Péter (1935); Turing (1936; 1947 lecture); Church (1936); Post (1936); Rosser (1936);
Gentzen (1936, 1943); Kleene (1938); Hilbert and Bernays, *Grundlagen der Mathematik* II (1939); Robinson (1950);
Henkin (1952); Rice (1953); Löb (1955); Tennenbaum (1959); Lucas, "Minds, machines and Gödel" (1961); Radó (1962);
Quine, "The ways of paradox" (1962); Lin and Radó (1965); Kolmogorov (1965); Benacerraf, "God, the Devil, and Gödel"
(1967); Matiyasevich (1970); Chaitin (1974, 1975); de Jongh (1975) and Sambin (1976); Solovay (1976); Paris and
Harrington (1977); Gandy (1980); Kirby and Paris (1982); Brady (1983); Marxen and Buntrock (1989); Penrose (1989,
1994); Shor (1994); Robertson and Seymour (2004); Cook (2004); Yedidia and Aaronson (2016); Aaronson, "The busy beaver
frontier" (2020); the Busy Beaver Challenge (2024).

## Problems and solutions

1. **MIU.** MI →(2) MII →(2) MIIII →(2) MIIIIIIII →(1) MIIIIIIIIU →(3) MIIIIIUU →(4) MIIIII. (The Reasoner's
   breadth-first search finds this six-step derivation.) MUIIIU has three I's, a multiple of three, so the invariant of
   Chapter 1 rules it out. In fact a string M*x* is a theorem exactly when its number of I's is not a multiple of three.
2. **1 × 2 = 2 in Q.** S0 × SS0 = (S0 × S0) + S0 (Q7) = ((S0 × 0) + S0) + S0 (Q7) = (0 + S0) + S0 (Q6) =
   S(0 + 0) + S0 (Q5) = S0 + S0 (Q4) = S(S0 + 0) (Q5) = SS0 (Q4). Seven steps; the Reasoner's `q_steps` gives the same.
3. **Remainders.** x ≡ 1 (mod 4), x ≡ 2 (mod 5), x ≡ 3 (mod 7): x = 17 (and 17 + 140k). To code 1, 2, 3 with β, take
   s = 3, d = 3! = 6; the moduli 1 + d = 7, 1 + 2d = 13, 1 + 3d = 19 are pairwise coprime, and the Chinese remainder
   theorem gives c = 288: 288 mod 7 = 1, 288 mod 13 = 2, 288 mod 19 = 3.
4. **PA ⊢ Con(PA) → G.** Write □ for Prov. G ↔ ¬□G gives PA ⊢ G → ¬□G, so by D1 and D2, PA ⊢ □G → □¬□G. By D3,
   PA ⊢ □G → □□G. Together, PA ⊢ □G → □(□G ∧ ¬□G), and since □G ∧ ¬□G → ⊥ is provable, D1 and D2 give PA ⊢ □G → □⊥.
   Contraposing: PA ⊢ ¬□⊥ → ¬□G, that is, Con(PA) → G.
5. **Equivalence is undecidable.** Fix any program P₀. "Computes the same function as P₀" is a property of what a
   program does, and it is non-trivial (P₀ has it; a program computing a different function does not). By Rice's
   theorem it is undecidable. A decider for "do P and Q compute the same function?" would decide it, by taking
   Q = P₀; so there is none.
6. **(Essay) Minds and machines.** A strong answer uses Chapter 16's Price List. For Lucas: say what grounds our
   knowledge that our own system is consistent, given that we have believed inconsistent things before (naive set
   theory, Part 6). For Benacerraf: say whether we could be a machine we cannot identify, and whether that is a
   coherent picture of mathematical knowledge. Either way, note Gödel's disjunction: the theorems leave open both a
   mind beyond machines and absolutely unsolvable problems.

## 习题与解答

1. **MIU。** MI →(2) MII →(2) MIIII →(2) MIIIIIIII →(1) MIIIIIIIIU →(3) MIIIIIUU →(4) MIIIII。（推理机的广度优先搜索找到了这个
   六步推导。）MUIIIU有三个I，是3的倍数，所以第1章的不变量排除了它。事实上，一个串M*x*是定理，恰好当其中I的个数不是3的倍数。
2. **在Q中推出1 × 2 = 2。** S0 × SS0 = (S0 × S0) + S0（Q7）= ((S0 × 0) + S0) + S0（Q7）= (0 + S0) + S0（Q6）=
   S(0 + 0) + S0（Q5）= S0 + S0（Q4）= S(S0 + 0)（Q5）= SS0（Q4）。共七步；推理机的`q_steps`给出同样的结果。
3. **余数。** x ≡ 1 (mod 4)，x ≡ 2 (mod 5)，x ≡ 3 (mod 7)：x = 17（以及17 + 140k）。要用β编码1, 2, 3，取s = 3，d = 3! = 6；
   模数1 + d = 7、1 + 2d = 13、1 + 3d = 19两两互素，中国剩余定理给出c = 288：288 mod 7 = 1，288 mod 13 = 2，288 mod 19 = 3。
4. **PA ⊢ Con(PA) → G。** 把Prov写成□。由G ↔ ¬□G得PA ⊢ G → ¬□G，于是由D1和D2，PA ⊢ □G → □¬□G。由D3，PA ⊢ □G → □□G。
   合起来，PA ⊢ □G → □(□G ∧ ¬□G)；而□G ∧ ¬□G → ⊥是可证的，所以由D1和D2得PA ⊢ □G → □⊥。取逆否：PA ⊢ ¬□⊥ → ¬□G，即
   Con(PA) → G。
5. **等价性不可判定。** 固定任一程序P₀。“与P₀计算同一个函数”是关于程序做什么的性质，而且是非平凡的（P₀有，计算别的函数的程序没有）。
   由赖斯定理，它不可判定。一个判定“P与Q是否计算同一个函数”的程序，取Q = P₀就能判定它；所以这样的程序不存在。
6. **（论述题）心灵与机器。** 好的回答利用第16章的代价清单。若站在卢卡斯一边：要说明我们凭什么知道自己的系统是一致的，毕竟我们以前就相信
   过不一致的东西（朴素集合论，第6部分）。若站在贝纳塞拉夫一边：要说明我们是否可能是一台自己无法辨认的机器，以及这是否是一幅融贯的数学
   知识图景。无论哪种，都要注意哥德尔的析取：这些定理既没有排除超越机器的心灵，也没有排除绝对不可解的问题。
