# Parts 1–3: local 4K/audio production handoff

## Cloud reactivation — 2026-11-01

**The current production target is the separate parent-owned cloud production task. The canceled local task remains stopped.** Local-owner/pilot instructions below are retained as dated history; they do not reactivate local execution. Part 4 now has its own [scoped cloud metadata handoff](production-handoff-part4.md), separate from this Parts 1–3 gate.

The original transfer remains **144 files / 73,024,949 bytes**: the 141 core cache files plus three strict novels-validator extras. The three cache ZIPs are already saved in Library and were handed to the cloud owner by the parent; this update creates, changes and uploads no archive. Optional real speech is outside that total and retains its separate voice/listening gates.

Keep source **`927fba668656a682b3e29a288de64130ddc680dd`** and the exact optional **`svd-reveal-v1`** manifest gate below. The later Part 3 Outro source **`e874a8da48693ea2c9ec75584e044d090a6bd9a39c8f0c193c1d245101a8ca24`** is excluded by the current gate; using it needs a new scoped manifest and production coordination. Neither its separate review nor a later branch HEAD silently expands this accepted source set.

The observed numerical versions remain **Torch `2.15.0+cpu`, Transformers `5.22.1`, NumPy `2.5.4`**, versus lockfile Torch `2.14.1` / Transformers `5.20.1`. The cloud owner must resolve strict runtime/cache portability and inherit fail-on-call producer protection in every renderer. Do not fake versions, weaken currentness, rewrite cache metadata or trigger recomputation. New narration/listening/synchronization and actual production-output review remain required.


Prepared in the cloud for the separate local owner `01a19439-c7ac-73a1-afe9-b5fd66b790ed`, relayed through the parent. **No command was run on the user's computer by this task.** No data archive, upload, model download, source/numerical change or publication was performed.

Use the reviewed source release **`927fba668656a682b3e29a288de64130ddc680dd`** for full Parts 1–3. It is already remote; local work need not wait for Part 4. Preserve existing local changes and the running pilot: use a separate clean checkout/worktree rather than resetting it. Obtain this handoff/evidence directory separately when working at the older pin. [Source identities and manifest order](evidence/production-handoff-parts1-3/reviewed-source-inventory.json) cover 17 + 16 + 19 scenes, or **104 bilingual chapter cases**. “38 Part 3 cases” means 19 scenes × 2 languages.

## The running SVD pilot can continue independently

The parent reports a bilingual **SVD 4K60 narrated pilot at `f00be66a0b47954bbdfe00a03dba7ebfe6c6fc4b`**, Mac M1/16 GB, existing BF16 Qwen3-TTS 1.7B / `qwen3-calm-a`, with synthesis observed around 8× real time. This is parent-reported progress, not a cloud performance/quality measurement or completed pilot approval.

[Exact comparison proof](evidence/production-handoff-parts1-3/svd-pilot-source-equivalence.json): `s08_svd.py` (`cd3b22f6…`), Part 3 `common.py` (`43bc0160…`), `compute.py` (`decde1f7…`), `zh_lines.py` (`ad8a17ed…`) and the global Chinese table (`8e4ed212…`) are byte-identical between f00 and 927. The autodiff module differs but SVD does not use it. SVD imports `load` yet has **zero `load()` calls**; it uses the fixed matrix `[[1.4, 1.1], [-0.5, 0.9]]` and local NumPy SVD/norm operations. **The cache transfer/version gates below do not block this cache-independent pilot.** Do not expand to full parts before resolving their separate gates. Inspect the actual new EN/ZH audio, timing, 4K layout and playback before calling the pilot successful.

## Exact transfer scope — paths and hashes, no archive yet

All paths below are relative to the cloud repository root `/workspace/explainer-videos` and must land at the same relative paths in the isolated local checkout. The parent must arrange an authorized transport; a cloud filesystem path is not a download URL.

| Set | Files | Exact bytes | Transfer instruction |
|---|---:|---:|---|
| `.cache/ai1/` | 81 | 52,350,045 | Complete non-lock set, including corpus/book sources and completed results |
| `.cache/ai2/` | 26 | 746,207 | Complete non-lock set |
| `.cache/ai3/` | 34 | 5,777,980 | Include all eight `_integrity/` sidecars unchanged |
| **Core total** | **141** | **58,874,232** | [Inventory](evidence/production-handoff-parts1-3/cache-inventory.json), [file list](evidence/production-handoff-parts1-3/transfer-core-files.txt), [SHA256 checks](evidence/production-handoff-parts1-3/transfer-core.sha256) |
| Strict-validator extras: `.cache/novels/{train.npy,valid.npy,tokenizer.json}` | 3 | 14,150,717 | [Extra file list](evidence/production-handoff-parts1-3/transfer-strict-extra-files.txt) and [checksums](evidence/production-handoff-parts1-3/transfer-strict-extra.sha256) |
| Optional existing real Information EN speech | 12 | 7,833,893 | Six WAV/JSON pairs only; [whitelist](evidence/production-handoff-parts1-3/transfer-optional-real-audio-files.txt) and [checksums](evidence/production-handoff-parts1-3/transfer-optional-real-audio.sha256) |

