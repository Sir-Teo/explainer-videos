# Philosophy, Built — Part 9: What Is Mathematics About?

Part 9 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): the philosophy of
mathematics, and the end of Act II. The Meno's doubled square; platonism (Plato, Frege, Gödel), Benacerraf's
"Mathematical truth" (1973) and Field's reliability challenge (1989); Kant against Frege on 7 + 5 = 12; Frege's numbers
as properties of concepts, Hume's principle and the Julius Caesar problem; Frege's theorem (Wright 1983, Boolos 1987)
step by step, and the discovery that Hume's principle has no finite model; neo-logicism and the bad company objection
(Basic Law V, the nuisance principle, Fine's stability); game formalism and Frege's reply, Bombelli's √−1 and
Hilbert's ideal elements; Brouwer, the digits of π and the weak counterexamples, and the continuity of every function;
the Curry–Howard correspondence, with a proof tree turned into a program, proof search, normalization and Griffin's
call/cc; predicativity, Russell's typical Englishman, Weyl and Feferman, and Gödel's defence of impredicativity;
Benacerraf's "What numbers could not be" (1965), Dedekind's categoricity, three structuralisms, and the identity of i
and −i; the indispensability argument (Quine, Putnam, Colyvan), Baker's cicadas and the objections; Field's
*Science without Numbers*, a representation theorem in miniature, and fictionalism; the Price List; homotopy type
theory and univalence; Lakatos's *Proofs and Refutations*; diagrams that prove (Liu Hui, Bhāskara) and lie (Curry's
missing square, Euclid I.1); and proofs by machine, from the four-colour theorem to Lean, the Liquid Tensor Experiment
and AI provers. Its brick in **the Wall** is "Benacerraf": we cannot know mathematical objects as we know tables. Its
**Price List** is the Benacerraf–Field puzzle: face-value reference, abstractness, knowledge, and the need for a
connection.

