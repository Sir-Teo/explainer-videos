# Knowledge graph polish: bounded final evidence

Node connectors now meet the rounded boxes with consistent glyph clearance. Relation captions use the rendered label's bounding-box support along the edge normal plus 0.12 units, clearing the near-vertical Ada–London shaft. Wording, node placement, colors, arrow directions and data are preserved. The caption collision may have been preexisting; this is not attributed solely to the connector change.

Final scene source SHA256: `1ca9dc3f872f515ff74b3c2517eb2c1093727adec3eeb3aca0f8069ba86b2a76`. All four final render records passed with zero automated warnings. The saved fingerprint/input check was true at the recorded freeze, not a promise about later repository state.

| Final silent 480p case | Selected times | Exact-PNG inherited | New selected times | New unique images viewed | New sheets | Native 480p followups |
|---|---:|---:|---:|---:|---:|---:|
| EN | 423 | 363 | 60 | 45 | 6 | 3 |
| ZH | 469 | 400 | 69 | 50 | 7 | 3 |

All 892 selected times are accounted for. Every changed unique selected image was viewed chronologically; inheritance and duplicate coverage require exact PNG SHA256 equality. The frozen tool decoded 6,849 source frames; the largest selected-time gap is 1 second. **5,957 unselected source frames remain visually unreviewed.** Continuous perceptual playback and narration/listening/synchronization remain unverified.

All 41 native 1920×1080 endpoints are accounted for: 35 exact-PNG inherited native reviews and six newly viewed native images. Both final contact sheets were viewed. These endpoint jobs skip animations and use silent placeholders; they do not certify a full 1080p movie. Sixteen boundary and sixteen caption-clearance geometry cases passed (eight actual EN/ZH relations plus eight synthetic cases).

The actual PNG pairs below preserve original bytes. EN compares the original scene to final output. ZH compares the connector-only intermediate to the final caption-clearance repair; the intermediate is explicitly not the original baseline.

| Evidence | Earlier | Final |
|---|---|---|
| EN box joins and captions, 185.8s | [Original](en-before-node-joins-1080.png) | [Final](en-final-node-joins-and-captions-1080.png) |
| ZH caption clearance, 212.4s | [Intermediate collision](zh-intermediate-caption-collision-1080.png) | [Final](zh-final-caption-clearance-1080.png) |

`final-review.json.gz` gives findings, exact movie/source/tool/data hashes, scope and limitations. `final-*-motion-review-map.json.gz` contains every selected time and PNG hash, direct-view versus exact-inheritance mapping, actual sheet hashes and native followups. `final-*-temporal-audit.json.gz` retains complete selections and unextracted frame gaps. Intermediate maps, native endpoint maps and preservation receipts keep the evidence chain inspectable. Original full-series motion proof remains in `../ai2-selected-review/`; the EN original 1080p ledger is included here.

JSON is gzip-compressed without changing its uncompressed bytes; `manifest.json` records hashes and sizes of the actual compressed files and their decoded contents. Paths inside frozen ledgers refer to the cloud evidence workspace at capture time. Movies, all extracted frames and most sheets remain in that workspace and are omitted here to bound repository size. The four PNGs are supporting examples, not a substitute for the recorded full selected-time review. No audio or final production approval is implied.

The selected-review current index now has 32 cases / 14,062 selected times / 105,217 automatically decoded frames. Its original 32-case summary (14,068 / 105,217) is separately frozen as `../ai2-selected-review/summary-original-32-cases.json.gz`. The six-time decrease is the replacement EN Knowledge selection count (429→423), not missing coverage. Scene hashes are named `scene_source_sha256_at_freeze` to avoid implying current freshness. Historical warning fields remain in the index; explicit replacement render results describe the new Knowledge jobs.
