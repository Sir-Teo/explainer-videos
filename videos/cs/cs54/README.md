# Computer Science, Built — Part 54: Proving Programs Correct

Part 54 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act X, *Horizons and Trust*. Testing can show that bugs are present
but never that they are absent, and Rice's theorem (Part 25) rules out deciding correctness in general. We prove
programs correct anyway, three ways round the theorem: by writing the invariants ourselves and letting Part 26's SAT
solver check the verification conditions, by exhausting a finite state space explicitly, with BDDs or with SAT, and by
approximating soundly. Along the way the solver finds Bloch's binary-search overflow and proves the repairs, a model
checker finds the bugs we plant in Peterson's lock, two-phase commit and a Raft election, an LCF kernel of 69 lines
checks proofs, and a fuzzer finds a bug planted in our own compiler and shrinks the program that shows it to nine
lines.

The instruments are in `explainer/cs/verify/` (tested in `tests/test_cs54_logic.py` and `tests/test_cs54_check.py`):
* `hoare.py`: a tiny imperative language (assignment, `if`, `while` with a given invariant and variant, `assert`,
  `assume`, `havoc`) over signed w-bit integers; Dijkstra's weakest preconditions and the verification conditions of
  a program (established, preserved, exit, variant non-negative, variant decreases); a Tseitin bit-blaster
  (ripple-carry adders, a shift-add multiplier, comparators) that hands the negation of each condition to Part 26's
  CDCL solver, decoding and re-checking every counterexample by evaluation; assertions flowing backward through a
  listing; max, the swap without a temporary, Gauss's summation loop, five binary-search midpoints and the search
  loop; Gauss's conditions timed against the word width.
* `absint.py`: the interval domain (join, meet, widening, narrowing) over the same language read on mathematical
  integers; interval arithmetic and refinement by conditions; a fixpoint iteration that records every round at every
  loop head; three loops with and without widening, and the relation $j = 2i$ that intervals cannot hold.
* `models.py`: guarded-command models explored breadth first into Kripke structures (so every counterexample is a
  shortest one); CTL by least and greatest fixpoints; LTL response properties under weak and strong fairness, with
  lassos as counterexamples; Peterson's lock and a broken variant (checked against Part 33's checker), the dining
  philosophers naive and with a global fork order, Lamport's TCommit and TwoPhase with a refinement check and a
  timeout bug, and an abstract Raft election with a voter that forgets its vote.
* `bdd.py`: a reduced ordered BDD manager (unique table, `apply`, `ite`, restriction, quantification and the
  relational product); the equality function under two variable orders; symbolic reachability of up to 16
  philosophers with one transition relation per command; bounded model checking as CNF for the CDCL solver.
* `lcf.py`: an LCF-style kernel for propositional natural deduction (eleven rules, the classical one double-negation
  elimination), a recorder outside it that logs proofs, four proofs including Peirce's law, five refused steps, and
  independent checks by truth tables and a two-world Kripke model.
* `testing.py`: property-based testing with greedy shrinking; a bug planted in the SCCP pass's constant folder for
  the duration of a `with` block, a fuzzer that hunts it with Part 13's random-program generator and differential
  runs, and hierarchical delta debugging of the failing program; the Job at every level against the IR interpreter
  and a Python reference; line and branch coverage with `sys.settrace`.

## Chapters

* **Hook.** Three bugs (Ariane 5 in 1996, Therac-25 in 1985–1987, Heartbleed in 2014) in tested programs, and
  Dijkstra's 1970 dictum. Binary search's midpoint as a SAT problem over 16-bit integers: in 0.03 s the solver finds
  lo = 8,997, hi = 27,291, whose sum 36,288 wraps to −29,248; `lo + ((hi - lo) >>> 1)` is UNSAT, a proof for every
  16-bit lo < hi (342 variables, 1,022 clauses). Rice's theorem and the three ways round it.
* **1. Specifications, and the first program proof.** Pre- and postconditions for max; a weakened specification met
  by the useless `m = 32767`, and a sort that returns `[]`; ghost variables for the swap, run on 30,000 and 20,000,
  whose sum wraps; Turing's 1949 "Checking a Large Routine", n! by repeated addition with assertions u = r! and
  u = s·r!, a run with n = 5; his column-addition analogy (1374 + 5926 + 2085, carries supplied); the paper largely
  overlooked until Morris and Jones (1984), while Floyd (1967) and Hoare (1969) rebuilt the idea as a logic.
* **2. Floyd–Hoare logic.** The triple and partial correctness; the assignment axiom by backward substitution
  (x > 5 after x := x + 1 needs x > 4), and the forward rule's existential; sequence on the swap, assertions pushed up
  line by line; consequence, with the identities true in wrap-around arithmetic; conditionals on max; the while rule
  and Gauss's invariant 2s = i(i + 1) preserved by algebra; soundness, incompleteness, and Cook's relative
  completeness (1978).
