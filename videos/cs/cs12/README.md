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

* **Six characters and an expensive rejection.** `(a+)+b` on failing all-a inputs; recorded Python growth, a 30-second timeout, and a noisy process-baseline-subtracted grep comparison. Cloudflare's 2019 outage motivates a separately labeled simplified experiment.
* **1. Languages.** Finite alphabets, finite strings and possibly infinite languages; recognition versus parsing; syntax acceptance versus semantic checks; memory models without fixed workspace bounds.
* **2. Regular expressions.** Union, concatenation and star over a chosen alphabet. Ordinary syntax is regular; practical backreferences require separate treatment. The binary-divisibility example accepts epsilon and leading zeros by convention.
* **3. Thompson.** A 14-state NFA for `(a|b)*abb`, its epsilon closure and active-set trace on `babbabb`. Epsilon consumes no input but takes computation. A bounded-degree Thompson construction gives O(mn) time and O(m) active storage; measured counters are work proxies.
* **4. Subsets and minimization.** Five reachable DFA states reduce to four. Minimal complete DFAs are unique up to renaming over a fixed alphabet. The n-th-from-end lower bound uses pairwise distinguishability; the n=3 enumeration checks 28 witnesses. Lazy caching helps the chosen book sample without removing exponential worst cases.
* **5. Kleene.** State elimination, complete-DFA complement, product intersection and decidable equivalence. A finite round-trip test checks an implementation; the construction supplies the general argument.
* **6. Pumping.** An arbitrary-p contradiction for aⁿbⁿ, illustrated by all 15 splits at p=5. Balanced parentheses are ruled out using intersection with opens-then-closes; a nonregular subset alone would not suffice. Fixed nesting depth changes the language.
* **7. Engine strategies.** Partition enumeration explains one naive exponential failure mode. Real engines optimize differently. The simplified unanchored Python `.*.*=.*` experiment shows superlinear behavior, with censored measurements labeled. The unary composite matcher assumes length at least two. Backreference NP-completeness is a combined pattern-and-text statement.
* **8. Lexing.** Seven token rules, longest-match policy and identifier-to-keyword lookup. The combined 96-state NFA has 30 reachable DFA states on the sampled alphabet. The Job has 2,285 characters, 651 tokens and locations/lexemes retained for the parser. Literal code tokens stay exact in both languages. Python's indentation uses a stack.
* **9. Grammars.** Derivations, parse trees, precedence, Catalan counts and dangling else. A nearest-else convention can be encoded through grammar design or parser resolution. Arbitrary CFG ambiguity is undecidable.
* **10. Hierarchy.** A stack for aⁿbⁿ and nondeterministic midpoint guessing for unmarked binary palindromes. Marked or unary palindromes differ. Production-language semantic disambiguation and unrestricted compile-time computation exceed a fixed CFG recognizer; actual compilers impose resource limits.
* **11. General CFG parsing.** CYK's triangle and Earley's items. Bounds assume a fixed grammar; empty-input CNF needs special handling. Item counts, elapsed time and worst-case bounds are distinct.
* **12. Top down.** Recursive descent, FIRST/FOLLOW, a conflict-free LL(1) table and 17-step trace, plus Pratt binding powers. Production recursive-descent front ends need not be LL(1).
* **13. Bottom up.** LR(0), SLR, LR(1) and LALR; merging equal LR(0) cores can introduce conflicts. Bison's selected tables agree in counts and conflicts, with its additional acceptance state. This is not a proof of table isomorphism.
* **14. Pebble.** A 79-rule, 146-state conflict-free LALR grammar (Bison: 147), the Job's 371-node AST and four error examples. The detection token need not locate the original mistake; syntax does not establish type correctness.
* **15. Frontier.** Honest log-millisecond timing axes and a fitted finite-sample slope. Specify regex pattern families, membership versus search, SETH quantifiers and computational models. The bounded-depth homogeneous membership classification was completed in 2017, with an intermediate Word Break case. Valiant, Lee and clique reductions have distinct model/grammar-size assumptions. Residual languages give the minimal derivative DFA; raw expression syntax needs normalization or equivalence reasoning. .NET's nonbacktracking guarantee concerns supported fixed patterns.

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

   *Solution.* There are different binary groupings of the three pairs, already proving ambiguity. In fact the original grammar has infinitely many parse trees for every word it generates: insert `S → S S` and derive ε on one branch, arbitrarily often. A language-preserving CNF conversion need not preserve those tree multiplicities; a finite CYK count for the converted grammar is not a count for this original grammar. The grammar `S → ( S ) S | ε` is unambiguous because a nonempty word's first opening parenthesis has a unique matching partner, fixing the recursive split.

