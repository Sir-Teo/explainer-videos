# Part1 Counting, Shannon1951 and Likelihood: EN/ZH temporal frame review

Completed six assigned cases. Every one of the **2,624 selected times** was actually viewed in **330 chronological contact sheets**, with **eight native854×480 followups**. No duplicate-only inference was used. One persistent visual readability defect and one bounded transition-polish finding remain for the parent-owned repair batch. No source code, cache, narration, model, render, commit or remote write was performed by this review task.

## Actual coverage

| Case | Movie duration (s) | Selected times viewed | Sheets viewed | Native followups | Source frames unviewed |
|---|---:|---:|---:|---:|---:|
| en-Counting | 279.999 | 599 | 75 | 4 | 3601 |
| en-Shannon1951 | 129.933 | 287 | 36 | 0 | 1662 |
| en-Likelihood | 177.733 | 375 | 47 | 1 | 2291 |
| zh-Counting | 307.266 | 665 | 84 | 3 | 3944 |
| zh-Shannon1951 | 139.733 | 319 | 40 | 0 | 1777 |
| zh-Likelihood | 186.800 | 379 | 48 | 0 | 2423 |

All native movies are854×480 at15fps. Sheets show8 selected frames per page at640px thumbnail width. The frozen extraction tool decoded all18,322 source frames for motion selection; that automated decode is distinct from human/model visual inspection. **15,698 source frames were not visually viewed.** Every selected time, selection reason, source frame index, frame SHA256, page SHA256, page time span and intervening unviewed gap is embedded in the JSON ledger. Maximum selected-time gap is1.0s (one floating-point value1.0000000000000284s). The full first-to-last decoded span is covered by selection, including titles and fades.

## Findings

**C01 — Counting annotation is crossed by the graph curves (EN and ZH).** The wide best-test label is centered above the minimum dot, placing its left portion over the declining train/test curves near context orders2–3. Native EN94.600s confirms the curve crossing the first words; the defect persists through selected holds to approximately115.9s. The Chinese label has the same problem from approximately103.6–127.2s. The source is [s10_counting.py:133](/workspace/explainer-videos/videos/ai/ai1/s10_counting.py:133). Place the annotation in clear graph space with a leader or opaque local backing, then recheck both languages and the entire hold.

- EN native evidence: [94.600s](/workspace/explainer-videos/renders/qa/temporal/ai1-en-Counting-dense-final/frames/0001419_000094.600s.png), SHA256 `0bb7a7900dff9028a345fe3810102c85df1aa888bd9bcd85269527d79b9bc7ee`.
- ZH native evidence: [103.533s](/workspace/explainer-videos/renders/qa/temporal/ai1-zh-Counting-dense-final/frames/0001553_000103.533s.png), SHA256 `c09da74e80a0f7aa3d349e88146bcfc033937c8947129a7530ca2a4a8511bba6`. The fully opaque annotation is also visible in sheet034.

**C02 — Counting ladder copies create brief glyph stacks and cross an explanatory line.** Native EN166.533s shows the copied equation traveling across the explanatory line. At180.666s and185.733s the moving row copies overlap formula glyphs. Native ZH187.066s and203.666s also show formula stacking; the Chinese explanatory text is positioned differently and is not crossed in these inspected native examples. All affected transitions resolve to clear endpoints. This is a bounded polish finding, not a lasting collision or continuous-playback judgment. Caller [s10_counting.py:271](/workspace/explainer-videos/videos/ai/ai1/s10_counting.py:271) uses the shared ladder helper. A crossfade or travel path outside the text rows is a possible repair; shared-helper changes require regression.

- EN [166.533s](/workspace/explainer-videos/renders/qa/temporal/ai1-en-Counting-dense-final/frames/0002498_000166.533s.png), SHA256 `0a5ce491027bf85f9cc1a22b7723ffd612ea5a85334771978415613476498656`.
- EN [180.666s](/workspace/explainer-videos/renders/qa/temporal/ai1-en-Counting-dense-final/frames/0002710_000180.666s.png), SHA256 `29b9c7d866ae192e439df8e012c7e5c8e3c1a9f344a66957a13a3621d2a8f460`.
- EN [185.733s](/workspace/explainer-videos/renders/qa/temporal/ai1-en-Counting-dense-final/frames/0002786_000185.733s.png), SHA256 `229aedb1fda4de0a680ade0062300af8fb768f6eef61ecd0029ee78565b9a9b7`.
- ZH [187.066s](/workspace/explainer-videos/renders/qa/temporal/ai1-zh-Counting-dense-final/frames/0002806_000187.066s.png), SHA256 `1cc57f0deae78640b98d833a9021abc5ee9d50e2052f2c4f5983fc55de5d7104`.
- ZH [203.666s](/workspace/explainer-videos/renders/qa/temporal/ai1-zh-Counting-dense-final/frames/0003055_000203.666s.png), SHA256 `74e64a58bb10e92733da4264b987516b8dc6e715ceac961e3b4b0808ebbcf083`.

