# Philosophy, Built — Part 6: Paradise and Paradox

Part 6 of *Philosophy, Built* ([series plan](../README.md), [syllabus](../SYLLABUS.md)): sets and the infinite. Galileo's
paradox and Hilbert's hotel; Cantor's countings and his diagonal; the absolute and its critics (Kronecker, Poincaré,
Weyl, Brouwer, Wittgenstein); Russell's letter and the axioms of ZFC; sets built from nothing and stacked in the
cumulative hierarchy; ordinals to ε₀, Goodstein's sequences and the hydra; the alephs and the size of the continuum;
choice, Vitali and Banach–Tarski; Gödel's L and Cohen's forcing; large cardinals and determinacy; realism, the
multiverse and rival foundations. Its brick in **the Wall** is "Russell; Cohen": not every condition defines a set,
and the axioms cannot settle the continuum. Its **Price List** is the continuum: realism, provability from justified
axioms, and the hope of new axioms.

Every count, code, table, ordinal, sequence and check on screen is computed by the Reasoner's set module
(`explainer/philosophy/reasoner/sets.py`: hereditarily finite sets and Ackermann's coding, the finite stages of the
hierarchy, Cantor's theorem by brute force, Cantor's pairing and the Calkin–Wilf enumeration, ordinal arithmetic below
ε₀ in Cantor normal form, Goodstein's sequences with their ordinals, the hydra battle, Kuratowski pairs, the free
group's paradoxical decomposition, a generic real, and Zermelo's backward induction), tested in
`tests/philosophy/test_sets.py` and cached by [`compute.py`](compute.py).

## Build it

```bash
python -m videos.philosophy.philosophy6.compute        # every computed item (a few seconds; cached in .cache/philosophy6)
python tools/build.py philosophy6 -q l                 # 480p preview
python tools/build.py philosophy6                      # 1080p30 -> renders/philosophy6.mp4
python tools/qa_scene.py philosophy6 Goodstein         # one chapter, silent, with a contact sheet
```

## Chapters

