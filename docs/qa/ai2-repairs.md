# Part 2 correctness preparation

This is source repair and small-fixture validation while Part 1 finishes sequential QA. It is **not** a Part 2 production, rendered, or playback pass. The initial preparation did not run production compute jobs. The later pure default-resolution regression runs the actual small family example without loading or saving the production cache; root owns persistent computation jobs. No scene render, narration synthesis, commit, or push was performed by this preparation agent.

The four source defects reproduced in [the original preparation](ai2-preparation/REPORT.md) are repaired:

- TSP comparison now caps actual candidate-cost evaluations, including initialization. A valid 2-opt delta and a scored genetic child each count once; this does not equalize CPU time. No-op annealing draws consume no evaluation. 2-opt retains the best evaluated improvement when a budget ends mid-sweep. Genetic elites reuse stored scores, initialization is charged, partial generations preserve evaluated children, and the final trace includes the returned best. The comparison records per-method counts and checks the requested budget exactly. Zero-move schedules and budgets smaller than a population no longer divide by zero or overrun the cap.
- A* dominance wording now qualifies consistent heuristics and the mandatory `f<C*` states. Work on the `f=C*` boundary depends on ties. The existing measured curves remain measurements; the total-expansion overclaim is removed.
- First-order resolution includes factoring and recognizes initially empty clauses. Unary factors appear in proof records and the Part 2 proof layout accepts one or two parents. Self-resolution standardizes variables apart. Set-of-support propagation handles existing and pending duplicate clauses; newly promoted support revisits pairs previously skipped. Resource exhaustion is explicitly `limit`, distinct from `saturated` or `refuted`. Set-of-support completeness assumes satisfiable background clauses.
- Random SAT keeps SAT, UNSAT and unknown outcomes separate, with full-sample SAT lower/upper bounds. Completed-run decision summaries exclude censored runs and remain explicitly conditional. Observed-work summaries and raw per-cell statuses/decisions are retained separately, with the decision cap. Censored sweeps do not fit a threshold crossing, width or completion-work peak. Missing bracketed crossings return unresolved instead of wrapping to the last interval. Scene and recap branches show bounds when censored and describe observed work rather than completion work.

`tsp` and `sat3` use Part 2 schema version 2; `resolution` uses version 3 so version-2 explosion summaries missing stopping status/cap cannot be reused. Normal loads/CLI recompute stale completion files under the existing item lock. Changed SAT partial parameters invalidate incompatible cells. Cached-only QA must reject stale data before entering the loader; the root agent owns that shared guard. Old production caches and rankings are not evidence for the repaired implementations.

Validation: `python -m unittest discover -s tests -p test_ai2_correctness.py -v` exercises score-call and delta-line counts, actual Numba kernels, factoring/refutation/support propagation, initial contradictions, self-resolution, SAT statuses/censoring and cache upgrades. A geometry-only proof-layout check uses synthetic boxes (no LaTeX or rendering). Source-based narration checks exercise the actual changed English expressions and Chinese templates, including both censored and uncensored branches and bookmark preservation. Part 2 compilation and `git diff --check` also pass.

Chinese narration updates are applied only in `videos/ai/ai2/zh_lines.py`. `tools/zh_lines.py ai2 --todo` reports 119/119 source lines covered after the stopping-outcome correction. It retains one pre-existing ambiguity warning for the displayed `try {NAMES[v]} {true/false}` label; this is not a new narration branch and was not expanded into another repair. Ten new global caption translations are handed to the root agent separately; global table ownership remains with root.

Remaining: root review, global caption merge, full production recomputation of affected items, bilingual endpoint/motion renders, actual full playback/listening/sync review, pacing and production-resolution validation, and regression of changed data across every dependent chapter. No default benchmark ranking, default SAT censoring frequency, or full-series production readiness is claimed.

The real default resolution example exposed an additional reporting defect: all-pairs search stops at the unchanged 4,000-clause cap without finding a proof, while set of support finds one after 2,823 recorded clauses (15 in its proof). Schema 3 retains each method's stopping status and clause cap. The scene now reports clauses recorded at stopping, including inputs, rather than claiming both bars measure clauses before a found proof. English/Chinese branches distinguish refutation, cap exhaustion, and no-new-clause saturation for both methods. Actual scene AST branch tests cover every outcome and preserve bookmarks; the default-resolution regression validates the real capped result without writing a cache. The algorithm and resource cap are unchanged. Global outcome-label translations are provided separately for root to merge.

Root verification: all116 current repository tests pass, including32 Part2 and6 temporal-audit regressions.
The real default TSP run completed in26seconds; each of three methods used exactly2,000,000 evaluations for each
of five seeds. Resolution recomputation confirmed the saturation cap at4,000 clauses and support proof with2,823
recorded clauses. Schema3 and all six bilingual outcome branches preserve that distinction.
[Actual values and source/data hashes](evidence/ai2-correctness/default-tsp-resolution.json) are retained.
Global caption handoffs have now been merged by root. Full Part2 benchmark/render/audio QA remains pending.

The complete16-chapter source review and a second bilingual correction batch are now applied.
[Head and tail records](evidence/ai2-source-review/) preserve coverage, primary references, fixed findings and
limits. Corrections include exact versus cutoff alpha-beta values; equal optimal cost versus identical paths;
sampling/baseline units; relaxed-planning complexity; MYCIN rating units; ELIZA historical provenance; multiplier
proof/search distinctions; PDDL-model assumptions; and the first-moment exercise explanation.

All19 default numerical items have now completed. SAT completed in453seconds with zero unknown outcomes in
its default sweep; CDCL completed in131seconds and blocks in32seconds. Current corpus/testset/model calculations
are genuine seeded runs. The source/translation batch passed all126 repository tests, whole-AI compilation,
diff checks and119/119 Part2 narration-source coverage. One pre-existing adjacent-value display-template warning
remains documented. Full Part2 endpoint, motion, audio, pacing and production-resolution checks remain pending
while Part1's complete dense transition review finishes. Future capped PDB-optimum handling remains a documented
conditional defect to repair before broader parameter variations; current30 default PDB cases all completed.

## Search and planning capped-result follow-up

Conditional capped-result defects are now repaired. Puzzle optimal lengths come from any completed admissible solver; unknown lengths are omitted and counted. Work comparisons use matched completed runs. Planning separates solved, capped/unresolved and not-run cases; failed -1 sentinels never enter solution-length averages. Current default PDB cases all completed, and all attempted default block problems solved; these were conditional reporting bugs, not evidence that those default runs failed.

Grid priority is now exact lexicographic (f, -g, node). The former epsilon subtraction returned a suboptimal path for a valid tiny positive cost scale; real Numba regression tests cover that reproduction. Grid and puzzle caches have versioned schemas and were regenerated (3 and 40 seconds respectively). Current file hashes and the original handoff limits are preserved in the source-review evidence directory.

All 143 repository tests passed after these repairs. Compilation and diff checks passed; 132/132 narration source lines are covered, with the previously documented adjacent-value template warning. Bilingual endpoint renders are now running and have already exposed three comma-materialized untranslated captions and one malformed Chinese TeX separator, corrected in the shared table. Current layout, motion, pacing, audio and full playback review remain in progress. No CI/CD was created.