Core + novels extras are **73,024,949 bytes**; adding the optional real speech gives **80,858,842 bytes**. The strict GPT-2 validator files below are additional, not hidden in these totals. **67 transient zero-byte advisory lock files are explicitly excluded** in the inventory; lock ownership/state must not be transferred. No regular non-lock file in the three requested directories was omitted. There are no model-checkpoint files in those three observed sets; do not delete trained/custom checkpoints elsewhere.

Do not transfer duplicate silent video bundles, frame collections, Manim compilation/partial-movie caches, the whole Hugging Face cache or the whole `.cache/tts`. Existing Git checkout supplies source and both reference voice WAVs. Inventory files are metadata only; numerical data and audio files have not been copied into this evidence package or archived/uploaded by this task.

## Full-part gate: copying 58.9 MB alone is insufficient

**The lockfile and the observed Part 3 integrity records disagree:** the reviewed `requirements-lock.txt` pins `torch==2.14.1`, `transformers==5.20.1`; the existing Power/GaLore-control records require **`torch==2.15.0+cpu`**, and Power requires **`transformers==5.22.1`**. Their recipe records require **`numpy==2.5.4`**, which matches the lockfile. Installing the lockfile and then normally loading these results can mark them stale and start expensive computation.

Install matching observed versions **only where genuinely supported**, then verify. A native Mac/CUDA wheel-tag mismatch is a **stop before normal load**, not permission to normalize version strings, weaken `current()`, regenerate results or rewrite/re-attest sidecars. Keep rendering and TTS environments separate: the TTS environment need not use the strict numerical-render environment's Torch build. A compatible environment or any portable frozen-payload reader must be coordinated and reviewed through the parent; this handoff introduces no loader override.

[Exact external dependency inventory](evidence/production-handoff-parts1-3/external-validation-dependencies.json) records:

- Power additionally hashes public `openai-community/gpt2` revision **`607a30d783dfa663caf39e06633721c8d4cfcd7e`**: `config.json` and `model.safetensors`, **548,105,836 bytes total**. This is a validation dependency, not inference needed by the completed scene results. Use an already matching cache or a normal authorized download of only those two exact files into a dedicated `HF_HUB_CACHE`; no large model archive is proposed. The current resolver honors `refs/main` first, otherwise requires exactly one snapshot. A different main ref or multiple ambiguous snapshots fails the gate.
- GaLore-control additionally hashes the three novels token/tokenizer files above and `explainer/ai/novels.py` / `explainer/lm/pocket.py`. Power also checks Letters lineage; Letters checks Part 1's bigram bytes/source. Sidecars describe dependency observations, not proof of historical consumed inputs.

Run the supplied **read-only** preflight from the numerical-render environment, with the transferred handoff directory available outside or inside the pinned checkout:

```bash
python "$HANDOFF_DIR/verify_handoff.py" --repo "$PRODUCTION_REPO" --strict-external
# Add --optional-audio only if the six real pairs were intentionally transferred.
```

`HANDOFF_DIR` is the local copy of `docs/qa/evidence/production-handoff-parts1-3`; `PRODUCTION_REPO` is the isolated 927 checkout. The script checks source/cache/dependency hashes and exact package metadata without importing scenes/producers or loading models. **It is not an inherited runtime producer guard.** Stop on any mismatch. Then run existing `tools/qa_series.py ai1 --lang en --cached-only` (repeat sequentially for ai2/ai3) with all data/source writers stopped; inspect its JSON warnings and cache-current outcomes, not just its exit code. This uses the existing guarded QA path and produces current English narration captures useful to `qa_audio.py`.

Production `build.py`/`make.py` have **no cached-only flag**. Before full-part expansion, the local owner must coordinate a fail-on-call producer guard propagated into every spawned Manim process, preserving normal `current()` checks. Patching only the parent process is insufficient. No such guard is installed by this handoff. Do not use default `make.py` steps or `--force`: default steps include compute, and a missing/stale normal scene load also computes. Reverify file hashes after production; keep all source/data/checkpoint files intact.

## Existing voice policy and hardware decision

