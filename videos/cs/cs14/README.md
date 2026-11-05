# Computer Science, Built — Part 14: Lambda and Types

Part 14 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, *Speaking to the Machine*. Church's λ-calculus is a whole programming
language made of functions alone; types tame it; well-typed programs cannot go wrong, which we prove and check; a
type can be inferred without being written; and types turn out to be propositions and programs to be proofs. The
instruments are Part 1's `explainer/cs/lam.py` (terms, substitution, normal order) and `explainer/cs/lang/lam/`:
`reduce.py` (five strategies, an environment machine with thunks that counts sharing, the whole reduction graph,
complete developments, de Bruijn indices, the Church encodings), `stlc.py` (the simply typed calculus with booleans
and naturals: derivations, small-step evaluation, a random generator, the safety theorems checked), `ml.py` (the
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
  boxes; plus, times and pow (6, 9 and 16 steps); pairs; Kleene's predecessor (9 + 10n steps); lists as folds.
* **4. Recursion without names.** Fixed points; Y unfolding; factorial through Y (24 for n = 4, in 10,384 steps);
  Y diverges under call-by-value, Z does not; the recursion theorem previewed.
* **5. Evaluation strategies.** Normal, applicative, by name, by value, by need; K a Ω under each; sharing counted
  (43 against 33 β-steps when an argument is used three times); the standardization theorem.
* **6. Church–Rosser, and de Bruijn.** The full reduction graph of a small term (6 terms, 7 steps, one normal
  form) and a bigger one (30 terms, 93 steps, confluent); the diamond and parallel reduction; de Bruijn indices.
* **7. Simple types.** Stuck terms; Milner's slogan; the syntax and rules; a derivation tree drawn by our checker;
  a small-step trace with its rules.
* **8. Well-typed programs cannot go wrong.** Progress and preservation; the proofs' key cases (canonical forms,
  the substitution lemma); both checked on 5,000 random terms and 50,516 steps; safety in real languages.
* **9. Every typed program stops.** Ω is untypable (`'a = 'a -> 'b`); Tait's strong normalization and logical
  relations; 136 of 2,000 random untyped terms still running after 400 steps, none of 5,000 typed ones; the price,
  and `fix`.
* **10. Hindley–Milner inference.** Unification (Robinson 1965) and its occurs check; our engine's trace for
  `fun f x -> f (f x)`; let-polymorphism; the Job's eleven principal types; the nested-let worst case, 2^(2^n)
  leaves, DEXPTIME-complete.
* **11. Polymorphism and free theorems.** System F; Church's encodings typed; parametricity; the free theorem
  `map f ∘ g = g ∘ map f` tested on four polymorphic functions (200/200 each) and broken at once by a
  monomorphic one.
* **12. Propositions as types.** The dictionary; programs found by proof search (S, K, composition,
  `¬¬(A ∨ ¬A)`); excluded middle, double negation, Peirce and de Morgan's half with no program; a two-world Kripke
  model; call/cc and Peirce's law (Griffin 1990).
* **13. Dependent and linear types.** Vectors indexed by length; Π and Σ; Martin-Löf, Coq/Rocq, Lean; linear,
  affine and relevant combinators; rustc's E0382 and E0502.
* **14. Data, subtyping and gradual types.** Algebraic data types and `option`; variance; TypeScript's covariant
  arrays accepted by `tsc --strict` and failing in node; `any`; Siek and Taha's gradual typing and its cost.