| # | Scene | What it establishes | Computed on screen |
|---|---|---|---|
| 0 | `Hook` | Hilbert's paradise (1926); squares and numbers; the diagonal and the two bricks; the plan. | the squares paired with the numbers; an 8 × 8 diagonal |
| 1 | `Hotel` | Aristotle's potential infinite; Galileo (1638); Hilbert's hotel: one guest, a bus; Bolzano (1851); Dedekind's definition of the infinite (1888); Cantor's definition of size. | the maps n ↦ n + 1 and n ↦ 2n on the rooms |
| 2 | `Countable` | Cantor's pairing of ℕ × ℕ; infinitely many buses; the Calkin–Wilf tree (2000); ℚ and the algebraic numbers countable, ℝ not (1874). | the pairing on a 6 × 6 grid; four levels of the tree and the first 15 rationals |
| 3 | `Diagonal` | the diagonal argument (1891); Cantor's theorem \|X\| < \|𝒫(X)\|, with the proof drawn; the endless ladder of infinities. | the diagonal of 8 listed rows; all 2, 16, 512 and 65,536 functions from sets of size 1–4 to their power sets miss the diagonal set |
| 4 | `Absolute` | Cantor's transfinite and absolute; inconsistent multiplicities (1899); Kronecker, Poincaré, Weyl, Brouwer; Wittgenstein (1939); the diagonal as an algorithm. | — |
| 5 | `Russell` | Frege's Basic Law V (1893); Russell's letter (1902); the paradox; Frege's reply; Burali-Forti, Cantor, Curry; half of the Wall's brick. | r ↔ ¬r unsatisfiable; c ↔ (c → q) ⊨ q |
| 6 | `Axioms` | types (Russell 1908) and axioms (Zermelo 1908); separation turns the paradox into a theorem; ZFC axiom by axiom (Fraenkel, Skolem 1922; von Neumann 1925). | — |
| 7 | `HF` | von Neumann's numbers (1923); Ackermann's coding (1937); V₀ … V₅; Kuratowski pairs; Zermelo's numerals; Benacerraf's question. | the first 16 hereditarily finite sets as boxes; the bijection for every n < 4096; \|Vₙ\| = 0, 1, 2, 4, 16, 65,536; Kuratowski pairs on all 256 pairs of 16 sets |
| 8 | `Cone` | the cumulative hierarchy; Zermelo (1930) and Boolos's iterative conception (1971); foundation; proper classes and limitation of size. | — |
| 9 | `Ordinals` | ω and beyond; all ordinals below ω² on one line; non-commutative arithmetic; Cantor normal form; ε₀; transfinite induction. | 1 + ω = ω, ω + 1 > ω, 2·ω = ω, ω·2 = ω + ω; a ladder of 17 ordinals up to ω^ω^ω, each comparison checked |
| 10 | `Goodstein` | hereditary base; Goodstein's game (1944); the sequences from 3 and 4; the ordinal proof; Kirby–Paris (1982). | the sequence from 3 to 0; the first terms from 4 (4, 26, 41, 60, 83, 109, 139, 173) with strictly falling ordinals |
| 11 | `Hydra` | Kirby and Paris's hydra; the battle and its ordinal; every strategy wins; unprovable in PA. | a battle of 13 blows drawn with its ordinals; blows for a neck of k heads: 3, 13, 22,539,988,369,405, and more than 10³⁰⁰⁰ |
| 12 | `Cardinals` | the alephs; infinite arithmetic (Hessenberg 1906); \|ℝ²\| = \|ℝ\| (Cantor 1877); Hilbert's curve; Brouwer's dimension theorem (1911); CH, König (1905), Easton (1970). | digit interleaving; Hilbert's curve, orders 1–5 |
| 13 | `Choice` | Russell's shoes and socks; the well-ordering theorem (1904), Zorn, bases, Tychonoff; Vitali's set (1905); Banach–Tarski (1924) and the free group. | the Cayley graph of F₂ to length 3; F₂ = W(a) ∪ aW(a⁻¹) = W(b) ∪ bW(b⁻¹) on all 1,457 words of length ≤ 6 |
| 14 | `Debate` | the five letters (1905); Gödel (1938) and Cohen (1963): choice independent; countable and dependent choice; Feferman–Lévy; Solovay (1970); the verdict. | — |
| 15 | `CH` | Hilbert's first problem (1900); Gödel's L (1938); Cohen's forcing (1963): conditions, dense sets, a generic real; **the Wall's sixth brick**; Boolean-valued models. | a generic path that meets a dense set for each of six ground reals |
| 16 | `Large` | inaccessibles and Gödel's second theorem; the consistency-strength ladder; Scott (1961); Lévy–Solovay (1967); Zermelo's games (1913); Gale–Stewart (1953); projective determinacy and Martin–Steel (1989). | noughts and crosses solved: 5,478 positions, a draw |
| 17 | `Realism` | Gödel's realism (1947); Maddy's intrinsic and extrinsic justification (1988); **Price List**: the continuum; Woodin, Hamkins's multiverse (2012), Feferman. | the MUS {R, K, N} and its three corrections |
| 18 | `Foundations` | set theory as the foundation; junk theorems; ETCS (Lawvere 1964), type theory, univalence; proof assistants. | four "junk theorems" under von Neumann's and Zermelo's codings |
| 19 | `Outro` | recap; the Reasoner's set module; the Wall; problems; payoffs; references. | — |

## Sources

Books: Enderton, *Elements of Set Theory* (1977); Kunen, *Set Theory* (2011); Jech, *Set Theory* (3rd ed., 2003);
Kanamori, *The Higher Infinite* (2003); Potter, *Set Theory and Its Philosophy* (2004); van Heijenoort (ed.), *From
Frege to Gödel* (1967); Hallett, *Cantorian Set Theory and Limitation of Size* (1984); Moore, *Zermelo's Axiom of
Choice* (1982); Wagon, *The Banach–Tarski Paradox* (1985); Maddy, *Defending the Axioms* (2011).