**No additional definite clipping or persistent collision was identified in the selected Shannon1951 or Likelihood frames in either language.** This is a bounded observation, not a full visual sign-off. Shannon coverage includes the sender/receiver reconstruction, entropy inequality, histogram, numerical bounds, counting-model comparison, human interval, and later historical caveat. Likelihood coverage includes the product/log/grouping derivation, histogram rearrangement, KL minimization, logits/exponentiation/normalization bars, neural-network callout, derivative explainer, softmax gradient and final forward references. Counting coverage includes the sample text, MLE rule, context-performance curves, sparsity examples, Bayesian smoothing derivation, prior/posterior illustration, alpha comparisons and closing references.

The Likelihood chapter-reference crossfade was investigated in native EN38.800s. The chapter reference fades out as the new explanatory caption appears, and the endpoint is clear; it was not classified as a lasting collision. ZH42.3–43.1s shows the equivalent clean resolution in the selected sequence.

## Provenance and verification

Frozen `tools/qa_motion.py` SHA256: `1d0cee16ad098360ceb70f9cbc513bbce334ea107e90982ace3a7fd3df73595e`. All six audit JSON hashes, original render-result hashes, six movie hashes,330 sheet hashes and2,624 frame-file hashes were reverified after review. Original cached input size/mtime signatures still match at completion; current input SHA256 values are embedded in the ledger.

| Case | Exact movie SHA256 |
|---|---|
| en-Counting | `fd5fd9e6133b75c2efabdd16dc438637304c13197d38df39d57e4586eb82fdda` |
| en-Shannon1951 | `aca7e82d8322508698fc2d10e665a88f47ef7ea5e2e91658a898f640a2d67754` |
| en-Likelihood | `362e158c187c866cc547107db9a11dadb1211b0a99e47cbd65196599f18d2dd5` |
| zh-Counting | `b26d2ddf16fdbd9f426a9b329f28284d4690ff0b40e8cad6d64ee156a13d15ea` |
| zh-Shannon1951 | `cc066fdab3527261ce68b5e89dc6944779158483b6206ceb1cbef64d9acb5458` |
| zh-Likelihood | `bef4c0226f05a6e76377e3510540c48f7baadcc398ea08a8f86fd02097aeecc0` |

The original render broad fingerprints are stale (`current_source_and_inputs:false`), including unrelated caption and Hook edits. This review applies to the exact movie hashes above. Original render fingerprints/input signatures and completion-time hashes of the three scenes, common helper, local Chinese narration, manifest and shared visual/lecture modules are retained. Completion-time hashes are not represented as original per-file render provenance.

Full machine-readable ledger: [ai1-counting-shannon-likelihood-motion-review.json](/workspace/runtime/ai1-counting-shannon-likelihood-motion-review.json). Ledger SHA256 at this report generation: `68a17697c531f6fd9a9a330139cddfd59dc8c5b0018c87914e48dbb4048aba08`.

## Remaining scope

- Selected-frame inspection is not continuous perceptual playback. Unextracted source frames remain unviewed, with exact gaps preserved per case.
- Maximum selected-time gap is1 second; motion-onset/midpoint/dense/endpoint frames supplement that bound, without guaranteeing capture of every transient.
- Source movies are silent480p15 previews; narrated timing, audio/listening/synchronization, final1080p output, player/responsive behavior were not assessed.
- Original render broad fingerprints are stale. These results apply only to the exact movie hashes recorded here, not current whole-repository approval.
- Current relevant source hashes are a completion-time snapshot only; original render results did not record per-file source hashes. Original input file size/mtime signatures and render fingerprint are retained.

The parent owns repairs and subsequent before/after rendering. Neither finding has been changed or rerendered by this task. There were no denied or pending tool operations and no access blockers.
