# Computer Science, Built — Part 58: Semantics

Part 58 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act XI, *The Research Frontier*. What does a program mean? Part 14
gave programs types; this part gives them meaning, three ways: as the steps a machine takes, as the mathematical
object a program denotes, and as the laws it obeys. One small language with recursion is given three interpreters
that must agree, a denotation in which recursion is a least fixed point, and proofs that the two meanings coincide;
then the same ideas decide when two programs are the same, read theorems off types, prove Hoare logic sound, and
stretch to effects, dependent types and communicating processes.

The instruments are in `explainer/cs/semantics/` (tested in `tests/test_cs58_semantics.py`):
* `meaning.py`: a PCF-like call-by-value language (integers, booleans, variables, functions, application,
  conditionals, `+ − × < =`, and `fix f x -> e`) with three operational semantics that must agree: a small-step
  interpreter by substitution (left to right), a big-step evaluator with environments and closures, and a CEK machine
  with an explicit continuation stack; a generator of closed, terminating random programs and the agreement
  experiment (300 programs); the small-step trace of `fact 3`; the Kleene chain of the factorial functional on inputs
  0 to 7; normalization by evaluation for the untyped λ-calculus in de Bruijn form (Python closures as the semantic
  domain, then read-back) against normal-order β-reduction on Church numerals; free theorems checked by property tests
  (2,000 random lists per rearrangement) with the counterexample for sort under a non-monotone map; strong
  bisimilarity by naive partition refinement, and trace sets to depth 3; one program run in the Maybe, State and List
  monads. (The scenes' illustrative pieces, such as the CEK run of `(fun x -> x + 1) 2`, the big-step tree, the
  factorial loop's states, the algebraic-effects handlers and the deadlock grid, whose states are enumerated by hand,
  are drawn inline.)

## Chapters

