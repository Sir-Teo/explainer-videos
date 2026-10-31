# Part 1 tail: sampled endpoint visual review

Inspected **18 EN/ZH contact sheets** across Arithmetic, Counting, Shannon1951, Likelihood, Information, Knowledge, Units, Scoreboard and Outro (326 endpoint thumbnails), plus **20 priority frames at native 854×480**. No concrete clipping or text-collision defect was observed in this scoped pass. No source edits, renders or compute were performed.

**This is sampled endpoint review, not continuous playback or audio sign-off.** Sheet thumbnails do not establish native-size readability for every frame. Priority native checks cover the revised Kraft note, selected context, independent Shannon comparison, shared-logit qualifier, joint two-letter caption, context heatmap, 31-model benchmark scope, packed bytes, Hutter footer and Gaussian recap.

## Case evidence

|Language|Chapter|Fingerprint prefix|Captured QA status|Native priority frame(s)|
|---|---|---|---|---|
|en|Arithmetic|55f0083d2b24|passed|026_00264.3s.png|
|en|Counting|55f0083d2b24|needs-review|013_00095.2s.png|
|en|Shannon1951|a3b80ce4acb5|passed|008_00073.7s.png|
|en|Likelihood|a3b80ce4acb5|passed|017_00154.6s.png|
|en|Information|a3b80ce4acb5|passed|005_00037.4s.png|
|en|Knowledge|a3b80ce4acb5|passed|006_00062.6s.png|
|en|Units|a3b80ce4acb5|passed|011_00109.7s.png|
|en|Scoreboard|a3b80ce4acb5|passed|014_00126.3s.png, 018_00183.0s.png|
|en|Outro|a3b80ce4acb5|passed|000_00038.5s.png|
|zh|Arithmetic|55f0083d2b24|needs-review|026_00269.5s.png|
|zh|Counting|a3b80ce4acb5|passed|014_00104.2s.png|
|zh|Shannon1951|a3b80ce4acb5|passed|008_00076.8s.png|
|zh|Likelihood|a3b80ce4acb5|passed|018_00159.0s.png|
|zh|Information|a3b80ce4acb5|passed|005_00041.5s.png|
|zh|Knowledge|a3b80ce4acb5|passed|006_00063.7s.png|
|zh|Units|a3b80ce4acb5|passed|011_00122.9s.png|
|zh|Scoreboard|a3b80ce4acb5|passed|014_00125.1s.png, 018_00182.8s.png|
|zh|Outro|a3b80ce4acb5|needs-review|000_00044.1s.png|

## Findings

- **Arithmetic:** Kraft normalization/code-weight qualifier fits between bidirectional arrows and compressed-size equation; no clipping or text collision in either language.
- **Counting:** The selected minimum is explicitly labeled best on this scored passage. Caption fits above the k=5 point and remains legible; linework crosses the plot area as intended.
- **Shannon1951:** Independent smoothed order-5 comparison, 2.02 bits, is separated from ideal-guess rank bounds. Caption fits in right-hand note stack.
- **Likelihood:** Shared-logit toy-model qualifier is legible below the pointwise derivative; neither language collides with bottom edge or main formula.
- **Information:** Joint previous-two-letters qualifier and lag-two-alone value fit on one bottom line. Main entropy and Venn elements remain clear. Memory/control annotations visible in sheet; native detail of memory plot not re-reviewed in this pass.
- **Knowledge:** Two token heatmaps fit and context comparison (13.0 vs 3.5 bits) fits below them. Legends and attribution remain separated. No conclusion about audio or continuous highlight animation.
- **Units:** 31 models across 12 benchmarks/domain-matched wording and Pearson -0.93 fit above schematic. Citation remains inside frame.
- **Scoreboard:** 688-byte packed known-length payload qualifier is legible in two bottom lines. Estimated whole-passage size is qualified. Hutter July24,2026 total100,424,672 bytes / 0.80bits per input byte footer and Oct31 check date fit without citation collision.
- **Outro:** All eight recap tiles fit. Both narrow and broad Gaussian pairs have curved peaks without the earlier flat cap; curves stay within tile. Bilingual labels fit at native frame size.

## Provenance and limits

All immutable snapshot originals, exact source fingerprints, input-current flags, source-current-at-snapshot flags, warning records and SHA-256 hashes are in [ai1-tail-visual-review.json](/workspace/runtime/ai1-tail-visual-review.json). Each case lists only files actually inspected separately from the full preserved file inventory. Chinese English-text-marker misses are translation effects; visually revised Chinese captions were confirmed.

Three QA records carry `source-changed-during-render`: EN Counting, ZH Arithmetic and ZH Outro. These are metadata warnings, not observed layout failures. Captures used source fingerprints `55f0083d2b24237cdfe45313eac0318f72ad00827b57c760d3dd81d4fb072045` or `a3b80ce4acb50a631be6be6f23cb1bf432e0ef923e839b119d296d0d22fc4a40`. Parent authorized inspection after head/shared translation edits invalidated chapter-global fingerprints; final source-current validation belongs to the refreshed parent pipeline.

Not covered: continuous playback, animation continuity, motion interpolation, final audio pronunciation, signal quality, narration synchronization, native inspection of every endpoint, or unrendered conditional failure branches. No denied/pending tool action blocked this review.
