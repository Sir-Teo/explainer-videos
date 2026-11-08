# Philosophy, Built: QA and polish

The source and silent visual QA pass is **complete** at `philosophy-built`
commit `548166a2` for all 42 parts, 678 scenes, and both English and Chinese
editions. All 1,356 scene/language cases passed against that source snapshot
and its computed inputs. Each has a visually inspected explanatory sample
bound to its captured image.
Verification covers silent narration-beat endpoints and sampled frames;
narrated playback and final master review remain unverified.

Unless stated otherwise, the checks and generated evidence below describe that
pre-merge snapshot. The merge into `main` preserves this evidence and its original
fingerprints; it does not relabel the captures as current for the combined tree.

## Completed checks

- All 1,356 scene/language cases completed with **zero endpoint warnings**.
  The captures contain 27,894 narration-beat endpoint frames. Every case has
  valid sampled-frame review evidence; the final coverage audit has zero issues.
- Final English and Chinese `--resume --cached-only` scans completed successfully.
  Evidence is current to source fingerprints and actual computed-input hashes.
- 343 tests and 1,048 subtests passed, including the philosophy Reasoner suite,
  translation, text wrapping, timeline layout, and QA provenance tests (one
  dependency deprecation warning).
- All philosophy Python sources compiled.
- All 650 computation items across the 42 parts completed without exceptions;
  the cache inventory has no missing items. Logs and the inventory are under
  `renders/qa/philosophy-compute*`.
- All 3,425 narration source entries have Chinese translation-table coverage.
  This checks source coverage, not spoken pronunciation or every computed splice.
- All 42 English opening title cards were typeset and measured; all fit inside
  the review margins (13.4 by 7.2 scene units).
- All 42 README chapter tables were compared with their manifests. Part 1 was
  missing the Arabic logic chapter; its table and subsequent numbering are fixed.
- All 594 numbered chapter cards and spoken introductions agree with the
  manifests in both languages. All 678 Chinese chapter metadata titles are
  present and their chapter numbers agree. Evidence is in
  `renders/qa/philosophy-chapter-numbering.json` and
  `renders/qa/philosophy-chapter-metadata.json`.

## Repairs and their evidence

