# Computer Science, Built — Part 1: What Is a Computation?

Part 1 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). Hilbert asked for a machine that settles every mathematical question; Turing defined
the machine, showed that one machine can imitate all others, and proved that no machine can do what Hilbert asked.
Every machine in this part runs on the computer that renders the video (`compute.py`); dates, quotations and the
proofs about busy beavers are the published ones, cited on screen.

* **Pebbles.** Euclid's algorithm played with two piles of pebbles by someone who knows nothing about numbers;
  *calculus* (Latin, a pebble) and the Roman counting board; Hilbert and Ackermann's *Entscheidungsproblem* (1928);
  Turing's answer (1936); objectives.
* **1. Algorithms before machines.** Euclid with division, as squares cut from a 1071 × 462 rectangle (gcd 21);
  correctness by an invariant (the common divisors of (a, b) and (b, r) coincide), termination by a decreasing
  sequence of natural numbers; the steps for every pair up to 233, computed, with the worst cases at consecutive
  Fibonacci numbers and Lamé's bound (1844) checked on the whole grid; al-Khwārizmī and the informal definition of an
  algorithm.
* **2. The engines.** Hand-computed tables and their errors (Babbage and Herschel, 1821); the method of finite
  differences on x² + x + 41, by additions only, primes up to x = 39 and 41² at x = 40; the Analytical Engine's store,
  mill and Jacquard cards, with branches and loops; Lovelace's Note G (1843) and the Bernoulli numbers, computed
  exactly (her B₇ is today's B₈ = −1/30); her notes on symbols, music, and the machine that originates nothing.
* **3. Hilbert's question.** Leibniz's *calculemus*; Frege's *Begriffsschrift* (1879) and mechanically checkable
  proofs; Hilbert's three wishes (complete, consistent, decidable) and the 1928 decision problem; Gödel in Königsberg
  (7 September 1930) and Hilbert's radio address the next day; why "no procedure exists" needs a definition of
  procedure; Church and Turing (1936).
* **4. Turing's machine.** Turing's analysis of a person computing (§9 of the 1936 paper) and the squared page that
  collapses to a tape; the formal definition and configurations; a unary adder (3 + 2) run rule by rule; the
  space–time diagram; a machine that never halts.
* **5. Programming with a table.** Palindromes on one tape: the program as a state diagram whose states carry the
  erased symbol; a run on 0110 (15 steps); the zig-zag of a 24-symbol input; steps measured for every length up to
  60 (≈ 0.50 n²); Hennie's Ω(n²) lower bound (1965) and the crossing-sequence idea.
* **6. More tapes, same power.** Palindromes on two tapes in exactly 3n + 3 steps; one tape simulating k tapes
  (tracks and dots, two sweeps per step), with the simulation's head moves counted on the real palindrome machine;
  every other variant at polynomial cost; nondeterminism as a computation tree, and the exponential simulation that P
  versus NP asks about (Part 26).
* **7. The universal machine.** A table written as a string ⟨M⟩; the universal machine U; ours (14 states,
  29 rules, three tapes) running the 2-state busy beaver live, 374 of U's steps for M's 6; U's cost on the 2-, 3- and
  4-state champions (62×, 107×, 130×); programs as data, and software.
* **8. Other machines, same power.** The λ-calculus: syntax, β-reduction, Church numerals, PLUS 2 3 reduced in 6
  normal-order steps; Minsky's counter machines as bowls of pebbles (3 + 4 in 24 steps), compiled to two counters
  (42 instructions, 578,473 steps, the Gödel number swelling to 5⁷); Rule 110 from one cell (Cook 2004); Gosper's
  glider gun in Conway's Life; the web of mutual simulations.
* **9. The Church–Turing thesis.** The informal and the formal, and why the thesis cannot be proved; its evidence;
  what it does not say; three theses (Church–Turing, physical, extended) and the quantum challenge to the last.
* **10. More problems than programs.** Pairing off infinite sets; Cantor's zig-zag through the pairs; programs as a
  countable list ((4n + 4)²ⁿ machines with n states, computed); Cantor's diagonal (1891); problems as infinite 0–1
  sequences: uncountably many, so most have no program.
* **11. The halting problem.** The decider H; a real halting table (two-state machines on inputs 1ʲ, run for 10,000
  steps) and why "still running" is ambiguous; the program D and D(⟨D⟩); the diagonal argument; Turing's formulas for
  machines and the negative answer to Hilbert.
* **12. Reductions.** Borrowing an impossibility; the blank-tape halting problem by the machine M_w; a gallery of
  undecidable questions; Rice's theorem (1953): behaviour against text; virus scanners (Cohen 1987), static
  analyzers, compilers, testing.
* **13. Busy beavers.** Radó's S(n) (1962); all 20,736 two-state machines run (9,784 halt, the longest in 6 steps);
  the 3- and 4-state champions (Lin & Radó 1965, Brady 1983); the 5-state champion (Marxen & Buntrock 1990) run for
  all 47,176,870 steps, with 4,098 ones, in one picture and its first 1,200 steps in full; S(5) proved by the
  bbchallenge collaboration (2024, checked in Coq); S is uncomputable, by reduction from Chapter 12.
* **14. Frontier: the edge of the knowable.** How BB(5) was proved: non-halting certificates (a set of
  configurations containing the start, closed under a step, with no halting configuration), the deciders (cyclers,
  translated cyclers, n-gram and repeated-word methods, finite-automata reduction) and the 13 sporadic machines.
  Knuth's arrows and the BB(6) record (Kropitz 2022, beyond 10↑↑15; mxdys 2025, beyond 10↑↑10↑↑10↑↑8). Antihydra
  (mxdys, 2024), run here for 100,000,000 steps without halting, and its Collatz-like rule (Racheline) run for a
  million rounds (c = 498,503); the gambler's-ruin heuristic, q = 1/φ, P(halt) ≈ 10^−104,181; why the parities resist
  proof (Collatz, Mahler's 3/2 problem). The smallest machines whose halting ZFC cannot settle: 7,910 states (2016),
  745 (2023), 636 (2024), 432 (2025, not yet formally verified).
* **15. What we will build.** The tower of abstractions and the eleven acts; Pebble-32, the computer of Part 6, running
  Euclid on this series' emulator (21, as the rectangle said); the Job and its ledger; in practice.
* **Recap, problems, and where this comes back.**

The 2025 and later claims about BB(6) are kept deliberately qualitative on screen ("the record has grown since"); the
2022 lower bound (more than 10↑↑15 steps) is the one stated.

## Build

```bash
python -m videos.cs.cs1.compute            # every number in the part (about two minutes)
python tools/build.py cs1 -q l             # a 480p preview
python tools/build.py cs1                  # 1080p
python tools/make.py cs1                   # compute, then English and Chinese
```

The machines are in `machines.py` (the hand-written Turing machines, the single-tape simulation, the universal machine,
the counter-machine compiler, the cellular automata) and in the series toolkit (`explainer/cs/turing.py`,
`explainer/cs/lam.py`, `explainer/cs/pebble/`); `tests/test_cs1_machines.py` checks them.

## Problems, with solutions

1. **A binary incrementer.** Design a Turing machine that adds one to a number written in binary, the head starting on
   the leftmost digit. How many steps does it take on 1ⁿ?

   *Solution.* State A walks right over the digits (0 → 0, R and 1 → 1, R) and, on the blank after the number, steps
   left into state C. State C propagates the carry: on 1 write 0 and move left (staying in C); on 0 write 1 and halt;
   on the blank (the number was all ones) write 1 and halt. On 1ⁿ: n steps right, one step back, n carries, one final
   write: **2n + 2 steps**, leaving 10ⁿ. (Checked with our simulator for n = 1, 3, 5: 4, 8 and 12 steps.)

2. **Countable and uncountable.** Show that the set of finite binary strings is countable, and the set of all subsets
   of ℕ is not.

   *Solution.* List the strings by length, and those of equal length in dictionary order: ε, 0, 1, 00, 01, …. There
   are 2ᴸ − 1 strings shorter than L, so a string of length L appears at a position below 2ᴸ⁺¹: every string gets a
   finite position. For the subsets, suppose A₁, A₂, … listed them all, and let D = {k : k ∉ Aₖ}. For every k, D and
   Aₖ disagree about k, so D is not Aₖ: D is missing from the list, a contradiction.

3. **Writing a 1.** Prove that "does M ever write a 1, started on a blank tape?" is undecidable.

   *Solution.* Reduce the blank-tape halting problem (Chapter 12) to it. Given M, build M′: it behaves like M but uses
   a fresh symbol 1′ wherever M uses 1 (so M′ never writes a real 1 while simulating), and wherever M would enter a
   halting state, M′ instead writes 1 and halts. M′ writes a 1 if and only if M halts on the blank tape, and M′ is
   built from M by a simple program. A decider for "ever writes a 1" would therefore decide blank-tape halting, which
   is impossible.

4. **S increases.** Prove S(n + 1) > S(n) for every n ≥ 1.

   *Solution.* Take an n-state machine M that halts after S(n) steps. Its last step is a transition into the halting
   state. Add a new state Q, redirect that transition to Q, and give Q, on either symbol, the action "write the same
   symbol, move right, halt". The new machine has n + 1 states and takes exactly one more step: S(n + 1) ≥ S(n) + 1.

5. **TIMES 2 2.** Reduce (λm n f. m (n f)) 2 2 to normal form.

   *Solution.* Normal order takes **7 β-steps**: substitute m, then n; then the outer 2 applied to (2 f) gives
   λx. (2 f) ((2 f) x); unfolding the two copies of 2 f gives λf x. f (f (f (f x))), the numeral 4. (Our reducer,
   `explainer/cs/lam.py`, prints every line.)

6. **Build: the universal machine's cost.** Run U on the 4-state champion and measure its steps per simulated step;
   reorder the rules so the most used come first.

   *Solution.* U takes 13,938 steps for M's 107: **about 130 per simulated step**, almost all spent scanning ⟨M⟩ for
   the matching rule and rewinding. Counting how often each rule fires and putting the busiest first inside each
   state's group (our encoding lists rules state by state) gives **13,308 steps, about 124 per step**: a 4.5% saving,
   because most of the scan is spent crossing the rules of *other* states. Numbering the busiest states first helps
   more; a real interpreter replaces the scan by a jump to the right rule, the idea behind Part 15's dispatch tables.

7. **★ Research: Antihydra.** Antihydra's rule is h ← 8, c ← 0; each round c ← c + 2 if h is even and c − 1 if h is
   odd, then h ← h + ⌊h/2⌋; it halts when c = −1. (a) Show that, for steps of +2 and −1 with equal probability, the
   probability of ever falling one below the start is 1/φ. (b) Show that Antihydra never halts if and only if, for
   every N, at least a third of h₀, …, h_{N−1} are even. (c) Open: prove it.

   *What is known, and where to start.* (a) Either the first step falls (probability ½) or it rises by two and must
   fall three times: q = ½ + ½q³, so (q − 1)(q² + q − 1) = 0 and the root below 1 is q = (√5 − 1)/2 = 1/φ. (b) After
   N rounds with E even values, c = 2E − (N − E) = 3E − N. The counter moves by +2 or −1, so it first goes negative
   exactly at −1, and c ≥ 0 for all N is the same as E ≥ N/3 for all N. (c) Nobody knows how. The parities of
   ⌊3h/2⌋-iterates are a deterministic sequence of the kind that defeats every known method: the same family as the
   Collatz conjecture and Mahler's 3/2 problem (does any α make the fractional parts of α(3/2)ⁿ stay below ½?). The
   bbchallenge wiki (Antihydra, Cryptids) collects what has been tried. Start from `compute_frontier` in
   `videos/cs/cs1/compute.py`: it runs a million rounds in half a minute with Python integers, and 3E − N is never
   negative in the first million rounds. A cheaper way to get the parities than carrying all of h (it has
   0.585 N bits after N rounds) would be news in its own right.

## 习题与解答

1. **二进制加一。** 设计一台图灵机，把纸带上写成二进制的数加一，读写头从最左边的数字开始。输入 1ⁿ 时要走多少步？

   *解答。* 状态 A 向右走过所有数字（0→0,R；1→1,R），读到数字后面的空白时左移一格，进入状态 C。状态 C 负责进位：读到 1，写 0
   并左移（仍在 C）；读到 0，写 1 并停机；读到空白（原数全是 1），写 1 并停机。输入 1ⁿ：向右 n 步，回退 1 步，进位 n 步，最后写
   1 共 1 步，合计 **2n + 2 步**，结果是 10ⁿ。（用本系列的模拟器验证：n = 1、3、5 时分别是 4、8、12 步。）

2. **可数与不可数。** 证明有限二进制串的集合是可数的，而 ℕ 的全部子集组成的集合不是。

   *解答。* 先按长度、再按字典序列出所有串：ε, 0, 1, 00, 01, …。长度小于 L 的串共有 2ᴸ − 1 个，所以每个串都在有限的位置上出现。
   对子集：假设 A₁, A₂, … 列出了全部子集，令 D = {k : k ∉ Aₖ}。对每个 k，D 与 Aₖ 在“k 是否属于它”上意见相反，所以 D 不等于任何
   Aₖ，不在这个列表里，矛盾。

3. **写出一个 1。** 证明“从空白纸带出发，M 是否会写出 1？”不可判定。

   *解答。* 把空白纸带停机问题（第12章）归约到它。给定 M，构造 M′：它模仿 M，但凡是 M 用 1 的地方都改用一个新符号 1′（因此模拟
   期间 M′ 从不写真正的 1）；凡是 M 要进入停机状态时，M′ 改为写一个 1 然后停机。于是 M′ 会写出 1 当且仅当 M 在空白纸带上停机，而
   M′ 可以由 M 机械地构造出来。若能判定“是否会写出 1”，就能判定空白纸带停机问题，而这是不可能的。

4. **S 严格递增。** 证明对每个 n ≥ 1 都有 S(n + 1) > S(n)。

   *解答。* 取一台 n 状态、恰好走 S(n) 步停机的机器 M。它的最后一步是进入停机状态的一次转移。新增一个状态 Q，把这次转移改为进入
   Q，并规定 Q 读到任何符号都“原样写回、右移、停机”。新机器有 n + 1 个状态，恰好多走一步，所以 S(n + 1) ≥ S(n) + 1。

5. **TIMES 2 2。** 把 (λm n f. m (n f)) 2 2 化为范式。

   *解答。* 按正规序需要 **7 次 β 归约**：先代入 m，再代入 n；外层的 2 作用在 (2 f) 上得到 λx. (2 f) ((2 f) x)；展开两份 2 f，
   得到 λf x. f (f (f (f x)))，也就是丘奇数 4。（本系列的归约器 `explainer/cs/lam.py` 会打印每一行。）

6. **动手：通用机的代价。** 让 U 运行 4 状态的冠军机器，测量每模拟一步所需的步数；再把最常用的规则排到前面。

   *解答。* M 走 107 步，U 要走 13,938 步：**每模拟一步约 130 步**，几乎全花在扫描 ⟨M⟩ 寻找匹配规则和倒带上。统计每条规则的使用
   次数，并在每个状态内部把最常用的排在前面（我们的编码按状态分组列出规则），得到 **13,308 步，约每步 124 步**：只省了 4.5%，因为
   扫描的大部分时间花在跨过*其他*状态的规则上。把最忙的状态编号排在前面效果更好；真正的解释器用一次跳转直接找到规则，这正是第15部分
   分派表的思想。

7. **★ 研究题：反九头蛇。** 反九头蛇的规则是：h ← 8，c ← 0；每一轮，h 为偶数时 c ← c + 2，为奇数时 c ← c − 1，然后
   h ← h + ⌊h/2⌋；c = −1 时停机。（a）证明对于等概率的 +2 和 −1 两种步长，有朝一日比起点低一的概率是 1/φ。（b）证明反九头蛇永不
   停机，当且仅当对每个 N，h₀, …, h_{N−1} 中至少有三分之一是偶数。（c）未解：证明它。

   *已知什么，从哪里入手。*（a）要么第一步就下降（概率 ½），要么先升二，然后必须下降三次：q = ½ + ½q³，于是
   (q − 1)(q² + q − 1) = 0，小于 1 的根是 q = (√5 − 1)/2 = 1/φ。（b）N 轮中有 E 个偶数时，c = 2E − (N − E) = 3E − N。计数器每次
   变化 +2 或 −1，所以它第一次变负时恰好是 −1；对所有 N 都有 c ≥ 0，等价于对所有 N 都有 E ≥ N/3。（c）没有人知道怎么做。⌊3h/2⌋
   迭代的奇偶性是一个确定性的序列，正是让所有已知方法失效的那一类：与考拉兹猜想和马勒的二分之三问题（是否存在 α，使 α(3/2)ⁿ 的小数
   部分始终小于 ½？）属于同一家族。bbchallenge 维基（Antihydra、Cryptids 条目）收集了已有的尝试。从 `videos/cs/cs1/compute.py` 里的
   `compute_frontier` 入手：它用 Python 整数半分钟跑一百万轮，前一百万轮里 3E − N 从未变负。如果能找到比携带整个 h（N 轮后有
   0.585 N 位）更便宜的办法得到奇偶性，那本身就是新闻。

## Sources

Books: Sipser, *Introduction to the Theory of Computation*, ch. 3–5; Petzold, *The Annotated Turing*; Moore & Mertens,
*The Nature of Computation*, ch. 7; Minsky, *Computation: Finite and Infinite Machines*; Boolos, Burgess & Jeffrey,
*Computability and Logic*; Davis, *The Universal Computer*; Hopcroft, Motwani & Ullman, *Introduction to Automata
Theory, Languages, and Computation*.

Papers and documents: Lovelace, notes to Menabrea's *Sketch of the Analytical Engine* (1843); Babbage, *Passages from
the Life of a Philosopher* (1864); Frege, *Begriffsschrift* (1879); Cantor (1891); Hilbert & Ackermann, *Grundzüge der
theoretischen Logik* (1928); Gödel (1931); Church, "An unsolvable problem of elementary number theory" (1936);
Turing, "On computable numbers, with an application to the Entscheidungsproblem" (1936); Rice (1953); Minsky (1961,
1967); Radó, "On non-computable functions" (1962); Hennie, "One-tape, off-line Turing machine computations" (1965);
Lin & Radó (1965); Brady (1983); Cohen, "Computer viruses: theory and experiments" (1987); Marxen & Buntrock (1990);
Cook, "Universality in elementary cellular automata" (2004); Yedidia & Aaronson, "A relatively small Turing machine
whose behavior is independent of set theory" (2016); the bbchallenge collaboration, "Determination of the fifth busy
beaver value" (2025).
