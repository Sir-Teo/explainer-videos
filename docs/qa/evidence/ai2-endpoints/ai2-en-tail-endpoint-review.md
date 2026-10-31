# Part2 English tail endpoint review

Inspected all 156 endpoint thumbnails across Logic, SAT, Plans, Knowledge, ELIZA, Winters, Survives and Outro, with 12 native priority frames. Refreshed Plans Chinese sheet adds 24 endpoint thumbnails and 2 native panel frames. This is sampled endpoint QA, not playback or listening.

The only confirmed concern was the original Plans coverage footer being too small. The revised right-column panel is rendered and inspected in both languages: primary counts are clearer, all counts and matched cases are preserved, and axes, legend, comparison and history footer remain separated. The native English BFS row increased from 9 to 15 pixels in foreground height. Before/after source and image SHA256 evidence is preserved in the companion JSON.

| Scene | EN endpoints | Input signatures current | Snapshot warnings |
|---|---:|---|---|
| Logic | 22 | True | source-changed-during-render |
| SAT | 26 | True | None |
| Plans | 22 | True | None |
| Knowledge | 20 | True | None |
| Eliza | 14 | True | None |
| Winters | 21 | True | None |
| Survives | 26 | True | None |
| Outro | 5 | True | source-changed-during-render |

Logic: Truth table entailment, quantified rule and three history cards, propositional/first-order resolution DAG, empty clause, factoring/no-cap caveat and actual capped all-pairs-vs-proved set-of-support results inspected. Refreshed rectilinear edges do not run through text.
SAT: DPLL formula/tree, random 3-SAT transition and observed-work graphs, CDCL first-conflict DAG/learned clause, ripple-carry/Kogge-Stone comparison inspected. No graph or caption clipping confirmed.
Plans: Constraint puzzle/AC3 candidates,313 deletions and search counts, STRIPS delete lists, Sussman interleaving, observed-work curves and new matched/coverage panel inspected. All defaultcounts preserved. Tiny original coverage concern repaired and EN/ZH endpoint regression passes.
Knowledge: Semantic network/default exception, expert-rule chain, positive certainty-factor0.6 → 0.8 → 0.88, MYCIN acceptability rating denominator and caveat, Cyc and knowledge graph inspected.
Eliza: Pattern substitution,15 historical-turn outputs (14 exact),new illustrative replies, attributed secretary account, recovered original versus separate Python DOCTOR 2025 study distinction inspected.
Winters: Historical funding/limits cards, two qualified winter windows, Moravec contrast, actual cumulative token-frequency curve and held-out unseen words inspected.
Survives: DeepBlue/AlphaZero, adder proof/broken-bit counterexample, multiplier difficulty qualification, machine-checked proof sketch, PlanBench bars and renamed-case caveat, LLM+P validity in given PDDLmodel, networks/symbols loop inspected.
Outro: All 8 mini-cards, roadmap,6 exercise equations, next-part word vectors and complete references inspected. Only 5 narration endpoints exist; reveal transitions are not manually covered by this endpoint pass.

No confirmed remaining endpoint clipping, overlap or misleading rendered branch was found in this scope. Small dense symbolic terms/reference text were checked at native size. Logic/Outro retain source-change warnings; aggregate source freshness is not certified by this report. Exact snapshots, timestamps and hashes are in JSON. Full-motion Plans review remains separate.