* **3. Binary search, proved.** The invariant on a sorted array of twelve primes, searching for the first element
  ≥ 20 (answer a[8] = 23). Our checker on the loop's skeleton, the comparison a havoc'd unknown, invariant
  0 ≤ lo ≤ hi and variant hi − lo: five conditions, all valid at 16 bits, the hardest (variant decreases, 2,352
  clauses) in 1.42 s; the search property itself is out of this checker's reach. With the textbook midpoint the
  solver refutes preservation at lo = 15,072, hi = 25,558: the sum 40,630 wraps to −24,906 and halves to −12,453,
  below lo (Bloch 2006; Bentley's proof was about mathematical integers). Five midpoints over every 16-bit input:
  `(lo + hi) >> 1` fails (0.028 s), `lo + ((hi - lo) >> 1)` with 0 ≤ lo is proved (1,035 clauses), `(lo + hi) >>> 1`
  is proved (795 clauses), the first fix without 0 ≤ lo fails at lo = −16,034, hi = 25,554, and
  `lo + ((hi - lo) >>> 1)` is proved for every lo < hi (1,022 clauses). Total correctness: the textbook midpoint also
  fails "variant decreases" (lo = 22,568, hi = 27,926); a run of the gap 1000, 499, 249, …, 3, 1, 0. Well-founded
  orders: pairs in dictionary order, Ackermann's function, Floyd's well-founded sets.
* **4. Weakest preconditions, checked by SAT.** Dijkstra's wp (1975): {P} c {Q} exactly when P ⇒ wp(c, Q); the rules
  as equations (assignment, sequence, conditional, `assert`, `havoc`); Gauss's first condition derived. Five
  verification conditions from an invariant and a variant. Bit-blasting: 16 Boolean variables per integer, adders as
  full-adder chains (Part 4), Tseitin's three clauses per and-gate; the swap's condition is 425 variables, 1,239
  clauses, 1,337 conflicts, UNSAT in 0.24 s. Every program so far: max (390 clauses), swap and the fixed binary
  search (5,040 clauses, 1.73 s) proved at 16 bits, Gauss's loop at 8 bits (4,976 clauses, 0.39 s), the textbook
  search refuted on two of its five conditions with the solver's values, each counterexample re-checked by evaluation.
  Multipliers are hard: Gauss's two product conditions take 5, 62, 298 and 2,082 ms at 4, 6, 8 and 10 bits. SMT
  solvers (Z3, 2008), Dafny, and proofs of UNSAT.
* **5. Separation logic.** Aliasing breaks the assignment axiom ({y.f = 2} x.f := 3 {y.f = 2} fails when x = y);
  the heap as one array costs a case split per pair of pointers. emp, x ↦ v, the separating conjunction, and the list
  predicate; the small axioms and the frame rule; Reynolds' in-place list reversal animated on three nodes and proved
  with one invariant, list(α, i) ∗ list(β, j) ∧ rev(α₀) = rev(α)·β. Bi-abduction (Calcagno, Distefano, O'Hearn and
  Yang, 2009), Facebook's Infer, concurrent separation logic (the 2016 Gödel Prize), Iris and RustBelt (Part 55).
* **6. Model checking.** Kripke structures; Peterson's lock is 20 states and 46 transitions. Computation trees, LTL
  (Pnueli 1977) and CTL (Clarke and Emerson 1981) on a five-state example (EF q and EG p hold, AG p and AF q fail);
  EF q as a least fixpoint, stable after four rounds; linear-time CTL checking (Clarke, Emerson and Sistla 1986).
  Peterson: six CTL questions, mutual exclusion, no deadlock and "can always get in" hold, "always gets in" fails;
  Part 33's checker (258 states of loads and stores) agrees on mutual exclusion. The liveness failure as a lasso, and
  weak fairness, under which the response property holds for both processes. Counterexamples: Peterson with the turn
  given away before the flag is raised, 32 states and a six-step path to both in the critical section; Raft-lite with
  three nodes and terms up to 2, 2,076 states and at most one leader per term; a voter that forgets its vote,
  158,647 states and nodes 0 and 2 both leaders of term 1 after six steps. State explosion: the dining philosophers
  grow from 6 states (n = 2) to 1,154 (n = 8), about ×2.4 per philosopher, a deadlock in n steps for every n; with
  ordered forks none (985 states at n = 8), though philosopher 0 can still starve under weak fairness (n = 3), not
  under strong.
* **7. Symbolic and bounded model checking.** Two bits per philosopher; a set of states as a Boolean function, a
  move as guard ∧ effect ∧ frame over current and primed bits. BDDs (Bryant 1986): the equality of two bit-pairs is a
  15-test decision tree, 6 nodes interleaved and 9 separated; at twelve pairs 36 against 12,285 = 3·2ⁿ − 3; best
  order NP-hard (Bollig and Wegener 1996), no good order for multiplication (Bryant 1991). Image computation and
  reachability (Burch et al. 1990): sixteen philosophers take 16 images, 1,331,714 states in a final diagram of 117
  nodes, 0.87 s; states grow about ×2.4 per philosopher while the diagram grows by 8 nodes; the explicit counts agree
  up to n = 8; the transition relation is 4,480 nodes at n = 16, and the one deadlock state is found symbolically.
  Bounded model checking (Biere, Cimatti, Clarke and Zhu 1999) on seven philosophers: UNSAT for k = 0 to 6, the
  hardest k = 6 at 2,598 conflicts; SAT at k = 7, the decoded deadlock. With ordered forks, five philosophers are
  UNSAT for every k ≤ 7 and the diameter is 5: a proof. k-induction (2000) and IC3 (2011).
* **8. Abstract interpretation.** Sound approximation (Cousot and Cousot 1977): the 11 states at a two-counter
  loop's head and their box i ∈ [0, 10], j ∈ [0, 20]; false alarms. The interval lattice, joins as hulls, the Galois
  connection ({1, 4, 6} ↦ [1, 6]), infinite ascending chains. Counting to 100: 101 rounds to the fixpoint [0, 100],
  the assertion proved. Widening and narrowing: [0, 1] jumps to [0, +∞], then narrows to [0, 100], two rounds and two
  narrowing steps; for a count to an input n ≤ 50, 51 rounds against 2 + 2; on the two-counter loop plain iteration
  never stops (round 60: j ∈ [0, 120]) and widening gives j ∈ [0, +∞], so `assert j == 20` is a false alarm. Karr's
  linear equalities (1976) and polyhedra (Cousot and Halbwachs 1978) keep j = 2i; octagons (Miné 2006) cut the box to a
  parallelogram but cannot. Astrée (2003) on the Airbus A340's flight-control software.
* **9. Types as lightweight proofs.** A type check speaks for every run: progress and preservation (Part 14),
  Milner's "well-typed programs cannot go wrong". Type checking as abstract interpretation (Cousot 1997), and a
  harmless expression it rejects. Refinement types (Freeman and Pfenning 1991): idx(n) <: nat as an implication.
  Bloch's bug as a type error: the repaired midpoint's subtyping condition is valid at 16 bits (346 variables, 1,035
  clauses, 0.13 s), the textbook one fails at lo = 8,997, hi = 27,291. Liquid types (Rondon, Kawaguchi and Jhala
  2008) by hand: of the qualifiers 0 ≤ v, v = 0, v < n, v ≤ n, two are struck out, leaving 0 ≤ v ≤ n. A ladder from
  simple types to dependent types.
* **10. Proof assistants.** Milner's LCF (1972): only the kernel makes theorems; ours has 69 lines and 11 rules, and
  ML came from LCF's tactic language. Gentzen's natural deduction, double negation the one classical rule. The
  kernel proves A ∧ B ⇒ B ∧ A in five calls (the Lean 4 version is one line). Five illegal steps refused with their
  messages; Python's limits, and the de Bruijn criterion. LCF style (HOL Light, Isabelle) against proof terms (Rocq,
  Lean, Agda). Mathematics checked: the four colour theorem (1976, in Coq 2005), the Kepler conjecture (1998,
  Flyspeck 2014), the odd order theorem (2012), the Liquid Tensor Experiment (2022), mathlib.