4. **LL(1).** Compute FIRST and FOLLOW for S → ( S ) S | ε, and decide whether it is LL(1).

   *Solution.* S is nullable; FIRST(S) = { ( }, FOLLOW(S) = { ), $ }. The table has S, ( → ( S ) S and S, ) → ε,
   S, $ → ε: one rule per cell, so it is LL(1) (our `ll1_table` reports no conflicts).

5. **Build: for loops.** Add `for` loops and the operators `+=` and `++` to the Pebble language: lexer, grammar, parser.
   Does the grammar stay LALR(1)?

   *Solution.* Lexer: add `+=` and `++` to the operator rule before `+` (maximal munch then does the rest) and `for`
   to the keywords. Grammar: `Stmt → for Simple ; Expr ; Simple Block | … | Simple ;` with
   `Simple → Expr | Expr = Expr | Expr += Expr | Expr ++`. Our LALR construction on the extended grammar finds 156
   states and no conflicts (SLR has none either), so this particular extension is LALR(1). Parser: in `Parser.stmt`, parse an expression and then look
   for `=`, `+=` or `++`; a `for` can lower to initialization, condition and body/update control flow. Preserve loop scope, and make `continue` execute the update before retesting; blindly replacing it with a while loop would skip that update. The expressions and assignments also need the language's later semantic checks.

6. ★ **Investigate: which regex problem is hard?** Reproduce one complexity result, stating its exact input model.

   *Where to start.* Read Backurs–Indyk (2016) together with Bringmann–Grønlund–Larsen (2017). The latter completes a classification of bounded-depth homogeneous **membership** types, including an intermediate Word Break case; do not present that classification as still unfinished. (a) State the pattern type, whether the task is membership or substring matching, and whether pattern size is fixed or variable. (b) Reproduce a small reduction or implement the corresponding easy-case algorithm. (c) Compare predictions with the simulator grid, explaining why finite active-set counts establish neither a general lower bound nor an engine-runtime guarantee. Further research must identify a specific extension outside the completed classification and check current literature before calling it open.

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

   *解答。* 三对括号可以有不同的二叉分组，这已经证明歧义。事实上，原文法生成的每个串都有无穷多棵语法树：反复插入 `S → S S`，并让一侧导出 ε。保持语言的 CNF 转换未必保持这些树的重数；转换后文法的有限 CYK 计数，不是原文法的计数。`S → ( S ) S | ε` 无歧义，因为非空串的第一个左括号有唯一的配对右括号，唯一决定递归切分。

4. **LL(1)。** 计算 S → ( S ) S | ε 的 FIRST 和 FOLLOW，判断它是否 LL(1)。

   *解答。* S 可空；FIRST(S) = { ( }，FOLLOW(S) = { ), $ }。分析表中 S, ( → ( S ) S，S, ) → ε，S, $ → ε：每格一条
   规则，所以是 LL(1)（我们的 `ll1_table` 报告没有冲突）。

5. **动手：for 循环。** 给 Pebble 语言加上 `for` 循环和运算符 `+=`、`++`：词法、文法、语法分析器。文法还是 LALR(1) 吗？

   *解答。* 词法：在运算符规则里把 `+=` 和 `++` 放在 `+` 之前（其余交给最长匹配），把 `for` 加进关键字。文法：
   `Stmt → for Simple ; Expr ; Simple Block | … | Simple ;`，`Simple → Expr | Expr = Expr | Expr += Expr | Expr ++`。
   我们的 LALR 构造在扩展后的文法上得到 156 个状态、没有冲突（SLR 也没有），所以是。语法分析器：在 `Parser.stmt` 里
   先分析一个表达式，再看后面是 `=`、`+=` 还是 `++`；`for` 可以降低为初始化、条件与循环体及更新控制流，但必须保持作用域，并让 `continue` 先执行更新再检查条件；直接替换为 while 会跳过这一步。表达式和赋值还需后续语义检查。

6. ★ **研究：哪一种正则问题困难？** 重现一项复杂度结果，并明确输入模型。

   *从哪里开始。* 对照阅读 Backurs–Indyk（2016）与 Bringmann–Grønlund–Larsen（2017）。后者完成了有界深度齐次模式的**成员判定**类型分类，其中包含处于中间复杂度的 Word Break；不能把这个分类说成尚未完成。（a）说明模式类型、整串成员判定还是子串匹配，以及模式大小固定还是随输入变化。（b）重现一个小型归约，或实现相应容易类别的算法。（c）与模拟器网格比较，解释为什么有限活跃集合计数既不能证明一般下界，也不能保证引擎耗时。进一步研究必须选定已经完成的分类以外的具体扩展，并检查当前文献后才称其为开放问题。

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
