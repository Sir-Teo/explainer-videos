# Part5 Decoding and Outro: actual bilingual endpoint review

All **50** captured states were actually inspected at original854×480 pixel scale on **15** unscaled four-up pages, plus **8** individual native followups. No exact-image inheritance substitutes for a new view in this review. The four raw endpoint records passed with **zero warnings**; runtime status is preserved independently of visual findings.

| Case | Captured states viewed | Unscaled pages | Individual native followups | Visual outcome |
|---|---:|---:|---:|---|
| EN Decoding |19|5|3|Two repairs required|
| ZH Decoding |21|6|3|Same two repairs required|
| EN Outro |5|2|1|Captured states accepted|
| ZH Outro |5|2|1|Captured states accepted|

Decoding's actualv3 graphic readouts match the completed data: humanreference1.01nats/character, greedy0.54,35% repeatedtoken4-grams, andSE0.05. At diversity0.85, all four rules have observed support; displayed interpolation is temperature1.043, top-k0.959, top-p1.003, min-p0.987. Top-k is the descriptive one-run minimum. The repaired Chinese greedy caption keeps digit4 and35%; Chinese axis/unit/SEtext fits. Real sampled prose remains English inbothlanguages intentionally. The mean SE summarizes unweighted promptwise means; headline NLL ischaracterweighted. No weighted-meanSE, CI or fullrawcharacter-count claim is made.

Two concrete defects require a local Decoding source repair:

1. **Entropy unit crowding:** EN005 at36.856308s andZH005 at42.260992s show the13.5 readout crowding the fixed bits/比特 label; the initial9.0 layout does not reserve enough changing-number space. See the preserved individual native images.
2. **CDF spline overshoot:** EN010 at71.996208s andZH011 at77.810417s show the confident-context running-total curve rising above its final near-one plateau, then decreasing/ringing. A cumulative probability must be monotone. The local source sends exact cumulative values through a smooth spline. The proposed repair is a piecewise-linear path through those unchanged points, without clipping or saturation.

Outro's10 states show the eight-panel synthesis, later-part continuity map, six exercises, illustrative least-squares teaser and bibliography/sourcecredits without an observed overlap or clipping defect. This accepts only those captured states, not transitions, narration attribution, playback or future production audio.

Frozen directscene SHA256: Decoding`b63ab6a919cf47dcdb053d2042b22c9ea83ce343d3faf14fe503378708df3b72`; Outro`c9e0e67ffe3b8976b1a5cea82de634312c3083300e79652ae927580cc2464fd9`. Shared captiontable snapshot`6220e391fe7c9bf714f5ad363b6ae8eeff3815b84f901ae5b1e5a5ec1ff9b231`. Every consumed JSON/NPZ has unchanged render-size/mtime and actualcontentSHA matching the completed28-item audit. Each complete ledger preserves every original PNG/time/reason/hash, actual viewed page/hash, nativefollowup, rawstatus/warning, source fingerprint, input hashes and provenance.

`report.json.gz` and per-case complete compressedledgers/rawresults retain the complete coverage map. Eight useful native images and exact source/tool/table snapshots are included; no movies. All50 originalPNG and15native pages remain at `/workspace/runtime/ai5-decoding-outro-endpoint-review/`. Source repairs and their future fresh regression must be recorded separately; these before findings are not rewritten into a pass. No models, inference, producer, renderer, TTS, data/source/globaltable edits, Drive or local execution occurred during this review.
