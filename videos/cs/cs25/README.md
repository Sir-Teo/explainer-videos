# Computer Science, Built — Part 25: Undecidable

Part 25 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act V, *Limits and Secrets*. Part 1 proved that one problem, halting,
cannot be decided. This part finds the same impossibility everywhere: in every question about what programs do, in
dominoes, tilings and equations over the integers, in Gödel's theorems, and in the busy beaver, where proof itself runs
out.

The instrument is `explainer/cs/algo/computability.py`. It holds:
* a breadth-first PCP solver over the "overhang", and Sipser's Turing-machine-to-PCP construction;
* computation histories of small Turing machines;
* a Wang-tile backtracker, for rectangles and tori, and Jeandel and Rao's eleven tiles;
* a Python quine and a Pebble-language quine, generated from a template;
* FRACTRAN and Conway's PRIMEGAME; Collatz trajectories;
* compressed sizes (zlib, bz2, xz) as upper bounds on Kolmogorov complexity; π by Machin's formula; Thue–Morse;
* Pell's equation by continued fractions; the outline of the 2023 "hat" monotile.

It is tested in `tests/test_cs25_computability.py`: both quines reproduce their source byte for byte (the Pebble one on
the emulator), the PCP solver agrees with known instances, the TM reduction's match is the machine's accepting
history, and the tiles, primes and Pell solutions are checked.

* **Three questions, one answer.** Hook.
  - Eleven tiles: a 12 × 12 patch at once, but never a repeating pattern.
  - x² − 61y² = 1: 78 million values of y in 20 seconds find nothing; the answer has x = 1,766,319,049.
  - A program that prints itself, in Python and in Pebble.
* **1. Decidable and recognizable.**
  - Decidable, recognizable (r.e.) and co-recognizable; K, the machines that halt on themselves.
  - Decidable = recognizable ∩ co-recognizable (proved, by running two recognizers in turn). K's complement is not
    recognizable. TOT is on neither side.
* **2. Mapping reductions.**
  - A ≤ₘ B by a computable f; undecidability flows forward.
  - A catalogue: A_TM, E_TM, EQ_TM, TOT, each by a machine that ignores its input.
* **3. Rice's theorem** (proved).
  - Every non-trivial semantic property of programs is undecidable.
  - Consequences: virus detection (Cohen 1987), optimal compilation, sound-and-complete static analysis; the escape by
    approximation (Part 14's types, Part 54's verifiers).
* **4. Programs that know their own code.**
  - A Python quine. A Pebble-language quine of 759 lines (735 assignments store the rest of the program as character
    codes) that the emulator runs in 98,687 instructions, printing its source byte for byte.
  - Kleene's recursion theorem (1938), and halting's undecidability in three lines.
* **5. Post's correspondence problem.**
  - Sipser's four dominoes and the five-domino match.
  - The reduction: dominoes for a two-rule Turing machine; the 13-domino match spells its accepting history
    `#q10#1p0#10a#`.
  - 20,000 random three-domino sets (words of 1–3 bits): 4,679 solved, the longest shortest match 15 dominoes. The
    four-domino instance (1000/0, 01/0, 1/101, 00/001) whose shortest match is 206 dominoes, confirmed by our search
    (73,134 states).
  - Decidable for two dominoes (1982), undecidable for five (Neary 2015), open for three and four.
  - Ambiguity of context-free grammars is undecidable, paying off Part 12's promise.
* **6. Tiling the plane.**
  - Jeandel and Rao's eleven Wang tiles (2015): squares up to 20 × 20 found (3.98 million tiles tried), and all 62
    tori up to 8 × 8 that the search could finish refuted.
  - Why tiling is undecidable: a tile per tableau cell (Berger 1966, 20,426 tiles; Robinson; Penrose; Kari–Culik).
  - The hat (Smith, Myers, Kaplan and Goodman-Strauss, 2023): 13 vertices, area 8√3; the spectre.
* **7. Hilbert's tenth problem.**
  - Pell's equation: brute force finds D = 13 in 180 tries and D = 29 in 1,820, and nothing for D = 61 in 78 million;
    continued fractions find every one in microseconds (D = 991: 30 digits).
  - The DPRM theorem: recognizable = Diophantine (Davis, Putnam, Robinson 1961; Matiyasevich 1970).
  - Jones, Sato, Wada and Wiens's 26-variable polynomial whose positive values are the primes (1976).
