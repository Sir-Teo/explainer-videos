# Part5 Decoding: local CDF and entropy-unit repair

This source freeze follows two actual bilingual endpoint findings in [the complete50-state review](../ai5-decoding-outro-endpoint-review/README.md). The original13.5 readout crowds the fixed bits/比特 unit, and the confident-context cumulative-probability spline overshoots its near-one plateau before decreasing.

Only two local sections of `s11_decoding.py` change. The entropy number's existing updater now positions the unit0.15world units after the updated DecimalNumber; clearing the number's updater also stops unit motion. The label/number anchor, semantic colors, fonts and values are retained. The CDF path now uses straight segments through exactly the original cumulative-probability points. No probabilities are capped, saturated, rescaled or otherwise changed; no shared curve helper changes.

Every voiceover expression/bookmark and every play/wait/wait-until AST call is identical. Restoring only the two changed methods makes the complete module AST identical to the before source. No new narration or caption keys are needed.

Four actual-Manim geometry tests pass (0.479s): both exact retained cached contexts pass unchanged cumulative anchors and sampled nondecreasing/bounded paths; a frozen historical-spline recipe demonstrates the confident fixture's prior>1.01 overshoot/decrease; extreme/flat probability vectors preserve mass; and20number-width states across actual English/Chinese labels maintain number/unit and label/number gaps at least0.15world units with right clearance. Scene initialization is fail-on-call. The tiny fixture records its completedtemperatureNPZ SHA; no model inference or producer runs. The existing21decoder-focused tests also pass (0.119s). TeX glyph compilation is test geometry, not scene/video rendering.

Before source`b63ab6a919cf47dcdb053d2042b22c9ea83ce343d3faf14fe503378708df3b72`; frozen after`be8c9b419ea61ecc004d275ccbef276db838bec0a29f57801c8f4db52c63e693`. All16frozen numerical/driver source hashes and the consumed temperaturepayload bytes retain their reviewed identities. No numerical cache, decoder/core/helper, shared-caption or dataset change was made.

Exact before/after source, patch, test/fixture snapshots, raw successful logs and invariant receipt are preserved. **Fresh actual EN/ZH endpoint and full silent-motion regressions remain pending at this source freeze.** No repaired-output appearance, continuous playback, listening, narrated export or production-resolution approval is implied. Root owns rendering, source publication and later closure.
