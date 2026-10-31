# AI, Built: source inventory and remaining workload

Snapshot ending **2026-10-31T11:58:37.891214+00:00**, on branch `qa/ai-series-cloud-20261031`, HEAD `af170318c179bfb56fa28aafe73477c56f5b80d8`. Uncommitted fixes are included; the [JSON evidence](ai-built-20261031-inventory.json) records hashes of all parsed source files. None changed during the source scan. Cache-marker observations are a non-atomic snapshot and can change while the root task computes Part 1.

This is **static inventory and planning evidence**, with no rendered-frame, factual, audio, animation, or playback approval. No scene or compute module was imported by the inventory generator, and it started no rendering, downloads, training, or computations.

The current manifests contain **31 parts, 553 chapters, and 1,106 English/Chinese chapter cases**. Every listed scene source and named class exists. All 31 parts have `zh_lines.py` Chinese template sources, and 30 have persisted `narration_zh.json` tables. **Part 26 has no persisted narration table in this checkout.** Its templates may generate the table later; absence alone does not prove runtime translation failure. Template/table presence does not establish translation coverage or quality. The earlier 20-part exports do not establish current-manifest coverage.

## Per-part snapshot

“Scene markers” counts distinct `(part, item)` cache keys resolved from literal `load` calls in that part's manifest-listed scene modules, including directly resolved cross-part aliases. “Compute markers” counts JSON completion markers for literal keys in that part's `compute.py` `ITEMS` dictionary. Neither column establishes cache freshness, array/model integrity, or complete runtime prerequisite availability.

| Part | Chapters | Bilingual cases | English source estimate, min | Scene markers present / identified | Compute markers present / registered |
|---|---:|---:|---:|---:|---:|
| ai1 | 17 | 34 | 56.8 | 21/28 | 23/31 |
| ai2 | 16 | 32 | 53.3 | 0/19 | 0/19 |
| ai3 | 19 | 38 | 51.1 | 0/17 | 0/17 |
| ai4 | 19 | 38 | 48.5 | 0/23 | 0/23 |
| ai5 | 19 | 38 | 52.5 | 0/28 | 0/28 |
| ai6 | 19 | 38 | 48.9 | 0/22 | 0/22 |
| ai7 | 18 | 36 | 51.3 | 0/25 | 0/24 |
| ai8 | 19 | 38 | 50.0 | 0/26 | 0/25 |
| ai9 | 17 | 34 | 53.9 | 1/21 | 0/18 |
| ai10 | 18 | 36 | 53.5 | 1/26 | 0/22 |
| ai11 | 18 | 36 | 53.2 | 0/14 | 0/14 |
| ai12 | 19 | 38 | 50.3 | 0/18 | 0/18 |
| ai13 | 19 | 38 | 52.7 | 0/18 | 0/15 |
| ai14 | 16 | 32 | 54.9 | 0/12 | 0/14 |
| ai15 | 17 | 34 | 51.6 | 0/19 | 0/19 |
| ai16 | 18 | 36 | 44.4 | 0/20 | 0/21 |
| ai17 | 16 | 32 | 54.4 | 0/10 | 0/10 |
| ai18 | 20 | 40 | 55.5 | 0/25 | 0/26 |
| ai19 | 19 | 38 | 55.0 | 0/18 | 0/17 |
| ai20 | 18 | 36 | 50.1 | 0/26 | 0/26 |
| ai21 | 19 | 38 | 54.1 | 0/19 | 0/18 |
| ai22 | 18 | 36 | 44.8 | 0/15 | 0/16 |
| ai23 | 18 | 36 | 53.4 | 0/16 | 0/16 |
| ai24 | 17 | 34 | 53.1 | 0/19 | 0/19 |
| ai25 | 19 | 38 | 59.6 | 0/18 | 0/19 |
| ai26 | 17 | 34 | 63.5 | 0/18 | 0/19 |
| ai27 | 15 | 30 | 48.0 | 1/16 | 0/15 |
| ai28 | 16 | 32 | 51.1 | 0/16 | 0/9 |
| ai29 | 18 | 36 | 53.1 | 0/12 | 0/12 |
| ai30 | 19 | 38 | 55.4 | 0/17 | 0/17 |
| ai31 | 16 | 32 | 55.8 | 0/15 | 0/15 |

Across part inventories, 24/596 literal scene-key observations had JSON markers. Deduplicating cross-part references gives **21/580 unique identified scene-cache keys** present. Separately, **23/584 registered compute-item JSON markers** existed; all 23 were in `ai1`. These are overlapping descriptions of the same caches and must not be added together.

The scan follows explicit imports of `load`, aliases of a part's `compute.load`, and literal `_result(compute_module, item)` calls. It does not follow arbitrary call reachability or evaluate runtime branches. Part 20 has three dynamic `load(f)` sites; Part 31's `mod.load(name)` helper and conditional final scoreboard need runtime review. `common.py` helper reads are listed separately in the JSON; shared/imported helpers, dynamic names, model checkpoints, and transitive computations may add requirements. Scanning all calls in a scene module may also include helper code that the scene does not execute. **Use cached-only scene QA to discover actual missing prerequisites; this inventory is not a runtime data-availability pass.**

## Playback and rendering cost

`python tools/lecture_length.py --series ai` was run successfully. The source-only calculation totals **1,633.57 minutes = 27.23 hours for English** at 140 words/minute, counting literal narration plus three words per f-string placeholder. This matches the tool's algorithm; there were no measured chapter durations to substitute. Dynamic prose, pauses, animation outside narration, and synthesized speech can change actual duration.