* **Hook.** Three meanings of factorial: as steps (our small-step interpreter rewrites `fact 3` in 18 steps, down to
  6), as a limit (the Kleene chain ⊥ ⊑ F(⊥) ⊑ F²(⊥) ⊑ ⋯) and as laws (equations and a Hoare triple). Why meaning
  matters: compiler correctness (CompCert, Part 54), refactoring (no context can tell old from new), language design
  (WebAssembly's formal specification). Our three interpreters agree on 300 of 300 random programs. The plan.
* **1. Meaning as steps.** The language and its values; factorial written with `fix`. Plotkin's structural
  operational semantics (1981): search rules (Op-L, Op-R, App-L, App-R) and reduction rules (Op, If-T, If-F, Beta,
  Fix), call by value, left to right. One step as a theorem: the derivation of 3 × fact (3 − 1) → 3 × fact 2 (Op-R,
  App-R, Op); determinism, by induction on derivations. The run of `fact 3`: the term grows as multiplications pile up
  (Part 11's call stack written into the term), then collapses to 6 after 18 steps. Kahn's natural semantics (1987):
  the derivation of (fun x → x × x)(1 + 2) ⇓ 9; e ⇓ v iff e →* v; our big-step evaluator agrees with the small-step
  interpreter on 300 of 300 random programs. The CEK machine (Felleisen and Friedman 1986): an illustrative run of
  `(fun x -> x + 1) 2` in eleven configurations; a mean of 294.4 CEK transitions per random program against 72.9 small
  steps, each transition constant work while each small step searches and copies the whole term; the interpreter loop
  of Part 15, derived from the rules.
* **2. Meaning as mathematics.** Scott and Strachey (1971): `fun x -> x * x` and `fun x -> x * x + 0` denote the same
  squaring function, a set of pairs. One equation per construct, with an environment ρ and ⊥ for a term that never
  finishes; compositionality, meanings flowing up the tree of (1 + 2) × x to 12 at x = 4. The meaning of
  (fun x → x × x)(1 + 2) computed by algebra alone: 9, the big-step tree's answer. Contexts: equal meanings stay equal
  in every context, which licenses Part 13's optimizer to rewrite x × x + 0 to x × x. Recursion as an equation
  g = F(g); for factorial two fixed points, one undefined on the negative numbers and one 0 there; `fact (-1)` never
  stops, so the meaning is the least defined solution.
* **3. Domains and fixed points.** Ordering by information: ℤ⊥ flat; partial functions pointwise (f ⊑ g, but f ⋢ h
  when h changes an answer). Complete partial orders: a least element, and least upper bounds of chains. Monotone and
  continuous functions; H (1 on total functions, ⊥ otherwise) is monotone but not continuous: ⊔ H(g_k) = ⊥ along the
  partial factorials, yet H(⊔ g_k) = 1, and H would decide totality, a cousin of Part 25's halting problem. Kleene's
  fixed-point theorem, proved in three steps (a chain; a fixed point, by continuity; the least, by induction), with
  Part 13's liveness analysis as the finite case. The Kleene chain of factorial computed: F^k(⊥) is defined on
  0, …, k − 1, rows k = 0 to 7 reaching 1, 1, 2, 6, 24, 120, 720; the limit is factorial on ℕ, still undefined on
  negative numbers; a while loop's meaning the same way. Scott's D∞ (1969): D ≅ [D → D] is impossible for all set
  functions (Cantor), possible for continuous ones, as the limit of D₀, D₁ = [D₀ → D₀], ….
* **4. Adequacy and full abstraction.** Two meanings of `fact 3`, both 6. Soundness (e →* v ⇒ ⟦e⟧ = ⟦v⟧) and
  adequacy (⟦e⟧ = n ⇒ e →* n, for closed integer programs), proved by Plotkin for PCF (1977). Soundness of Beta by a
  substitution lemma, of Fix by the fixed-point equation. Adequacy fails by naive induction at an application, so a
  logical relation, a ladder of types (simplified after Winskel's proof for an eager language); the fundamental lemma,
  with `fix` handled through the Kleene chain (shown on inputs 0 to 4) and admissibility; at type int it is adequacy.
  Contextual equivalence; full abstraction fails for PCF: parallel-or is continuous but no sequential program
  computes it, so two tests that differ only on parallel-or are contextually equivalent with different meanings;
  adding parallel-or makes Scott's model fully abstract. Game semantics (Abramsky, Jagadeesan and Malacaria; Hyland
  and Ong; Nickau, in the 1990s): the strategy of `not` in four moves, sequentiality built in.
* **5. When are two programs the same?** `fun x -> x + x` against `fun x -> 2 * x` in three contexts (10, 7 and 4 for
  both), out of infinitely many. a.(b + c) against a.b + a.c: the same traces {ε, a, ab, ac}, but the attacker wins
  the bisimulation game, and the Hennessy–Milner formula ⟨a⟩(⟨b⟩true ∧ ⟨c⟩true) tells them apart. Park's
  bisimulation (1981) as the greatest fixed point of a monotone F (Knaster–Tarski), and coinduction. Two vending
  machines proved bisimilar by exhibiting R = {(V₁, W₁), (V₂, W₂), (V₁, W₃)} and checking one step; our partition
  refinement finds 2 blocks after 2 rounds (V₁ ∼ W₁) for them and 6 blocks after 3 rounds (P ≁ Q) for the pair above.
  Applicative bisimulation (Abramsky 1990), relating the two doubling functions; Howe's method makes it a congruence.
  Logical relations between programs: the fundamental property gives contextual equivalence with no context examined;
  with `fix`, admissibility or step-indexing (Appel and McAllester 2001). Tait's reducibility (1967), and normalization
  by evaluation (Berger and Schwichtenberg 1991): our NbE and normal-order reduction reach the same normal form on
  2 + 3, 2 × 3, 3 × 4, 2³ and 3³ (5, 6, 12, 8, 27; normal order takes 6, 7, 9, 16 and 28 β-steps).
* **6. Theorems for free.** Reynolds's two counters (one counts up; the other counts down and reads its state negated)
  related by m = −n; the abstraction theorem (1983) and "type structure is a syntactic discipline for enforcing levels
  of abstraction". Every type read as a relation (Int, →, lists, ∀). The free theorem for r : ∀a. [a] → [a] derived:
  map f ∘ r = r ∘ map f. The square for reverse and squaring; reverse, take 3, every other and rotate each held on
  100% of random lists with random f(x) = ax² + b (Part 14 tested linear f only). Wadler (1989): sort commutes with
  map f when f preserves and reflects the order; f(x) = 2x + 1 held on 100% of random lists; for g(x) = x² our test
  found [−6, −15, 18, 3, −2, 14, 7], where sorting then squaring gives [225, 36, 4, 9, 49, 196, 324] and squaring
  then sorting gives [4, 9, 36, 49, 196, 225, 324] (−15 < −6 but 225 > 36). Where the theorem bends (a Java identity
  with `instanceof`; general recursion, which needs f strict; Haskell's `seq`) and where it pays (foldr/build fusion
  in GHC, Gill, Launchbury and Peyton Jones 1993; representation independence).
* **7. Hoare logic, proved sound.** Derivable (⊢, a derivation such as the Seq tree for
  {x > 4} x := x + 1; y := x {y > 5}) against true (⊨, every run from P that ends, ends in Q); soundness, and Cook's
  relative completeness (1978). Big-step rules for commands, with the loop in its own premise. Soundness by induction
  on the derivation: assignment through a substitution lemma, then Seq and Consequence. The while case: factorial as
  a loop with invariant x ≥ 0 ∧ y · x! = 3!, run from x = 3 through (x, y) = (3, 1), (2, 3), (1, 6), (0, 6), leaving
  with y = 6; an inner induction on the run's derivation. The same proof against the denotation: the loop as fix Φ,
  safety closed under limits of chains, Scott's fixed-point induction (the loop's iterates from y = 1 end in the
  numbers of chapter three's chain). Cook's proof through the weakest liberal precondition; why only relative:
  {true} skip {P} holds iff P is true, and by Gödel (1931) no proof system lists every true statement of arithmetic.
  Part 54's tools discharge exactly those assertions.
* **8. Effects and monads.** Moggi (1989, 1991): a computation of an integer means an element of T ℤ; failure
  (ℤ + {err}), state (S → ℤ × S) and choice (List ℤ). Return and bind as plumbing; a `do` block is bind (Wadler
  1992). One program in three monads: Maybe gives Nothing, Just 5 and Just 4 for b = 0, 3 and 4; State (tick twice
  from 0, return ten times the counter) gives (20, 2); List (b from 1 to 4) gives [12, 6, 4, 3]. The three monad laws,
  the left unit checked for State by algebra; Kleisli composition, a category with return as identity; Moggi's `let`
  as bind. Algebraic effects (Plotkin and Power 2001) and handlers (Plotkin and Pretnar 2009): `if choose () then 6
  else if choose () then 4 else fail ()` as a tree, run by a handler that collects every result ([6, 4]) and by one
  that backtracks (6); OCaml 5, Koka and Eff.
* **9. Dependent types.** Π and Σ as columns over A, becoming → and × when B does not depend on x; Martin-Löf's type
  theory (from 1972). Vec A n: nil, cons, head on Vec A (n + 1), append; [7, 2] appended to [5] has type
  Vec ℕ (2 + 1), which the checker computes to Vec ℕ 3; `head nil` is rejected before the program runs.
  Propositions as types extended (Part 14): ∀ as Π, ∃ as Σ, equality as a type made by refl; Π(n:ℕ). Σ(m:ℕ). n < m
  proved by the program λn. (n + 1, lt_succ n). 2 + 2 = 4 proved by refl, because 2 + 2 computes to 4 in four lines;
  n + 0 = n does not compute and is proved by a recursive function: induction is recursion. Why every program must
  terminate: type equality by normalization, and `bad = bad` would prove False; structural recursion; normalization by
  Tait's method, extended to polymorphism by Girard (1972); intensional equality keeps checking decidable, Martin-Löf's
  extensional theory (1984) does not. A proof assistant's kernel: the calculus of constructions (Coquand and Huet
  1988) at the core of Coq; tactics and the elaborator untrusted, the kernel trusted.
* **10. Processes and channels.** CCS (Milner 1980): actions a, ā, τ; 0, α.P, P + Q, P | Q, (νa)P and named
  processes; a customer coin‾.tea.0 and a machine coin.tea‾.V, joined and restricted; Hoare's CSP (1978) and Go's
  channels. The rules Act, Sum, Par, Com and Res; the first τ step derived; the closed system takes two τ steps and
  stops, and is weakly bisimilar to 0; strong bisimilarity is preserved by every CCS operator. The π-calculus (Milner,
  Parrow and Walker 1992): names sent over names, and scope extrusion of a private channel. Deadlock: two threads
  taking two locks (Part 33) in opposite orders, as CCS processes; the state grid (enumerated by hand) has 19
  reachable states, 22 τ steps and 2 states with no move, the finish and the deadlock; finding one is a search, as in
  Part 54's model checker; session types (Part 43).
* **11. Frontier: semantics of real languages.** Mechanized semantics at full size: CompCert's C (Leroy 2009),
  CakeML (Kumar et al. 2014), WebAssembly's small-step specification and its type soundness in Isabelle (Haas et al.
  2017; Watt 2018); still missing, C's concurrency (Part 33's out-of-thin-air problem) and most languages people
  write. Equality rethought: proofs of equality as values, Voevodsky's univalence, equalities as paths; homotopy type
  theory (the HoTT book, 2013), and cubical type theory, in which univalence computes. Four open problems and the ★
  research problem.
