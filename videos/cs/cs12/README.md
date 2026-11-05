# Computer Science, Built — Part 12: Languages and Automata

Part 12 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, *Speaking to the Machine*. To compile a program, something must first
read it. This part builds the theory of reading: languages as sets of strings, regular expressions and finite
automata, grammars and pushdown automata, and seven parsing algorithms, ending with the Pebble language's own lexer,
grammar and parser. The tools live in `explainer/cs/lang/`: `regex.py` (Thompson's construction, a backtracking
matcher, Brzozowski derivatives), `automata.py` (the subset construction, minimization, state elimination, pushdown
automata), `grammar.py` (FIRST/FOLLOW, LL(1), LR(0), SLR, LALR, LR(1), CYK, Earley) and `pebble_lang.py` (the
language: tokens, AST, recursive-descent and Pratt parser, its grammar, and the Job written in it), all tested in
`tests/test_cs12_lang.py` against Python's `re`, brute-force enumeration and textbook counts; the LR tables are also
checked against bison on this machine. Every number is computed in `compute.py`.

* **Six characters that stop a computer.** `(a+)+b` on a string of a's: Python's `re` takes ×4 per two more a's
  (7.8 s at 28), GNU grep 1.5 ms for a million; the Cloudflare outage of 2 July 2019. The Job in the Pebble language,
  2,285 characters, 651 tokens, a 371-node tree.
* **1. Languages as sets of strings.** Alphabets, strings, languages; recognizing against parsing; the ladder of
  memory (finite, a stack, linear, unbounded).
* **2. Regular expressions and automata.** Kleene's three operations (1951); the divisible-by-3 DFA run on `1001`;
  Kleene's theorem as a triangle.
* **3. Thompson's construction.** One fragment per operator; the 14-state NFA for `(a|b)*abb` run on `babbabb` with
  its state sets; O(mn) time, measured linear.
* **4. The subset construction and minimization.** Rabin and Scott (1959): 5 DFA states for `(a|b)*abb`, Moore's
  refinement to 4; the n-th-from-end language, 2ⁿ states (4,096 at n = 12), and the Myhill–Nerode proof checked on
  every pair for n = 3.
* **5. Kleene's theorem.** State elimination turns the divisible-by-3 DFA into `(0|1(01*0)*1)*`, checked on
  1 … 4,095; closure under complement and intersection; decidable equivalence.
* **6. What regular languages cannot do.** The pumping lemma (Bar-Hillel, Perles and Shamir 1961) and its pigeonhole
  proof; aⁿbⁿ refuted on all 15 splits for p = 5; nesting is out of reach.
* **7. Backtracking engines.** 2ⁿ⁻¹ groupings; our backtracker at 29,360,126 steps for n = 22; Python, Perl's cache,
  grep; `.*.*=.*`: 0.12 s → 56 s from 1,000 to 8,000 characters (×8 per doubling), grep unmoved; Stack Overflow 2016;
  Cox 2007 and RE2; back-references (`(11+)\1+` finds composites) and NP-completeness.
* **8. Lexing the Pebble language.** Seven token rules, keywords by lookup, maximal munch (`x-->y` is x, -, ->, y), a
  30-state combined DFA from 96 NFA states; the Job's 651 tokens.
* **9. Context-free grammars.** Chomsky (1956), Backus and Naur (ALGOL 60); a leftmost derivation and its tree;
  ambiguity counted by CYK (the Catalan numbers, 58,786 trees for 12 operands); the dangling else.
* **10. Stacks and the Chomsky hierarchy.** A pushdown automaton for aⁿbⁿ, run step by step; palindromes need
  nondeterminism; the four types and their machines.
* **11. Parsing any grammar: CYK and Earley.** The CYK triangle for `id + id * id`; Earley's items; item counts
  measured, linear on the layered grammar and quadratic on the ambiguous one.
* **12. Top-down parsing.** Recursive descent and left recursion; FIRST, FOLLOW and the LL(1) table; a 17-step trace;
  Pratt's binding powers, the Pebble language's expression parser.