* **15. Frontier: the edges of type theory.** Inference linear in practice (measured to 352 definitions);
  refinement types and SMT; homotopy type theory, univalence and cubical type theory; effect handlers; open
  problems.
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs14.compute           # every number in the part (under a minute)
python tools/build.py cs14 -q l            # a 480p preview
python tools/build.py cs14                 # 1080p
```

The `rust` and `gradual` items call `rustc` and `tsc`/`node` on this machine and record their versions; the
`frontier` timings belong to the computer that runs them. Everything else is exact.

## Problems, with solutions

1. **Two orders.** Reduce `(λx y. y x x) ((λz. z) a) (λw. w)` to normal form by normal order and by applicative
   order, count the steps, and explain the difference.

   *Solution.* Normal order (5 steps): substitute the unreduced argument `(λz. z) a` for x, giving
   `(λy. y A A) (λw. w)` with A = `(λz. z) a`; then `(λw. w) A A`, then `A A`, then reduce each copy of A: `a A`,
   `a a`. Applicative order (4 steps): reduce A to `a` first, then `(λx y. y x x) a` → `λy. y a a`, then apply it
   to the identity and reduce `(λw. w) a a` → `a a`. Normal order copied the argument before evaluating it, so it
   evaluated it twice; applicative order evaluated it once. Both reach the same normal form, as Church–Rosser
   promises. (Our reducer, `reduce.run`, gives 5 and 4.)

2. **More arithmetic.** Define exp, iszero and sub on Church numerals, and explain why `sub m n` takes time
   proportional to m · n.

   *Solution.* exp m n = n m (m to the n). iszero = λn. n (λz. false) true: applying "always false" zero times
   leaves true. sub = λm n. n pred m. Each pred on a numeral k rebuilds k pairs (Kleene's trick), costing about
   10k steps by our measurement, and sub applies pred n times to numbers no larger than m, so the cost is about
   10 m n: Church numerals are unary, and pred has to count all the way up each time.

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

5. **Build: data types in the λ-core.** Add `type` declarations with constructors and exhaustive `match`, with
   inference, and rewrite the Job's table with an `option`.

   *Solution.* Parse `type t = A of τ | B of τ * τ | C` into a table of constructors with their argument types and
   result type t (with parameters 'a for polymorphic types such as `'a option`). In inference, a constructor is a
   function from its arguments to t, instantiated freshly at each use; a `match` infers the scrutinee's type,
   unifies it with t, and types each branch with the constructor's fields bound; check exhaustiveness by
   comparing the constructors named with those declared and report the missing ones. In the evaluator a
   constructed value is a tagged tuple. For the Job, write `let rec find w table = match table with [] -> None |
   p :: rest -> if fst p = w then Some p else find w rest` and rebuild `bump` from it; inference gives
   `find : 'a -> ('a * 'b) list -> ('a * 'b) option`. Test against `job_reference` as `tests/test_cs14_types.py`
   does.

6. **★ Research: cheap sound gradual typing.** Design a sound gradual type system whose run-time checks cost a
   provably bounded factor, or show that some program mix must pay unboundedly.

   *Where to start.* Siek and Taha (2006) defined gradual typing and its consistency relation; Siek, Vitousek,
   Cimini and Boyland (2015) gave the refined criteria (the "gradual guarantee"). Takikawa et al., "Is sound
   gradual typing dead?" (POPL 2016), measured Typed Racket's lattice of partially typed configurations and found
   slowdowns beyond 100×; Bauman et al. (2017) and Kuhlenschmidt, Almahallawi and Siek's Grift (2019) cut them with
   space-efficient coercions and monotonic references; Greenman and Felleisen compare "natural", "transient" and
   "erasure" semantics. Open: (a) a bound on the cost of the natural semantics in terms of program structure;
   (b) a lower bound showing that wrapper chains must sometimes grow, for higher-order values crossing boundaries
   repeatedly; (c) a compilation scheme, measured on the λ-core with an `any` type, that meets it.

## 习题与解答

1. **两种顺序。** 分别用正规序和应用序把 `(λx y. y x x) ((λz. z) a) (λw. w)` 归约到范式，数出步数，并解释差别。

   *解答。* 正规序（5 步）：把尚未归约的实参 `(λz. z) a` 代入 x，得到 `(λy. y A A) (λw. w)`，其中 A = `(λz. z) a`；
   然后是 `(λw. w) A A`，再到 `A A`，再分别归约 A 的两个副本：`a A`、`a a`。应用序（4 步）：先把 A 归约成 `a`，
   然后 `(λx y. y x x) a` → `λy. y a a`，再作用于恒等函数，`(λw. w) a a` → `a a`。正规序在求值之前复制了实参，
   所以求值了两次；应用序只求值一次。两者到达同一个范式，正如丘奇–罗瑟定理所保证的。（我们的归约器
   `reduce.run` 给出 5 和 4。）

