# Computer Science, Built — Part 14: Lambda and Types

Part 14 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, *Speaking to the Machine*. Church's λ-calculus is a whole programming
language made of functions alone; types tame it; well-typed programs cannot go wrong, which we prove and check; a
type can be inferred without being written; and types turn out to be propositions and programs to be proofs. The
instruments are Part 1's `explainer/cs/lam.py` (terms, substitution, normal order) and `explainer/cs/lang/lam/`:
`reduce.py` (five strategies, an environment machine with thunks that counts sharing, the whole reduction graph,
complete developments, de Bruijn indices, the Church encodings), `stlc.py` (the simply typed calculus with booleans
and naturals: derivations, small-step evaluation, a random generator, finite checks of the safety rules), `ml.py` (the
λ-core, a small ML with Hindley–Milner inference by Algorithm W with levels, an evaluator, and the Job written in
it) and `logic.py` (proof search as program search, truth tables, Kripke countermodels), tested in
`tests/test_cs14_types.py`. Every number is computed in `compute.py`; `rustc` and `tsc` on this machine supply
chapters 13 and 14's compiler messages.

* **A language made of functions.** The Job in the λ-core with not one annotation, and every type inferred
  (`bump : 'a -> ('a * int) list -> ('a * int) list`); 2 + 3 in pure λ, six β-steps to the numeral 5.
* **1. Terms, variables and substitution.** Three kinds of term and their trees; free and bound variables;
  α-equivalence; the capture trap, `(λx. λy. x) y`, and capture-avoiding substitution.
* **2. Reduction and normal forms.** β-reduction; a step that copies a redex; 2 + 3 redex by redex; Ω; a term with
  a normal form along one path and an infinite path along another.
* **3. Programming with nothing.** Booleans as choices (and/or checked); numerals as repetition, drawn as nested
  boxes; plus, times and pow (6, 9 and 16 steps); pairs; Kleene's predecessor (9 steps at zero; 10n + 6 at positive n); lists as folds.
* **4. Recursion without names.** Fixed points; Y unfolding; factorial through Y (24 for n = 4, in 10,384 steps);
  Y cannot return a closure under call-by-value; Z can, but strict factorial also needs delayed conditional branches. The repaired example computes 0! through 3! with actual CBV numeral readback.
* **5. Evaluation strategies.** Normal, applicative, by name, by value, by need; K a Ω under each; sharing counted
  (43 against 33 β-steps when an argument is used three times); the standardization theorem.
* **6. Church–Rosser, and de Bruijn.** The full reduction graph of a small term (6 terms, 7 steps, one normal
  form) and a bigger one (30 terms, 93 steps, confluent); the diamond and parallel reduction; de Bruijn indices.
* **7. Simple types.** Stuck terms; Milner's slogan; the syntax and rules; a derivation tree drawn by our checker;
  a small-step trace with its rules.
* **8. Well-typed programs cannot go wrong.** Progress and preservation; the proofs' key cases (canonical forms,
  the substitution lemma); both checked on 5,000 random terms and 50,516 steps; safety in real languages.
* **9. Strong normalization in the recursion-free simply typed core.** Ω is untypable (`'a = 'a -> 'b`); Tait's strong normalization and logical
  relations; 136 of 2,000 random untyped terms still running after 400 steps, none of 5,000 typed ones; the price,
  and `fix`.
* **10. Hindley–Milner inference.** Unification (Robinson 1965) and its occurs check; our engine's trace for
  `fun f x -> f (f x)`; let-polymorphism; the Job's eleven principal types; the nested-let worst case, 2^(2^n)
  leaves, DEXPTIME-complete.
* **11. Polymorphism and free theorems.** System F; Church's encodings typed; parametricity; the free theorem
  `map f ∘ g = g ∘ map f` tested on four polymorphic functions (200/200 each) and broken by a monomorphic function. An additional equality-selector counterexample has the same printed polymorphic type in our toy core: unrestricted structural equality is outside pure System F parametricity. A commuting-square diagram shows the actual failure on [1,2] mapped to [0,0]. Real ML equality-type constraints need more modeling than this printer provides.
* **12. Propositions as types.** The dictionary; programs found by proof search (S, K, composition,
  `¬¬(A ∨ ¬A)`); excluded middle, double negation, Peirce and de Morgan's half with no program; a two-world Kripke
  model; call/cc and Peirce's law (Griffin 1990).