| Part / scene | Repair | Verification |
| --- | --- | --- |
| 1 / Hook | State the existence assumption behind traditional Darapti; replace the claim about every modern textbook with the modern classical reading. Update Chinese narration and the on-screen caption. | English endpoint: 16 frames, no warnings. |
| 1 / Argument | Bring the premise/conclusion braces inside the frame. Keep the translated formulas in separate columns. Show the validity card during the introductory narration instead of leaving a blank screen. | English and Chinese endpoints: 20 frames each, no warnings. |
| 1 / Zeno | Keep Achilles's initial label inside the frame. Show Parmenides during his introduction and the series terms during the limit explanation; reveal the sum when it is explained. | English endpoint: 19 frames, no warnings. |
| 1 / Euthyphro | Show the first horn during the dilemma's introduction, removing a blank interval under narration. | English and Chinese endpoints: 15 frames each, no warnings. |
| 1 / Import | Separate the full count of 24 moods, including subaltern conclusions, from the medieval mnemonic. Qualify historical existence assumptions. Narrow the central explanation so it clears the surrounding claims. | English and Chinese endpoints: 13 frames each, no warnings. |
| 2 / Boole | Correct the derivation's invalid layout boundary; clear the graph as the centered derivation starts, retaining it through the spoken lead-in. | English endpoint: 23 frames, no warnings. Silent motion render: 265 seconds, no blank runs of at least 1.5 seconds. |
| 2 / Hook, Soundness | Remove the brick number under the question mark; place the countermodel verdict below the argument instead of over its card. | Both languages: no endpoint warnings or text-overlap candidates. |
| 3 / Hook, Proof, Compact | Clarify nontermination on invalid inputs, the role of term substitution in cut elimination, and the pure-equality qualification of the infinitude claim. Update Chinese narration. | All 16 chapters rendered in both languages without visual flags. |
| 3 / Tableau, Lindstrom | Wrap the captions beside the proof tree and EF game inside their columns. | Both languages: no endpoint warnings. |
| 4 / FMP | Label the complexity table as SAT. Distinguish S5 satisfiability (NP-complete) from validity (coNP-complete), and qualify the named decidable propositional systems. | English and Chinese endpoints: 19 frames each, no warnings; revised table frames inspected. |
| 19 / Games | Correct the reversed tie-payoff explanations and inward/outward panel data. Penalized ties stabilize the equal mix; rewarded ties destabilize it. Keep vertex labels within their panels. Upgrade old RPS caches before builds and reject them in read-only QA. | Trajectory invariants and cache migration/guard checks pass; English and Chinese endpoints: 24 frames each, no warnings. Revised panels inspected in both languages. |
| 21 / Copies | Show the uploading definition during the opening narration, replacing a near-empty hold on a two-character Chinese heading. State that the model-instance example compares independent runs without shared conversation histories. | English endpoints: 33 frames; Chinese: 34. No warnings. Revised opening and both explanatory overviews inspected. |
| 25 / Hands | Move Kant's three claims into the upper-right column so the Chinese explanation clears the history card. Preserve the hand comparison and reveal timing. | English endpoints: 23 frames; Chinese: 25. No warnings. Enlarged revised frames inspected in both languages. |
| 28 / RSA, Vectors | Bring the reference-game row labels inside the frame. Keep corpus lexemes as model data in both editions, fit the neighbor table, and separate the animal/Darwin plot labels. | Focused bilingual checks have no warnings or overlap candidates; full explanatory overviews and enlarged repaired frames inspected. Whole-part current-source checks pass. |
| 29 / Signs | Replace fixed coordinate/correlation/group snapshots with invariant checks and measured on-screen values. Keep both narrations consistent with the computed data. | Both languages: 28 endpoints, no warnings. Revised rotation enlarged; all 17 explanatory chapter samples inspected per language; no overlap candidates. Whole-part current-source checks pass. |
| 30 / Represent | Wrap the expanded Chinese varitel-semantics label inside its left column. | English: 21 endpoints; Chinese: 22. No warnings or overlap candidates. Enlarged repaired row inspected; all 15 chapter samples reviewed per language. Whole-part current-source checks pass. |
| 31 / Zombies | Remove the caption claiming that a zombie's words mean nothing; the thought experiment stipulates absence of conscious experience. | Both languages: 21 endpoints, no warnings. All 17 chapter samples reviewed per language, including enlarged Chinese colour-discrimination and simplified-Φ diagrams. No overlap candidates. |
| 32 / Compatibilism | Fit the 61-cell Lewis automaton into its left column instead of setting an oversized height that clipped the grid and time label. | Both languages: 31 endpoints, no warnings; enlarged grids inspected. All 16 chapter samples reviewed per language, with no overlap candidates. Whole-part current-source checks pass. |
| 33 / Kelly | Replace the claim that one never-losing path carries expected wealth with rare histories containing unusually many wins. Highlight the expectation column during that explanation; update Chinese narration. | Both languages: 23 endpoints, no warnings. Enlarged comparison tables and all 17 chapter samples inspected; no overlap candidates. Exact binomial weighting checked in `philosophy33-kelly-expectation.json`. |
| 35 / Welfare | Lift the experience-machine claims and De Brigard annotation above the survey bars. | English: 17 endpoints; Chinese: 18; no warnings. Both enlarged repaired frames and all 14 chapter samples per language inspected. |
| 36 / Effective | Include disability severity weights in DALYs; define YLL and duration in both narrations. Qualify the simplified QALY scale. | English: 20 endpoints; Chinese: 21; no warnings. Enlarged formulas and all 13 chapter samples per language inspected; no overlap candidates. |
| 37 / Realism, Equilibrium | Wrap the twin-earth planet captions into separate columns and constrain the equilibrium legend inside the frame. | Bilingual focused checks: 31/32 and 26/26 endpoints, no warnings. Enlarged repaired frames and all 13 chapter samples per language inspected; no overlap candidates. |
| 39 / Rules, Jury | Qualify the IRV minimum to the implemented search restrictions and show its vote reversal. Wrap chart captions before aligning the jury-probability and diversity panels. | Bilingual focused checks: 35/36 and 25/25 endpoints, no warnings. Enlarged repaired frames and all 13 chapter samples per language inspected; no overlap candidates. |
| 40 / Greeks, Harmony, Outro | Show the first rasa definition during the introduction. Specify positive integer powers in the tuning proof and exercise; explain parity after clearing denominators. Correct harmonic coincidence to the lower third and higher second partial at 3:2. | Bilingual focused checks: 19/20, 25/25, 15/17 endpoints, no warnings. All 13 chapter samples per language and enlarged repaired formulas/exercises inspected; no overlap candidates. |
| 41 / Criteria, Impossible | Apply the independence criteria to the same prediction, state perfect/uninformative exceptions, distinguish scores from separately adjusted decisions, and use class-average scores in the Kleinberg Price List. Qualify the PPV boundary cases and show the imperfect-score assumption beneath the Wall card. | All 13 chapters checked and sampled per language; enlarged formulas, identity, Price List and qualified Wall card inspected. No warnings or overlap candidates. Fairness tests and exact rational counterexamples pass. |
| 41 / Privacy, Discrimination, Explain | Use probability densities for the continuous Laplace ratio; explain its implication for output ranges. Separate reconstruction bars, captions and the calculation note. Wrap proxy/explanation captions before aligning them and give Shapley values their own column. | Both privacy checks: 25 endpoints, no warnings. Enlarged probability plots, reconstruction charts, Shapley bars and proxy example inspected; no overlap candidates. |
| 42 / Goodhart, OffSwitch, Wall, Leibniz | Wrap optimization captions before placement and align off-switch equations after fitting. Remove numbered placeholders when named Wall bricks appear. Update the count to 271 test functions and qualify model calculations versus cited empirical figures. | All 13 chapter samples per language inspected, with enlarged pressure plots, game trees, source statistics and staged Wall frames. No warnings; all 66 placeholder-overlap leads resolved. Source and cached statistics agree: 47 modules, 23,963 lines, 1,040 public functions, 271 test functions. |
| Documentation | Qualify computational-provenance claims in the series overview and affected READMEs; align example metrics and exercise notes with computed results. | Chapter tables and metadata still agree with the manifests; numerical model outputs and cited empirical figures are distinguished. |
| Shared timeline | Preserve edge-label gaps and show readable dates when a year's combined event names crowd the strip. Chapter history cards retain the relevant names. | Chinese Axial and Lewis cards inspected; four regression cases cover both edges, long names, row crowding, and duplicate glyphs. |