* **Outro.** Recap, payoffs (Parts 59, 60 and 61; back to Parts 54 and 55), practice, problems, next part (Part 59,
  Distributed Computing Theory).

## Build

```bash
python -m videos.cs.cs58.compute
python -m unittest tests.test_cs58_semantics
python tools/build.py cs58
```

## Problems, with solutions

1. **Determinism.** Prove that small-step evaluation is deterministic for our language.

   *Solution.* The rules are the search rules Op-L, Op-R, App-L, App-R and the one that steps the condition of an
   `if`, and the reduction rules Op, If-T, If-F, Beta and Fix. First, values never step: every rule's left-hand side
   is an operation, an application or a conditional, and n, b, fun x → e and fix f x → e are none of these. We prove,
   by induction on the derivation of e → e₁, that e → e₂ implies e₁ = e₂. Take e = e′ ⊕ e″. If e′ is not a value,
   only Op-L can apply (Op-R and Op need e′ to be a value), so both derivations end in Op-L, with premises e′ → e′₁
   and e′ → e′₂, and the induction hypothesis gives e′₁ = e′₂. If e′ is a value and e″ is not, Op-L is excluded
   because values do not step and Op needs e″ to be a value, so only Op-R applies, and induction again. If both are
   values, neither search rule applies, and Op gives the one number n₁ ⊕ n₂ (or nothing, if they are not numbers: the
   term is stuck). An application is the same, with App-L, App-R and then Beta or Fix, chosen by the shape of the
   function value; substitution is a function, so the result is unique. A conditional steps its condition when that
   is not a value, and otherwise If-T or If-F, by whether it is true or false. So at most one rule fits any term, and
   its premise is unique by induction. Hence a run is a line, not a tree, and the value v with e →* v, if there is
   one, is unique: `step` in `meaning.py` can be a function for exactly this reason, and the 18-step trace of
   `fact 3` is the only run there is.

