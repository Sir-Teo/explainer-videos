# Part 6 Lasso: motion findings and local repair

Both silent baseline movies have completed selected-time visual review:

| Language | Selected times | Unique images actually viewed | Exact duplicate times | Native sheets | Decoded / unselected frames |
| --- | ---: | ---: | ---: | ---: | ---: |
| English | 475 | 413 | 62 | 52 | 2,479 / 2,004 |
| Chinese | 512 | 429 | 83 | 54 | 2,706 / 2,194 |

All selected native images were inspected on chronological, unscaled sheets. Ten additional individual 854 × 480 views confirm four findings. Full mappings and page, frame, source, input, and raw-record hashes are compressed beside representative original pages. Adaptive motion sampling uses 0.25 seconds and a maximum selected gap of 1 second. Automatic decoding covered every encoded frame; the unselected frames were not visually reviewed. Continuous perceptual playback, listening, and final 1080p/4K review remain unverified.

The four findings are:

1. Default scaled emphasis moves the illustrated constrained optimum away from the diamond corner and zero axis.
2. The active white contour crosses the held zero-weight caption.
3. Both soft-threshold proof appends briefly overprint retained original rows with transformed copies.
4. The dashed identity line crosses the threshold annotation.

Some gray outer background contours crop at the canvas edge. No loss of educational meaning was established there, and those contours were preserved.

The authorized repair changes only five local AST sites in `s05_lasso.py`: emphasis with scale factor 1, a caption position below the loss contour, `transform=False` for soft steps 1 and 2, and a 0.9-unit right shift of the threshold annotation. Original words, narration, bookmarks, requested durations, data, and curve points are preserved. `invariants.json` verifies all other AST and all string values are identical; the shared ladder's Write branch retains its requested 1.2-second duration. Isolated actual-Manim fixtures for English and Chinese verify caption clearance and that all points remain fixed at 41 emphasis interpolation samples. These fixtures do not replace actual scene review. No numerical producer or model import was run.

The candidate and exact baseline hashes are in `summary.json` and `freeze.json`. That source-only candidate stage is historical. Fresh cached-only English and Chinese endpoints and full silent-motion regressions are now complete; exact current artifact acceptance is bounded below. Independent original movie copies remain runtime witnesses; no movies were hardlinked. Original raw `passed` records and empty warning arrays remain intact. Later helper files do not retrospectively prove historical imports or broad source currency.

The supplemental endpoint baseline also covers all 19 English and 18 Chinese images, actually viewed at native resolution on six chronological sheets. Per-image and per-page proof is in each `endpoint-review.json.gz`. Endpoint coverage remains distinct from motion coverage.

`patch.diff.gz` losslessly preserves the exact patch. Source snapshots and complete compressed ledgers support review; full movies and numerical or model payloads are excluded.

## Current rendered regression

All four focused captures returned raw `passed` with no warnings, unchanged observed source/data snapshots, and current record input signatures at the recorded `dc8391c0…` gate. Current direct source remains `bff5e9b4…`; source and numerical inputs were not edited during capture. Exact durations, narration/word timing/bookmarks, and record input signatures equal the preserved baseline.

| Language | Current selected / decoded | Exact prior PNG times | New unique images actually viewed | New exact duplicates | Actual native sheets | Unselected frames | Endpoint reuse / new views |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| English | 531 / 2,479 | 395 | 123 | 13 | 16 | 1,948 | 17 / 2 |
| Chinese | 568 / 2,706 | 404 | 149 | 15 | 19 | 2,138 | 16 / 2 |

Every encoded frame in four bounded repair windows per language is selected and mapped in `regression-summary.json`; the remaining whole-file sample retains adaptive 0.25-second motion selection and maximum gap 1 second. Eight additional individual current native views confirm fixed optimum geometry, single retained proof rows, and readable captions. All four findings are resolved in this actual image coverage, with no additional defect found. Exact original and current movie hashes were reverified against independent copies.

Only full native PNG SHA-256 equality transfers prior actual visual coverage. Every novel selected image was actually viewed at original resolution. The new-only reviewer-sheet optimization is documented separately; it does not change detection thresholds, selected frames, time gaps, or full-file decoding. Unseen internal tool sheets are not claimed as actual views. Raw receipts and complete compressed ledgers preserve the coverage chain.

Continuous perceptual playback, narration listening/synchronization, and final production-resolution motion remain unverified. The optional read-only live process-environment check was denied by OS permissions and was not retried or escalated; that runtime observation remains unavailable and does not affect capture or visual evidence. The adapter's task-specific output constant does not assign any system home environment variable, as shown by the preserved code and command environment whitelist.