Across Parts 4–42, 99 introductory reveals in 77 scene files now show a relevant
visual before the first narrated hold. Three first-iteration reveals in Parts 4
and 5 and additional lead-ins in Parts 1–3 are also repaired. Subsequent staged
reveals retain their bookmarks. The ordered bilingual scan has verified these edits.

Boole's motion scan flags one 2.8-second sparse interval around 163 seconds.
The inspected transition shows the first equation being written and its reason
appearing. This is an accepted sparse reveal; the automatic warning remains in
the evidence. Contact-sheet inspection and selected transition frames do not
constitute a full narrated playback review.

## QA tooling

`tools/qa_series.py` now fingerprints the requested series, its shared language
table, the part's sources, and referenced parts. Previously it always searched
the AI tree, allowing philosophy source changes to leave cached evidence current.
A regression test checks source, translation, and dependency invalidation.

The evidence report supports `--series philosophy` and writes a separate
`renders/qa/series/index_philosophy.html`. Reviewed image hashes must belong to
the current capture and match its bytes; sampled-frame review is recorded
separately from full motion and narrated playback.

Finished TeX SVGs are reused through an immutable pool. Each worker retains its
own scratch directory so Manim's cleanup cannot delete another worker's files.

## Coverage and limits

At the reviewed commit, all 42 parts have passing endpoint captures and sampled
visual evidence in both languages. At least one dense explanatory endpoint per scene/language
was inspected; repaired and suspect frames were enlarged. This does not claim
visual inspection of every animation frame.

The global text-overlap scan has no unresolved leads. Its two remaining leads
are Part 12's English and Chinese diversity formulas: their union bounding boxes
include empty space above separate labels. Both current frames were inspected
enlarged and accepted, with image hashes in `philosophy-overlap-review.json`.

Three selected full **silent** motion renders were decoded and scanned:
Argument (Chinese, 183.20 seconds), Boole (English, 265.00 seconds), and Games
(English, 230.53 seconds). Their contact sheets and selected transition frames
were inspected. Boole's accepted sparse-reveal warning remains recorded above.

Narrated playback/listening, speech synchronization, final-resolution review,
subtitles, chapter joins, and final master exports remain unverified. The
narration server was unavailable in this workspace, which contains no philosophy
master exports. Silent endpoint timing estimates do not verify final neural
narration timing.