* **13. Bottom-up parsing.** Shift and reduce on `id * id + id`; the 12-state LR(0) automaton and its two conflicts;
  SLR, LR(1) (22 states) and LALR (12); a grammar SLR cannot handle; bison agrees state for state (plus its accept
  state) and on the dangling-else conflict.
* **14. The Pebble language, parsed.** Name-first declarations and mandatory braces; 79 rules, a conflict-free
  146-state LALR table (bison: 147); the AST of lookup's loop; error messages.
* **15. Frontier: how fast can we parse?** Thompson's work measured as m × n; Myers, and Backurs and Indyk under
  SETH; Valiant's reduction to matrix multiplication, Lee's converse, Abboud–Backurs–Williams; derivatives, which
  give the minimal DFA on every example, and their revival in .NET's engine.
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs12.compute           # every number in the part (a few minutes: it waits for Python's re)
python tools/build.py cs12 -q l            # a 480p preview
python tools/build.py cs12                 # 1080p
```

The timings (`blowup`, `cloudflare`, `primes`, `cyk`, `frontier`) belong to the computer that runs them; the
automata, grammars and tables are exact.

## Problems, with solutions

1. **Divisible by 5.** Draw a DFA for binary numbers divisible by 5, and turn it into a regular expression by state
   elimination.

   *Solution.* States 0–4 are remainders; reading bit b takes r to (2r + b) mod 5; start and accept at 0. Eliminating
   the states in the order 0, 1, 2, 3, 4 (as `automata.to_regex` does) gives an expression of 275 characters, which
   `compute`-style checking confirms on every number up to 2,000. The length is the lesson: state elimination is
   correct but can produce expressions exponentially longer than the automaton, and the order of elimination matters
   a great deal.

2. **Equal counts.** Use the pumping lemma to show that the strings over {a, b} with as many a's as b's are not
   regular.

   *Solution.* Suppose a DFA with p states recognizes it. Take s = aᵖbᵖ, which is in the language and has length ≥ p.
   Any split s = xyz with |xy| ≤ p and |y| > 0 puts y inside the a's, so xy²z has more a's than b's and is not in the
   language: a contradiction. (Alternatively: intersect with the regular language a*b*; the result, aⁿbⁿ, would be
   regular, but chapter 6 showed it is not.)

3. **Balanced parentheses.** Show that S → S S | ( S ) | ε is ambiguous, and write an unambiguous grammar.

   *Solution.* `()()()` has two trees, (S S) S and S (S S), and CYK on the grammar's normal form counts exactly 2; the
   empty string even has infinitely many derivations, through S → S S → S. The grammar S → ( S ) S | ε is
   unambiguous: the first parenthesis of a non-empty string has a unique matching partner, which fixes the split.

4. **LL(1).** Compute FIRST and FOLLOW for S → ( S ) S | ε, and decide whether it is LL(1).

   *Solution.* S is nullable; FIRST(S) = { ( }, FOLLOW(S) = { ), $ }. The table has S, ( → ( S ) S and S, ) → ε,
   S, $ → ε: one rule per cell, so it is LL(1) (our `ll1_table` reports no conflicts).

5. **Build: for loops.** Add `for` loops and the operators `+=` and `++` to the Pebble language: lexer, grammar, parser.
   Does the grammar stay LALR(1)?

   *Solution.* Lexer: add `+=` and `++` to the operator rule before `+` (maximal munch then does the rest) and `for`
   to the keywords. Grammar: `Stmt → for Simple ; Expr ; Simple Block | … | Simple ;` with
   `Simple → Expr | Expr = Expr | Expr += Expr | Expr ++`. Our LALR construction on the extended grammar finds 156
   states and no conflicts (SLR has none either), so yes. Parser: in `Parser.stmt`, parse an expression and then look
   for `=`, `+=` or `++`; a `for` desugars to `Simple; while Expr { Block; Simple }`, which Part 13's compiler then
   needs no new machinery for.

6. ★ **Research: which patterns are hard?** For which regular expressions can matching be done in time O(n + m), and
   for which does SETH forbid it? Complete the classification.

   *Where to start.* Backurs and Indyk, "Which regular expression patterns are hard to match?" (FOCS 2016), classify
   patterns by the depth and operator types of their syntax trees, proving SETH-hardness for many and giving
   near-linear algorithms for others. Bringmann, Grønlund and Larsen, "A dichotomy for regular expression membership
   testing" (FOCS 2017), complete the picture for a large class. (a) Reproduce one hardness reduction: encode an
   Orthogonal Vectors instance as a pattern and a text. (b) Use `compute_frontier`'s grid as a test bed: find a
   pattern type whose measured work grows more slowly than m × n under our simulation, and explain why. (c) Read
   the open cases in the 2017 paper and attack the smallest one.

## 习题与解答

1. **被 5 整除。** 画出识别能被 5 整除的二进制数的 DFA，并用状态消去法把它变成正则表达式。

   *解答。* 状态 0–4 表示余数；读入位 b 时，r 变成 (2r + b) mod 5；起始状态和接受状态都是 0。按 0、1、2、3、4 的顺序
   消去（`automata.to_regex` 就是这样做的），得到一个 275 个字符的表达式，对 2,000 以内的每个数都检验无误。长度本身就是
   教训：状态消去是正确的，但得到的表达式可能比自动机长得多，而消去顺序影响很大。

2. **个数相等。** 用泵引理证明：{a, b} 上 a 和 b 一样多的串不是正则语言。

   *解答。* 设有一个 p 个状态的 DFA 识别它。取 s = aᵖbᵖ，它在语言中且长度不小于 p。任何满足 |xy| ≤ p、|y| > 0 的切分
   s = xyz 都使 y 落在 a 里，于是 xy²z 的 a 比 b 多，不在语言中：矛盾。（也可以：与正则语言 a*b* 求交，得到 aⁿbⁿ，它会
   是正则的，但第六章已证明它不是。）

3. **括号匹配。** 证明 S → S S | ( S ) | ε 是有歧义的，并写出一个无歧义的文法。

   *解答。* `()()()` 有两棵树，(S S) S 和 S (S S)，在它的范式上运行 CYK 恰好数出 2；空串甚至有无穷多种推导，经由
   S → S S → S。文法 S → ( S ) S | ε 无歧义：非空串的第一个括号有唯一的配对括号，它决定了切分。

4. **LL(1)。** 计算 S → ( S ) S | ε 的 FIRST 和 FOLLOW，判断它是否 LL(1)。

   *解答。* S 可空；FIRST(S) = { ( }，FOLLOW(S) = { ), $ }。分析表中 S, ( → ( S ) S，S, ) → ε，S, $ → ε：每格一条
   规则，所以是 LL(1)（我们的 `ll1_table` 报告没有冲突）。

5. **动手：for 循环。** 给 Pebble 语言加上 `for` 循环和运算符 `+=`、`++`：词法、文法、语法分析器。文法还是 LALR(1) 吗？

   *解答。* 词法：在运算符规则里把 `+=` 和 `++` 放在 `+` 之前（其余交给最长匹配），把 `for` 加进关键字。文法：
   `Stmt → for Simple ; Expr ; Simple Block | … | Simple ;`，`Simple → Expr | Expr = Expr | Expr += Expr | Expr ++`。
   我们的 LALR 构造在扩展后的文法上得到 156 个状态、没有冲突（SLR 也没有），所以是。语法分析器：在 `Parser.stmt` 里
   先分析一个表达式，再看后面是 `=`、`+=` 还是 `++`；`for` 可以脱糖成 `Simple; while Expr { Block; Simple }`，这样第13部分
   的编译器不需要任何新机制。

6. ★ **研究：哪些模式难？** 哪些正则表达式能在 O(n + m) 时间内匹配，哪些被 SETH 禁止？完成这个分类。

   *从哪里开始。* Backurs 与 Indyk，《Which regular expression patterns are hard to match?》（FOCS 2016），按语法树的深度
   和运算符种类给模式分类，证明许多模式是 SETH 难的，另一些有近线性算法。Bringmann、Grønlund 与 Larsen，《A dichotomy
   for regular expression membership testing》（FOCS 2017），对一大类模式完成了分类。（a）重现一个难度归约：把一个正交
   向量实例编码成一个模式和一段文本。（b）把 `compute_frontier` 的网格当作试验台：找出一种模式，它在我们的模拟中测得的
   工作量增长得比 m × n 慢，并解释原因。（c）读 2017 年论文中的开放情形，从最小的一个入手。

## Glossary additions

字母表 alphabet · 串 string · 空串 empty string · 语言 language · 识别器 recognizer · 语法分析器 parser · 正则表达式
regular expression · 并 / 连接 / 星号 union / concatenation / star · 有限自动机 finite automaton · 确定性 / 非确定性
deterministic / nondeterministic · ε 边 ε-edge · 汤普森构造 Thompson's construction · 子集构造 subset construction ·
最小化 minimization · 可区分 distinguishable · 状态消去 state elimination · 克莱尼定理 Kleene's theorem · 封闭性 closure
property · 泵引理 pumping lemma · 回溯 backtracking · 回溯引用 back-reference · 词法分析 lexing · 记号 token · 最长匹配
maximal munch · 上下文无关文法 context-free grammar · 终结符 / 非终结符 terminal / nonterminal · 推导 derivation · 语法树
parse tree · 歧义 ambiguity · 悬空 else dangling else · 下推自动机 pushdown automaton · 乔姆斯基层级 Chomsky hierarchy ·
乔姆斯基范式 Chomsky normal form · 自顶向下 / 自底向上 top-down / bottom-up · 递归下降 recursive descent · 左递归 left
recursion · FIRST 集 / FOLLOW 集 FIRST / FOLLOW sets · 绑定力 binding power · 移进 / 归约 shift / reduce · 项 item ·
冲突 conflict · 抽象语法树 abstract syntax tree · 导数 derivative

## Sources

*Canon.* Books: Sipser, *Introduction to the Theory of Computation*, ch. 1–2; Hopcroft, Motwani & Ullman,
*Introduction to Automata Theory, Languages, and Computation*; Aho, Lam, Sethi & Ullman, *Compilers: Principles,
Techniques, and Tools* (the Dragon Book), ch. 2–4; Grune & Jacobs, *Parsing Techniques: A Practical Guide*; Nystrom,
*Crafting Interpreters*.

Papers: Kleene, "Representation of events in nerve nets and finite automata" (1956); Chomsky, "Three models for the
description of language" (1956); Moore, "Gedanken-experiments on sequential machines" (1956); Rabin & Scott, "Finite
automata and their decision problems" (1959); Backus et al., "Report on the algorithmic language ALGOL 60" (1960);
Bar-Hillel, Perles & Shamir, "On formal properties of simple phrase structure grammars" (1961); Brzozowski,
"Derivatives of regular expressions" (1964); Knuth, "On the translation of languages from left to right" (1965);
Younger, "Recognition and parsing of context-free languages in time n³" (1967); Thompson, "Regular expression search
algorithm" (1968); Lewis & Stearns, "Syntax-directed transduction" (1968); DeRemer, "Practical translators for LR(k)
languages" (1969) and "Simple LR(k) grammars" (1971); Earley, "An efficient context-free parsing algorithm" (1970);
Pratt, "Top down operator precedence" (1973); Valiant, "General context-free recognition in less than cubic time"
(1975); Johnson, "Yacc: yet another compiler-compiler" (1975); Lesk, "Lex: a lexical analyzer generator" (1975);
Aho, "Algorithms for finding patterns in strings" (1990); Myers, "A four Russians algorithm for regular expression
pattern matching" (1992).

*Recent.* Lee, "Fast context-free grammar parsing requires fast Boolean matrix multiplication" (2002); Cox, "Regular
expression matching can be simple and fast" (2007); Owens, Reppy & Turon, "Regular-expression derivatives
re-examined" (2009); Might, Darais & Spiewak, "Parsing with derivatives" (2011); Abboud, Backurs & Vassilevska
Williams, "If the current clique algorithms are optimal, so is Valiant's parser" (2015); Backurs & Indyk, "Which
regular expression patterns are hard to match?" (2016); Bringmann, Grønlund & Larsen, "A dichotomy for regular
expression membership testing" (2017); Moseley et al., "Derivative based nonbacktracking real-world regex matching
with backtracking semantics" (2023); Stack Overflow, outage postmortem, 20 July 2016; Cloudflare, "Details of the
Cloudflare outage on July 2, 2019".