* **8. Gödel, through halting.**
  - Gödel numbering: 0 = 0 is 2¹·3³·5¹ = 270; ∀x(x + 0 = x) has 47 digits, and factoring recovers it.
  - The first incompleteness theorem from the halting problem (proved). The Gödel sentence as a program, via the
    recursion theorem. The second theorem, and the end of Hilbert's program.
* **9. Oracles and the arithmetic hierarchy.**
  - Oracle machines and the jumps ∅ < K < K′ < ….
  - Σ₁ to Σ₃ with examples: Goldbach, the Riemann hypothesis and Con(ZFC) are Π₁; TOT, twin primes, Collatz and
    P ≠ NP are Π₂. Post's theorem (1948); FIN, TOT, COF complete at their levels.
  - Post's problem and the priority method (Friedberg 1957, Muchnik 1956); Sacks's density theorem.
* **10. Kolmogorov complexity.**
  - Six kinds of data, 100,000 bytes each, through three compressors: random bytes 100,041 (no gain); English
    31,759; π's digits 43,229; Thue–Morse 91; all zeros 47. A 19-line function prints all of π's digits.
  - The invariance theorem (proved); incompressible strings by counting (proved); K is uncomputable (Berry's
    paradox); Chaitin's incompleteness theorem.
* **11. Chaitin's Ω.**
  - The halting probability, approachable from below but never certified.
  - A computable cousin: 5,000 random three-state machines. The fraction halted reaches 0.4502 by 16 steps and never
    moves again in 2,000; the longest halting run is 11 steps. Exact, because S(3) = 21.
  - Ω's first n bits decide every n-bit program; Ω is random; the 64 bits computed by Calude, Dinneen and Shu (2002);
    Solovay's Ω of which ZFC can determine no bit.
