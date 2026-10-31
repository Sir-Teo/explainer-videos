# Part 3 HighDim and JL: bilingual selected-motion QA

HighDim's reviewed selected content is clear in both languages. JL's percentage readout and final history-card margin repairs pass actual bilingual rendered regression. No remaining concrete defect was found within the documented selected-frame coverage.

| Original silent case | Decoded source frames | Selected times covered | Unique images actually viewed | Pages viewed | Native followups | Render warnings |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| EN HighDim | 2,152 | 371 | 308 | 39 | 6 | 0 |
| ZH HighDim | 2,067 | 360 | 298 | 38 | 6 | 0 |
| EN JL, after percentage repair | 2,748 | 390 | 292 | 37 | 6 | 0 |
| ZH JL, after percentage repair | 2,964 | 402 | 303 | 38 | 6 | 0 |

The original four cases cover 1,523 selected timestamps: 1,201 actually inspected unique images on 152 pages, plus 24 native followups. Their 9,931 frames were automatically decoded across the complete files. Initial bilingual endpoint review adds 68 inspected screenshots and 18 native followups. A separately preserved English readout endpoint regression adds 17 screenshots and two native checks. These are coverage counts, not a claim of continuous perceptual playback.

## Actual findings and repairs

The English JL readout originally displayed **100%** at k=400, despite the measured rate and narration being **99.6%**. The widening number also crowded its descriptor. One decimal place and a dynamic 0.2-unit text gap fix both problems without changing the data, narration or timing. [Actual native before/after](en-JL-percent-before-after.png) shows the repair; different endpoint/movie capture times are labeled explicitly. Actual EN/ZH geometry fixtures used all five completed-cache rates. Both rendered languages confirm the repair.

A native followup then found the final English history-card border touching upper strokes of “fabricated bounds” in the bottom disclosure. The shorter Chinese caption was already clear. A unified local 0.4-unit card lift adds roughly nine pixels of vertical clearance without moving the data or changing the lesson. [English native before/after](en-JL-history-before-after.png), [Chinese native before/after](zh-JL-history-before-after.png), and the [original English border crop](en-JL-history-before-border-crop.png) preserve the actual evidence.

| Final margin regression | Selected times covered | Newly viewed unique images | Exact PNG inheritance | Changed pages viewed | Native followups |
| --- | ---: | ---: | ---: | ---: | ---: |
| EN JL | 390 | 18 | 274 | 3 | 3 |
| ZH JL | 402 | 19 | 283 | 3 | 3 |

Every final selected timestamp is accounted for. All 37 changed unique images were directly inspected in chronological order, including reveal, hold and fade. The 557 inherited representatives match full PNG SHA hashes to previously actually viewed baseline images. Six native checks confirm the disclosure gap and clear plotted points, confidence line, legend and tick text. All six changed contact pages are included, with exact per-page and per-frame receipts in the compressed ledgers.

HighDim's Chinese d=10 histogram was absent from endpoint sampling but is actually present and held at 18.133–19.000 seconds in the silent movie. [Native d=10 evidence](zh-HighDim-original-native-01.png) closes that coverage gap. The [variance plot](zh-HighDim-original-native-03.png), [explicitly schematic feature diagram](zh-HighDim-original-native-04.png), [normalized histogram and absolute-spread derivation](zh-HighDim-original-native-05.png), and [exaggerated-width shell diagram](zh-HighDim-original-native-06.png) preserve representative native views. Complete temporal mappings cover the remaining selected content.

## Exact provenance

HighDim module SHA: `7ea3b0e73d85f3e65876f095416b21a4ae8165179e0246811545d52641ed1b55`.

JL after-readout module SHA: `6cb5b16754a225018b047c77c5f3913139920ebcc17019b90b873a32fe337447`.

Final JL module SHA: `b0ce1007f88106ee78554e4438d2267f32678df53819c24a06d43c13bf842ac5`.

| Reviewed movie | SHA-256 |
| --- | --- |
| EN HighDim | `2a2fced91ba48283573ab976e136655a401043b9c2b3e976c1b2c312bc107349` |
| ZH HighDim | `99740cf77fbda540bb2b8685ffa2881e9e57740ae2bb82cb704c32b4fa075473` |
| EN JL after readout repair | `eb006f0b9a848ae0c4d8a739d300601cea12aa5348b040a5e73ca03542bb5fd0` |
| ZH JL after readout repair | `1eb4979f34433bf2ebb6024a83b2d3dbdb5b4b64158b663e2398353a616026d1` |
| Final EN JL | `8a426cb1f8c5828cca9b485b912c81c366270437e015ae1131b2bbb3503217fe` |
| Final ZH JL | `dad7819ed327049736bd1e3b44d8e197426bf6f1c9b1843bcc897450189ce0b3` |

Both final JL records report passed with zero warnings and fingerprint `34b6bce39640ff3daeeb4b2d5222d9bcc0e2fb7770bc4e1ec886104addae12f0`. Their direct module and movie bytes independently match the parent's frozen handoff. The parent's initially supplied Chinese hash had an extra trailing `1`; its explicit correction and the verified 64-character hash remain in the provenance receipt.

Historical HighDim endpoint source-change warnings remain preserved. Clean later motion records do not erase those warnings. The separate English readout endpoint record `e9eff8a4…` and imported source `6cb5b167…` were explicitly attested for the 19:46–19:50 UTC worker; the later `b0ce1007…` source-at-review copy is labeled separately. Whole-part fingerprints may become stale after unrelated edits, without changing these exact reviewed artifacts. Current shared-file hashes in the manifest describe packaging time, not historical worker imports.

## Complete receipts and limits

The deterministic gzip files preserve complete scoped initial endpoint reviews, original motion reviews, temporal audits, final margin reviews, render records, input signatures/hashes, source snapshots, geometry fixtures, handoffs and review scripts. [manifest.json](manifest.json) hashes every payload and its uncompressed source. All selected timestamps, exact inheritance mappings, page-view checkpoints, native receipts, warnings and unselected source-frame gaps are retained. Absolute runtime paths are historical provenance. Full movies and original contact pages remain runtime artifacts; the complete ledgers, all final changed pages and useful native PNG examples are included here.

Frozen extraction tool SHA: `1d0cee16ad098360ceb70f9cbc513bbce334ea107e90982ace3a7fd3df73595e`. It streams full-file RGB decoding and selects transition extras plus a configured maximum one-second gap. EN JL's measured maximum `1.0000000000000018` seconds is retained as floating-point representation. Exact full-PNG equality is required for inheritance; perceptual similarity is not used.

This is selected-frame QA of silent 854×480, 15 fps previews. Unselected frames were not individually perceived, and brief or subthreshold defects may fall between selections. Continuous perceptual playback, audio listening/narration alignment, production-resolution readability and player/responsive behavior remain unverified by this package. Historical pending notes in the original consolidated report are superseded only by the separately preserved final margin report. Packaging changed only this new directory; original receipts and the Matrices/Eigen package remain unchanged.
