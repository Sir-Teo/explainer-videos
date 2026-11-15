# Statistics, Built: QA and polish pass, 14–15 November 2026

A scene-by-scene preflight of all 65 parts on a clean container (manim 0.22.1, NumPy 2.5.4 and SciPy 1.18.1 as in
`requirements-lock.txt`, TeX Live with dvisvgm), followed by repairs. English only; Chinese production, listening and
narrated masters remain the separate gates listed in `statistics-built-progress.md`.

## What was run

| Check | Scope | Result |
|---|---|---|
| `tests/test_stats*.py` and `tests/test_series_site.py` | 141 files | 1122 passed, 5 subtests (before and after the repairs below) |
| `tools/check_course.py stats` (entry, lab, interactive, built page at desktop and phone width, every slider and button) | 65 parts | all OK |
| `tools/qa_series.py statsN` (narration-beat frames, text-overlap and runtime preflight) | 65 parts, 888 chapters | every chapter renders; no text-overlap warning remains (see "Known false positives") |
| Narration lint (doubled words, unbalanced brackets and quotes, spacing, stray TeX) over every `voiceover` string | 65 parts | one real defect (Part 7) |
| Cross-references ("Part N") in narration: 1,194 mentions checked for topic and direction | 65 parts | no wrong reference |
| README run times against the narration estimate (`tools/lecture_length.py`) | 65 parts | consistent |

The first test run had 16 failures, all `FileNotFoundError: 'latex'` (no TeX in the container); with TeX installed
they pass. Running them under `pytest -n` races on `media/Tex`; run them serially.

## Repairs

| Part | Chapter | Defect | Repair |
|---|---|---|---|
| 1 | Correlation | the axis label "obs. 3" printed over the vector label; the other label sat on its own arrow | both vector labels moved clear |
| 3 | Tails | the citation line ran through the x-axis label of the histogram | histogram raised |
| 5 | Joint (two dice) | narration and caption said the zeros are *above* the diagonal and the twos *below*; the table draws them the other way round. The caption also overlapped the table's margin sums | narration and caption now match the figure; rows moved right |
| 7 | Metropolis | "is an an integral" in the narration | doubled word removed |
| 11 | Pivots | tick labels 2.7 and 3.3 printed on top of each other on the chi-squared axis | the second label drops a row, in its line's colour |
| 12 | Geometry | "obs 3" cut through the chapter title | axes lowered |
| 18 | Weighting | "income band" and "age band" over the band names | axis titles lowered |
| 31 | PCA, CCA | state and country names overlapped each other, dots and the axes; "Guatamala" (the spelling in the source data) on screen | `place_labels` picks the first free spot, stays inside the plot; display spelling corrected (the Museum's copy of the data is untouched); two names, not three, at CCA's crowded end |
| 36 | Sensitivity, TimeVarying | chapter-card timeline names overlapped | short event names |
| 36–39 | chapter cards | the same overlap wherever two lit years carried long topic lists | `timeline()` now cuts a year's list after the last whole topic under 52 characters when a chapter gives no name of its own |
| 37 | SDID | rotated state names crowded | right-aligned at their ticks |
| 47 | Hajek | y ticks 0 and 1 overprinted | the tick at 1 dropped (the legend says "1 at every h") |
| shared | `explainer/ai/cache.py` | an item that returns nested arrays crashed with `TypeError: only 0-dimensional arrays can be converted to Python scalars` (NumPy 2.5) when a scene triggered it on first use; only `python -m ...compute`, which wraps items in `nest()`, could cache it. Parts 43–47 were affected | the cache serializer writes arrays as lists and NumPy scalars as Python ones |

## Known false positives

* Part 35, Potential: the "?" cells deliberately sit on the numbers they hide.
* Part 37, SDID: the checker compares the bounding boxes of rotated labels; the frames are clear.

## Left as is

* About 130 unused locals, 53 f-strings without placeholders and the shadowed `polyline`/`clip_curve` in Parts 48–59's
  `common.py` (the later definition is the clipping-aware one) are harmless; editing them would only invalidate
  existing source fingerprints.
* Coverage Board scenes need each part's `board` compute item. Scene rendering does not run it, so on a fresh checkout
  run `python -m videos.stats.statsN.compute board` first. The heavy ones are Parts 27 (about 7 min), 34 (the
  forests' `ij` and `ij_sub` items, about 27 min, then the board), 37 (15 min), 39, 41 (57 min) and 59.

## Method limits

Frames were checked by the overlap preflight for every chapter and by eye wherever it flagged something, plus a
sample of contact sheets; not every frame of every chapter was inspected, and no narrated playback or audio was
reviewed.