* **11. Verified systems.** CompCert (Leroy 2006): ten languages from CompCert C to Asm, each pass proved to shrink
  the set of behaviours, the inclusions chained. Csmith (2011) found hundreds of bugs in GCC and LLVM and no
  wrong-code bugs in CompCert's verified middle. seL4 (2009): abstract and executable specifications refined by about
  8,700 lines of C, with about 200,000 lines of Isabelle proof; the 2009 assumptions, and the binary checked against
  the C in 2013. The simulation square with stuttering. Verified cryptography: p = 2²⁵⁵ − 19, five 51-bit limbs and
  the 19s in the code; Fiat-Crypto and HACL*. CakeML (2014) and what is left to trust.
* **12. Specifying systems: TLA+.** Init ∧ □[Next]_vars ∧ Fairness (Lamport 1994). TCommit (Gray and Lamport 2006):
  3ⁿ + 2ⁿ − 1 reachable states, 12, 34, 96 and 274 for two to five managers, as the checker counts. TwoPhase: 56,
  288, 1,568 and 8,832 states (115 to 37,589 transitions, longest paths 7 to 16), consistent throughout. A coordinator
  that commits on a timeout: 623 states and a three-step counterexample, one committed and one aborted. TwoPhase
  refines TCommit, every reachable step checked for two, three and four managers. States grow ×5.1 to ×5.6 per
  manager, yet the bug needed three managers and three steps (Jackson's small scope hypothesis); TLAPS for every n.
* **13. Testing as science.** Coverage on Myers's triangle classifier (1979): 300 random tests (171 invalid, 124
  scalene, 5 isosceles, no equilateral) reach 7 of 9 lines and 6 of 8 branch outcomes. An insert with an off-by-one
  passes three unit tests with full coverage; a property test fails on its ninth input and shrinks it to
  `insert([0], 1)`, which returns `[1, 0]`. Mutation testing (DeMillo, Lipton and Sayward 1978): four mutants worked
  by hand, one equivalent, score 1/3. QuickCheck (2000): a sort through a set fails on its 27th list,
  [3, −3, −3, 1], shrunk after 11 candidates to [0, 0]. Coverage-guided fuzzing (Miller 1990, AFL 2013, OSS-Fuzz
  2016): 256⁻³ = 1/16,777,216 against about 3 × 256 tries. Symbolic and concolic execution: the path condition for
  `equilateral` solved to a = b = c = 1 (KLEE 2008, DART 2005).
* **14. Fuzzing and validating our compiler.** Differential testing of random Pebble programs on the IR interpreter
  and at four levels, with a planted bug: SCCP folds division by floor, so (−7)/256 becomes −1 with remainder 249
  instead of 0 and −7. The hunt: five programs in 2.7 s, three agree, one skipped at the step limit, seed 4
  disagrees (75 lines, 6 functions, 92 bytes of output), at level 3 only, from byte 1; without the bug every program
  agrees. Delta debugging (Zeller and Hildebrandt 2002, hierarchical after Misherghi and Su 2006): 75 tests, 54
  accepted removals, 4.4 s, 75 lines down to 9; f1(−7, −78) = −7 prints `f90000` against `f9ffff`. The Job on five
  texts up to 226 bytes agrees at every level with the interpreter and a Python reference (38,633 steps unoptimized,
  12,854 at level 3): evidence, not proof. Translation validation (Pnueli, Siegel and Singerman 1998), illustrated by
  a validator for constant folding that would refuse the bad fold (not run); CompCert's validated register allocation.
  Proof-carrying code (Necula 1997) and its descendants.
* **15. Frontier: proofs at scale.** TLA+ at Amazon (Newcombe et al. 2015), verified cryptography in browsers,
  static analysis on every change; machines that write proofs, safe because our kernel's 69 lines check every step;
  language models writing Lean, Coq and Dafny proofs, and 2024's kernel-checked olympiad solutions. Four open problems
  (invariant inference, specifications, scale, concurrency and hardware) and the ★ research problem.
* **Outro.** Recap, payoffs (Parts 55, 58, 59, 60, 61), practice, problems, next part.

## Build

```bash
python -m videos.cs.cs54.compute
python -m unittest tests.test_cs54_logic tests.test_cs54_check
python tools/build.py cs54
```

## Problems, with solutions

