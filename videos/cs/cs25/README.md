# Computer Science, Built — Part 25: Undecidable

Part 25 of the [61-part series](../README.md), opening Act V, *Limits and Secrets*.
The episode connects recognition, reductions, self-reference, arithmetic and
information. Every impossibility result has an explicit model and hypotheses;
finite unsuccessful searches retain their cutoff status.

The instrument is `explainer/cs/algo/computability.py`; numerical producers are
`compute.py`, with separate certificate checkers and native references in
`computational_references.py`. Tests exercise domains, budgets, full witnesses,
independent short PCP enumeration, tape boundaries and both executed quines.

The bilingual source registry contains 68 exact narration pairs. Plain complexity
is written **C**; optimal prefix-free complexity is written **K**. Chinese source
and cue agreement is distinct from synthesized speech and listening approval.

- **Hook:** finite Wang patches, positive Pell solutions, and constructive quines
  illustrate three connections. Quine existence itself has a constructive answer.
- **Classes and reductions:** a recognizer never falsely accepts; dovetailing waits
  for acceptance. Reducing self-halting to acceptance uses a halt-then-accept
  wrapper, including simulated rejection. Emptiness reverses the acceptance answer;
  exercise 1 supplies both equivalence reductions.
- **Rice:** nontrivial extensional properties of partial computable functions in
  an effective universal system. Under the stated observations, faults and
  divergence are both undefined; “never divides by zero” is not an extensional
  example. Analyzer, malware and optimization consequences need a specified
  property, objective and unbounded model. Totality alone does not decide every
  semantic question.
- **Self-reference:** Kleene's theorem assumes an acceptable effective numbering
  and a total computable index transformer. It constructs embedded descriptions;
  it is not an introspection facility for arbitrary existing source files.
  The forward Pebble quine prints 13,380 bytes in 98,687 instructions; the executed
  reverse-printing exercise prints 15,705 bytes in reverse in 472,027 instructions.
- **PCP:** matches are nonempty. The displayed TM construction is forced-first
  **MPCP**, under disjoint one-character alphabets, a reserved separator, nonempty
  input and rejection of a left move off cell zero. A separate standard reduction
  yields ordinary PCP. Full concatenated rows, not only history prefixes, are
  checked. The four-domino example's shortest length **206** is actually searched:
  73,135 dequeued states including the root (73,134 with the legacy root-excluding
  convention). A retained independent residual-distance closure certificate and
  full string witness exclude shorter matches. Five-pair undecidability follows
  Neary's **published 2015** theorem; the conflicting four-pair 2013 preprint is
  superseded. CFG intersection/ambiguity follow the marker construction; CFG
  universality needs another reduction.
- **Tiles:** every 4, 8, 12, 16 and 20 square grid is retained and independently
  edge-checked. The bounded torus search finishes 62 refutations and leaves two
  cutoffs among the 64 sizes up to 8 by 8. A separate complete closed-row graph
  and topological certificate for **each width 1–8 excludes every positive
  height** at those widths. This finite-width result does not prove full-plane
  aperiodicity. Jeandel–Rao Figure 3's five-color set T is covered by their
  Theorem 3; their four-color variant is a different set. The eleven-tile minimum
  concerns oriented Wang squares. The plane reduction also needs hierarchical
  forcing of initialized computations at arbitrary scales. The hat needs reflected
  copies; the spectre does not. Integer lattice cross products certify hat area
  exactly as **8√3** and verify every displayed vertex.
- **Hilbert:** Pell assumes positive nonsquare D and y>0. A deterministic
  million-attempt brute cap finds D=13 in 180 attempts and D=29 in 1,820; D=61
  remains unresolved by that brute prefix. Continued fractions give its least
  positive solution (1,766,319,049, 226,153,980). All ten convergent certificates
  and nine monotonic timing repetitions per D are retained. Leastness uses the
  standard Pell-convergent theorem. DPRM uses natural-number parameters and
  auxiliaries; standard encodings transfer to integer-variable solvability.
  The prime polynomial asserts existence of auxiliary tuples, not that arbitrary
  tuples work at a prime k+2.