2. **Kleene's chain.** Show that the factorial functional is continuous, and that its least fixed point is factorial.

   *Solution.* F takes a partial function h : ℤ ⇀ ℤ to F(h)(0) = 1, F(h)(n) = n · h(n − 1) for n ≠ 0 when h(n − 1) is
   defined, and undefined otherwise. Partial functions ordered by extension (h ⊑ h′ if h′ is defined wherever h is,
   and agrees) form a cpo: the least element ⊥ is the empty function, and a chain h₀ ⊑ h₁ ⊑ ⋯ has as least upper
   bound the union of the graphs, a function because members of a chain agree wherever both are defined. F is
   monotone: if h ⊑ h′ and F(h)(n) is defined, then either n = 0, and both give 1, or h(n − 1) is defined, so
   h′(n − 1) = h(n − 1) and F(h′)(n) = F(h)(n). F is continuous: ⊔ₖ F(hₖ) ⊑ F(⊔ₖ hₖ) by monotonicity; conversely, if
   F(⊔ₖ hₖ)(n) is defined, it consulted ⊔ₖ hₖ at the single point n − 1 (or not at all), which is already defined in
   some hₖ, so F(hₖ)(n) is defined with the same value. (F reads a finite part of its input, which is what continuity
   asks.) By Kleene's theorem the least fixed point is ⊔ₖ F^k(⊥). By induction on k, F^k(⊥) is defined exactly on
   {0, …, k − 1}, with value n! there: true for k = 0; F(F^k(⊥))(0) = 1; for n ≥ 1 it is defined iff
   n − 1 ∈ {0, …, k − 1}, that is n ∈ {1, …, k}, with value n · (n − 1)! = n!; and for n < 0, n − 1 is negative and
   never defined. (Our instrument's chain shows k = 0 to 7, ending 1, 1, 2, 6, 24, 120, 720.) The union is n ↦ n! on
   ℕ, undefined on the negative numbers, where the program indeed recurses forever. Least matters: the function that
   is 0 on the negative numbers is also a fixed point, and Kleene's theorem places every fixed point above each
   F^k(⊥), so above their union.

3. **Same traces, not bisimilar.** Show that a.(b + c) and a.b + a.c have the same traces but are not bisimilar, with
   a distinguishing formula.

   *Solution.* As transition systems: P →a P₁, P₁ →b P₂, P₁ →c P₃; and Q →a Q₁ →b Q₃, Q →a Q₂ →c Q₄. Both have the
   traces {ε, a, ab, ac}: Q reaches ab through Q₁ and ac through Q₂. Suppose R is a bisimulation with P R Q. The move
   P →a P₁ must be matched by Q →a Q₁ or Q →a Q₂ with P₁ R Qᵢ. If Q₁, then P₁ →c P₃ must be matched, and Q₁ has no
   c; if Q₂, then P₁ →b P₂ must be matched, and Q₂ has no b. Either way R fails, so P ≁ Q. The formula
   φ = ⟨a⟩(⟨b⟩true ∧ ⟨c⟩true) says "can do a and then both b and c": P ⊨ φ through P₁, and Q ⊭ φ, since
   Q₁ ⊭ ⟨c⟩true and Q₂ ⊭ ⟨b⟩true. (By the Hennessy–Milner theorem, image-finite states are bisimilar exactly when
   they satisfy the same formulas, so a non-bisimilar finite pair always has such a formula.) Our partition
   refinement shows the same thing: the first round splits states by the actions they can do, {P, Q}, {P₁}, {Q₁},
   {Q₂} and the four end states; the second separates P from Q, because P's a leads into P₁'s block and Q's into Q₁'s
   and Q₂'s; the third changes nothing: 6 blocks after 3 rounds, with P and Q apart. Read a as a coin and b and c as
   tea and coffee: Q chooses your drink when it takes the coin.

4. **A free theorem.** Derive the free theorem for r : ∀a. [a] → [a].

   *Solution.* Read types as relations: at Int, equality; f ⟦A → B⟧ g iff x ⟦A⟧ y implies f x ⟦B⟧ g y; xs ⟦[A]⟧ ys
   iff the lists have the same length and are related element by element; t ⟦∀α. A⟧ t′ iff for all types X, X′ and
   every relation R between them, the instances t_X and t′_X′ are related at A with α read as R. Reynolds's
   abstraction theorem says that every closed term is related to itself at its type. For r this gives: for all A, B
   and R ⊆ A × B, if xs [R] ys then r_A xs [R] r_B ys. Now choose R to be the graph of a function f : A → B, a R b iff
   f a = b; then xs [R] ys says exactly map f xs = ys. Take ys = map f xs: the conclusion is
   map f (r_A xs) = r_B (map f xs), for every f, that is map f ∘ r = r ∘ map f. For example reverse [1, 2, 3] squared
   is [9, 4, 1], and [1, 4, 9] reversed is [9, 4, 1]. A corollary shows how little r can do: for xs of length n, let
   f i be the i-th element of xs, so that map f [0, …, n − 1] = xs; then r xs = map f (r [0, …, n − 1]): r can only
   select, drop, repeat and reorder positions, in a way that depends on the length alone. The proof assumes a total,
   pure language: with general recursion every type contains ⊥ and the theorem needs f strict (Wadler 1989); `seq`
   and run-time type tests weaken or break it. Our property test found no exception: reverse, take 3, every other and
   rotate each held on 100% of 2,000 random lists, with random f(x) = ax² + b, neither monotone nor one-to-one.

5. **Build.** Add exceptions to our interpreters, and check the three still agree on random programs.

   *Solution notes.* Add two terms to `meaning.py`: `("raise", e)`, which raises the integer value of e, and
   `("try", e, x, h)`, which runs e and, if it raises v, runs h with x bound to v; extend `show` and `subst` (the
   handler binds x, so substitution stops there, as at `lam`). Small step: a raised value is a final answer but not a
   value, so add `is_final`, and let `small` stop on either. Add propagation rules, one frame per step: when the
   subterm a search rule would step is `("raise", v)` with v a value, the whole frame becomes `("raise", v)`, in both
   positions of an operation and of an application, in the condition of an `if`, and inside another `raise`; then
   `try v ...` → v, and `try (raise v) with x -> h` → h[v/x], with a search rule stepping the body. Big step: return
   tagged results, `("ok", v)` or `("exn", n)`, and propagate the first `exn` premise in each rule, left to right;
   this is chapter 8's exceptions monad, with bind in every rule. (A Python exception class carrying n is the shorter
   alternative.) CEK: push a frame `("try", x, h, E)` when entering a `try` and pop it when a value returns through it;
   on a raised value, pop frames until a `try` frame and continue with h in its environment extended by x, or return
   `("exn", n)` if the stack empties. Extend `_val` so that an uncaught exception compares as `("exn", n)`. In
   `random_program`, generate `raise` with a small probability, often under a conditional (`if e < k then raise n
   else e`) so that only some runs raise, and wrap some subterms in `try`; termination is unaffected, since raising only
   ends a computation early. Then run `agreement()` on 300 programs and add a test beside
   `test_three_semantics_agree` that also requires raising and non-raising programs both to occur. Agreement now tests
   the order of evaluation as well as the values: in `(raise 1) + (raise 2)` all three must raise 1, so a big-step rule
   that evaluated the right operand first would be caught. The determinism proof of Problem 1 extends,
   because the propagation rules also fire only when everything to their left is a value.