1. **Gauss's loop.** Prove {n ≥ 0} the summation loop {s = n(n+1)/2} with an invariant and a variant.

   *Solution.* The loop is `i = 0; s = 0; while i < n: i = i + 1; s = s + i`. Take the invariant
   I: 0 ≤ i ≤ n ∧ 2s = i(i + 1) and the variant V = n − i. Five conditions. Established: with i = s = 0, I reads
   0 ≤ 0 ≤ n ∧ 0 = 0·1, which follows from n ≥ 0. Preserved: from I and i < n, the body gives i' = i + 1 and
   s' = s + i + 1; then 0 ≤ i' and i' ≤ n (integers, i < n), and 2s' = 2s + 2(i + 1) = i(i + 1) + 2(i + 1) =
   (i + 1)(i + 2) = i'(i' + 1). Exit: I and ¬(i < n) give i = n, so 2s = n(n + 1); since n(n + 1) is a product of
   consecutive integers it is even, and s = n(n+1)/2. Variant non-negative: i < n gives n − i > 0. Variant decreases:
   n − (i + 1) < n − i. The variant is a natural number that falls by one on each pass, so the loop stops after
   exactly n passes, and the triple holds in the total sense. Our checker discharges the five conditions at 8 bits
   (4,976 clauses, 0.39 s); there the equation is read modulo 2⁸, and i + 1 cannot overflow because i < n ≤ 127. Note
   that 2s ≡ n(n + 1) (mod 2ʷ) fixes s only modulo 2ʷ⁻¹, a weaker statement than the loop's actual result.

2. **The swap's weakest precondition.** Compute wp for the swap without a temporary, and show that it holds for all
   w-bit values.

   *Solution.* Push the postcondition x = Y ∧ y = X up from the last line. Through `x = x - y`: x − y = Y ∧ y = X.
   Through `y = x - y`: x − (x − y) = Y ∧ x − y = X. Through `x = x + y`: (x + y) − ((x + y) − y) = Y ∧
   (x + y) − y = X. The condition is x = X ∧ y = Y ⇒ that. In the integers (x + y) − y = x and (x + y) − x = y, so it
   reduces to y = Y ∧ x = X, which is the hypothesis. For w-bit words, two's-complement +, − are the operations of
   the ring ℤ/2ʷℤ: each computed value is congruent modulo 2ʷ to the same expression evaluated in ℤ, so the final x is
   congruent to the initial y and the final y to the initial x; both lie in the representative range
   [−2ʷ⁻¹, 2ʷ⁻¹), where congruent numbers are equal. With 16 bits, 30,000 and 20,000: x becomes −15,536 (50,000
   wrapped), then y = −35,536 + 65,536 = 30,000 and x = −45,536 + 65,536 = 20,000. Our SAT solver confirms it for
   every 16-bit pair: 425 variables, 1,239 clauses, UNSAT in 0.24 s. The proof needs wrap-around: with saturating or
   floating-point arithmetic it fails, and if x and y name the same storage the three lines leave 0.