- **Gödel:** effective axiomatization, arithmetic strength and soundness scope
  the nonhalting proof. Rosser's consistency-only refinement is distinct from
  Gödel's original omega-consistency hypothesis for the opposite direction.
  The second theorem uses the standard provability predicate and derivability
  conditions; it does not follow merely from the informal soundness argument.
  Hilbert's objective is obstructed when its proposed finitistic reasoning is
  formalizable inside the theory, not by banning all external consistency proofs.
- **Degrees:** decidable sets are Δ1, distinct from bounded-formula Δ0. Quantifier
  blocks have computable matrices. Σ(n+1) is recognizable relative to the nth
  jump; Π(n+1) is co-recognizable. One oracle query follows a computable reduction.
  Sacks density requires distinct comparable c.e. degrees, not the incomparable
  displayed A and B. “Natural intermediate” is an informal research theme.
- **Complexity:** compression container bytes times eight plus fixed decoding,
  interpreter and framing costs bound plain C. The finite pi printer also needs
  its length argument, caller and dependencies. Every full compressed output
  round-trips; the independent interval-certified Chudnovsky computation agrees
  with all 100,000 digits, **including the leading 3**, from integer Machin.
  Invariance requires optimal description machines with additive simulation cost.
  Fewer than 2^-c of n-bit strings have C<n-c; the exact C≥n threshold guarantees
  some strings, not an overwhelming fraction. Chaitin's theorem requires an
  effectively axiomatized sound theory.
- **Omega:** an optimal prefix-free halting domain defines the measure of infinite
  coin streams having a halting program prefix. No uniform computable convergence
  modulus supplies arbitrary precision; special finite prefixes may be certified.
  Given dyadic truncation a, stop enumeration when q≥a: equality is sufficient if
  attained, while waiting only for equality can miss an overshoot. Prefix randomness
  uses prefix-free K, distinct from plain C. Effective sound-theory hypotheses
  apply, including Solovay's special-machine ZFC claim.
  The separate finite sample has **2,251/5,000 = 0.4502** halting machines, with an
  iid Wilson 95% interval approximately **[0.4365, 0.4640]**. All machine strings
  and halt times are retained. Independent native replay through **S(3)=21**
  matches every 2,000-step result. This exactly classifies the sample, not the
  16^6-machine population probability; observed empirical fractions are not
  deterministic lower bounds on that population measure.
- **Busy beavers:** S counts steps; Σ counts ones. The dominance sketch covers
  both parities and nonmonotone total computable f by computing
  max(f(2n), f(2n+1)). Total-language diagonalization states its effective syntax,
  Nat-to-Nat and closure assumptions. Exact-value unprovability requires an
  effective sound sufficiently strong arithmetic theory. Goldbach's reported
  27-state encoding is unverified, so no unconditional S(27) consequence follows.
  The checked published 7,910-state ZFC construction is distinguished from the
  432-state 2025 claim conditional on verification.
- **Boundary and applications:** Presburger's lower bound is worst case as formula
  length grows; real-closed-field decision concerns first-order polynomial
  formulas. Matrix mortality's 2×2 status is explicitly the cited 2015 literature
  status, not a new current survey. PRIMEGAME outputs are powers of two reached
  **after positive steps**, excluding initial 2^1. The actual three-million-step
  instruction trace is independently replayed using prime-exponent registers;
  every first-applicable instruction and all prime outputs through 127 agree.
  Full stopping lengths and tail-aware trajectory peaks for every positive
  Collatz start below a million agree with a guarded independent native replay.
  Ordinary Collatz may be false or true; no independence theorem is established.
  Universality examples assume ideal unbounded resources. Move-only computation
  needs repeating control flow. The spectral-gap theorem concerns promised
  robust thermodynamic families of 2D translation-invariant nearest-neighbor
  Hamiltonians with fixed local dimension. Finite exhaustive testing can establish
  absence of bugs within a completely specified finite model.