6. **★ Research.** A relaxed-memory semantics for C without out-of-thin-air values.

   *Discussion.* Open. The C and C++ memory model, formalized by Batty et al. (2011), allows relaxed atomic loads to
   return values that justify themselves in a cycle: with x = y = 0 initially, thread 1 runs r1 = x; y = r1 and thread
   2 runs r2 = y; x = r2, and the formal model does not forbid r1 = r2 = 42, although no known hardware or compiler
   produces it. The standard only recommends that implementations avoid such values. The obvious fixes each lose
   something. Forbidding cycles in program order together with reads-from (the choice of RC11, Lahav et al. 2017) rules out the
   42, but also the outcome r1 = r2 = 1 of the same test without the dependency (each thread writes 1 instead of its
   register), which the ARM and Power architectures allow, so compiled relaxed loads must then be followed by a fence
   or a false dependency. Forbidding only cycles through dependencies fails because dependencies are not syntactic:
   compilers delete them (`if (r1 == 1) y = 1; else y = 1;` becomes `y = 1`), so a syntactic rule forbids valid
   optimizations. Operational models such as the promising semantics (Kang et al. 2017) and event-structure models
   take other routes, but no model has yet been accepted that forbids thin-air values, permits the optimizations
   compilers perform and compiles efficiently to the main processors, with all three proved. A good partial answer
   would fix a fragment (only relaxed and release/acquire accesses, say, or no read-modify-writes), give a model for
   it, and prove, preferably mechanically, that it forbids the standard thin-air litmus tests, validates a stated list
   of compiler transformations, and maps to x86, ARMv8 and Power without extra fences; or prove that no model in a
   natural class can have all three properties.

## 习题与解答

1. **确定性。** 证明我们的语言的小步求值是确定的。

   *解答。* 规则包括搜索规则 Op-L、Op-R、App-L、App-R 和对 `if` 的条件走一步的那条规则，以及归约规则 Op、If-T、If-F、
   Beta 和 Fix。首先，值不会走步：每条规则的左边都是一个运算、一个应用或一个条件式，而 n、b、fun x → e 和 fix f x → e
   都不是。我们对 e → e₁ 的推导作归纳，证明 e → e₂ 蕴含 e₁ = e₂。取 e = e′ ⊕ e″。若 e′ 不是值，只有 Op-L 适用（Op-R 和
   Op 都要求 e′ 是值），所以两个推导都以 Op-L 结尾，前提分别是 e′ → e′₁ 和 e′ → e′₂，由归纳假设 e′₁ = e′₂。若 e′ 是值而
   e″ 不是，Op-L 被排除（值不走步），Op 要求 e″ 是值，所以只有 Op-R 适用，再用归纳。若两者都是值，两条搜索规则都不适用，
   Op 给出唯一的数 n₁ ⊕ n₂（如果它们不是数，就什么也不给：这个项卡住了）。应用的情形相同：App-L、App-R，然后按函数值的
   形状选 Beta 或 Fix；代换是一个函数，所以结果唯一。条件式在条件不是值时对条件走一步，否则按条件为真或假用 If-T 或 If-F。
   所以任何项至多有一条规则适用，而它的前提由归纳也是唯一的。因此一次运行是一条线而不是一棵树，满足 e →* v 的值 v
   （若存在）是唯一的：`meaning.py` 里的 `step` 能写成一个函数正是因为这一点，`fact 3` 的 18 步轨迹也是唯一的运行。

2. **克莱尼链。** 证明阶乘泛函是连续的，并且它的最小不动点就是阶乘。

   *解答。* F 把部分函数 h : ℤ ⇀ ℤ 映到 F(h)(0) = 1；当 n ≠ 0 且 h(n − 1) 有定义时 F(h)(n) = n · h(n − 1)；否则无定义。
   部分函数按延拓排序（h′ 在 h 有定义处都有定义且与之一致时 h ⊑ h′），构成一个完全偏序：最小元 ⊥ 是空函数，链
   h₀ ⊑ h₁ ⊑ ⋯ 的最小上界是各图像之并，它是一个函数，因为链中的成员在都有定义处一致。F 是单调的：若 h ⊑ h′ 且 F(h)(n)
   有定义，则要么 n = 0，两边都是 1；要么 h(n − 1) 有定义，于是 h′(n − 1) = h(n − 1)，F(h′)(n) = F(h)(n)。F 是连续的：
   由单调性 ⊔ₖ F(hₖ) ⊑ F(⊔ₖ hₖ)；反过来，若 F(⊔ₖ hₖ)(n) 有定义，它只在一个点 n − 1 上查看了 ⊔ₖ hₖ（或者根本没看），这个点
   已经在某个 hₖ 中有定义，所以 F(hₖ)(n) 有定义且值相同。（F 只读取输入的有限部分，这正是连续性的要求。）由克莱尼定理，
   最小不动点是 ⊔ₖ F^k(⊥)。对 k 归纳：F^k(⊥) 恰好在 {0, …, k − 1} 上有定义，值为 n!。k = 0 时成立；F(F^k(⊥))(0) = 1；
   n ≥ 1 时它有定义当且仅当 n − 1 ∈ {0, …, k − 1}，即 n ∈ {1, …, k}，值为 n · (n − 1)! = n!；n < 0 时 n − 1 为负，永远
   无定义。（我们的仪器算出的链从 k = 0 到 7，最后是 1、1、2、6、24、120、720。）它们的并是 ℕ 上的 n ↦ n!，在负数上无
   定义，而程序在那里确实永远递归下去。“最小”很要紧：在负数上取 0 的函数也是不动点，而克莱尼定理把每个不动点都放在每个
   F^k(⊥) 之上，因而在它们的并之上。

