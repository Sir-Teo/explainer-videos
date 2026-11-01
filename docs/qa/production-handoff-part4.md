# Part 4: cloud production handoff

Use source commit **`1927e6b7a99192344bd4c00ca7aae3abdd499369`** for Part 4, *Change*. This metadata handoff binds completed numerical data and accepted preview review. It does not approve a future narrated or 4K output. Execution belongs to the separate authorized cloud production owner. This task ran no production render, upload, archive transfer, local-computer task or CI job.

At 2026-11-01T02:44:18.460146+00:00, all **23** named items passed `cache_current()` and actual `CACHE.load()` with `_produce` and every cache producer replaced by fail-on-call mocks: **zero producer calls**. All **42** JSON/NPZ payloads retained their hashes, sizes and mtimes, totaling **796,899 bytes**. [Complete metadata](evidence/ai4-production-handoff/handoff-metadata.json) includes every item’s completion record, recipe and dependency hashes; [checksums](evidence/ai4-production-handoff/payload-files.sha256) enumerate every present payload. This is integrity/currentness evidence, not a new scientific experiment.

## Source and preview identity

Every file in `videos/ai/ai4/` and the numerical/cache/contour dependencies below was compared directly with the recommended Git tree. All matched. The global caption table is deliberately pinned to that commit; the working tree has later Part 5 additions. Source-byte equivalence does not prove which shared bytes an old renderer imported.

| Source | SHA-256 at recommended commit |
|---|---|
|`videos/ai/ai4/compute.py`|`d596f3d0e90e4fbe6bd9846121a67b327048e03d331985533bfd891498f44352`|
|`videos/ai/ai4/contracts.py`|`4e0b841d49e6113309d838f567a103837ae28244cb4d13cba01bb26dab81e3ac`|
|`videos/ai/ai4/cache_contract.py`|`259a3fe3d320480dc9bd09958b164e6958cd533e8282b4b5a1dbacf25c4b6c30`|
|`explainer/ai/autodiff.py`|`2d2a0661b518ddfd2b16b31f9efdcbfdc573d5d1fdf06c2c1dc17c0975c8f1a0`|
|`explainer/ai/viz.py`|`9f31d9eea0073ddd34935f40165bafa02ffa668c45d733a2d1b8a03c2afe6c16`|
|`videos/ai/ai4/zh_lines.py`|`ec04b2f4c18551b990707465209d3f4472d3b098ccf16e61a1d2d558bb089e08`|

The pinned global Chinese table is **`20229b679782e6b183a87b809cd2124dbb48950de7179b5be22fb3f04013a182`**. Its bytes also match the archived pre-Part-5 table in [the caption source review](evidence/ai5-source-review/README.md). The existing comparison covers **142 captured Part 1–4 collections / 4,142 observed caption keys, zero changed outputs**; later Hook and seven-caption updates have matching-rule supplements. This is a bounded observed-key proof, not blanket approval of current HEAD or unobserved branches. The recommended source pin avoids needing later additions.

Accepted [canonical preview map](ai4-final-preview-map.json): **`33071a124497a163341b0ddff5cbf3e6423a43fb1c2a412c8a48374346963656`**. It binds **38 bilingual chapter movies**, **13,670 selected image appearances**, **101,192 automatically decoded video frames** and **537 native 1080p endpoint images**. Native supplements resolve specific source changes; they do not constitute full native motion review. Raw movie records retain 36 `passed`, 2 `needs-review`, and 2 warnings. Historical aggregate fingerprints/currentness fields remain historical; no all-current fingerprint is claimed.

The history-qualified silent assemblies were rehashed against the accepted [assembly evidence](evidence/ai4-history-qualified-assembly/README.md):

| Language | Exact assembly SHA-256 | Bytes | Duration |
|---|---|---:|---:|
|en|`bda4603fef4a06b72d06182b550c4688c8e2661d128ee391899cdcfbf8532782`|31,319,908|3267.356125 s|
|zh|`322c81224ea983f72c3e01ce6daa9a16e173e036713bcc1bfbc901158a9c6dd0`|32,065,039|3478.819813 s|

Each assembly contains 19 chapters. Technical evidence includes full video/audio-stream decoding and timestamp checks; their PCM was digitally silent. All **36 chapter joins** have scoped review coverage, with exact-byte inheritance for unaffected joins. Selected review does not establish continuous perceptual viewing or narrated synchronization. The preserved warnings are an EN Layers source-change warning and an EN GradCheck 1.5-second sparse-state warning; accepted source/image evidence remains separate from raw statuses.

## Exact numerical transfer scope

Completed files belong at their same repository-relative paths in the isolated cloud production checkout. This document creates no archive and copies no numerical payload. Advisory locks and partial state are excluded. Absent `.npz` files for `params`, `tiny`, `tape` and `check` are expected, explicit absences.