* **12. Busy beavers, again.**
  - Three speeds of growth: primitive recursion, Ackermann (Part 11's promise), the busy beaver. A total language
    cannot interpret itself (Part 14's promise).
  - Proof that S eventually exceeds every computable function.
  - Famous questions as busy-beaver values: Erdős (15 states), Goldbach (27, unverified), Riemann (744), Con(ZFC)
    (432 to 7,910).
* **13. Where decidability ends.**
  - Presburger and Tarski (decidable), arithmetic and the rationals (undecidable).
  - The word problem for groups (Novikov, Boone); matrix mortality (Paterson 1970; open for 2 × 2).
  - Conway's PRIMEGAME: every prime up to 127 as a power of 2, in 2,835,628 steps.
  - Collatz: 837,799 takes 524 steps; 704,511 climbs to 56,991,483,520; Conway's undecidable generalization.
* **14. Undecidability in the wild.**
  - C++ templates, Java generics (Grigore 2017), TypeScript's types, Magic: the Gathering (2019), x86 `mov`, Conway's
    Life.
  - The spectral gap (Cubitt, Pérez-García and Wolf, 2015).
* **15. Frontier: Hilbert's tenth over other rings.**
  - Undecidable over every ring of integers of a number field: Koymans and Pagano (2024), and independently Alpöge,
    Bhargava, Ho and Shnidman (2025).
  - Over ℚ: open. Mazur's conjecture; Poonen (2009) and Koenigsmann (2016) define ℤ in ℚ with quantifiers.
  - How small an undecidable problem can be: 9 unknowns over ℕ, 11 over ℤ (Sun 2021), 5 dominoes, 3 × 3 matrices.
  - Open problems. Outro.

## Build

```bash
python -m videos.cs.cs25.compute           # every number in the part (about four minutes)
python tools/build.py cs25 -q l            # a 480p preview
python tools/build.py cs25                 # 1080p
```

## Problems, with solutions

1. **Equivalence.** Prove that EQ_TM is neither recognizable nor co-recognizable.

   *Solution.* Reduce A_TM to the complement of EQ_TM. Map ⟨M, w⟩ to ⟨M₁, M₂⟩, where M₁ rejects everything and M₂
   ignores its input and runs M on w, accepting if M does. If M accepts w, L(M₂) = Σ* ≠ ∅ = L(M₁); otherwise both
   are empty. So A_TM ≤ₘ co-EQ_TM, hence co-A_TM ≤ₘ EQ_TM. Since co-A_TM is not recognizable, neither is EQ_TM.
   Next, reduce A_TM to EQ_TM itself. Map ⟨M, w⟩ to ⟨M₁, M₂⟩ where M₁ accepts everything and M₂ is as before. Then M
   accepts w iff L(M₁) = L(M₂). So co-A_TM ≤ₘ co-EQ_TM, and co-EQ_TM is not recognizable either. That is, EQ_TM is
   not co-recognizable.

2. **Rice, and what it does not cover.** Show that "M accepts some palindrome" is undecidable, and explain why "M's
   description is a palindrome" is not.

   *Solution.* Whether L(M) contains a palindrome depends only on L(M), so the property is semantic. It is non-trivial:
   a machine accepting {a} has it, and a machine accepting nothing does not. By Rice's theorem it is undecidable. The
   second property is about the text ⟨M⟩, not about L(M). Two machines with the same language can differ on it, so it
   is not semantic, and a program decides it by reading the string from both ends.

3. **Enumerating in order.** Prove that a language is decidable if and only if some enumerator prints it in
   increasing (shortlex) order.

   *Solution.* (⇒) Given a decider D, run D on every string in shortlex order and print those it accepts. (⇐) If L is
   finite it is decidable, by a table. If L is infinite and E prints it in increasing order, decide w as follows. Run E
   until it prints w (accept) or prints a string that comes after w (reject). Since L is infinite, E prints strings
   beyond w eventually, so the procedure always halts, and since the order is increasing, w cannot appear later.

4. **Complexity bounds.** Show that K(x) ≤ |x| + c and K(xx) ≤ K(x) + c, and conclude that at most half of the
   strings of each length have K(x) < |x| − 1.

   *Solution.* The program "print the following literal: x" has length |x| plus the fixed length of the printing
   code. If p prints x, the program "run p, and print its output twice" has length |p| + c′. For the count: the
   programs of length less than n − 1 number 1 + 2 + … + 2ⁿ⁻² = 2ⁿ⁻¹ − 1. Each prints at most one string, so fewer than
   2ⁿ⁻¹, half of the 2ⁿ strings of length n, can have K(x) < n − 1.

5. **Build: a backwards quine.** Write a Pebble-language program that prints its own source backwards, and run it on
   the emulator.

   *Solution.* Keep the structure of chapter 4's quine: a head that declares an array `d`; a data section of
   assignments `d[k] = c;` holding the character codes of the head and the tail; and a tail. Instead of printing
   directly, the tail writes the whole source into a buffer in three passes. First it copies the head from `d`, then
   it writes the text of each assignment (the decimal digits of k and c with the fixed punctuation), and then it
   copies the tail from `d`. Finally it prints the buffer from its last byte to its first. Generate the program with a
   short Python script, as `computability.pebble_quine` does. Check it the same way: compile it, run it on the
   emulator, and compare the output with the source reversed. The recursion theorem guarantees such a program
   exists for any computable transformation of the text, reversal included.

6. ★ **Research: three dominoes.** Is Post's correspondence problem decidable for three dominoes? Start with words of
   length at most 3: find the longest shortest match, or prove the lengths are bounded.

   *Where to start.* The two-domino case was decided by Ehrenfeucht, Karhumäki and Rozenberg (1982) and simplified by
   Halava, Harju and Hirvensalo (2002). Their method, analysing how the overhang can evolve, is the natural thing to
   push to three. Neary (2015) gives undecidability for five, so the methods must break somewhere between three and
   five, and finding where is itself informative. Computationally, our solver handles 20,000 random instances in two
   minutes. Enumerate all three-domino instances over {0, 1} with words of length at most 3, removing symmetries
   (swapping 0 and 1, reversing every word, permuting the dominoes). Solve them by breadth-first search over the
   overhang. Then try to certify the unsolved ones as unsolvable with simple invariants: a length imbalance that can
   never be repaired, an overhang that can never be extended, or a finite-automaton certificate in the style of the
   busy-beaver deciders of Part 1. The instances that resist every certificate are where the question lives.

## 习题与解答

1. **等价性。** 证明 EQ_TM 既不可识别，也不是补可识别的。

   *解答。* 把 A_TM 归约到 EQ_TM 的补：把 ⟨M, w⟩ 映到 ⟨M₁, M₂⟩，其中 M₁ 拒绝一切，M₂ 忽略输入、在 w 上运行 M，M 接受则接受。若 M 接受 w，
   则 L(M₂) = Σ* ≠ ∅ = L(M₁)；否则两者都为空。所以 A_TM ≤ₘ co-EQ_TM，从而 co-A_TM ≤ₘ EQ_TM；co-A_TM 不可识别，所以 EQ_TM 也不可识别。
   再把 A_TM 归约到 EQ_TM 本身：映到 ⟨M₁, M₂⟩，M₁ 接受一切，M₂ 同上；M 接受 w 当且仅当 L(M₁) = L(M₂)。于是 co-A_TM ≤ₘ co-EQ_TM，co-EQ_TM
   也不可识别，即 EQ_TM 不是补可识别的。

2. **Rice 定理，以及它管不到的。** 证明“M 接受某个回文”不可判定，并解释为什么“M 的描述是回文”可判定。

   *解答。* L(M) 是否含有回文只取决于 L(M)，所以这是语义性质；它非平凡：接受 {a} 的机器有，什么都不接受的机器没有。由 Rice 定理，它不可判定。
   第二个性质关乎文本 ⟨M⟩ 而不是 L(M)：两台语言相同的机器可以在这一点上不同，所以它不是语义性质，程序从两端读这个字符串就能判定。

3. **按序枚举。** 证明一个语言可判定，当且仅当某个枚举器按递增（先短后字典）顺序打印它。

   *解答。* (⇒) 给定判定器 D，按先短后字典的顺序在每个字符串上运行 D，打印它接受的。(⇐) 若 L 有限，查表即可判定。若 L 无限且 E 按递增顺序
   打印它，判定 w 时就运行 E，直到它打印出 w（接受）或一个排在 w 之后的字符串（拒绝）。L 无限，所以 E 终究会打印出 w 之后的字符串，过程总会停机；
   而顺序递增，w 不可能再晚出现。

4. **复杂度的界。** 证明 K(x) ≤ |x| + c 且 K(xx) ≤ K(x) + c，并推出每种长度的字符串中至多一半满足 K(x) < |x| − 1。

   *解答。* 程序“打印下面这段字面量：x”的长度是 |x| 加上打印代码的固定长度。若 p 打印 x，则“运行 p，把输出打印两遍”的长度为 |p| + c′。计数：
   长度小于 n − 1 的程序共有 1 + 2 + … + 2ⁿ⁻² = 2ⁿ⁻¹ − 1 个，每个至多打印一个字符串，所以少于 2ⁿ⁻¹ 个，即长度为 n 的 2ⁿ 个字符串中不到一半，
   能有 K(x) < n − 1。

5. **动手：倒着打印自己的程序。** 用 Pebble 语言写一个把自己的源代码倒着打印出来的程序，并在模拟器上运行。

   *解答。* 沿用第 4 章自打印程序的结构：头部声明数组 `d`；数据段由赋值 `d[k] = c;` 组成，存放头部和尾部的字符编码；然后是尾部。尾部不直接打印，
   而是分三趟把整个源代码写进一个缓冲区：先从 `d` 复制头部，再写出每条赋值的文本（k 和 c 的十进制数字加上固定的标点），最后从 `d` 复制尾部。
   然后从最后一个字节到第一个字节打印缓冲区。像 `computability.pebble_quine` 那样用一小段 Python 脚本生成这个程序，再用同样方式检查：编译，
   在模拟器上运行，把输出与反转后的源代码比较。递归定理保证，对文本的任何可计算变换（包括反转），这样的程序都存在。

6. ★ **研究：三张多米诺。** 三张多米诺的 Post 对应问题可判定吗？从长度至多为 3 的词入手：找出最长的最短匹配，或者证明这些长度有界。

   *从哪里入手。* 两张多米诺的情形由 Ehrenfeucht、Karhumäki 与 Rozenberg（1982）解决，Halava、Harju 与 Hirvensalo（2002）作了简化；他们分析
   悬垂部分如何演变的方法，是推向三张时最自然的工具。Neary（2015）给出五张时的不可判定性，所以这些方法必然在三到五之间的某处失效，而找出在哪里
   失效本身就很有价值。计算上，我们的求解器两分钟能处理 20,000 个随机实例。枚举 {0, 1} 上词长至多为 3 的全部三张多米诺实例，去掉对称性（交换
   0 和 1、反转每个词、置换多米诺）；用悬垂部分上的广度优先搜索求解；再用简单的不变量证明未解出的实例无解：无法修复的长度失衡、无法延伸的悬垂，
   或者像第 1 部分忙碌海狸判定器那样的有限自动机证书。抵抗住所有证书的那些实例，就是问题真正所在。

## Glossary additions

可判定 decidable · 可识别（递归可枚举） recognizable (recursively enumerable) · 补可识别 co-recognizable · 映射归约 mapping
reduction · 语义性质 semantic property · Rice 定理 Rice's theorem · 自打印程序 quine · 递归定理 recursion theorem · Post 对应问题
Post's correspondence problem · 计算历史 computation history · 歧义文法 ambiguous grammar · Wang 砖 Wang tile · 非周期铺砌 aperiodic
tiling · 单瓦（帽子） monotile (the hat) · 丢番图集 Diophantine set · Pell 方程 Pell's equation · 连分数 continued fraction · Gödel
编码 Gödel numbering · 不完备性 incompleteness · 一致性 consistency · 可靠 sound · 谕示机 oracle machine · 图灵跳跃 Turing jump ·
算术层级 arithmetic hierarchy · 优先方法 priority method · Kolmogorov 复杂度 Kolmogorov complexity · 不变性定理 invariance theorem ·
不可压缩 incompressible · Berry 悖论 Berry's paradox · 停机概率 halting probability · Chaitin 常数 Chaitin's constant · 原始递归
primitive recursion · Ackermann 函数 Ackermann function · 忙碌的海狸 busy beaver · Presburger 算术 Presburger arithmetic · 字问题
word problem · 矩阵致死性 matrix mortality · FRACTRAN · Collatz 猜想 Collatz conjecture · 谱隙 spectral gap · 整数环 ring of
integers · 数域 number field

## Sources

*Canon.* Books:
- Sipser, *Introduction to the Theory of Computation* (3rd ed., 2012), ch. 4–6;
- Rogers, *Theory of Recursive Functions and Effective Computability* (1967);
- Soare, *Turing Computability* (2016);
- Boolos, Burgess & Jeffrey, *Computability and Logic* (5th ed., 2007);
- Li & Vitányi, *An Introduction to Kolmogorov Complexity and Its Applications* (4th ed., 2019);
- Matiyasevich, *Hilbert's Tenth Problem* (1993);
- Grünbaum & Shephard, *Tilings and Patterns* (1987).

Papers:
- Foundations: Turing (1936, 1939); Kleene (1938); Post (1944, 1946, 1948); Rice (1953); Friedberg (1957); Muchnik
  (1956); Sacks (1964); Cohen, "Computer viruses" (1987).
- PCP and grammars: Ehrenfeucht, Karhumäki & Rozenberg (1982); Halava, Harju & Hirvensalo (2002); Neary,
  "Undecidability in binary tag systems and the Post correspondence problem for five pairs of words" (2015);
  Cantor (1962); Floyd (1962); Chomsky & Schützenberger (1963).
- Tiles: Wang (1961); Berger (1966); Robinson (1971); Kari (1996); Culik (1996); Jeandel & Rao, "An aperiodic set of
  11 Wang tiles" (2015, published 2021); Smith, Myers, Kaplan & Goodman-Strauss, "An aperiodic monotile" (2023) and
  "A chiral aperiodic monotile" (2023).
- Hilbert's tenth: Davis, Putnam & Robinson (1961); Matiyasevich (1970); Davis, "Hilbert's tenth problem is
  unsolvable" (1973); Jones, Sato, Wada & Wiens, "Diophantine representation of the set of prime numbers" (1976);
  Jones (1982); Sun (2021).
- Logic: Gödel (1931); Rosser (1936); Presburger (1929); Fischer & Rabin (1974); Tarski (1948); Robinson (1949);
  Novikov (1955); Boone (1958); Paterson (1970).
- Information: Kolmogorov (1965); Chaitin (1966, 1974, 1975); Solomonoff (1964); Calude, Dinneen & Shu, "Computing a
  glimpse of randomness" (2002); Solovay, "A version of Ω for which ZFC can not predict a single bit" (2000).
- Busy beavers and iterations: Radó (1962); Conway, "Unpredictable iterations" (1972) and "FRACTRAN" (1987);
  Yedidia & Aaronson (2016); Aaronson, "The busy beaver frontier" (2020); Stérin & Woods (2021); the bbchallenge
  collaboration (2024); Barina (2020).
- In the wild: Veldhuizen, "C++ templates are Turing complete" (2003); Grigore, "Java generics are Turing complete"
  (2017); Churchill, Biderman & Herrick, "Magic: the Gathering is Turing complete" (2019); Dolan, "mov is
  Turing-complete" (2013); Cubitt, Pérez-García & Wolf, "Undecidability of the spectral gap" (2015).
- Frontier: Denef & Lipshitz (1978); Mazur (1992); Poonen (2009); Mazur & Rubin (2010); Koenigsmann, "Defining ℤ in
  ℚ" (2016); Koymans & Pagano, "Hilbert's tenth problem via additive combinatorics" (2024); Alpöge, Bhargava, Ho &
  Shnidman (2025).