Papers and texts: Galileo, *Two New Sciences* (1638); Bolzano, *Paradoxien des Unendlichen* (1851); Dedekind,
*Stetigkeit und irrationale Zahlen* (1872) and *Was sind und was sollen die Zahlen?* (1888); Cantor (1874, 1877
letter, 1878, 1883, 1891, 1899 letter); Frege, *Grundgesetze* I (1893) and II (1903); Burali-Forti (1897); Hilbert,
"Mathematical Problems" (1900) and "On the Infinite" (1926); Russell, letter to Frege (1902) and "Mathematical logic as
based on the theory of types" (1908); Zermelo (1904, 1908, 1913, 1930); König (1905); Vitali (1905); Hessenberg
(1906); Poincaré (1906); Brouwer (1911); Weyl, *Das Kontinuum* (1918); Kuratowski (1921); Fraenkel (1922); Skolem
(1922); von Neumann (1923, 1925); Banach and Tarski (1924); Sierpiński and Tarski (1930); Ulam (1930); Zorn (1935);
Ackermann (1937); Gödel (1938) and "What is Cantor's continuum problem?" (1947, 1964); Wittgenstein, *Lectures on the
Foundations of Mathematics* (1939, ed. 1976); Curry (1942); Bernays (1942); Goodstein (1944); Gale and Stewart (1953);
Scott (1961); Cohen (1963, 1964); Feferman and Lévy (1963); Lawvere (1964); Benacerraf, "What numbers could not be"
(1965); Lévy and Solovay (1967); Easton (1970); Solovay (1970); Boolos, "The iterative conception of set" (1971);
Martin-Löf (1972); Kirby and Paris, "Accessible independence results for Peano arithmetic" (1982); Maddy, "Believing
the axioms" (1988); Martin and Steel (1989); Calkin and Wilf, "Recounting the rationals" (2000); Woodin, "The continuum
hypothesis" (2001); Feferman, "Is the continuum hypothesis a definite mathematical problem?" (2011); Hamkins, "The
set-theoretic multiverse" (2012).

## Problems and solutions

