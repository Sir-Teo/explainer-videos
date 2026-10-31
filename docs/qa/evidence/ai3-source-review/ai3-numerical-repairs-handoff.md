# Part 3 numerical producer handoff

No production computation, downloads, model training, cache writes or renders were launched. Source is frozen pending independent feedback. Source SHA256: `b69d3281f4f5e8d34867de976d98cc9e4268a0a1fd6bcc9631b6ce9bc5f45a3a`.

## Affected persisted items

- **norms** (schema 1): Adds explicit single MLP-shaped random reference shape/seed; numerical comparison preserved, scene qualifies verdict.
- **mp** (schema 1): Uses both empirical CDF sides for KS tail selection; strict above-edge counts match plotted limiting edge; edge rule and unavailable-fit diagnostics explicit.
- **galore** (schema 1): Preserves measured NS singular-value history; adds true Frobenius initialization, coefficients, iteration count and dtype metadata.
- **words** (schema 1): Explicit self mask/stable ties/nonzero neighbour policy; authenticated current corpus bytes, exact ordered vocabulary and recipe; avoids Part1 memoized text.
- **sgns** (schema 1): Same corrected neighbour semantics; raw corpus/token/subsampled-sequence/negative-distribution/ordered-vocabulary/settings lineage; atomic checkpoint contract and completed item; exact words alignment; actual loss/snapshot steps.
- **jl** (schema 1): Explicit delta .05 / confidence .95; inverse two-tail union failure bound <=delta; NaN unavailable for epsilon<1; unchanged measured projections on future computation.
- **mf** (schema 1): Mean and bias final baselines fit train|valid, matching final low-rank models; tuning remains train/valid; split fingerprint/fitting counts, exact without-self genre chance.
- **twotower** (schema 1): Standard macro recall over distinct unseen targets, full eligible-target denominator, explicit empty cohort NaN/counts; raw conditional-score inference default, prior-added outputs labeled ablation.

Normal loaders and compute CLI invalidate legacy/recipe-mismatched data under the item lock. Cached-only QA detects missing/stale data before an upgrading loader; it never trains or recomputes. Both completed words/SGNS artifacts and resumed SGNS checkpoints bind corpus bytes, exact vocabulary row order and settings. Unreadable checkpoints fail closed and stay available for inspection.

## Validation

Focused numerical, integration and visual-math tests: see `ai3-numerical-integrity-math-tests.log`. Includes real tiny Torch serialized-resume equivalence, rejection without live mutation, actual cached-only worker interception, consumed-corpus freshness, standard recall, raw/prior ranking, SciPy KS comparison, self ties, MF fitting masks and JL confidence/geometry. No full model measurements are implied.

## Future compute workload

- **norms**: 48 GPT-2 block SVDs plus one 768x3072 random SVD and 75 small conditioning trials; no benchmark wall time measured.
- **mp**: Random + shuffled + 48 GPT-2 ESDs, then trained/fresh novels-model block ESDs; requires authenticated GPT-2 and novels models. No wall time measured.
- **galore**: Up to 16 seeded 600-step transformer runs (track, 9 learning-rate candidates, 6 extra seeds); resume authenticated existing parameter-matched partial pieces. GaLore control item is unchanged.
- **words**: Corpus normalization/counting, symmetric window4 sparse 10000x10000 table and rank100 sparse SVD. No wall time measured.
- **sgns**: 3 passes over P symmetric pairs: 3*ceil(P/4096) stochastic Adam updates, plus 3x3000 full-objective 300-word diagnostics. Checkpoint after each pass. Existing legacy/mismatched checkpoint preserved under digest-qualified rejected name; unreadable checkpoint aborts preserved. No full run measured.
- **jl**: GPT-2 vectors; 5 initial projection maps, then 9 dimensions x5 seeds on 1000 points/all499500 pairs. No wall time measured.
- **mf**: 30 validation fits +18 final seeded rank fits +2 replay fits +1 bias fit, each40 epochs (51 fits/2040 epoch passes). Also final4000x1200 completed-matrix SVD. No wall time measured.
- **twotower**: 3000 minibatch512 training updates plus11 full warm/cold evaluation checkpoints; corrected metric needs re-evaluation/retraining because old outputs have no saved model/rankings. No wall time measured.

Scene data-key handoffs sent to motion_foundations and motion_theory; local Chinese narration is owned by ai1_review. No shared captions or scene files edited by this owner. The complete report contains exact source/base provenance and remaining untested scope.


## GPT-2 tie follow-up

Source SHA256: `2b03a02de9ae201a9955f6a88ed56f6433b5d0602186c5a3978cd4d565a616e2`. The neighbour loop now ranks stably, explicitly removes the query index, and retains the original 79-other-token search budget, case/duplicate/nonalpha guards, and six-result cap. GPT-2 now also has schema 1 and a matching recipe entry. Two tiny fixtures execute the actual loop: tied query not first retains the valid first neighbour, and out-of-budget candidates remain excluded. This is a conditional tie repair, not an observed production GPT-2 defect. No production run launched. Test log: `ai3-gpt2-neighbour-followup-tests.log`.