One continuous review pass in each language is therefore a planning workload of **about 54.45 hours**, assuming similar English and Chinese durations, before replays, bug investigation, fixes, and regression review. This is not measured Chinese playback time. Endpoint checks and contact sheets cannot replace those passes. Silent motion review, narration listening, narrated synchronization, final-resolution layout, and chapter-join continuity remain separate coverage dimensions.

Part 26's English source estimate is **63.5 minutes**, above the [syllabus](../../videos/ai/SYLLABUS.md)'s 30–60 minute target. Confirm actual narrated duration before treating this as a pacing defect; the length tool enforces only its 30-minute minimum. The root README says a 50-minute 1080p part takes a few hours to render and a low-resolution preview takes minutes per chapter. Those are repository estimates, not timings measured on this cloud worker; rendering 62 language editions must be planned separately from 54 hours of watching them.

## Documented compute and storage needs

The [lecture guide](../../videos/ai/LECTURE_GUIDE.md) gives a general budget of about two CPU-hours per part and requires seeded, resumable long jobs. More specific part documentation includes larger jobs; the repository's timing statements describe different machines and should not be treated as guarantees:

| Work | Documented requirement or timing | Source |
|---|---|---|
| Part 1 corpus and pretrained models | About 40 MB of books; GPT-2/GPT-2 XL and Qwen3 base models total about 19 GB; README estimates about 15 minutes on four cores, plus additional items | [Part 1](../../videos/ai/ai1/README.md) |
| Part 12 experiments | About 2.7 CPU-hours on one thread | [Part 12](../../videos/ai/ai12/README.md) |
| Part 13 transformer experiments | About 2.5 CPU-hours on one or two threads; transformer about 70 minutes; checkpoints and per-run partials | [Part 13](../../videos/ai/ai13/README.md) |
| Part 16 sparsity experiments | About three CPU-hours, resumable | [Part 16](../../videos/ai/ai16/README.md) |
| Part 23 multimodal experiments | About four hours on a busy four-core host using one torch thread; Kokoro voices, Whisper base.en about 290 MB; narrator codes additionally need Qwen3-TTS-12Hz-1.7B-Base and its TTS environment | [Part 23](../../videos/ai/ai23/README.md) |
| Parts 24 and 25 | Each about 3.5 hours of wall time on the documented busy host; Part 24 cache about 60 MB; Part 25 uses synthetic data and saved local models | [Part 24](../../videos/ai/ai24/README.md), [Part 25](../../videos/ai/ai25/README.md) |
| Part 26 AlphaZero and evaluation | Specific part README: about seven hours on four cores for 80 generations, plus three to four hours for the other computations; root README instead summarizes AlphaZero as about five hours | [Part 26](../../videos/ai/ai26/README.md), [root README](../../README.md) |
| Shared novels model | Root README estimates about one hour; consumed by later parts | [root README](../../README.md) |
| Part 27 post-training | Root README says about two hours; the part's measured busy-host item timings total roughly 6.5 hours on one thread; checkpoints and per-run partials | [Part 27](../../videos/ai/ai27/README.md) |
| Parts 28, 30 and 31 | Part 28 about three hours on one thread; Part 30 build instructions say two to three CPU-hours while its historical results section says about 1.5; Part 31 about two hours on the documented shared host | [Part 28](../../videos/ai/ai28/README.md), [Part 30](../../videos/ai/ai30/README.md), [Part 31](../../videos/ai/ai31/README.md) |
| Production narration on CPU | Documented 16 GB RAM is enough; Qwen3 narration runs 10–30 times slower than real time on CPU | [Narration setup](../../README.md) |

At this snapshot the cloud cgroup allowed **four CPU equivalents and 16 GiB memory**, with **24.74 GiB filesystem space free**. Part 1's documented model downloads alone could consume most of that free space. Total space for all models, chapter renders, encoding intermediates, and final bilingual masters has not been measured. No GPU throughput or full-series storage capacity has been established. All timing and size statements above are source documentation, not new benchmark results.

If all 54.45 assumed hours of narration were uncached and synthesized at the documented CPU rate, speech synthesis alone would be on the order of 545–1,634 hours. This is a conditional planning calculation, not a measured runtime estimate; cached speech, different language durations, hardware, and synthesis settings can change it substantially. It explains why a silent preview is useful while production audio stays explicitly untested.

## Instructions and next executable step

No `AGENTS.md` or repository `.agents/**/SKILL.md` was found in this checkout. Ancestor `/workspace/AGENTS.md` and `/AGENTS.md` were absent; `/workspace/.agents` was empty. The checked-in `CLAUDE.md`, series README, syllabus, lecture guide, and bilingual guide remain the relevant repository conventions.

Keep one compute owner. Start each part's dependent computations before its QA; do not render while its inputs are still being written. The current root task owns Part 1. After its missing data finishes, the existing workflow is:

```bash
# From the repository root in the prepared Python 3.12/Manim environment.
# One compute owner only; this step may download/train and is not part of this inventory scan.
python tools/make.py ai1 --steps compute

python tools/qa_series.py ai1 --cached-only --resume
python tools/qa_series.py ai1 --lang zh --cached-only --resume
python tools/qa_series.py ai1 --motion --cached-only --timeout 1200 --resume
python tools/qa_series.py ai1 --lang zh --motion --cached-only --timeout 1200 --resume
# After starting the documented production TTS server:
python tools/qa_audio.py ai1 --lang en
python tools/qa_audio.py ai1 --lang zh
python tools/qa_report.py
```

Read each result JSON even when a process exits successfully; review every warning and retain explicit missing/stale/failed/pending states. Record actual full playback and listening coverage separately, then proceed to `ai2` and onward in manifest order. A final-resolution narrated build and review is still required for production approval.
