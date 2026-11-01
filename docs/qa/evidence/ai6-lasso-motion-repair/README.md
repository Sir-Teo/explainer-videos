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

The candidate and exact baseline hashes are in `summary.json` and `freeze.json`. Fresh parent-owned English and Chinese endpoint and full silent-motion regressions are pending. The candidate is not visually accepted yet. Independent original movie copies remain runtime witnesses; no movies were hardlinked. Original raw `passed` records and empty warning arrays remain intact. Later helper files do not retrospectively prove historical imports or broad source currency.

The supplemental endpoint baseline also covers all 19 English and 18 Chinese images, actually viewed at native resolution on six chronological sheets. Per-image and per-page proof is in each `endpoint-review.json.gz`. Endpoint coverage remains distinct from motion coverage.

`patch.diff.gz` losslessly preserves the exact patch. Source snapshots and complete compressed ledgers support review; full movies and numerical or model payloads are excluded.