The AI series' documented production choice is **Qwen3-TTS / `qwen3-calm-a`**, `EXPLAINER_TTS=server`, speed 1.0. Generic `explainer/tts.py` defaults to Kokoro `af_heart`; do not accidentally obtain that generic fallback or `silent` preview timing when intending the bilingual production voice. The profile specifies English `tools/voice_refs/kokoro_en.wav` and Chinese `tools/voice_refs/serenaflat_zh.wav`, their transcripts, temperature 0.7, and chunk targets 260 EN / 90 ZH characters.

The local owner must inspect available hardware, RAM/free disk, installed dependencies, fonts and actual pilot performance before choosing concurrency or any alternative within the authorized policy. The repository chooses **MLX on Apple Silicon** (`mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16`); its Torch engine uses `Qwen/Qwen3-TTS-12Hz-1.7B-Base`, CUDA when available, otherwise CPU FP32. ASR/forced alignment are part of the server. CPU requests are serially chunked to avoid the observed batched OOM. The cloud's 16 GB CPU run was slow (~22× real time under that workload); neither that nor the reported M1 pilot is a full-series speed/quality forecast. Do not substitute an unvalidated precision/model change based on a tiny kernel benchmark.

Start the already installed appropriate service in its own environment/terminal (do not start a duplicate during the running pilot):

```bash
.venv-tts/bin/python tools/tts_server.py --voice qwen3-calm-a                 # Apple Silicon / MLX
# Or the existing Torch policy, where supported:
.venv-tts/bin/python tools/tts_server.py --voice qwen3-calm-a --engine torch
```

The cloud **evicted only the inactive public pretrained Torch TTS download** at revision **`fd4b254389122332181a7c3db7f27e918eec64e3`**, reclaiming 4,544,170,364 logical bytes through the normal cache manager. Generated speech/custom checkpoints/results were preserved. [Exact receipt](evidence/cloud-capacity-20261031/inactive-tts-public-download/README.md). Cloud Torch TTS would require a normal authorized redownload; this does not evict the local Mac model or change the local MLX policy. The server's model loading does not pin remote revision, and the utterance key does not include actual engine/model revision; record the local model identity/version and listen to consistency before sharing an audio cache across environments.

The optional six Information EN pairs are genuinely nonzero PCM, with durations **3.57, 35.63, 23.88, 29.20, 37.68, 32.68 seconds** (162.64 s speech). [Exact keys, hashes, profile and alignment evidence](evidence/production-handoff-parts1-3/real-information-audio.json). Reuse only if the actual current spoken text/profile/cache key matches and the local owner accepts voice consistency. Remaining `.cache/tts` contents are not a production-audio transfer set; silent preview placeholders provide estimated timings only. The six clips have automated signal/alignment and independent numeric-ASR evidence, **no manual listening approval**.

## 4K commands — local owner only, after the full-part gates

Run from the isolated repo. Start with one rendering job; increase only after measured hardware/pilot evidence. Check system FFmpeg, xelatex/dvisvgm, Python 3.12 and platform Chinese fonts per the pinned README. Cross-platform font changes can change layout, so 480p cloud approval does not approve a local 4K render.

```bash
export EXPLAINER_TTS=server EXPLAINER_VOICE=qwen3-calm-a EXPLAINER_SPEED=1.0
# Optional: after a fresh guarded EN QA capture, pre-synthesize and inspect actual speech:
python tools/qa_audio.py ai1 --lang en
python tools/qa_audio.py ai1 --lang zh
# Review all signal/alignment/ASR leads; this is not listening approval.
python tools/build.py ai1 --lang en -q k --fps 60 --crf 16 -j 1
python "$HANDOFF_DIR/index_master_narration.py" --repo . --part ai1 --crf 16 --fps 60
python tools/zh_lines.py ai1 --verify --lang zh
python tools/build.py ai1 --lang zh -q k --fps 60 --crf 16 -j 1
```

Repeat **one part at a time**, ai2 then ai3, only after checking the preceding part. `-q k` selects 2160p; explicit 60 fps and CRF16 select the documented 4K60 profile. The index helper copies **completed EN master narration JSON only**, no movies/source/data: `narrate.py`/`zh_lines --verify` discover `media/aiN/videos/...`, while a CRF master writes `media/aiN/crf16/videos/...`. It refuses to overwrite different existing metadata. This avoids a fresh-checkout discovery failure; it does not pretend a base-path movie exists. `tools/narrate.py` also requires prior EN render metadata, so do not run it on a clean checkout and assume it evaluates narration from source. A `build.py --only` invocation still stitches all manifest scenes; use the local owner's standalone pilot workflow for one-scene tests.