- **Frontier:** Koymans–Pagano and independent Alpöge–Bhargava–Ho–Shnidman results
  give H10 undecidability over all number-field integer rings; distinguish elliptic
  rank stability/additive combinatorics from the abelian-variety route. The broader
  ring statement concerns effectively presented infinite commutative unital
  finitely generated Z-algebras. Koenigsmann's universal definition and his
  different ∀∃ definition with one universal variable are separate results.
  Smith's 2007 two-state three-symbol claim uses a nonstandard infinite background.

## Build and verification

```bash
python -m unittest tests.test_cs25_computability
python -m videos.cs.cs25.compute --force
python tools/build.py cs25 -q l
python tools/build.py cs25
```

Schema-2 caches validate source signatures and their retained artifacts. Complete
native sources, compiler flags/version, images, inputs, outputs and sanitizer
receipts are retained. Durations describe this workload on the shared host;
deterministic budgets and verified witnesses are the central results.

The episode checkpoint evidence is documented in
[the QA packet](../../../docs/qa/evidence/cs25-polish-20261111/README.md).
Continuous narrated playback/listening, Chinese speech/listening, whole-video
native production and runtime at the selected narration pace remain separate
production gates.

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

4. **Plain complexity bounds.** Fix an optimal plain description machine; sizes are bits. Show that C(x) ≤ |x| + c and C(xx) ≤ C(x) + c, and conclude that at most half of the
   strings of each length have C(x) < |x| − 1.

   *Solution.* The program "print the following literal: x" has length |x| plus the fixed length of the printing
   code. If p prints x, the program "run p, and print its output twice" has length |p| + c′. For the count: the
   programs of length less than n − 1 number 1 + 2 + … + 2ⁿ⁻² = 2ⁿ⁻¹ − 1. Each prints at most one string, so fewer than
   2ⁿ⁻¹, half of the 2ⁿ strings of length n, can have C(x) < n − 1.

5. **Build: a backwards quine.** Write a Pebble-language program that prints its own source backwards, and run it on
   the emulator.

   *Executed solution.* `computability.pebble_backward_quine()` constructs the program below. The retained O2 compiler image runs for 472,027 emulator instructions and outputs exactly the 15,705 source bytes in reverse order. The source fits the explicitly checked 32,768-entry output buffer.

   Keep the structure of chapter 4's quine: a head that declares an array `d`; a data section of
   assignments `d[k] = c;` holding the character codes of the head and the tail; and a tail. Instead of printing
   directly, the tail writes the whole source into a buffer in three passes. First it copies the head from `d`, then
   it writes the text of each assignment (the decimal digits of k and c with the fixed punctuation), and then it
   copies the tail from `d`. Finally it prints the buffer from its last byte to its first. Generate the program with a
   short Python script, as `computability.pebble_quine` does. Check it the same way: compile it, run it on the
   emulator, and compare the output with the source reversed. The recursion theorem guarantees such a program
   exists for any computable transformation of the text, reversal included.

6. ★ **Research: three dominoes.** Is Post's correspondence problem decidable for three dominoes? Start with words of length at most 3: retain match certificates, finite-graph refutations and unresolved cutoffs. A fixed finite family automatically has some finite maximum among its shortest matches; seek explicit values/certificates, then a computable bound as a function of general input size.

   *Where to start.* The two-domino case was decided by Ehrenfeucht, Karhumäki and Rozenberg (1982) and simplified by
   Halava, Harju and Hirvensalo (2002). Their method, analysing how the overhang can evolve, is the natural thing to
   push to three. Neary (2015) gives undecidability for five, so the methods must break somewhere between three and
   five, and finding where is itself informative. Our retained fixed-budget run covers 20,000 random instances: 4,679 matches, 11,819 finite-graph exhaustions, 2,217 depth cutoffs and 1,285 node cutoffs. All inputs, statuses and matches are saved. Cutoffs are unresolved. The finite word-length-three experiment does not resolve unrestricted three-domino PCP. Enumerate all three-domino instances over {0, 1} with words of length at most 3, removing symmetries
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