1. **The finite subsets of ℕ are countable.** Send a finite set S to the number Σ_{n ∈ S} 2ⁿ. Every natural number
   has exactly one binary expansion, so this is a bijection between the finite subsets of ℕ and ℕ itself: S is read
   off from the 1-bits. (This is Ackermann's idea, applied once instead of hereditarily.) By contrast, *all* subsets
   of ℕ are uncountable (Chapter 3): the infinite ones are what the diagonal catches.
2. **The functions ℕ → ℕ cannot be listed.** Given any list f₀, f₁, f₂, …, define g(n) = fₙ(n) + 1. Then g differs
   from fₙ at the argument n, for every n, so g is not on the list. (In fact there are 2^ℵ₀ such functions: at
   least as many as the 0/1-valued ones, and at most as many as the subsets of ℕ × ℕ.)
3. **Ordinal arithmetic.** (ω + 1)·2 = (ω + 1) + (ω + 1) = ω + (1 + ω) + 1 = ω + ω + 1 = ω·2 + 1. 2·(ω + 1) =
   2·ω + 2·1 = ω + 2 (left distributivity holds; 2·ω = ω). ω·(ω + 1) = ω·ω + ω = ω² + ω. And ω + ω² = ω², since ω²
   absorbs the smaller ω placed before it, while ω² + ω > ω². The Reasoner's `Ord` gives the same four answers.
4. **Goodstein's sequence from 5.** Base 2: 5 = 2² + 1, ordinal ω^ω + 1. Base 3: 3³ + 1 − 1 = 27 = 3³, ordinal
   ω^ω. Base 4: 4⁴ − 1 = 255 = 3·4³ + 3·4² + 3·4 + 3, ordinal ω³·3 + ω²·3 + ω·3 + 3. Base 5: 3·5³ + 3·5² + 3·5 + 3 − 1
   = 467, ordinal ω³·3 + ω²·3 + ω·3 + 2. Base 6: 775, ordinal ω³·3 + ω²·3 + ω·3 + 1. Each ordinal is smaller than the
   last, as the proof requires.
5. **No set contains every set.** For any set A, separation gives R_A = {x ∈ A : x ∉ x}. If R_A were in A, it would
   belong to itself exactly when it does not; so R_A ∉ A, and A is not the set of all sets. On the iterative
   conception, every set is formed at a stage from sets formed earlier, and for any set A the set {A} is formed at a
   later stage; a set containing every set would have to contain sets formed after it, and itself, which no stage
   allows.
6. **(Essay) Is the continuum hypothesis true, false, or neither?** A strong answer uses Chapter 17's Price List and
   says which claim it gives up and at what cost. *New axioms* (Gödel, Woodin): the cost is to show that some
   candidate axiom is justified, intrinsically or by its consequences, and Lévy–Solovay rules out the large
   cardinals as such axioms. *No fact of the matter* (Hamkins, Feferman): the cost is explaining why the same doubt
   does not spread to arithmetic, where most of these philosophers are realists. *Unknowable truth*: the cost is a
   truth with no possible evidence, which many think makes "true" idle.

## 习题与解答

1. **ℕ的有限子集是可数的。** 把有限集S送到数Σ_{n ∈ S} 2ⁿ。每个自然数恰有一种二进制展开，所以这是ℕ的有限子集与ℕ本身之间的双射：
   S由各个为1的位读出。（这是阿克曼的想法，只用一次，而不是层层用。）相反，ℕ的*全部*子集是不可数的（第3章）：对角线抓住的正是那些无穷子集。
2. **ℕ → ℕ的函数无法列成表。** 给定任何列表f₀, f₁, f₂, …，定义g(n) = fₙ(n) + 1。那么对每个n，g在自变量n处与fₙ不同，所以g不在
   表上。（事实上这样的函数有2^ℵ₀个：至少和取值0/1的函数一样多，至多和ℕ × ℕ的子集一样多。）
3. **序数算术。** (ω + 1)·2 = (ω + 1) + (ω + 1) = ω + (1 + ω) + 1 = ω + ω + 1 = ω·2 + 1。2·(ω + 1) = 2·ω + 2·1 = ω + 2
   （左分配律成立；2·ω = ω）。ω·(ω + 1) = ω·ω + ω = ω² + ω。而ω + ω² = ω²，因为ω²吞没了放在它前面的较小的ω，而ω² + ω > ω²。
   推理机的`Ord`给出同样的四个答案。
4. **从5开始的古德斯坦序列。** 底2：5 = 2² + 1，序数ω^ω + 1。底3：3³ + 1 − 1 = 27 = 3³，序数ω^ω。底4：4⁴ − 1 = 255 =
   3·4³ + 3·4² + 3·4 + 3，序数ω³·3 + ω²·3 + ω·3 + 3。底5：3·5³ + 3·5² + 3·5 + 3 − 1 = 467，序数ω³·3 + ω²·3 + ω·3 + 2。底6：775，
   序数ω³·3 + ω²·3 + ω·3 + 1。每个序数都比前一个小，正如证明所要求的。
5. **没有集合包含每个集合。** 对任何集合A，分离公理给出R_A = {x ∈ A : x ∉ x}。如果R_A在A中，它就恰好在不属于自身时属于自身；所以
   R_A ∉ A，A不是所有集合的集合。按迭代观念，每个集合都在某个阶段由更早形成的集合构成，而对任何集合A，集合{A}在更晚的阶段形成；一个包含
   每个集合的集合，就必须包含在它之后形成的集合，以及它自己，这在任何阶段都不可能。
6. **（论述题）连续统假设是真的、假的，还是两者都不是？** 好的回答利用第17章的代价清单，说明它放弃哪一个断言，代价是什么。*新公理*
   （哥德尔、伍丁）：代价是要表明某个候选公理是有理由的，无论是内在的还是凭其后果的，而列维–索洛维排除了把大基数当作这样的公理。
   *没有事实可言*（汉金斯、费弗曼）：代价是要解释为什么同样的怀疑不会蔓延到算术，而这些哲学家大多在算术上是实在论者。*不可知的真理*：
   代价是一个不可能有任何证据的真理，许多人认为这使“真”变得空洞。