Outputs per part: `renders/aiN_2160p.mp4`, `.srt`, `.chapters.txt`; Chinese adds `_zh` before the extension. Names omit FPS/CRF, so preserve versioned copies and receipts before reruns with different profiles. `--crf` uses per-scene PCM/ALAC intermediates where WAVs exist; final AAC is 48 kHz stereo/384 kbps with high-pass and two-pass normalization targeting −16 LUFS / −1.5 dBTP. Verify actual streams, frame cadence, decoded video/audio, chapters/subtitles, boundaries, loudness/clipping and every spoken bookmark against the new output; targets are not measured results. Inspect actual EN/ZH listening, pronunciation, pacing and continuous playback. Do not reuse silent animation timing as narrated-sync approval, or publish/upload/merge/deploy from this handoff.

## What the cloud review does and does not establish

| Part | Completed scoped evidence | Still open for production |
|---|---|---|
| 1: 34 cases | All 17 chapters EN/ZH endpoint/silent-motion selected review; baseline 15,194 selected times plus scoped repair regressions. Information EN has one 169.57 s 1080p narrated chapter/six real speech blocks, signal/bookmark/independent ASR checks. | Other 33 narrated cases; actual listening, subjective pacing, new spoken sync, remaining final resolution/full-part joins/exports and 4K review. Original exact native playback is not blanket approval of newer files. |
| 2: 32 cases | All 16 EN/ZH endpoint/silent-motion selected review (current 14,067 times). Knowledge 41 bilingual native 1080 endpoints; EN Hook silent 1080 pilot has 246 selected times and native checks. | All 32 narrated cases/listening/sync; full-part/4K production motion and final mux/joins. Exact original Logic/Hook playback receipts are scoped, not narrated approval. |
| 3: 38 cases | All 19 sources / 17 data items; final 38-case selected map 14,729 times, 695 native 1080 endpoints at declared review scales plus critical native checks. Final silent EN/ZH 19-chapter assemblies and 36 join windows reviewed; raw warnings retained. | All 38 narrated cases/listening/sync/subjective pacing, except the separate local SVD pilot is now in progress rather than completed. Whole-part narrated/4K motion, native new masters and production export checks remain open. Silent lengths 3281.81/3469.09 s are not spoken-duration forecasts. |
| 4 onward | Separate cloud QA continues. | **Part 4 is not production-ready and is excluded from this local expansion.** Parts 5–31 remain queued. |

[Cloud status](STATUS.md), [production/listening queue](remaining-production-qa.md), [Part3 chapter checklist](ai3-chapter-checklist.md) and exact evidence retain historical fingerprints/warnings and distinguish selected frames from continuous perception. No tracked web-player application exists; external hosting responsiveness is not tested here. This handoff is a production plan and exact transfer inventory, not completed 4K/audio approval.


## Explicit reviewed SVD reveal overlay

The original `927fba668656a682b3e29a288de64130ddc680dd` gate remains the default. A separately reviewed SVD reveal fix may be checked only by explicitly selecting `--overlay svd-reveal-v1`. Its versioned [manifest](evidence/production-handoff-parts1-3/overlays/svd-reveal-v1.json) binds the original base, reviewed patch commit `7c47c11e3802390141c9551ac376ebe4ddf31e0e`, and the exact `videos/ai/ai3/s08_svd.py` replacement SHA256 `291bba0e7c180750274e2117114cc22382f3b9b81880db0a499791b4b2e3e322` (11,747 bytes; before SHA `cd3b22f6…`, 11,730 bytes).

Use an isolated checkout of the original base with that exact scene patch, or an equivalent source-only/cherry-picked tree. Only the 103 exact optional SVD review-evidence additions listed in the manifest are also permitted. The verifier checks HEAD, index and worktree against the base and rejects unrelated changes or nonignored untracked files. Keep `HANDOFF_DIR` outside this production checkout for overlay verification. Checking out a later branch HEAD, including `7c47c11` with its unrelated ancestors, is not a substitute for the bounded overlay. The separate f00 pilot equivalence does not authorize full-part f00 expansion.

```bash
python "$HANDOFF_DIR/verify_handoff.py" --repo "$PRODUCTION_REPO" --strict-external --overlay svd-reveal-v1
```

Unknown or altered manifests fail closed. Every original core-cache, other-source, external-data/model/revision, exact package-tag and optional-audio check remains effective; `current()` is unchanged. Without `--overlay`, the changed SVD scene still fails the original preflight. This adds no runtime producer guard and does not run production locally. The existing source/data-writer, compatible environment, inherited producer-guard, local-owner review and actual narrated/4K validation gates still apply. Historical verifier/manifest bytes are retained under `historical/v1/`; scoped cloud test receipts are under `overlay-checks/`.