3. **List reversal.** Show that in-place list reversal is correct in separation logic.

   *Solution.* The program is `j = nil; while i != nil: k = i.next; i.next = j; j = i; i = k`, with precondition
   list(α₀, i) and postcondition list(rev(α₀), j), where list(ε, i) ⇔ emp ∧ i = nil and list(a·α, i) ⇔
   ∃k. i ↦ a, k ∗ list(α, k). Invariant I: ∃α, β. list(α, i) ∗ list(β, j) ∧ rev(α₀) = rev(α)·β. Established: after
   `j = nil`, list(ε, j) is emp, so list(α₀, i) ∗ list(ε, j) holds with α = α₀, β = ε. Preserved: i ≠ nil rules out
   α = ε (that case says i = nil), so α = a·α', and unfolding gives i ↦ a, k₀ ∗ list(α', k₀) ∗ list(β, j). The read
   `k = i.next` touches only the first cell and sets k = k₀. The store `i.next = j` is the small axiom on that one
   cell, {i.next ↦ −} i.next := j {i.next ↦ j}, and the frame rule carries list(α', k) ∗ list(β, j) through
   unchanged; the star guarantees that the cell is in neither list, so no case split for aliasing is needed. Folding,
   i ↦ a, j ∗ list(β, j) is list(a·β, i), so we have list(α', k) ∗ list(a·β, i), and `j = i; i = k` renames it to
   list(α', i) ∗ list(a·β, j). The ghost equation holds since rev(a·α')·β = rev(α')·a·β. Exit: I and i = nil give
   α = ε (list(α, nil) forces it) and emp for that part, so list(β, j) with rev(α₀) = β, the postcondition. Every
   dereference is of a cell the assertion owns, so the program is also memory-safe, and the length of α is a variant.

4. **Widening.** Show that interval analysis without widening may not terminate, and that widening makes it
   terminate.

   *Solution.* Take `i = 0; j = 0; while i < 10: i = i + 1; j = j + 2`. Kleene iteration at the loop head computes
   X₀ = (i ∈ [0, 0], j ∈ [0, 0]) and X_{k+1} = X₀ ⊔ body(X_k ⊓ (i < 10)). By induction X_k = (i ∈ [0, min(k, 10)],
   j ∈ [0, 2k]): the filter i < 10 bounds i but says nothing about j, the body adds 1 and 2, and the join with X₀
   keeps the lower bounds at 0. So j's upper bound grows for ever (round 60 of our analyser has j ∈ [0, 120]); the
   interval lattice has infinite ascending chains, and nothing in the program bounds j on its own. (Iteration can
   terminate without widening, as counting to 100 does in 101 rounds, but only by climbing the chain one step at a
   time.) With widening, Y_{k+1} = Y_k ∇ F(Y_k), where a bound that moved goes to ±∞ and a stable bound stays.
   Whenever Y_{k+1} ≠ Y_k some finite bound has become infinite, and an infinite bound never changes again, so with n
   variables there are at most 2n strict steps per loop head. When Y_{k+1} = Y_k, every bound of F(Y_k) lies within
   Y_k's (otherwise it would have been widened), so F(Y) ⊑ Y: a post-fixpoint, which by Tarski's theorem lies above
   the least fixpoint and is therefore sound. Narrowing then lets only infinite bounds come back down, so it too stops
   within 2n steps and stays above the least fixpoint. Our analyser: counting to 100, two rounds and two narrowing
   steps instead of 101; to an input n ≤ 50, the same instead of 51; on the two-counter loop it stops at
   i ∈ [0, 10], j ∈ [0, +∞], where plain iteration never stops.

5. **Build.** Plant a different bug in our compiler's optimizer, and measure how many random programs the fuzzer needs.

   *Solution notes.* In `explainer/cs/verify/testing.py`, add an entry to `BUGS` and make `_BuggyFolder` dispatch on
   the kind (as written, `planted_bug` installs the floor-division folder whatever kind it is given). Bugs that fit
   the folder, which SCCP calls through `interp.binop` for every operator: folding shifts without masking the count to
   five bits (`ub & 31`), folding a signed comparison as unsigned, or a remainder that takes the sign of the divisor.
   Check that it is scoped, as `tests.test_cs54_check.Fuzz.test_planted_bug_is_scoped` does for the original. Then run
   `hunt(kind, seeds=range(s0, s0 + 200))` for, say, twenty disjoint seed ranges: `programs` is the number generated
   up to the first disagreement (skipped programs included) and `clean_agree` must be true. If each program triggers
   the bug independently with probability p, the count is geometric with mean 1/p; report the median and quartiles,
   and estimate p as finds over programs, with a confidence interval. Expect the count to depend on how often the
   generator makes the operator's operands constant (only level 3 inlines, which is why the planted bug showed at
   level 3 alone) and on how often the operands hit the buggy case (both signs differing; a shift count of 32 or
   more). Finish with `shrink_program` on each find and add a test like `Fuzz.test_hunt`.

6. **★ Research.** Complete, practical invariant inference for loops with multiplication.

   *Discussion.* Open. Over the integers, even checking that a candidate invariant is inductive means proving a
   universally quantified formula of nonlinear integer arithmetic, which is undecidable in general (Hilbert's tenth
   problem, Part 25); over w-bit words it is decidable but, as Gauss's conditions showed (5 ms at 4 bits, over 2 s at
   10), multiplier reasoning is the classic hard case for SAT. Known complete methods cover restricted classes:
   polynomial equalities for loops whose updates are affine, or invariants of bounded degree found with Gröbner bases
   or linear algebra, while practical tools fall back on templates, interpolation, data-driven guessing and, lately,
   language models whose guesses a checker filters. A good answer would fix a class of invariants (for instance
   polynomial equalities of degree at most d together with linear inequalities), a class of loops with polynomial
   updates and guards, and prove the procedure finds an inductive invariant in the class whenever one exists that
   proves the assertion, with a stated complexity and an implementation that handles Gauss's loop, cubic sums and
   integer square root in seconds. Partial results would already be valuable: completeness for one interesting
   subclass, a sharp decidability boundary between classes, or the same results for modular (bit-vector) arithmetic,
   where 2s = n(n + 1) no longer determines s.

## 习题与解答

1. **高斯求和循环。** 用一个不变量和一个递减量（变式），证明 {n ≥ 0} 求和循环 {s = n(n+1)/2}。

   *解答。* 循环是 `i = 0; s = 0; while i < n: i = i + 1; s = s + i`。取不变量 I：0 ≤ i ≤ n ∧ 2s = i(i + 1)，变式
   V = n − i。共五个条件。进入时成立：i = s = 0 时 I 为 0 ≤ 0 ≤ n ∧ 0 = 0·1，由 n ≥ 0 推出。循环体保持：由 I 和
   i < n，循环体给出 i' = i + 1、s' = s + i + 1；于是 0 ≤ i'，且 i' ≤ n（整数，i < n），并且 2s' = 2s + 2(i + 1) =
   i(i + 1) + 2(i + 1) = (i + 1)(i + 2) = i'(i' + 1)。退出：I 与 ¬(i < n) 给出 i = n，所以 2s = n(n + 1)；n(n + 1) 是
   两个相邻整数之积，必为偶数，故 s = n(n+1)/2。变式非负：i < n 给出 n − i > 0。变式递减：n − (i + 1) < n − i。变式是
   自然数，每一轮减一，所以循环恰好在 n 轮后停止，三元组在完全正确性的意义下成立。我们的检查器在 8 位上判定这五个条件都
   有效（4,976 个子句，0.39 秒）；在那里等式按模 2⁸ 理解，而且因为 i < n ≤ 127，i + 1 不会溢出。注意 2s ≡ n(n + 1)
   (mod 2ʷ) 只把 s 确定到模 2ʷ⁻¹，比循环实际算出的结果要弱。

2. **交换的最弱前置条件。** 计算无临时变量交换的 wp，并证明它对所有 w 位的值成立。

   *解答。* 把后置条件 x = Y ∧ y = X 从最后一行往上推。经过 `x = x - y`：x − y = Y ∧ y = X。经过 `y = x - y`：
   x − (x − y) = Y ∧ x − y = X。经过 `x = x + y`：(x + y) − ((x + y) − y) = Y ∧ (x + y) − y = X。验证条件是
   x = X ∧ y = Y ⇒ 上式。在整数中 (x + y) − y = x，(x + y) − x = y，所以它化为 y = Y ∧ x = X，正是假设。对 w 位的字，
   补码的 +、− 就是环 ℤ/2ʷℤ 的运算：每个算出的值都与同一表达式在 ℤ 中的值模 2ʷ 同余，所以最后的 x 与开始的 y 同余，
   最后的 y 与开始的 x 同余；它们都在代表元范围 [−2ʷ⁻¹, 2ʷ⁻¹) 里，同余即相等。16 位下取 30,000 和 20,000：x 变成
   −15,536（50,000 回绕），然后 y = −35,536 + 65,536 = 30,000，x = −45,536 + 65,536 = 20,000。我们的 SAT 求解器对
   每一对 16 位值确认了这一点：425 个变量，1,239 个子句，0.24 秒内不可满足。这个证明依赖回绕：换成饱和运算或浮点数
   就不成立；如果 x 和 y 指的是同一块存储，三行之后只剩 0。