4. **普通复杂度的界。** 固定最优普通描述机，长度单位为比特。 证明 C(x) ≤ |x| + c 且 C(xx) ≤ C(x) + c，并推出每种长度的字符串中至多一半满足 C(x) < |x| − 1。

   *解答。* 程序“打印下面这段字面量：x”的长度是 |x| 加上打印代码的固定长度。若 p 打印 x，则“运行 p，把输出打印两遍”的长度为 |p| + c′。计数：
   长度小于 n − 1 的程序共有 1 + 2 + … + 2ⁿ⁻² = 2ⁿ⁻¹ − 1 个，每个至多打印一个字符串，所以少于 2ⁿ⁻¹ 个，即长度为 n 的 2ⁿ 个字符串中不到一半，
   能有 C(x) < n − 1。

5. **动手：倒着打印自己的程序。** 用 Pebble 语言写一个把自己的源代码倒着打印出来的程序，并在模拟器上运行。

   *已执行的解答。* `computability.pebble_backward_quine()` 构造该程序。保留的 O2 编译镜像运行 472,027 条模拟器指令，把 15,705 个源码字节精确反向输出；构造时检查源码能装入 32,768 个条目的输出缓冲区。

   沿用第 4 章自打印程序的结构：头部声明数组 `d`；数据段由赋值 `d[k] = c;` 组成，存放头部和尾部的字符编码；然后是尾部。尾部不直接打印，
   而是分三趟把整个源代码写进一个缓冲区：先从 `d` 复制头部，再写出每条赋值的文本（k 和 c 的十进制数字加上固定的标点），最后从 `d` 复制尾部。
   然后从最后一个字节到第一个字节打印缓冲区。像 `computability.pebble_quine` 那样用一小段 Python 脚本生成这个程序，再用同样方式检查：编译，
   在模拟器上运行，把输出与反转后的源代码比较。递归定理保证，对文本的任何可计算变换（包括反转），这样的程序都存在。

6. ★ **研究：三张多米诺。** 三张多米诺的 Post 对应问题可判定吗？从长度至多为 3 的词入手：保留匹配证书、有限图排除证明，以及尚未解决的截断。固定有限集合的最短匹配长度必有某个有限最大值；任务是找出显式数值与证书，再探索依赖一般输入规模的可计算界。

   *从哪里入手。* 两张多米诺的情形由 Ehrenfeucht、Karhumäki 与 Rozenberg（1982）解决，Halava、Harju 与 Hirvensalo（2002）作了简化；他们分析
   悬垂部分如何演变的方法，是推向三张时最自然的工具。Neary（2015）给出五张时的不可判定性，所以这些方法必然在三到五之间的某处失效，而找出在哪里
   失效本身就很有价值。保留的固定预算运行覆盖 20,000 个随机实例：4,679 个匹配、11,819 个有限图穷尽、2,217 个深度截断、1,285 个节点截断。全部输入、状态与匹配均已保存；截断仍未解决。词长至多三的有限实验并未解决一般三张 PCP。枚举 {0, 1} 上词长至多为 3 的全部三张多米诺实例，去掉对称性（交换
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


Primary version reconciliation:

- [Neary, STACS 2015](https://doi.org/10.4230/LIPIcs.STACS.2015.649), Section 4,
  Theorem 11: **five** nonempty binary pairs; use this published version.
- [Jeandel–Rao](https://arxiv.org/abs/1506.06492), Figure 3 and Theorem 3:
  five-color T and its separately colored variants.
- [Koymans–Pagano](https://arxiv.org/abs/2412.01768), Theorems 1.1–1.2;
  [Alpöge et al.](https://arxiv.org/abs/2501.18774),
  [published DOI](https://doi.org/10.1007/s00222-025-01392-3).
- [Koenigsmann](https://arxiv.org/abs/1011.3424): distinguish universal from
  the alternative one-universal-variable ∀∃ definition.
- [Cubitt–Pérez-García–Wolf](https://arxiv.org/abs/1502.04573): exact
  thermodynamic promise and locality assumptions.