## Merge validation

The integration combines philosophy commit `548166a2` with `main` at
`90fa999a`. The shared QA tools retain Statistics' per-video reports and
cross-series dependency fingerprints alongside Philosophy's sampled-image
proofs and isolated TeX workers. Both courses remain documented in the root
README and contributor instructions.

- The focused shared QA regression suite passed: 21 tests and 2 subtests.
- After the integration fix, all 345 philosophy and shared-text regression
  tests passed, with 1,048 subtests (one dependency deprecation warning).
- The combined worker/render regression sequence passed: 33 tests and 33
  subtests. It checks that a failed worker restores its TeX hook before later
  text rendering; the merge uncovered and fixed a leaked temporary-pool hook.
- Fresh silent endpoint checks for Argument (Part 1) and Privacy (Part 41),
  each in English and Chinese, passed with zero warnings. All 90 captured PNGs
  match the reviewed pre-merge captures byte for byte. Source fingerprints and
  computed-input hashes were checked against the combined tree.
- All Python sources in `explainer`, `tools`, `videos/philosophy`, and
  `tests/philosophy` compiled successfully.

The render receipt is tracked in
[`evidence/philosophy-merge-20261108/render-smoke.json`](evidence/philosophy-merge-20261108/render-smoke.json).
Fresh captures are isolated under `renders/qa/philosophy-merge/series/` so the
original 1,356-case evidence and provenance remain intact. The combined tree's
broader dependency fingerprints can invalidate earlier captures; the four
fresh smoke checks do not stand in for a new full-series render pass.

A broader test attempt recorded 1,766 passes and two failures before being
stopped during the statistics numerical tests (690 seconds). One was the TeX
hook leak fixed above. The other is the existing AI Part 4 optimizer test
`test_actual_optimizer_failure_survives_without_hoped_outcome_assertions`:
its assertion requires a strictly positive equality residual, but the installed
solver returns zero even when the iteration cap is reached. The identical
failure was reproduced on unchanged `main` at `90fa999a` (812 other tests and
2,335 subtests passed in that baseline sequence). This is not a full-suite pass.
Logs are preserved beside the render receipt.

## Evidence and regeneration

Generated pre-merge evidence is under `renders/qa/`:

- `philosophy-series-completion.json`: all 42 parts, 1,356 current cases,
  1,356 reviewed cases, zero endpoint warnings and zero audit issues.
- `series/index_philosophy.html`: browsable scene results, images and logs;
  sampled visual, motion and audio evidence are reported separately.
- `series/review.json`: inspected-frame hashes and review scope.
- `philosophy-test-results.log`: the selected regression suite.
- `philosophy-final-verification.json`: consolidated checks and playback scope;
  `philosophy-report-links.json` records 4,077 working local evidence links.
- `philosophy-compute-inventory.json` and `philosophy-final-inventory.log`:
  650 computation items, none missing; cached Reasoner statistics match source.
- `philosophy-source-translations.json`: 3,425 source entries, none missing.
- `philosophy-chapter-numbering.json`, `philosophy-chapter-metadata.json`,
  and `philosophy-cards/titles.json`: chapter and title checks.
- `philosophy-overlap-candidates.json` and `philosophy-overlap-review.json`:
  the two accepted bounding-box leads and their current image hashes.

Each `series/philosophyN/{en,zh}/Scene/` directory contains `result.json`,
endpoint images, a contact sheet and a render log. The completion audit and
report require current source/data and image-byte membership in the capture;
stale results were rendered again during the pre-merge pass.

To regenerate the standard checks from the repository root:

```bash
python tools/qa_series.py --series philosophy --lang en --resume --cached-only --timeout 900
python tools/qa_series.py --series philosophy --lang zh --resume --cached-only --timeout 900
python tools/qa_report.py --series philosophy
```

The regression command used for this pass:

```bash
python -m pytest -q tests/philosophy tests/test_qa_integrity.py \
  tests/test_qa_report_series.py tests/test_qa_series_fingerprint.py \
  tests/test_wrapped_lines.py tests/test_zh_numeric_grouping.py \
  tests/test_zh_templates.py tests/test_text_zh_add.py \
  tests/test_philosophy_timeline_layout.py
```

For this cloud workspace, first source `/workspace/environment/activate.sh` to
expose the installed rendering tools. The repository README describes the
narration service needed for narrated builds.