* **13. Dependent and linear types.** Vectors indexed by length; Π and Σ; Martin-Löf, Coq/Rocq, Lean; linear,
  affine and relevant combinators; rustc's E0382 and E0502.
* **14. Data, subtyping and gradual types.** Algebraic data types and `option`; variance; TypeScript's covariant
  arrays accepted by `tsc --strict` and failing in node; `any`; Siek and Taha's gradual typing and its cost.
* **15. Frontier: the edges of type theory.** Single-host inference samples for 32 copies of eleven definitions (352 total), with a data-derived axis;
  refinement types and SMT; homotopy type theory, univalence and cubical type theory; effect handlers; open
  problems.
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs14.compute           # compute missing items; timings depend on this host
python tools/build.py cs14 -q l            # a 480p preview
python tools/build.py cs14                 # 1080p
```

The `rust` and `gradual` items call `rustc` and `tsc`/`node` on this machine and record their versions; the
`frontier` timings belong to the computer that runs them. Finite random samples check implementations; they do not prove general theorems. Beta-step counts describe this encoding and evaluator, excluding syntax-copy, allocation and machine-time costs. RustBelt verifies a realistic subset and selected unsafe abstractions, not every Rust implementation. Strong normalization and parametricity claims retain their pure-core assumptions; explicit System F checking differs from unrestricted implicit inference.

## Problems, with solutions

1. **Two orders.** Reduce `(λx y. y x x) ((λz. z) a) (λw. w)` to normal form by normal order and by applicative
   order, count the steps, and explain the difference.

   *Solution.* Normal order (5 steps): substitute the unreduced argument `(λz. z) a` for x, giving
   `(λy. y A A) (λw. w)` with A = `(λz. z) a`; then `(λw. w) A A`, then `A A`, then reduce each copy of A: `a A`,
   `a a`. Applicative order (4 steps): reduce A to `a` first, then `(λx y. y x x) a` → `λy. y a a`, then apply it
   to the identity and reduce `(λw. w) a a` → `a a`. Normal order copied the argument before evaluating it, so it
   evaluated it twice; applicative order evaluated it once. Both reach the same normal form, as Church–Rosser
   promises. (Our reducer, `reduce.run`, gives 5 and 4.)

2. **More arithmetic, with a cost model.** Define exp, iszero and saturating sub on Church numerals. Count beta contractions for an algorithm that fully normalizes each predecessor result before the next application. Explain why a universal Theta(m*n) runtime claim is unjustified.

   *Solution.* `exp = λm n. n m`, `iszero = λn. n (λz. false) true`, and `sub = λm n. n pred m`. The result is max(m−n,0). For this library's predecessor, full normal-order contraction counts are p(0)=9 and p(k)=10k+6 for positive k. Normalizing each intermediate numeral gives sum(p(max(m−i,0)), i=0..n−1). With r=min(m,n), this is r(10m+6)−5r(r−1)+9(n−r). Thus this particular contraction-count algorithm has order n+m*min(m,n) for nontrivial inputs, including saturation at zero. Counting the four outer beta contractions in the literal `sub` term matches our 63 sampled (m,n) pairs, but finite agreement is not a universal complexity proof for every reducer. At n=0 the term returns an already present numeral in four contractions; printing its m applications or copying syntax has another cost. State the representation, stopping criterion, sharing and unit cost before comparing implementations.

3. **Two cases of progress.** Prove progress for If and Succ, stating the canonical forms lemma you need.

   *Solution.* Canonical forms: a value of type Bool is true or false; a value of type Nat is 0 or succ v with v a
   numeric value; a value of type A → B is a λ. Case If: ⊢ if c a b : T needs ⊢ c : Bool. By induction c is a
   value or steps. If it steps, E-If makes the whole term step. If it is a value, by canonical forms it is true or
   false, and E-IfTrue or E-IfFalse applies. Case Succ: ⊢ succ t : Nat needs ⊢ t : Nat. If t steps, so does succ t
   (E-Succ); if t is a value, it is a numeric value by canonical forms, so succ t is itself a value.

4. **Inference by hand.** Infer the principal type of `λf g x. g (f x) x`, showing each unification.

   *Solution.* Assume f : α, g : β, x : γ. `f x` forces α = γ → δ. `g (f x)` forces β = δ → ε. `(g (f x)) x`
   forces ε = γ → ζ. Substituting: f : γ → δ, g : δ → γ → ζ, x : γ, result ζ. Renaming, the principal type is
   `('a -> 'b) -> ('b -> 'a -> 'c) -> 'a -> 'c`, exactly what our engine reports, with the same three bindings in
   the same order.

5. **Build: a precisely scoped option type.** Add an `'a option = None | Some of 'a` declaration and matches in which each constructor is followed only by distinct variable binders. Infer types and rewrite the Job's lookup to return an option.

   *Solution.* Give `None` the scheme forall a. a option and `Some` the scheme forall a. a -> a option. Instantiate freshly at each use. In a match, unify the scrutinee with option tau, bind the `Some` field at tau, and unify branch result types. In this shallow pattern fragment, coverage means both None and Some occur, or a final wildcard covers the remainder; reject duplicates or report them as unreachable. Merely counting top-level constructors does **not** check nested patterns such as `Some (Some x)` exhaustively. An extension to nested patterns needs recursive pattern-matrix specialization and default cases. Evaluate options as tagged values. Implement `find : 'a -> ('a * 'b) list -> ('a * 'b) option`, then compare the rewritten Job with `job_reference` on empty input, repeated words, ties and absent keys. Equality constraints in a realistic ML require explicit treatment; our toy printer omits them. This is a build specification, not a claim that the current repository already implements user-defined ADTs.

6. **★ Investigation: space-efficient gradual checks.** Reproduce a known coercion-composition scheme for a small higher-order gradual calculus, then state and investigate one extension.

   *Where to start.* Fix the typed/untyped boundary semantics, observable errors, baseline program and cost model. A direct wrapper-chain implementation can accumulate proxies; known space-efficient coercions compose checks and prevent that growth. Reproduce that result before proposing a lower bound. Track maximum live coercion size, allocations, checks and runtime separately. Then choose one extension—such as mutable references with a specified semantics—and review existing results before claiming novelty. The 2016 Typed Racket study measured over 100× overhead in some tested configurations; that is a historical workload result, not a universal lower bound. A representation-space bound also does not establish a universal constant runtime-overhead factor. See Siek and Taha (2006), refined gradual criteria (2015), Grift (2019), and *Space-Efficient Gradual Typing in Coercion-Passing Style* (ECOOP 2020).

## 习题与解答

1. **两种顺序。** 分别用正规序和应用序把 `(λx y. y x x) ((λz. z) a) (λw. w)` 归约到范式，数出步数，并解释差别。

   *解答。* 正规序（5 步）：把尚未归约的实参 `(λz. z) a` 代入 x，得到 `(λy. y A A) (λw. w)`，其中 A = `(λz. z) a`；
   然后是 `(λw. w) A A`，再到 `A A`，再分别归约 A 的两个副本：`a A`、`a a`。应用序（4 步）：先把 A 归约成 `a`，
   然后 `(λx y. y x x) a` → `λy. y a a`，再作用于恒等函数，`(λw. w) a a` → `a a`。正规序在求值之前复制了实参，
   所以求值了两次；应用序只求值一次。两者到达同一个范式，正如丘奇–罗瑟定理所保证的。（我们的归约器
   `reduce.run` 给出 5 和 4。）

2. **带代价模型的算术。** 定义丘奇幂、零测试和饱和减法。采用每次求前驱后先完全正规化结果的算法，统计 β 收缩，说明为何不能笼统声称运行时间为 Theta(m*n)。

   *解答。* `exp = λm n. n m`，`iszero = λn. n (λz. false) true`，`sub = λm n. n pred m`，结果是 max(m−n,0)。本库的完全正规序前驱计数为 p(0)=9，正数时 p(k)=10k+6。每次先正规化中间数，计数是对 i=0..n−1 求和 p(max(m−i,0))。令 r=min(m,n)，得到 r(10m+6)−5r(r−1)+9(n−r)。对非平凡输入，这一特定收缩计数算法的阶是 n+m*min(m,n)，包含归零后的饱和行为。再加上字面 `sub` 项外层的四次收缩，与本次 63 组 (m,n) 样本一致，但有限一致不证明所有归约器的普遍复杂度。n=0 时四次收缩就返回已有数；输出 m 次应用、复制语法和分配内存另有代价。比较实现前应明确表示、停止标准、共享与单位代价。

3. **进展性的两个情形。** 证明 If 和 Succ 两种情形下的进展性，并写出所需的典范形式引理。

   *解答。* 典范形式：Bool 类型的值是 true 或 false；Nat 类型的值是 0 或 succ v（v 是数值）；A → B 类型的值是一个
   λ。If 情形：⊢ if c a b : T 需要 ⊢ c : Bool。由归纳假设，c 是值或能走一步。若能走一步，E-If 使整个项走一步。若是
   值，由典范形式它是 true 或 false，于是 E-IfTrue 或 E-IfFalse 适用。Succ 情形：⊢ succ t : Nat 需要 ⊢ t : Nat。
   若 t 能走一步，succ t 也能（E-Succ）；若 t 是值，由典范形式它是数值，于是 succ t 本身就是值。

4. **手工推断。** 推断 `λf g x. g (f x) x` 的主类型，写出每一次合一。

   *解答。* 设 f : α，g : β，x : γ。`f x` 迫使 α = γ → δ。`g (f x)` 迫使 β = δ → ε。`(g (f x)) x` 迫使
   ε = γ → ζ。代入后：f : γ → δ，g : δ → γ → ζ，x : γ，结果为 ζ。改名之后，主类型是
   `('a -> 'b) -> ('b -> 'a -> 'c) -> 'a -> 'c`，与我们的引擎报告的完全一致，三次绑定的顺序也相同。

5. **构建范围明确的 option 类型。** 加入 `'a option = None | Some of 'a`，先只允许构造子后接互异变量的浅层模式。支持类型推断，并让任务的查找返回 option。

   *解答。* `None` 的方案为 forall a. a option，`Some` 为 forall a. a -> a option，每次使用重新实例化。匹配时，把被匹配值与 option tau 合一，给 Some 的字段绑定 tau，并合一各分支结果。这个浅层片段中，None 与 Some 均出现，或最后的通配分支覆盖余项，即为穷尽；重复分支应拒绝或报告不可达。仅数顶层构造子，不能判断 `Some (Some x)` 等嵌套模式是否穷尽；扩展需要递归的模式矩阵专化与默认情形。求值使用带标签的值。实现 `find : 'a -> ('a * 'b) list -> ('a * 'b) option` 后，用空输入、重复词、同频词和缺失键，对照 `job_reference`。真实 ML 还须明确处理相等约束，本玩具打印器没有显示它们。这是构建规格，不表示仓库已经实现用户自定义 ADT。

6. **★ 研究：空间高效的渐进检查。** 为一个小型高阶渐进演算复现已知的强制组合方案，再定义一个扩展并调查。

   *从哪里开始。* 明确有类型与无类型边界的语义、可观察错误、基准程序及代价模型。直接使用包装链可能积累代理，但已有空间高效强制通过组合检查阻止这种增长；提出下界之前，先复现该结果。分别跟踪最大存活强制大小、分配次数、检查次数与运行时间。然后选择例如具有明确语义的可变引用扩展，调查已知结果后再主张新颖性。2016 年 Typed Racket 研究在部分被测配置中观察到超过 100 倍开销；这是历史负载结果，不是普遍下界。表示的空间上界也不等于运行时间具有普遍常数开销因子。可从 2006 年渐进类型、2015 年细化判据、Grift（2019）以及 ECOOP 2020 的强制传递风格空间高效渐进类型工作开始。

## Glossary additions

λ 演算 lambda calculus · 项 term · 抽象 abstraction · 应用 application · 自由变量 / 约束变量 free / bound variable ·
α 等价 alpha-equivalence · 变量捕获 variable capture · 避免捕获的代换 capture-avoiding substitution · β 归约
beta-reduction · 可约式 redex · 范式 normal form · 丘奇数 Church numeral · 丘奇编码 Church encoding · 不动点 fixed
point · Y 组合子 Y combinator · 归约策略 reduction strategy · 正规序 / 应用序 normal / applicative order · 传名 / 传值
/ 传需 call-by-name / -value / -need · 共享 sharing · 标准化定理 standardization theorem · 合流性 confluence · 丘奇–
罗瑟定理 Church–Rosser theorem · 平行归约 parallel reduction · 德布鲁因指标 de Bruijn index · 简单类型 simple types ·
类型规则 typing rule · 推导 derivation · 卡住 stuck · 进展性 progress · 保持性 preservation · 典范形式 canonical forms ·
代换引理 substitution lemma · 强正规化 strong normalization · 逻辑关系 logical relations · 类型推断 type inference ·
合一 unification · 出现检查 occurs check · 主类型 principal type · let 多态 let-polymorphism · System F · 参数性
parametricity · 免费定理 free theorem · 柯里–霍华德对应 Curry–Howard correspondence · 直觉主义逻辑 intuitionistic logic ·
克里普克模型 Kripke model · 续延 continuation · 依赖类型 dependent type · Π 类型 / Σ 类型 Pi / Sigma type · 线性 / 仿射
类型 linear / affine type · 所有权 ownership · 借用 borrowing · 代数数据类型 algebraic data type · 模式匹配 pattern
matching · 子类型 subtyping · 协变 / 逆变 / 不变 covariant / contravariant / invariant · 渐进类型 gradual typing · 精化类型
refinement type · 一价公理 univalence · 效应处理器 effect handler

## Sources

*Canon.* Books: Pierce, *Types and Programming Languages*; Harper, *Practical Foundations for Programming
Languages*; Barendregt, *The Lambda Calculus: Its Syntax and Semantics*; Hindley & Seldin, *Lambda-Calculus and
Combinators*; Sørensen & Urzyczyn, *Lectures on the Curry–Howard Isomorphism*; Girard, Lafont & Taylor, *Proofs and
Types*; Martin-Löf, *Intuitionistic Type Theory* (1984).

Papers: Church, "An unsolvable problem of elementary number theory" (1936); Church & Rosser, "Some properties of
conversion" (1936); Church, "A formulation of the simple theory of types" (1940); Curry & Feys, *Combinatory Logic*
(1958); Robinson, "A machine-oriented logic based on the resolution principle" (1965); Kripke, "Semantical analysis
of intuitionistic logic I" (1965); Tait, "Intensional interpretations of functionals of finite type I" (1967);
Hindley, "The principal type-scheme of an object in combinatory logic" (1969); Howard, "The formulae-as-types
notion of construction" (1969, published 1980); Wadsworth, *Semantics and Pragmatics of the Lambda-Calculus*
(1971); de Bruijn, "Lambda calculus notation with nameless dummies" (1972); Girard, *Interprétation fonctionnelle et
élimination des coupures* (1972); Reynolds, "Towards a theory of type structure" (1974) and "Types, abstraction and
parametric polymorphism" (1983); Milner, "A theory of type polymorphism in programming" (1978); Damas & Milner,
"Principal type-schemes for functional programs" (1982); Girard, "Linear logic" (1987); Coquand & Huet, "The
calculus of constructions" (1988); Wadler, "Theorems for free!" (1989); Mairson, "Deciding ML typability is complete
for deterministic exponential time" (1990); Kfoury, Tiuryn & Urzyczyn, "ML typability is DEXPTIME-complete" (1990);
Griffin, "A formulae-as-types notion of control" (1990); Rémy, "Extending ML type system with a sorted equational
theory" (1992); Wells, "Typability and type checking in the second-order λ-calculus are equivalent and undecidable"
(1994); Kfoury & Wells, "A direct algorithm for type inference in the rank-2 fragment" (1994).

*Recent.* McAllester, "A logical algorithm for ML type inference" (2003); Siek & Taha, "Gradual typing for
functional languages" (2006); Rondon, Kawaguchi & Jhala, "Liquid types" (2008); Plotkin & Pretnar, "Handlers of
algebraic effects" (2009); Hoare, "Null references: the billion dollar mistake" (2009); The Univalent Foundations
Program, *Homotopy Type Theory* (2013); Cohen, Coquand, Huber & Mörtberg, "Cubical type theory" (2015); Siek,
Vitousek, Cimini & Boyland, "Refined criteria for gradual typing" (2015); Takikawa et al., "Is sound gradual typing
dead?" (2016); Jung et al., "RustBelt: securing the foundations of the Rust programming language" (2018);
Sivaramakrishnan et al., "Retrofitting effect handlers onto OCaml" (2021); Wadler, "Propositions as types" (2015).