3. **迹相同，却不互模拟。** 证明 a.(b + c) 与 a.b + a.c 有相同的迹，却不互模拟，并给出一个区分它们的公式。

   *解答。* 写成迁移系统：P →a P₁，P₁ →b P₂，P₁ →c P₃；Q →a Q₁ →b Q₃，Q →a Q₂ →c Q₄。两者的迹都是 {ε, a, ab, ac}：
   Q 经 Q₁ 得到 ab，经 Q₂ 得到 ac。假设 R 是一个互模拟且 P R Q。动作 P →a P₁ 必须由 Q →a Q₁ 或 Q →a Q₂ 匹配，并且
   P₁ R Qᵢ。若是 Q₁，则 P₁ →c P₃ 必须被匹配，而 Q₁ 没有 c；若是 Q₂，则 P₁ →b P₂ 必须被匹配，而 Q₂ 没有 b。两种情况
   R 都不成立，所以 P ≁ Q。公式 φ = ⟨a⟩(⟨b⟩true ∧ ⟨c⟩true) 说的是“能做 a，然后 b 和 c 都能做”：P 经 P₁ 满足 φ，Q 不满足
   φ，因为 Q₁ ⊭ ⟨c⟩true，Q₂ ⊭ ⟨b⟩true。（由亨尼西–米尔纳定理，像有限的状态互模拟当且仅当它们满足相同的公式，所以不互模拟
   的有限对总有这样的公式。）我们的划分细化给出同样的结论：第一轮按能做的动作把状态分开，得到 {P, Q}、{P₁}、{Q₁}、{Q₂}
   和四个终止状态；第二轮把 P 和 Q 分开，因为 P 的 a 通向 P₁ 所在的块，而 Q 的 a 通向 Q₁ 和 Q₂ 的块；第三轮没有变化：
   3 轮之后 6 个块，P 与 Q 分处两块。把 a 读作投币，b、c 读作茶和咖啡：Q 在收下硬币时就替你选好了饮料。

4. **一条免费定理。** 推导 r : ∀a. [a] → [a] 的免费定理。

   *解答。* 把类型读作关系：Int 上是相等；f ⟦A → B⟧ g 当且仅当 x ⟦A⟧ y 蕴含 f x ⟦B⟧ g y；xs ⟦[A]⟧ ys 当且仅当两个列表
   长度相同且逐个元素相关；t ⟦∀α. A⟧ t′ 当且仅当对任意类型 X、X′ 和它们之间的任意关系 R，实例 t_X 与 t′_X′ 在把 α 读作
   R 的 A 上相关。雷诺兹的抽象定理说：每个闭项在它自己的类型上与自身相关。对 r 而言：对任意 A、B 和 R ⊆ A × B，若
   xs [R] ys，则 r_A xs [R] r_B ys。现在取 R 为函数 f : A → B 的图像，a R b 当且仅当 f a = b；于是 xs [R] ys 恰好是
   map f xs = ys。取 ys = map f xs，结论就是 map f (r_A xs) = r_B (map f xs)，对每个 f 都成立，即
   map f ∘ r = r ∘ map f。例如 reverse [1, 2, 3] 再平方是 [9, 4, 1]，[1, 4, 9] 再反转也是 [9, 4, 1]。一个推论说明 r 能做
   的事有多少：对长度为 n 的 xs，令 f i 为 xs 的第 i 个元素，则 map f [0, …, n − 1] = xs，于是
   r xs = map f (r [0, …, n − 1])：r 只能挑选、丢弃、重复和重排位置，而且方式只取决于长度。这个证明假定语言是全的、纯的：
   有一般递归时每个类型都含 ⊥，定理需要 f 是严格的（Wadler 1989）；`seq` 和运行时类型测试会削弱乃至破坏它。我们的性质
   测试没有发现例外：reverse、take 3、隔一取一和轮转在各 2,000 个随机列表上都 100% 成立，f(x) = ax² + b 随机选取，
   既不单调也不是一一的。

5. **动手。** 给我们的解释器加上异常，并检查三者在随机程序上仍然一致。

   *解答要点。* 在 `meaning.py` 里加两种项：`("raise", e)` 抛出 e 的整数值；`("try", e, x, h)` 运行 e，若它抛出 v，就在
   x 绑定为 v 的情况下运行 h。扩展 `show` 和 `subst`（处理器绑定 x，所以代换在那里停下，和 `lam` 一样）。小步：被抛出的
   值是最终答案但不是值，所以加一个 `is_final`，让 `small` 在两者之一时停下。加上传播规则，每步一层：当搜索规则要走一步的
   子项是 `("raise", v)` 且 v 是值时，整个外层变成 `("raise", v)`；这适用于运算和应用的两个位置、`if` 的条件，以及另一个
   `raise` 的内部；然后 `try v ...` → v，`try (raise v) with x -> h` → h[v/x]，并有一条搜索规则对主体走一步。大步：返回带标签
   的结果 `("ok", v)` 或 `("exn", n)`，每条规则从左到右把第一个 `exn` 前提传播出去；这就是第 8 章的异常单子，每条规则里都
   有一次 bind。（用一个携带 n 的 Python 异常类是更短的写法。）CEK：进入 `try` 时压入帧 `("try", x, h, E)`，值经过它返回时
   弹出；遇到被抛出的值时，一直弹帧直到 `try` 帧，在它的环境加上 x 后继续运行 h；若栈空了，就返回 `("exn", n)`。扩展
   `_val`，使未捕获的异常比较为 `("exn", n)`。在 `random_program` 中以小概率生成 `raise`，常常放在条件式下
   （`if e < k then raise n else e`），使只有一部分运行会抛出，并把一些子项包进 `try`；终止性不受影响，因为抛出只会让计算
   提前结束。然后在 300 个程序上运行 `agreement()`，并在 `test_three_semantics_agree` 旁加一个测试，同时要求抛出和不抛出的
   程序都出现。现在一致性检验的不仅是值，还有求值顺序：在 `(raise 1) + (raise 2)` 中三者都必须抛出 1，所以一条先求右操作数
   的大步规则会被抓住。第 1 题的确定性证明可以推广，因为传播规则也只在它左边的一切都是值时才触发。

