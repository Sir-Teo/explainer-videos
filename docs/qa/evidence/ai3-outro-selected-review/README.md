# Outro: recap typography repair and scoped visual regression

The two longest recap footers now use two centered lines at their original font size. The full “separately peak-normalized” and “generalized shifted PMI” qualifications remain visible. No picture, tile box, other caption, measured data, narration or animation code changed. The parent merged exactly four new Chinese caption keys; the retained table delta has no changed or removed entries.

| English footer | Before glyph height at 854×480 | After line heights at 854×480 | After line heights at native 1920×1080 |
|---|---:|---:|---:|
| Spectra qualifier | 6.73 px | 11.48 / 11.34 px | 25.82 / 25.51 px |
| SGNS qualifier | 8.08 px | 11.63 / 9.14 px | 26.17 / 20.57 px |

These measurements come from actual captured text bounds. Both fresh native 480p recap frames and **all 12 fresh native 1920×1080 endpoint images** were inspected. Footers clear the diagrams and box edges; no clipping or overlap was found. Pixel comparison of the 480p recap images found **zero changed pixels outside the two footer rectangles**. The other ten 480p endpoint images exactly match the already inspected baseline PNGs.

| Current silent 480p case | Selected times | Exact-PNG inherited from inspected baseline | New unique images inspected | New chronological sheets inspected | New native encoded followups | Decoded frames | Individually unviewed frames |
|---|---:|---:|---:|---:|---:|---:|---:|
| EN | 310 | 239 | 71 | 9 | 3 | 2,159 | 1,849 |
| ZH | 338 | 269 | 69 | 9 | 3 | 2,355 | 2,017 |

All **648 current selected times** are accounted for through 508 exact-PNG inheritances and 140 new images actually inspected across 18 sheets, plus six fresh native encoded followups. Every inherited time maps to an exactly matching PNG in the completed baseline review. The maximum selected-time gap is one second within floating-point tolerance. Both complete movies were automatically decoded, but **3,866 source frames were not individually visually reviewed**. This is selected-frame regression, not continuous perceptual playback or narration/listening/synchronization approval.

The separate baseline review inspected all 12 native 480p endpoints, 558 unique images on 70 chronological sheets and 12 encoded native followups, accounting for 643 selected times through 85 exact duplicates. Historical counts are preserved and are not added to the current total. EN's five additional selected times reflect the detector responding to the larger captions; movie durations and decoded-frame counts did not change.

All six fresh **cached-only** jobs passed with zero QA-result warnings: bilingual 480p endpoints, bilingual complete silent 480p movies, and bilingual native 1080p endpoints. All 29 existing focused visual-math, narration and layout tests passed. Fresh motion logs retain Manim's warning that `shortest`/`metadata` mux options were unused; stream probes and full decode audits completed. Both movies contain AAC silent timing-placeholder streams. No assertion of absent audio streams or reviewed narration is made.

## Evidence and provenance

- `final-review.json.gz` contains exact current counts, per-case movie/source/tool/record hashes, checklist, evidence paths and limitations.
- `*-selected-frame-review-map.json.gz` accounts for every current selected time, exact baseline inheritance, new actual page inspection and native followup.
- `*-temporal-audit.json.gz` retains automatic full-decode selections and unextracted-frame gaps.
- `after-freeze.json.gz` retains all six render records' associations, the 94-file source-hash ledger, input signatures/hashes, images and preserved movies. The new records match the frozen aggregate fingerprint at review time.
- `captured-footer-glyph-bounds.json.gz`, `source-and-pixel-scope-checks.json.gz` and `shared-caption-delta.json.gz` retain bounded geometry, unchanged-pixel and exact translation-change evidence.
- `baseline/` preserves original endpoint/motion records, the complete old selected-review maps, exact old scene source, numerical recap checks and baseline images. Historical canonical movie paths may now refer to the replacement movie; the baseline freeze explicitly identifies the separately preserved immutable old movie and its hash.

Final scene source SHA256: `4e1d29200637256128acf72ecffd0f02caaf6733a4222808dd0b32bf82981ed7`. Chinese table SHA256: `075af7895f39456b287f7e8a6e7dbc4e2c36798e72d4adb2aafe6858251e1d3a`. After-render fingerprint: `198fd0d4f6fb8f222bd2ab0506043e8f7be158187036539d81c490848dca3bbf`. Numerical JSON/NPZ input bytes and signatures stayed unchanged. Original baseline fingerprints and warning history remain untouched. The later baseline source snapshot differs from the original baseline aggregate after unrelated changes and is not represented as import-time bytes.

Historical QA input ledgers track JSON/NPZ signatures and omit the new integrity sidecars. Later sidecar observations remain explicitly separate from original consumed-input attestation. No numerical production computation, model/training or synthesis was performed for this repair. Native 1080p captures skip animations; **no full 1080p movie, final narrated export, player/responsive QA, primary bibliography verification or full production approval is implied**.

## Actual image examples

| Language | Before 480p | After 480p | After native 1080p |
|---|---|---|---|
| EN | [Before](baseline/en-recap-before-480.png) | [After](en-recap-after-480.png) | [Native](en-recap-after-native1080.png) |
| ZH | [Before](baseline/zh-recap-before-480.png) | [After](zh-recap-after-480.png) | [Native](zh-recap-after-native1080.png) |

These are actual unmodified PNG bytes. They illustrate the repair; the full coverage claims rely on the complete mapped review ledgers. Gzip members preserve exact decoded bytes. `manifest.json` records actual packaged compressed and decoded hashes/sizes and excludes itself. Full movies, all extracted PNGs and sheets remain in the cloud evidence workspace and are omitted to bound repository size. Paths inside frozen records identify that workspace at capture time.