2. **更多的算术。** 在丘奇数上定义 exp、iszero 和 sub，并解释为什么 `sub m n` 的时间与 m · n 成正比。

   *解答。* exp m n = n m（m 的 n 次方）。iszero = λn. n (λz. false) true：把“总是 false”应用零次，留下 true。
   sub = λm n. n pred m。每次对数 k 求 pred 都要重建 k 个序对（克莱尼的技巧），按我们的测量约需 10k 步；sub 对不超过
   m 的数应用 n 次 pred，所以代价约为 10 m n：丘奇数是一进制的，pred 每次都得从头数上来。

3. **进展性的两个情形。** 证明 If 和 Succ 两种情形下的进展性，并写出所需的典范形式引理。

   *解答。* 典范形式：Bool 类型的值是 true 或 false；Nat 类型的值是 0 或 succ v（v 是数值）；A → B 类型的值是一个
   λ。If 情形：⊢ if c a b : T 需要 ⊢ c : Bool。由归纳假设，c 是值或能走一步。若能走一步，E-If 使整个项走一步。若是
   值，由典范形式它是 true 或 false，于是 E-IfTrue 或 E-IfFalse 适用。Succ 情形：⊢ succ t : Nat 需要 ⊢ t : Nat。
   若 t 能走一步，succ t 也能（E-Succ）；若 t 是值，由典范形式它是数值，于是 succ t 本身就是值。

4. **手工推断。** 推断 `λf g x. g (f x) x` 的主类型，写出每一次合一。

   *解答。* 设 f : α，g : β，x : γ。`f x` 迫使 α = γ → δ。`g (f x)` 迫使 β = δ → ε。`(g (f x)) x` 迫使
   ε = γ → ζ。代入后：f : γ → δ，g : δ → γ → ζ，x : γ，结果为 ζ。改名之后，主类型是
   `('a -> 'b) -> ('b -> 'a -> 'c) -> 'a -> 'c`，与我们的引擎报告的完全一致，三次绑定的顺序也相同。

5. **动手：λ-核心中的数据类型。** 加上带构造子的 `type` 声明和穷尽的 `match`，并支持推断；用 `option` 改写任务的表。

   *解答。* 把 `type t = A of τ | B of τ * τ | C` 解析成一张构造子表，记下各自的参数类型和结果类型 t（像 `'a option`
   这样的多态类型带参数 'a）。推断时，构造子是从其参数到 t 的函数，每次使用都重新实例化；`match` 先推断被匹配值的
   类型，与 t 合一，再在绑定好字段的情况下给每个分支定型；把出现过的构造子与声明的比较，报告遗漏的那些，以检查
   穷尽性。在求值器里，构造出来的值是一个带标签的元组。对任务，写出 `let rec find w table = match table with [] ->
   None | p :: rest -> if fst p = w then Some p else find w rest`，并用它重写 `bump`；推断给出
   `find : 'a -> ('a * 'b) list -> ('a * 'b) option`。像 `tests/test_cs14_types.py` 那样对照 `job_reference` 测试。

6. **★ 研究：廉价的可靠渐进类型。** 设计一个可靠的渐进类型系统，其运行时检查的代价有可证明的常数上界；或者证明
   某些程序组合必须付出无界的代价。

   *从哪里开始。* 西克与塔哈（2006）定义了渐进类型及其一致性关系；西克、维图塞克、奇米尼与博伊兰（2015）给出了
   细化的判据（“渐进保证”）。高川等人的《Is sound gradual typing dead?》（POPL 2016）测量了 Typed Racket 部分定型
   配置构成的格，发现了超过 100 倍的减速；鲍曼等（2017）以及库伦施密特、阿尔马哈拉维与西克的 Grift（2019）用空间
   高效的强制和单调引用把它降了下来；格林曼与费莱森比较了 “natural”、“transient” 和 “erasure” 三种语义。尚未解决
   的：（a）用程序结构给出 natural 语义代价的上界；（b）一个下界，证明当高阶值反复穿过边界时，包装链有时必然增长；
   （c）一种编译方案，在带 `any` 类型的 λ-核心上测量，达到这个上界。

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