6. **★ 研究。** 一个没有凭空出现的值的 C 宽松内存语义。

   *讨论。* 尚未解决。Batty 等人（2011）形式化的 C 和 C++ 内存模型允许宽松的原子读返回在一个环中自我证明的值：初始
   x = y = 0，线程 1 执行 r1 = x; y = r1，线程 2 执行 r2 = y; x = r2，形式模型并不禁止 r1 = r2 = 42，尽管已知的硬件和
   编译器都不会产生它。标准只建议实现避免这样的值。显而易见的修补各有损失。禁止程序顺序与读取来源（reads-from）合起来成环
   （RC11 的选择，Lahav 等人 2017）排除了 42，却也排除了同一测试去掉依赖后（每个线程写 1 而不是写寄存器）的结果
   r1 = r2 = 1，而 ARM 和 Power 架构允许这个结果，于是编译出来的宽松读后面必须跟一个栅栏或一个假依赖。只禁止经过
   依赖的环也不行，因为依赖不是语法上的东西：编译器会删掉它们（`if (r1 == 1) y = 1; else y = 1;` 变成 `y = 1`），所以一条
   语法规则会禁止合法的优化。承诺语义（promising semantics，Kang 等人 2017）这类操作模型和基于事件结构的模型走了别的路，
   但还没有一个模型被接受，能同时禁止凭空之值、允许编译器实际做的优化、高效地编译到主流处理器，并且三者都有证明。好的部分
   答案可以固定一个片段（比如只有宽松访问和释放/获取访问，或者没有读-改-写），为它给出一个模型，并证明（最好是机器检查的
   证明）它禁止标准的凭空值试金石测试、验证一张列明的编译器变换清单、无需额外栅栏就能映射到 x86、ARMv8 和 Power；或者证明
   某个自然的模型类中没有模型能同时具备这三条性质。

## Glossary additions

* **operational semantics: small-step (structural) and big-step (natural)** — meaning as one step e → e′ at a time;
  meaning as a relation e ⇓ v from a term to its value.
* **value, call by value, search and reduction rules, derivation tree, determinism, stuck term** — finished terms;
  arguments evaluated before the call; where to look and what to do; a step as a proof; at most one next step; a
  non-value with no step.
* **CEK machine: control, environment, continuation** — an abstract machine whose stack of frames is explicit.
* **denotational semantics, denotation, semantic brackets ⟦·⟧, environment ρ, compositionality, context C[·]** —
  meaning as a mathematical object, built only from the meanings of the parts; a program with a hole.
* **bottom (⊥), information order (⊑), flat domain ℤ⊥, pointwise order** — no information; more defined; numbers
  side by side above ⊥; functions compared input by input.
* **complete partial order (cpo), chain, least upper bound, monotone, (Scott-)continuous** — a least element and limits
  of chains; F of a limit is the limit of F.
* **functional, Kleene's fixed-point theorem, Kleene chain, least fixed point** — fix F = ⊔ₙ Fⁿ(⊥) for continuous F.
* **D∞, domain equation D ≅ [D → D]** — Scott's model of the untyped λ-calculus.
* **soundness, adequacy, full abstraction, PCF, parallel-or, sequentiality** — the steps and the mathematics agree;
  the model distinguishes exactly what programs can; the function a sequential language cannot define.
* **logical relation, fundamental lemma, admissible relation, step-indexing** — a relation built type by type; every
  program related to itself; closed under limits of chains; relations indexed by a number of steps.
* **game semantics, strategy, Opponent and Player** — a type as a game, a program as a rule for its next move.
* **contextual equivalence (≅)** — no context can tell two programs apart.
* **labelled transition system, trace equivalence, bisimulation, bisimilarity (∼), coinduction, greatest fixed
  point, Knaster–Tarski theorem** — moves matched forever; the union of all bisimulations; exhibit one relation and
  check one step.
* **Hennessy–Milner logic, partition refinement** — formulas ⟨a⟩φ that separate non-bisimilar states; splitting
  blocks until stable.
* **applicative bisimulation, Howe's method, congruence** — bisimulation for functions, one argument at a time; the
  proof that it is preserved by every context.
* **reducibility (Tait), strong normalization, normalization by evaluation (NbE), read-back** — Tait's predicate on
  types; every reduction stops; evaluate into a semantic domain, then read a normal form back.
* **parametricity, relational interpretation of types, abstraction theorem, representation independence, free
  theorem, shortcut (foldr/build) fusion** — a polymorphic program respects every relation; a law read off a type.
* **derivable (⊢) and valid (⊨) triples, relative completeness, weakest liberal precondition (wlp), expressiveness,
  fixed-point induction** — built from the rules against true of every run; complete given the true assertions; the
  states from which a command ends in Q or runs forever; assertions able to state wlp; a property closed under limits
  holds of a least fixed point.
* **monad, return, bind, monad laws, Kleisli composition, Kleisli category** — computations T A; sequencing with the
  effect in the joints; effectful functions as arrows.
* **algebraic effect, operation, effect handler** — an effect given by its operations; what each operation does, given
  the rest of the program as a continuation.
* **dependent function type (Π), dependent pair type (Σ), Vec A n, identity type, refl, definitional equality,
  structural recursion** — types that depend on values; equality as a type; equal by computing; recursion on smaller
  arguments.
* **intensional and extensional type theory, calculus of constructions, proof assistant kernel** — decidable against
  undecidable type checking; Coq's core; the small trusted checker of proof terms.
* **CCS: action, co-action, τ, prefix, choice, parallel composition, restriction; weak bisimulation** — Milner's
  calculus of communicating systems; bisimulation with τ steps unseen.
* **CSP, π-calculus, scope extrusion, session types** — Hoare's synchronous processes; names sent over names; a
  private name passed outside its scope; a channel's protocol as its type.
