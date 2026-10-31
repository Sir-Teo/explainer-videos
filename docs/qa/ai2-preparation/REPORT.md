# Part 2: independent test-only preparation

All four requested hypotheses were reproduced with tiny deterministic fixtures. These are bug reproductions, not a Part 2 QA pass. No source/tests, repository caches, training runs, chapter renders, narration, or commits were changed by this test process.

Evidence: `reproduce.py` (standalone executable fixtures), `results.json` (actual records and source hashes), and `run.log` (console output), all in `/workspace/runtime/ai2-test-preparation/`.

Run again:

```bash
cd /workspace/explainer-videos
source /workspace/runtime/activate.sh
NUMBA_DISABLE_JIT=1 PYTHONDONTWRITEBYTECODE=1 python /workspace/runtime/ai2-test-preparation/reproduce.py
```

The functions ran in Python mode with JIT disabled, so no compiled Numba cache was written. A process-local audit hook rejected any attempted write or mutation beneath `/workspace/explainer-videos`; its recorded write-attempt list is empty. The fixtures temporarily patched functions only in this process. Production JIT execution and full Part 2 computations remain untested here.

## 1. Travelling-salesman budget comparison

Exact APIs:

- `local.two_opt_climb(t, D, budget) -> (length, looked)` mutates `t`.
- `local.anneal(t, D, T0, alpha, moves_per_T, n_temps, seed, snap_every, snaps, trace) -> (best_length, best_tour)`.
- `local.genetic(D, pop_size, gens, p_mut, seed, best_per_gen, snaps, snap_gens) -> best_length`.

A six-city integer-distance fixture starts at tour `[0,2,4,1,3,5]`, length 71. Exact source-line events and `tour_len` calls were instrumented.

| Case | Observed result |
|---|---|
| 2-opt budget 1 | Nine candidate deltas evaluated, matching reported `looked=9`; budget check happens after the complete sweep. Returns original length 71 although the evaluated sweep contains a length-58 tour. The best move is discarded when the budget condition returns. |
| Annealing, seed 17, 4 temperatures × 5 proposals | 20 random-pair proposals, seven valid delta evaluations, 13 no-op draws skipped before evaluating a candidate. One initial full-tour evaluation. Returned best length 43 matches its returned tour and final trace best. |
| Caller budget 199 with 200 temperatures | `moves_per_T = budget // n_temps = 0`; actual call raises `ZeroDivisionError` at acceptance-rate calculation. This is a small-budget robustness defect; the default 2,000,000 budget is not affected by this zero quotient. |
| GA nominal budget 8, population 4, two generations, seed 1 | Twelve full `tour_len` evaluations: initial population plus two reevaluated populations. Generation trace is `[62,61]`; returned final best is 50. The last generation's improvement is retained by the return value but absent from `best_per_gen`. Repeated elite evaluation is included in these call counts. |

Source: `videos/ai/ai2/local.py:129–148`, `152–185`, `213–256`; caller `compute.py:339–362`. The comparison scene explicitly calls the nominal counts an equal budget of “tours looked at” in `s06_local.py:279–292`. Actual counting currencies differ: evaluated neighbor deltas, random proposals including no-ops, and full population evaluations. These fixtures establish the mismatch; they do not measure the default berlin52 result ordering or justify a new ranking without recomputation.

Suggested regression contract for the eventual fix: define and save a common actual-evaluation budget; never exceed it; handle budgets smaller than schedule/population sizes; include or explicitly exclude initialization consistently; retain the best evaluated candidate and record the final result in replay data. No fix was made in this preparation.

## 2. A* heuristic dominance claim

The repository has fixed-domain `search.grid_search(free,sr,sc,gr,gc,wg,wh,moves)` and `search.astar8(start,kind)`, not a general weighted-graph A* API. Both use the actual `_heap_push`/`_heap_pop` helpers. Grid keys use `f - 1e-7*g`; 8-puzzle keys use `g+h - 1e-3*g`, favoring larger `g` at equal `f`.

The requested graph was run through those actual heap helpers in a small graph adapter, using each exact priority formula:

- Edges: S→A:1, A→G:9, S→B:5, B→G:10.
- h1(S,A,B,G)=(0,0,5,0); h2=(0,9,5,0).
- Assertions verify both heuristics are consistent and h2 dominates h1.
- h1 pops **S,A,G**; h2 pops **S,B,A,G**. Both find optimal cost 10.

The grid API includes the goal pop in its returned expansion count and exposes `order`; `astar8` excludes the goal and returns no order trace. The counterexample is 3 vs 4 pops including goal, or 2 vs 3 expansions excluding it. It reproduces the theorem-framing overclaim at `s05_heuristics.py:117–129` under either counting convention. It does **not** establish a correctness failure in the fixed-domain grid or puzzle implementations. The extra work is on the `f=C*` boundary; the blanket “never expands more” sentence requires tie qualifications.

## 3. First-order resolution

Exact API: `logic.refute(kb, negated_goal, strategy="saturate", max_clauses=20000)`. Literals are created with `logic.lit(sign, predicate, *args)`; each clause is a `frozenset`.

| Fixture | Expected | Actual |
|---|---|---|
| KB `{P(x)∨P(y), ¬P(x)∨¬P(y)}`, no goal clauses, saturation limit 64 | Contradiction | `found=False`, saturated at level 2 after deriving only the additional mixed clause `P(x)∨¬P(y)` |
| KB initially contains empty clause | Immediate contradiction | `found=False`, level 1, despite displayed `□` |
| Empty clause in negated goal, support strategy | Immediate contradiction | `found=False`, level 1 |
| Positive unit `P(x)` versus negative unit `¬P(A)` | Contradiction sanity check | `found=True`, proof `[0,1,2]` |

The first KB is unsatisfiable under universal closure: setting x=y gives both P(z) and ¬P(z). Binary resolution alone lacks the required factoring step. The initial-empty cases are separate input-handling defects. Source: `logic.py:110–175`.

## 4. SAT unknown/censored outcomes

Exact API: `sat.solve_dpll(clauses, n, max_decisions=10**9) -> (status, decisions)`, where status 1=SAT, 0=UNSAT, -1=gave up. Actual three-variable calls returned:

- Single satisfiable clause with limit 100: `(1,1)`.
- All eight three-literal sign combinations, with limit 100: `(0,3)`.
- Single satisfiable clause with limit 0: `(-1,0)`.

`compute.compute_sat3(ns=(3,), alphas=(1.,2.,3.), per=(3,))` was then executed with its `Partial` replaced by an in-memory dict and its solver wrapper routed to nine of these actual tiny calls. No partial/completion cache was written. Controlled cells contain `(SAT,SAT,unknown)`, `(SAT,UNSAT,unknown)`, and `(UNSAT,UNSAT,unknown)`.

Actual `psat_3` is `[2/3,1/3,0]`, with no unknown/censor counts or flags. Its median/mean/q90 decision summaries also combine completed and truncated runs. `(st == 1).mean()` at `compute.py:622` treats an unknown as a non-SAT result in the denominator, so the value is only a lower bound on the full-sample SAT fraction when unknowns exist. For these fixtures, honest full-sample bounds are `[2/3,1]`, `[1/3,2/3]`, and `[0,1/3]`; unknown fraction is 1/3 in each cell. The resolved-only fractions `[1,.5,0]` are descriptive conditional statistics, not unbiased replacements for overall SAT probability: hard-instance censoring can be informative. Crossing/width estimates should remain marked censored or unresolved when their underlying cells are unresolved.

These runs establish aggregation behavior only. They do not show whether the default billion-decision cap is reached in the production sweep, and the full random-SAT sweep was not run.