3. **链表反转。** 用分离逻辑证明原地反转链表是正确的。

   *解答。* 程序是 `j = nil; while i != nil: k = i.next; i.next = j; j = i; i = k`，前置条件 list(α₀, i)，后置条件
   list(rev(α₀), j)，其中 list(ε, i) ⇔ emp ∧ i = nil，list(a·α, i) ⇔ ∃k. i ↦ a, k ∗ list(α, k)。不变量 I：
   ∃α, β. list(α, i) ∗ list(β, j) ∧ rev(α₀) = rev(α)·β。进入时成立：`j = nil` 之后 list(ε, j) 就是 emp，所以
   list(α₀, i) ∗ list(ε, j) 在 α = α₀、β = ε 时成立。循环体保持：i ≠ nil 排除了 α = ε（那种情形要求 i = nil），所以
   α = a·α'，展开得 i ↦ a, k₀ ∗ list(α', k₀) ∗ list(β, j)。读 `k = i.next` 只碰第一个格子，令 k = k₀。写
   `i.next = j` 是那一个格子上的小公理 {i.next ↦ −} i.next := j {i.next ↦ j}，框架规则把 list(α', k) ∗ list(β, j)
   原样带过去；分离合取保证这个格子不在两个链表里，所以不必为别名分情况。折叠：i ↦ a, j ∗ list(β, j) 就是
   list(a·β, i)，于是得到 list(α', k) ∗ list(a·β, i)，而 `j = i; i = k` 把它改名为 list(α', i) ∗ list(a·β, j)。幽灵
   等式成立，因为 rev(a·α')·β = rev(α')·a·β。退出：I 与 i = nil 给出 α = ε（list(α, nil) 迫使如此），那一部分是 emp，
   于是 list(β, j) 且 rev(α₀) = β，正是后置条件。每次解引用的格子都归断言所有，所以程序也是内存安全的；α 的长度是变式。

4. **加宽。** 证明不加宽的区间分析可能不终止，而加宽使它终止。

   *解答。* 取 `i = 0; j = 0; while i < 10: i = i + 1; j = j + 2`。在循环头上的克莱尼迭代计算
   X₀ = (i ∈ [0, 0], j ∈ [0, 0]) 和 X_{k+1} = X₀ ⊔ body(X_k ⊓ (i < 10))。归纳可得 X_k = (i ∈ [0, min(k, 10)],
   j ∈ [0, 2k])：过滤 i < 10 约束了 i，却对 j 什么也没说；循环体加 1 和加 2；与 X₀ 的并把下界保持在 0。所以 j 的上界
   永远增长（我们的分析器第 60 轮时 j ∈ [0, 120]）；区间格有无限的上升链，程序里也没有什么单独约束 j。（不加宽也可能
   终止，比如数到 100 用了 101 轮，但那是沿着链一步一步爬上去的。）加宽时 Y_{k+1} = Y_k ∇ F(Y_k)：动过的界送到 ±∞，
   稳定的界保留。只要 Y_{k+1} ≠ Y_k，就有某个有限的界变成了无穷，而无穷的界不再改变，所以 n 个变量时每个循环头至多有
   2n 次严格上升。当 Y_{k+1} = Y_k 时，F(Y_k) 的每个界都落在 Y_k 之内（否则它会被加宽），所以 F(Y) ⊑ Y：这是一个后
   不动点，由塔尔斯基定理它位于最小不动点之上，因而是可靠的。随后的窄化只允许无穷的界降回来，所以也在 2n 步内停止，
   并且仍在最小不动点之上。我们的分析器：数到 100，用两轮加两步窄化，而不是 101 轮；数到输入 n ≤ 50，同样是 2 + 2，
   而不是 51 轮；在双计数器循环上它停在 i ∈ [0, 10]、j ∈ [0, +∞]，而普通迭代永不停止。

5. **动手。** 在我们编译器的优化器里植入另一个错误，测量模糊测试器需要多少个随机程序。

   *解答要点。* 在 `explainer/cs/verify/testing.py` 里给 `BUGS` 加一项，并让 `_BuggyFolder` 按种类分派（按现在的写法，
   不管传入哪个种类，`planted_bug` 装上的都是向下取整除法的折叠器）。适合这个折叠器的错误（SCCP 对每个运算符都通过
   `interp.binop` 调用它）：折叠移位时不把移位数屏蔽到五位（`ub & 31`），把有符号比较当成无符号来折叠，或者让余数取除数的
   符号。像 `tests.test_cs54_check.Fuzz.test_planted_bug_is_scoped` 对原来的错误那样，检查它只在 with 块内生效。然后对
   比如二十个互不相交的种子区间运行 `hunt(kind, seeds=range(s0, s0 + 200))`：`programs` 是直到第一次不一致时生成的程序数
   （包括跳过的），`clean_agree` 必须为真。如果每个程序独立地以概率 p 触发错误，这个数服从均值为 1/p 的几何分布；报告中位数
   和四分位数，并用“找到次数除以程序数”估计 p，附上置信区间。可以预期，这个数取决于生成器多常让该运算符的操作数成为常量
   （只有第 3 级做内联，所以植入的错误只在第 3 级出现），也取决于操作数多常落进出错的情形（两数符号不同；移位数不小于
   32）。最后对每次发现运行 `shrink_program`，并仿照 `Fuzz.test_hunt` 加一个测试。

6. **★ 研究。** 对带乘法的循环，给出完备而实用的不变量推断。

   *讨论。* 尚未解决。在整数上，即使只是检查一个候选不变量是否归纳，也要证明一个全称量化的非线性整数算术公式，这在一般
   情况下不可判定（希尔伯特第十问题，第25部分）；在 w 位字上它可判定，但正如高斯循环的条件所示（4 位 5 毫秒，10 位超过
   2 秒），乘法器推理是 SAT 的经典难题。已知的完备方法只覆盖受限的类：更新为仿射的循环的多项式等式，或用格罗布纳基、
   线性代数求出的有界次数的不变量；实用工具则退而使用模板、插值、数据驱动的猜测，以及近来由检查器筛选其猜测的语言模型。
   好的答案应固定一类不变量（例如次数至多为 d 的多项式等式加上线性不等式）和一类带多项式更新与条件的循环，证明只要该类
   中存在能证明断言的归纳不变量，过程就能找到一个，给出复杂度，并有一个能在几秒内处理高斯循环、立方和与整数平方根的
   实现。部分结果就已有价值：对某个有意思的子类的完备性，类与类之间清晰的可判定性边界，或者在模算术（位向量）下的同样
   结果，在那里 2s = n(n + 1) 已不能确定 s。

## Glossary additions

* **specification, precondition, postcondition, ghost variable** — what a program should do; what the caller
  promises; what the code promises; a name for a past value that lives only in the specification.
* **Hoare triple, partial and total correctness** — {P} c {Q}; correct if it terminates; correct and terminates.
* **assignment axiom, sequence, consequence and while rules** — Hoare's rules; substitution runs backwards.
* **invariant, variant, well-founded order** — a fact every pass preserves; a quantity every pass decreases; an order
  with no infinite descending chain.
* **soundness, relative completeness** — every derivable triple is true; every true triple is derivable given an
  oracle for arithmetic (Cook).
* **weakest precondition, verification condition (VC)** — the largest set of start states from which c surely ends in
  Q; a closed formula whose validity implies correctness.
* **bit-blasting, Tseitin encoding, SMT** — words as Boolean variables and circuits as clauses; SAT with theory
  solvers.
* **separation logic, points-to, separating conjunction, frame rule, footprint, bi-abduction** — assertions that own
  heap cells; x ↦ v; P ∗ Q on disjoint heaps; local reasoning; the cells a command touches; inferring footprints and
  frames.
* **Kripke structure, computation tree, LTL, CTL, fixpoint** — states, transitions and labels; all futures unrolled;
  path and branching temporal logics; how CTL is checked.
* **safety, liveness, fairness (weak, strong), lasso** — nothing bad happens; something good happens; assumptions on
  the scheduler; a stem and a cycle, the shape of a liveness counterexample.
* **state explosion, BDD, variable order, image, bounded model checking, diameter, k-induction, IC3** — exponential
  state counts; canonical decision diagrams; their sensitivity to order; a set's successors; SAT on k-step
  unrollings; the longest shortest path; proof by induction over k steps; incremental inductive invariants.
* **abstract interpretation, Galois connection, interval domain, widening, narrowing, false alarm** — sound
  approximation; the best abstraction of a set; one range per variable; forcing convergence; recovering precision; a
  warning about a correct program.
* **relational domains: octagons, polyhedra** — bounds on ±x ± y; linear inequalities over all variables.
* **progress, preservation, refinement type, subtyping, liquid types, qualifier** — what a type check proves; a type
  plus a predicate; implication; inference over conjunctions of candidate facts.
* **LCF, kernel, natural deduction, sequent, proof term, de Bruijn criterion** — theorems as an abstract type; the
  trusted rules; Gentzen's system; Γ ⊢ A; a proof as a program; independent re-checkability.
* **refinement (of systems), simulation, stuttering** — an implementation whose behaviours the specification allows;
  the square that shows it; steps that change nothing visible.
* **TLA+, TLC, TLAPS, small scope hypothesis** — Lamport's specification language, its model checker and its prover;
  most bugs have small counterexamples.
* **coverage (line, branch), mutation testing, equivalent mutant, mutation score** — where tests have been; testing
  the tests; a change no test can detect; killed over non-equivalent.
* **property-based testing, shrinking, fuzzing, corpus, symbolic and concolic execution, path condition** — laws
  tried on random inputs; reducing a failure; random input guided by coverage; inputs kept for new branches; running
  on symbols; the constraint for reaching a branch.
* **differential testing, delta debugging, translation validation, proof-carrying code** — comparing
  implementations; shrinking a failing input; checking each compilation; code shipped with its proof.

## Sources

* M. Huth and M. Ryan, *Logic in Computer Science: Modelling and Reasoning about Systems* (2nd ed., 2004); C. Baier
  and J.-P. Katoen, *Principles of Model Checking* (2008); E. M. Clarke, O. Grumberg, D. Kroening, D. Peled and
  H. Veith, *Model Checking* (2nd ed., 2018).
* T. Nipkow and G. Klein, *Concrete Semantics with Isabelle/HOL* (2014); B. C. Pierce et al., *Software Foundations*;
  A. R. Bradley and Z. Manna, *The Calculus of Computation* (2007); D. Kroening and O. Strichman, *Decision
  Procedures* (2nd ed., 2016).
* E. W. Dijkstra, *A Discipline of Programming* (1976); D. Gries, *The Science of Programming* (1981); L. Lamport,
  *Specifying Systems* (2002); A. Møller and M. I. Schwartzbach, *Static Program Analysis*; X. Rival and K. Yi,
  *Introduction to Static Analysis* (2020); A. Zeller, R. Gopinath, M. Böhme, G. Fraser and C. Holler, *The Fuzzing
  Book*.
* J. L. Lions et al., *Ariane 5 Flight 501 Failure: Report by the Inquiry Board* (1996); N. G. Leveson and
  C. S. Turner, "An investigation of the Therac-25 accidents", IEEE Computer 1993; CVE-2014-0160 (Heartbleed).
* A. M. Turing, "Checking a large routine", Report of a Conference on High Speed Automatic Calculating Machines,
  Cambridge, 1949; F. L. Morris and C. B. Jones, "An early program proof by Alan Turing", IEEE Annals of the History
  of Computing 1984.
* R. W. Floyd, "Assigning meanings to programs", Proc. Symposia in Applied Mathematics 19, 1967; C. A. R. Hoare, "An
  axiomatic basis for computer programming", CACM 1969; S. A. Cook, "Soundness and completeness of an axiom system for
  program verification", SIAM J. Comput. 1978; E. W. Dijkstra, "Guarded commands, nondeterminacy and formal
  derivation of programs", CACM 1975.
* J. Bloch, "Nearly all binary searches and mergesorts are broken", Google Research blog, 2006; J. Bentley,
  *Programming Pearls* (1986).
* J. C. Reynolds, "Separation logic: a logic for shared mutable data structures", LICS 2002; P. O'Hearn, J. Reynolds
  and H. Yang, "Local reasoning about programs that alter data structures", CSL 2001; C. Calcagno, D. Distefano,
  P. O'Hearn and H. Yang, "Compositional shape analysis by means of bi-abduction", POPL 2009; P. W. O'Hearn,
  "Resources, concurrency and local reasoning", and S. Brookes, "A semantics for concurrent separation logic", both
  Theor. Comput. Sci. 2007.
* A. Pnueli, "The temporal logic of programs", FOCS 1977; E. M. Clarke and E. A. Emerson, "Design and synthesis of
  synchronization skeletons using branching time temporal logic", Logics of Programs 1981; J.-P. Queille and
  J. Sifakis, "Specification and verification of concurrent systems in CESAR", International Symposium on Programming
  1982; E. M. Clarke, E. A. Emerson and A. P. Sistla, "Automatic verification of finite-state concurrent systems using
  temporal logic specifications", TOPLAS 1986; G. L. Peterson, "Myths about the mutual exclusion problem", IPL 1981.
* R. E. Bryant, "Graph-based algorithms for Boolean function manipulation", IEEE Trans. Computers 1986, and "On the
  complexity of VLSI implementations and graph representations of Boolean functions with application to integer
  multiplication", IEEE Trans. Computers 1991; J. R. Burch, E. M. Clarke, K. L. McMillan, D. L. Dill and L. J. Hwang,
  "Symbolic model checking: 10²⁰ states and beyond", LICS 1990; B. Bollig and I. Wegener, "Improving the variable
  ordering of OBDDs is NP-complete", IEEE Trans. Computers 1996.
* A. Biere, A. Cimatti, E. Clarke and Y. Zhu, "Symbolic model checking without BDDs", TACAS 1999; M. Sheeran,
  S. Singh and G. Stålmarck, "Checking safety properties using induction and a SAT-solver", FMCAD 2000;
  A. R. Bradley, "SAT-based model checking without unrolling", VMCAI 2011.
* P. Cousot and R. Cousot, "Abstract interpretation: a unified lattice model for static analysis of programs by
  construction or approximation of fixpoints", POPL 1977; M. Karr, "Affine relationships among variables of a
  program", Acta Informatica 1976; P. Cousot and N. Halbwachs, "Automatic discovery of linear restraints among
  variables of a program", POPL 1978; A. Miné, "The octagon abstract domain", Higher-Order and Symbolic Computation
  2006; B. Blanchet et al., "A static analyzer for large safety-critical software", PLDI 2003.
* R. Milner, "A theory of type polymorphism in programming", JCSS 1978; P. Cousot, "Types as abstract
  interpretations", POPL 1997; T. Freeman and F. Pfenning, "Refinement types for ML", PLDI 1991; P. M. Rondon,
  M. Kawaguchi and R. Jhala, "Liquid types", PLDI 2008.
* R. Milner, "Logic for computable functions: description of a machine implementation", Stanford AIM-169, 1972;
  M. Gordon, "From LCF to HOL: a short history" (2000); G. Gonthier, "Formal proof — the four-color theorem", Notices
  of the AMS 2008; G. Gonthier et al., "A machine-checked proof of the odd order theorem", ITP 2013; T. Hales et al.,
  "A formal proof of the Kepler conjecture", Forum of Mathematics, Pi 2017.
* X. Leroy, "Formal certification of a compiler back-end, or: programming a compiler with a proof assistant", POPL
  2006, and "Formal verification of a realistic compiler", CACM 2009; X. Yang, Y. Chen, E. Eide and J. Regehr,
  "Finding and understanding bugs in C compilers", PLDI 2011.
* G. Klein et al., "seL4: formal verification of an OS kernel", SOSP 2009; T. Sewell, M. O. Myreen and G. Klein,
  "Translation validation for a verified OS kernel", PLDI 2013; R. Kumar, M. O. Myreen, M. Norrish and S. Owens,
  "CakeML: a verified implementation of ML", POPL 2014.
* D. J. Bernstein, "Curve25519: new Diffie–Hellman speed records", PKC 2006; A. Erbsen et al., "Simple high-level code
  for cryptographic arithmetic — with proofs, without compromises", IEEE S&P 2019; J.-K. Zinzindohoué,
  K. Bhargavan, J. Protzenko and B. Beurdouche, "HACL*: a verified modern cryptographic library", CCS 2017.
* L. Lamport, "The temporal logic of actions", TOPLAS 1994; J. Gray and L. Lamport, "Consensus on transaction commit",
  TODS 2006; D. Ongaro and J. Ousterhout, "In search of an understandable consensus algorithm", USENIX ATC 2014;
  C. Newcombe et al., "How Amazon Web Services uses formal methods", CACM 2015; D. Jackson, *Software Abstractions*
  (2006).
* G. J. Myers, *The Art of Software Testing* (1979); R. A. DeMillo, R. J. Lipton and F. G. Sayward, "Hints on test
  data selection: help for the practicing programmer", Computer 1978; K. Claessen and J. Hughes, "QuickCheck: a
  lightweight tool for random testing of Haskell programs", ICFP 2000.
* B. P. Miller, L. Fredriksen and B. So, "An empirical study of the reliability of UNIX utilities", CACM 1990;
  C. Cadar, D. Dunbar and D. Engler, "KLEE: unassisted and automatic generation of high-coverage tests for complex
  systems programs", OSDI 2008; P. Godefroid, N. Klarlund and K. Sen, "DART: directed automated random testing", PLDI
  2005; A. Zeller and R. Hildebrandt, "Simplifying and isolating failure-inducing input", IEEE TSE 2002; G. Misherghi
  and Z. Su, "HDD: hierarchical delta debugging", ICSE 2006.
* A. Pnueli, M. Siegel and E. Singerman, "Translation validation", TACAS 1998; S. Rideau and X. Leroy, "Validating
  register allocation and spilling", CC 2010; G. C. Necula, "Proof-carrying code", POPL 1997; G. Morrisett, D. Walker,
  K. Crary and N. Glew, "From System F to typed assembly language", POPL 1998.