* **deadlock (reachable stuck state)** — no move, and not finished.
* **mechanized semantics, univalence, homotopy type theory, cubical type theory** — semantics checked by a proof
  assistant; equivalent types are equal; equalities as paths; a theory in which univalence computes.
* **relaxed memory model, out-of-thin-air value, load buffering** — what concurrent loads may return; a value that
  justifies itself in a cycle; the litmus test where each thread reads before it writes.

## Sources

* G. Winskel, *The Formal Semantics of Programming Languages: An Introduction* (1993); R. Harper, *Practical
  Foundations for Programming Languages* (2nd ed., 2016); B. Pierce et al., *Software Foundations* (online);
  R. Milner, *Communicating and Mobile Systems: the π-Calculus* (1999).
* G. Plotkin, "A structural approach to operational semantics", Aarhus University DAIMI FN-19, 1981; G. Kahn,
  "Natural semantics", STACS 1987; M. Felleisen and D. Friedman, "Control operators, the SECD-machine, and the
  λ-calculus", Formal Description of Programming Concepts III, 1986.
* D. Scott and C. Strachey, "Toward a mathematical semantics for computer languages", Oxford PRG-6, 1971; D. Scott,
  "Outline of a mathematical theory of computation", Princeton Conference on Information Sciences and Systems, 1970;
  D. Scott, "Continuous lattices", Lecture Notes in Mathematics 274, 1972; A. Tarski, "A lattice-theoretical
  fixpoint theorem and its applications", Pacific J. Math. 1955.
* G. Plotkin, "LCF considered as a programming language", Theoretical Computer Science 1977; S. Abramsky,
  R. Jagadeesan and P. Malacaria, "Full abstraction for PCF", and J. M. E. Hyland and C.-H. L. Ong, "On full
  abstraction for PCF: I, II and III", both Information and Computation 2000; H. Nickau, "Hereditarily sequential
  functionals", LFCS 1994.
* D. Park, "Concurrency and automata on infinite sequences", GI Conference on Theoretical Computer Science 1981;
  M. Hennessy and R. Milner, "Algebraic laws for nondeterminism and concurrency", J. ACM 1985; P. Kanellakis and
  S. Smolka, "CCS expressions, finite state processes, and three problems of equivalence", PODC 1983; R. Paige and
  R. Tarjan, "Three partition refinement algorithms", SIAM J. Comput. 1987.
* S. Abramsky, "The lazy lambda calculus", in *Research Topics in Functional Programming* (1990); D. Howe, "Proving
  congruence of bisimulation in functional programming languages", Information and Computation 1996; A. Appel and
  D. McAllester, "An indexed model of recursive types for foundational proof-carrying code", TOPLAS 2001.
* W. Tait, "Intensional interpretations of functionals of finite type I", J. Symbolic Logic 1967; U. Berger and
  H. Schwichtenberg, "An inverse of the evaluation functional for typed λ-calculus", LICS 1991.
* J. Reynolds, "Types, abstraction and parametric polymorphism", Information Processing 83 (IFIP 1983); P. Wadler,
  "Theorems for free!", FPCA 1989; A. Gill, J. Launchbury and S. Peyton Jones, "A short cut to deforestation", FPCA
  1993.
* C. A. R. Hoare, "An axiomatic basis for computer programming", Commun. ACM 1969; S. Cook, "Soundness and
  completeness of an axiom system for program verification", SIAM J. Comput. 1978.
* E. Moggi, "Computational lambda-calculus and monads", LICS 1989, and "Notions of computation and monads",
  Information and Computation 1991; P. Wadler, "The essence of functional programming", POPL 1992; G. Plotkin and
  J. Power, "Adequacy for algebraic effects", FoSSaCS 2001; G. Plotkin and M. Pretnar, "Handlers of algebraic
  effects", ESOP 2009.
* P. Martin-Löf, *Intuitionistic Type Theory* (1984); J.-Y. Girard, *Interprétation fonctionnelle et élimination
  des coupures de l'arithmétique d'ordre supérieur* (thesis, Université Paris VII, 1972); T. Coquand and G. Huet,
  "The calculus of constructions", Information and Computation 1988.
* C. A. R. Hoare, "Communicating sequential processes", Commun. ACM 1978; R. Milner, *A Calculus of Communicating
  Systems* (LNCS 92, 1980); R. Milner, J. Parrow and D. Walker, "A calculus of mobile processes, I and II",
  Information and Computation 1992.
* X. Leroy, "Formal verification of a realistic compiler", Commun. ACM 2009; R. Kumar, M. Myreen, M. Norrish and
  S. Owens, "CakeML: a verified implementation of ML", POPL 2014; A. Haas et al., "Bringing the web up to speed with
  WebAssembly", PLDI 2017; C. Watt, "Mechanising and verifying the WebAssembly specification", CPP 2018.
* The Univalent Foundations Program, *Homotopy Type Theory: Univalent Foundations of Mathematics* (2013); C. Cohen,
  T. Coquand, S. Huber and A. Mörtberg, "Cubical type theory: a constructive interpretation of the univalence
  axiom", TYPES 2015.
* M. Batty, S. Owens, S. Sarkar, P. Sewell and T. Weber, "Mathematizing C++ concurrency", POPL 2011; M. Batty,
  K. Memarian, K. Nienhuis, J. Pichon-Pharabod and P. Sewell, "The problem of programming language concurrency
  semantics", ESOP 2015; O. Lahav, V. Vafeiadis, J. Kang, C.-K. Hur and D. Dreyer, "Repairing sequential consistency
  in C/C++11", PLDI 2017; J. Kang, C.-K. Hur, O. Lahav, V. Vafeiadis and D. Dreyer, "A promising semantics for
  relaxed-memory concurrency", POPL 2017.