| Item | Present payloads | Bytes | Upstream raw corpus dependencies |
|---|---:|---:|---|
|`params`|1|2,976|—|
|`linapprox`|2|10,662|—|
|`depth`|2|11,372|—|
|`jacobians`|2|5,377|—|
|`modes`|2|13,460|—|
|`tiny`|1|1,259|—|
|`mlp2`|2|3,638|—|
|`tape`|1|2,975|—|
|`check`|1|1,344|—|
|`train`|2|51,297|ai1/train.txt, ai1/valid.txt|
|`grad0`|2|5,419|ai1/train.txt|
|`gdlr`|2|18,069|ai1/train.txt|
|`floats`|2|11,590|—|
|`cancel`|2|14,456|—|
|`vcurve`|2|26,459|—|
|`checkpoint`|2|3,883|—|
|`newton`|2|62,731|—|
|`hessian`|2|466,666|—|
|`valley`|2|4,810|—|
|`quad`|2|21,654|—|
|`lagrange`|2|33,401|—|
|`kkt`|2|11,472|—|
|`deq`|2|11,929|—|

Part 1 raw dependencies are already within the separately prepared Parts 1–3 cache archives. Match these bytes before any loader call; do not rebuild corpus or substitute another text release:

| Path | Bytes | SHA-256 |
|---|---:|---|
|`.cache/ai1/train.txt`|23,728,683|`51f51a196c17cf5222811570c9d21acacae92fb754267d29a2ffa8dca7f3d2b8`|
|`.cache/ai1/valid.txt`|1,242,871|`a2ca0736ae115afb121503da07dd5625f469354cbf78f9626c2a182cceb58a54`|

`train` consumes both files; `grad0` and `gdlr` consume `train.txt`. Recipes also bind Part 1’s exact `compute.py`. Fresh Part 4 metadata records those observed inputs; it does not reconstruct historical lineage of older Part 1 results. No Part 2/3 numerical payload or full model weights are required by Part 4’s cache dependencies. The earlier Parts 1–3 document supplies archive inventories only; its historical local-execution instructions are not this cloud handoff’s execution policy.

Stored parameter counts are **124,439,808** for GPT-2 and **4,022,468,096** for Qwen3-4B-Base. Both used pinned safetensors-header reads, without historical fallback. Metadata records repository revisions, header/config/index hashes and tied-weight policy. Cached rendering needs no new header request or full Qwen/GPT-2 weight download.

## Runtime portability gate

Observed numerical environment: Python **3.12.14**, NumPy **2.5.4**, SciPy **1.18.1**, Torch **2.15.0+cpu**, Manim **0.22.0**. These are actual package metadata, not proposed overrides.

**Strict cache recipes and the lockfile disagree.** The reviewed lockfile pins `torch==2.14.1`; every Part 4 recipe records `torch==2.15.0+cpu`. Observed `transformers==5.22.1` also differs from the lockfile’s `5.20.1`; Transformers is not one of Part 4’s three recipe-library fields. A different Torch version or CUDA wheel suffix fails Part 4 currentness. Source-only compatibility and this CPU environment’s success do not prove the cloud production environment has compatible packages.

Resolve this with genuinely compatible packages and exact frozen payload identities. Do not fake/normalize package metadata, rewrite completion records, retag caches or weaken `current()` to force reuse. A separately coordinated portable frozen-payload reader requires explicit validation; this handoff does not implement or approve one. Numerical rendering and TTS may use separate environments, with actual identities recorded.

## Required inherited production safeguards

1. Use the exact source pin, match all 42 payload and upstream file hashes, and verify recipe-library identities before importing scenes. Retain metadata and known file absences.
2. Install a fail-on-call producer guard in **every renderer subprocess before scene imports**, including processes launched by build/assembly wrappers. Require `current()` before any loader that can upgrade or compute. Patching only the orchestration parent is insufficient.
3. Pinned `tools/qa_series.py --cached-only` demonstrates guarding before the loader, but its low-quality silent/endpoints output is not a production command. Pinned `build.py`/`make.py` have no automatic equivalent; default make steps include computation. Neither defaults nor the metadata-inspection script supplied here replace the inherited renderer guard.
4. Record the separately approved cloud tooling/profile overlay, environment/fonts, numerical identities, TTS engine/model revision and voice/profile. Preserve source/data hashes before and after jobs. Stop on stale/missing data or unsupported runtime rather than recomputing.
5. Review actual new output at intended resolution/cadence: narration pronunciation/listening, synchronization, transitions, text/layout/clipping, stream timestamps, chapters/subtitles, joins and playback. Preview approval does not transfer automatically to new fonts, speech timing or 4K geometry.

The preview map also references the historical **40 guarded Part 3+4 loads / zero producers / 76 unchanged artifacts** receipt. That proof and this current 23-item check are separate. Known representability-gap NaNs in format-spacing arrays and an unavailable fit slope remain documented in the [original data validation](evidence/ai4-data-source-validation/README.md), rather than being relabeled finite successful measurements.

Remaining gates: cloud runtime/cache portability, the inherited per-renderer guard, real narration/listening/synchronization, continuous perception, final production-resolution geometry and current-output acceptance. The metadata handoff is complete; the production owner can request the small cache transfer after resolving transport and runtime.

## Confirmed frozen payload transfer

Library `libfile_f4c89a91670c81918ceb5d298b9f84b9`, version0: 761,466 bytes; archive SHA256 `f317945f1d258e2d1e85e4b43aaa8ad30aaa43c16a57185c190838a421e7a390`. Exactly42payloads/796,899bytes match the original source1927e6b7 handoff signatures, with optionalNPZabsence retained. [Archive manifest and successful Library receipt](evidence/ai4-payload-transfer/README.md). No duplicate earlier-transfer archive, numerical regeneration, metadata retag or new production approval. Cross-runtime inherited-producer-guard gate remains open.