Every count, proof, program, symmetry and check on screen is computed by the Reasoner's new modules:
`explainer/philosophy/reasoner/types.py` (propositions as types: a parser, a forty-line type checker, proof search
that returns lambda terms, Kripke countermodels, normalization by reduction, transport between unary and binary
numerals, winding numbers) and `explainer/philosophy/reasoner/mathphil.py` (Frege's numbers on a finite domain,
abstraction principles counted, a model of Hume's principle, Bombelli's arithmetic, the digits of π by Gibbons's
spigot, Brouwer's real, Goldbach checked, Russell's typical Englishman, automorphisms of small structures, cicada
periods, Field's betweenness and congruence with every coordinate system, Euler characteristics, the missing square,
and a misstated Euclid), tested in `tests/philosophy/test_types.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy9.compute        # every computed item (about half a minute; .cache/philosophy9)
python tools/build.py philosophy9 -q l                 # 480p preview
python tools/build.py philosophy9                      # 1080p30 -> renders/philosophy9.mp4
python tools/qa_scene.py philosophy9 Curry             # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Russell's joke (1901); the Meno; necessary, a priori, applicable (Wigner 1960); six answers; the plan. | the boy's squares: 16, 9, and 8 on the diagonal |
| 1 | `Platonism` | Plato, Frege, Gödel (1944, 1964); Benacerraf's dilemma (1973); Field's reliability challenge (1989). | — |
| 2 | `Logicism` | Kant (1781) and Frege (1884) on 7 + 5 = 12; numbers belong to concepts; Hume's principle; Julius Caesar and Basic Law V. | 16 concepts on four objects fall into five numbers, 1-4-6-4-1, with successor running 0 → 4 |
| 3 | `Theorem` | Parsons, Wright (1983), Boolos (1987); numbers counting themselves; the key steps of Frege's theorem. | Hume's principle fails on every world of 1–5 objects; a model on ℕ checked on all 127 finite concepts on seven objects |
| 4 | `Company` | neo-logicism (Hale and Wright 2001); directions; Basic Law V and the nuisance principle; Dummett, Boolos (1997), Fine (2002). | objects needed by HP, BLV and NP on worlds of 1–5 objects, and on ℵ₀ |
| 5 | `Formalism` | Heine (1872), Thomae (1880) and Frege (1903); Bombelli (1572); Hilbert's letter (1899) and ideal elements (1925); Curry (1951). | (2 + i)³ = 2 + 11i, so x = 4 solves x³ = 15x + 4 |
| 6 | `Brouwer` | Brouwer (1907, 1908, 1924); the weak counterexamples; Bishop (1967). | 3,000 digits of π; six 9s at place 762; Goldbach checked to 100,000; Brouwer's real |
| 7 | `Curry` | Curry and Feys (1958), Howard (1969/1980); the dictionary; a proof as a program; Prawitz (1965); Griffin (1990); Martin-Löf. | proof search for ten propositions: seven programs, type-checked, and three countermodels; a proof normalized step by step |
| 8 | `Predicative` | Poincaré (1906), Russell (1908); the typical Englishman; Weyl (1918), Feferman–Schütte (1964), Feferman (1988); Gödel (1944). | typical at level 0: Edith; at level 1 and over all 128 properties: nobody |
| 9 | `Structure` | Benacerraf (1965); Dedekind (1888); *ante rem*, eliminative and modal structuralism; Burgess, Keränen, Shapiro (2008), Ladyman (2005); **the Wall's ninth brick**. | unary and binary numerals: inverse maps respecting successor; the symmetries of {1, i, −1, −i} and of five graphs |
| 10 | `Indisp` | Quine (1948), Putnam (1971), Colyvan (2001); Baker's cicadas (2005); Maddy (1992), Sober (1993), Melia (2000). | coincidence rates for cycles of 10–20 years: the primes are the low points, 13 and 17 between 12 and 18 |
| 11 | `Field` | Field (1980) and Hilbert's geometry (1899); conservativeness; fictionalism; Malament (1982), Shapiro (1983), the easy road. | five points known by 20 betweenness and 6 congruence facts: exactly four coordinate systems, x ↦ ±x, ±2x |
| 12 | `Price` | **Price List**: the Benacerraf–Field puzzle; four answers side by side. | the MUS {O, A, K, C} and its four corrections |
| 13 | `Univalence` | identity as paths (Hofmann–Streicher, Awodey–Warren, Voevodsky); the circle (Licata–Shulman 2013); univalence; structuralism built in. | winding numbers 0, 1, 2, −1; "even" transported from unary to binary |
| 14 | `Lakatos` | Euler (1750), Cauchy (1813); Lakatos (1976); monster-barring, exception-barring, lemma-incorporation; χ = 2 − 2g. | V − E + F for tetrahedron, cube, octahedron (2), picture frame (0), twin tetrahedra (3), the urchin (−6) |
| 15 | `Pictures` | the Zhoubi and Liu Hui (263); Bhāskara; proofs that explain (Steiner 1978, Lange 2017); Curry's missing square (1953); Euclid I.1, Pasch, Hilbert, Manders. | odd numbers as L-shaped layers; slopes 3/8, 2/5, 5/13 and areas 32, 33, 32½ |
| 16 | `Machines` | Appel–Haken (1976), Tymoczko (1979), Gonthier (2005); de Bruijn's criterion; Lean and Mathlib; the Liquid Tensor Experiment (2020–22); Flyspeck; AI provers (2024, 2025); Thurston (1994). | the Reasoner's kernel: 40 lines; "there is a prime" certified with the witness 2 |
| 17 | `Outro` | recap; the Reasoner's two modules; the Wall; problems; payoffs; references. | — |

## Sources

Books: Shapiro, *Thinking about Mathematics* (2000) and *Philosophy of Mathematics: Structure and Ontology* (1997);
Linnebo, *Philosophy of Mathematics* (2017) and *Thin Objects* (2018); Benacerraf and Putnam (eds.), *Philosophy of
Mathematics: Selected Readings* (1964, 2nd ed. 1983); Hale and Wright, *The Reason's Proper Study* (2001); Wright,
*Frege's Conception of Numbers as Objects* (1983); Heck, *Frege's Theorem* (2011); Fine, *The Limits of Abstraction*
(2002); Field, *Science without Numbers* (1980) and *Realism, Mathematics and Modality* (1989); Colyvan, *The
Indispensability of Mathematics* (2001); Maddy, *Realism in Mathematics* (1990); Hellman, *Mathematics without Numbers*
(1989); Balaguer, *Platonism and Anti-Platonism in Mathematics* (1998); Leng, *Mathematics and Reality* (2010);
Bishop, *Foundations of Constructive Analysis* (1967); Sørensen and Urzyczyn, *Lectures on the Curry–Howard
Isomorphism* (2006); the Univalent Foundations Program, *Homotopy Type Theory* (2013); Lakatos, *Proofs and
Refutations* (1976); Lange, *Because Without Cause* (2017).

Papers and texts: Plato, *Meno* 82b–85b; Liu Hui, commentary on the *Nine Chapters* (263); Bombelli, *L'Algebra*
(1572); Hume, *Treatise* I.iii.1 (1739); Kant, *Critique of Pure Reason* B15 (1781); Frege, *Grundlagen* (1884) and
*Grundgesetze* II (1903); Dedekind (1888); Hilbert to Frege (1899), *Grundlagen der Geometrie* (1899), "On the
infinite" (1925); Russell (1901, 1908); Poincaré (1906); Brouwer (1907, 1908, 1924); Weyl, *Das Kontinuum* (1918);
Curry (1934), Curry and Feys (1958); Gödel (1944, 1964); Quine (1948); Wigner (1960); Benacerraf (1965, 1973); Parsons
(1965); Prawitz (1965); Howard (1969, published 1980); Putnam (1971); Martin-Löf (1972, 1984); Feferman–Schütte (1964);
Appel and Haken (1976); Steiner (1978); Tymoczko (1979); Malament (1982); Shapiro (1983, 2008); Boolos (1987, 1997);
Feferman (1988); Griffin (1990); Maddy (1992); Sober (1993); Thurston (1994); Hofmann and Streicher (1994); Resnik
(1997); Pollack (1998); Burgess (1999); Melia (2000); Keränen (2001); Gonthier (2005); Baker (2005); Ladyman (2005);
Manders (2008); Awodey and Warren (2009); Licata and Shulman (2013); Avigad, "Mathematics and the formal turn" (2024).

## Problems and solutions

1. **Frege's numbers on five objects.** There are 2⁵ = 32 concepts. Pairing off sorts them by size into six numbers,
   0 to 5, with 1, 5, 10, 10, 5 and 1 concepts each (a row of Pascal's triangle). Hume's principle makes each number an
   object of the domain and different numbers different objects, so it needs six objects in a world of five: by the
   pigeonhole principle, it cannot hold.
2. **Basic Law V and Hume's principle.** Basic Law V needs a one-to-one map from the concepts on a domain D (its
   subsets) into D itself. By Cantor's theorem (Part 6) there are more subsets than elements for every D, finite or
   infinite, so it has no model. Hume's principle holds on {0, 1, 2, …} with #F = 0 if F is infinite and #F = |F| + 1
   if F is finite: two finite concepts get the same number exactly when they have the same size; two infinite concepts
   on a countable domain are both countably infinite, so equinumerous, and both get 0; and a finite and an infinite
   concept are neither equinumerous nor given the same number.
3. **A program and a countermodel.** λf. λg. λx. g (f x), composition, has type (A → B) → (B → C) → A → C. For
   Peirce's law take two worlds w₀ ≤ w₁, with A true only at w₁ and B nowhere. A → B fails at w₀ and at w₁ (at w₁, A
   holds and B does not), so (A → B) → A holds at w₀ vacuously; A does not hold at w₀; so the root does not force
   ((A → B) → A) → A.
4. **Brouwer's real and continuity.** r = 0 exactly when Goldbach's conjecture is true, so a constructive proof of
   "r = 0 or r ≠ 0", which must say which, would decide the conjecture. A computable function on the reals reads
   finitely many digits of x before it outputs f(x) to a given precision; all reals that share those digits, an
   interval around x, get the same output to that precision, which is continuity at x.
5. **Symmetry.** A path of four points has two symmetries, the identity and the reversal (the ends swap, and so do the
   inner points); the reversal fixes no point, so no single point is picked out by structure alone, though "an end"
   and "an inner point" are structural kinds. The square has eight symmetries; the rotation by a quarter turn fixes no
   corner.
6. **(Essay) The Price List.** A strong answer uses Chapter 12's Price List and comparison table, and meets the
   objection its exit faces: for concrete numbers, the infinite; for modal structuralism, knowledge of possibility;
   for fictionalism, why the fiction applies (Wigner); for platonism, Field's reliability challenge.

## 习题与解答

1. **五个对象上的弗雷格数。** 共有2⁵ = 32个概念。一一配对把它们按大小分成六个数，0到5，每个数分别有1、5、10、10、5和1个概念（帕斯卡三角形的
   一行）。休谟原则使每个数都是论域中的一个对象，且不同的数是不同的对象，所以在五个对象的世界里它需要六个对象：由鸽巢原理，它不能成立。
2. **基本定律V与休谟原则。** 基本定律V需要一个从论域D上的概念（D的子集）到D自身的一一映射。由康托尔定理（第6部），对每个D，无论有限还是
   无穷，子集都比元素多，所以它没有模型。休谟原则在{0, 1, 2, …}上成立：F无穷时令#F = 0，F有限时令#F = |F| + 1。两个有限概念恰好在大小相同
   时得到同一个数；可数论域上的两个无穷概念都是可数无穷的，因而等数，都得到0；一个有限概念和一个无穷概念既不等数，也不得到同一个数。
3. **一个程序和一个反模型。** λf. λg. λx. g (f x)，即复合，类型为(A → B) → (B → C) → A → C。对皮尔士定律取两个世界w₀ ≤ w₁，A只在w₁为真，
   B处处为假。A → B在w₀和w₁都不成立（在w₁，A成立而B不成立），所以(A → B) → A在w₀空洞地成立；A在w₀不成立；所以根世界不迫使
   ((A → B) → A) → A。
4. **布劳威尔的实数与连续性。** r = 0恰好当哥德巴赫猜想为真，所以“r = 0或r ≠ 0”的构造性证明——它必须说出是哪一个——会判定这个猜想。实数上的
   可计算函数在以给定精度输出f(x)之前只读取x的有限多位数字；所有共享这些数字的实数，即x周围的一个区间，在这一精度下得到相同的输出，这就是在x
   处的连续性。
5. **对称性。** 四个点的路径有两个对称：恒等和翻转（两端互换，两个内点也互换）；翻转不固定任何点，所以没有哪个单独的点能仅凭结构挑出，尽管
   “端点”和“内点”是结构上的种类。正方形有八个对称；转四分之一圈的旋转不固定任何角。
6. **（论述题）代价清单。** 好的回答利用第12章的代价清单和比较表，并回应其出路所面对的反驳：对具体的数，是无穷；对模态结构主义，是关于可能性的
   知识；对虚构主义，是虚构为何适用（维格纳）；对柏拉图主义，是菲尔德的可靠性挑战。
