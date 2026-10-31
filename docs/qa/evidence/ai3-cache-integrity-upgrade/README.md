# Part 3 cache-integrity upgrade

The old producer reported all 17 items current, but its checks had two scopes: nine items checked embedded schema/recipe/array-hash metadata; eight returned true from JSON existence alone. That historical receipt is preserved verbatim. Its 17 true values were accurate about the predicate and did **not** establish uniform integrity or consumed-input provenance. `scope-correction.json` names both groups and the remaining limits.

The eight formerly shallow items now use `_integrity/<item>.json` sidecars, exact JSON/NPZ hashes, strict structure/shape/finite-value contracts, cheap algebraic identities, scoped producer/helper/global-constant AST recipes and dependency observations. Sidecars live below a private subdirectory, preserving top-level completion counts. All eight real payloads were validated and all eight sidecars staged under the existing JSON item locks **before** the stricter guard was activated. The migration never rewrote numerical payloads or invoked a producer.

All eight records explicitly use `origin=postproduction-attestation`. They bind frozen producer `2b03a02de9ae201a9955f6a88ed56f6433b5d0602186c5a3978cd4d565a616e2`, declared expected JSON/NPZ hashes, the published completion receipt and successful generation-log lines/hashes. Highdim's generation appears in the independent log; the main job's later cached marker is not substituted for it. Current dependency fingerprints are labeled later observations. **Original consumed dependency hashes remain unknown.** These records do not pretend the old producer wrote the new metadata.

Future producer-save records have a distinct origin. The normal loader/CLI observes recipe/dependencies before generation and at publication and rejects detected changes. Fresh prerequisite creation is explicitly labeled incomplete-before observation; direct save has publication observations only. These checks do not instrument every original dependency read.

## Validation and preservation

- **40 focused tests passed without warnings:** 19 new integrity tests, eight existing integration tests and 13 existing numerical tests. These use temporary deterministic fixtures and tiny existing kernels, not production models or datasets.
- All **17 actual current checks and cache loads succeeded** while every registered producer was replaced by a mock that raises if called: **zero producer calls**.
- All **26 completed numerical JSON/NPZ files** retained exact bytes, sizes and modification timestamps. All eight staged sidecars retained their staged bytes.
- All **nine existing recipe fingerprints** stayed unchanged. All **54 top-level numerical producer/helper functions** are AST-identical to frozen 2b03; implementation changes in compute.py concern cache orchestration.
- Tests cover malformed/non-dict/nonfinite JSON; truncated, missing, object and wrong-shape NPZ; byte tampering; recipe/dependency drift; legacy metadata handling; migration hash rejection and all-item preflight; interrupted sidecar publication; item-lock blocking; cached-only stale guards with zero producer calls; and future-save provenance. The control contract correctly expects **120 stored curve points** from 600 steps with `curve[::5]`.

Exact final source hashes are in `source-freeze-and-preservation.json.gz`; final compute.py SHA256 is `decde1f7874d08148cf35ac8067cb6ea6cf051d058ce052a6282afdca4cdb41a`. `attestation-staging-receipt.json.gz` records pre-activation staging and payload preservation; `preactivation-baseline.json.gz` records original nine recipe fingerprints and numerical-file identities. `postactivation-validation.json.gz` records the zero-producer load check, and the final freeze repeats it after the final code changes. All eight exact sidecars and original source/run evidence are included.

## Historical QA limits

Earlier QA input ledgers track numerical JSON/NPZ signatures, not these new sidecars. This package does not retroactively bind old renders to the new metadata or validator. Original render fingerprints and warning history remain unchanged; source changes may conservatively stale earlier or active artifacts. No shared QA tool or numerical generator body was changed in this bounded repair. The parent's separate full-suite integration is not attributed to the focused 40-test run here.

Hash integrity is not adversarial authentication, a numerical rerun or visual/audio approval. There is no narration/listening, continuous playback or production-export claim. Gzip members preserve exact decoded source bytes; `manifest.json` hashes both actual compressed bytes and decoded bytes. Absolute paths inside frozen ledgers identify the cloud workspace at observation time. Numerical payloads and model weights are not packaged.

The parent’s separate full-repository unittest run also passed: **235 tests in 26.689 seconds, exit 0**. Exact log and receipt are `full-repository-unittest.log.gz` and `full-repository-unittest.json`. This run predates the subsequent GaLore wording changes and does not validate those later edits.
