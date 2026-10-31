# Part3 independent QA integrity review

Independent Part3 cache/provenance/statistical source review and small integration fixtures. No production computation/data download/rendering/audio/CI, no source edits outside one owned test file.

Frozen focused run: **18 tests passed**, zero failures/errors; compute SHA `e7640aef00128d58e3faf18b697c36be01a1d862ba4fb479aab9edc10a08522a` unchanged across run. Eight new independent tests are in `tests/test_ai3_qa_integrity.py`; ten numerical producer tests belong to ai2_fixes. Part3 production cache remains absent.

## Repaired findings

- **AI3-QA-01:** Part1 text memoization can return old normalized corpus tokens while a fresh raw train.txt hash is stamped into lineage. Owner changed book_words to read/authenticate the same raw artifact bytes and normalize directly with ai1.to27; tested.
- **AI3-QA-02:** The initial restore helper mutated both live embeddings before malformed optimizer restore raised ValueError; caller then caught it and continued as fresh. Owner preflights independent copies/models/optimizer/NumPy/Torch RNG; only IncompatibleSGNSCheckpoint permits fresh start. Real tiny Torch fixture proves malformed optimizer does not mutate live state. Unexpected final commit errors abort.
- **AI3-QA-03:** Hashing raw corpus only when long computation finishes can label earlier tokens with a replaced corpus digest. Owner captures digest from consumed bytes; SchemaCache.save rejects publication if corpus digest differs. Tested temporary changed artifact.

## Actual coverage

- **cached-only QA (tested):** Actual qa_series.worker with fake scene calling common.load records missing-data/stale-data before upgrading loader; no shared guard edit needed.
- **schema breadth (tested):** Legacy completion markers rejected for norms,mp,galore,words,sgns,jl,mf,twotower. Existing unmodified items retain base semantics.
- **cache refresh/locks (tested):** Changed recipe invalidates already-loaded JL fixture and reloads new arrays; concurrent CLI+loader stale-item consumers invoke one producer under shared item lock.
- **completed SGNS lineage (tested):** Current words/SGNS fixtures accepted; SG_K change, ordered words vocabulary replacement and malformed array bytes rejected without corpus/model data loaders.
- **SGNS restoration (tested with tiny state; production remains untested):** Independent malformed optimizer isolation passes; combined numerical tests serialize tiny Torch checkpoint and compare resumed next-step state with uninterrupted state. Actual production SGNS compute loop not run.
- **matrix factorization fairness (actual producer orchestration tested with mocked training; source reviewed):** Mean and bias final baselines now use train|valid like final ranks; tuning uses train and validation separately. Fit counts/split fingerprint and mf partial v2 recorded. Independent combined run includes owner actual compute_mf fixture.
- **recall and sampled logits (tiny actual helpers/evaluator tested in combined suite; source reviewed):** Distinct unseen relevant-target denominator, macro averaging and empty cohort NaN/counts explicit. Raw corrected-training scores remain default inference; prior-added branch labelled ablation. No measured performance claim.
- **JL confidence and other statistical fixes (source reviewed; companion visual_math tests observed during in-progress broad run):** Explicit delta union inversion, unavailable epsilon<1 points, two-sided KS, self-masked neighbours, strict edge counts and corrected no-self genre chance checked in source. Frozen focused18 receipt does not include visual_math suite.

No shared `qa_series.py` change is needed: its existing local instance guard works with Part3 dynamic loading.

The separate in-progress 39-test Part3 run found five failures and two errors in changing Chinese narration templates. Parent was informed; this is not a completed broad-suite sign-off. Full log: `part3-targeted-tests.log`.

## Remaining

- No actual Part3 numerical cache exists; root owns future production computation.
- Production SGNS large-corpus training/resume and crash/concurrency across OS processes are untested.
- Thread-level CLI/loader lock fixture is covered; not a multiprocess stress test.
- Render, source-to-caption layout, EN/ZH playback, listening and synchronization are unreviewed for Part3.
- No external historical/statistical empirical attribution was newly verified; review covers mathematical/internal implementation consistency.
- Broad Part3 narration tests require parent final translation batch and rerun.

Exact source ranges, SHA receipts, test logs and the original partial-restore failure probe are in this directory. No unresolved producer blocker identified in the reviewed source batch.
