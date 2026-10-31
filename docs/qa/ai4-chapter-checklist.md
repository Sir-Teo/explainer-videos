# Part4 chapter QA checklist

Observed 2026-10-31T23:15:01.710363+00:00. This is a runtime/actual-review inventory, not production signoff.

All38 endpoint records exist, with 537 captured endpoint appearances. Raw statuses: {'passed': 28, 'needs-review': 10}; raw warnings: 10. The38current image sets are hash-matched only where an actual reviewer receipt supplies coverage. Tail uses the observed10-case interim checkpoint; final reviewer/repository handoff remains pending.

|Position / scene|EN runtime · warning count|ZH runtime · warning count|Actual endpoint-image evidence|Other work|
|---|---|---|---|---|
|1. Hook|passed · 0|passed · 0|First-five actual image review; EN 19/19; ZH 19/19|Motion/native/audio scope separate; continuous playback unverified|
|2. Derivative|passed · 0|passed · 0|New fixed-tangent supplement + prior exact-image inheritance; EN 17/17; ZH 17/17|New tangent motion/1080review pending; audio unverified|
|3. Gradient|passed · 0|passed · 0|First-five actual image review; EN 19/19; ZH 19/19|Expected viewport clipping resolved; motion/native/audio separate|
|4. Jacobian|passed · 0|passed · 0|First-five actual image review; EN 10/10; ZH 10/10|Motion/native/audio scope separate; continuous playback unverified|
|5. Layers|passed · 0|needs-review · 1|First-five actual image review; EN 14/14; ZH 14/14|Motion/native/audio scope separate; continuous playback unverified|
|6. Modes|passed · 0|needs-review · 1|Mid-head actual endpoint review; EN 17/17; ZH 17/17|Motion/native/audio scope separate; continuous playback unverified|
|7. Backprop|passed · 0|passed · 0|Mid-head actual endpoint review; EN 17/17; ZH 17/17|Motion/native/audio scope separate; continuous playback unverified|
|8. Library|passed · 0|needs-review · 1|Mid-head actual endpoint review; EN 16/16; ZH 16/16|Motion/native/audio scope separate; continuous playback unverified|
|9. Train|passed · 0|passed · 0|Mid-head actual endpoint review; EN 13/13; ZH 13/13|Motion/native/audio scope separate; continuous playback unverified|
|10. Floats|needs-review · 1|needs-review · 1|Mid-head actual endpoint review; EN 16/16; ZH 16/16|Motion/native/audio scope separate; continuous playback unverified|
|11. GradCheck|passed · 0|passed · 0|Theory actual endpoint review; EN 14/14; ZH 14/14|Motion/native/audio scope separate; continuous playback unverified|
|12. Memory|passed · 0|needs-review · 1|Theory actual endpoint review; EN 14/14; ZH 14/14|Motion/native/audio scope separate; continuous playback unverified|
|13. Newton|passed · 0|needs-review · 1|Theory actual endpoint review; EN 10/10; ZH 11/11|Motion/native/audio scope separate; continuous playback unverified|
|14. HVP|passed · 0|passed · 0|Theory actual endpoint review; EN 10/10; ZH 10/10|Motion/native/audio scope separate; continuous playback unverified|
|15. Quadratic|passed · 0|passed · 0|Tail interim image checkpoint; final handoff pending; EN 16/16; ZH 16/16|Motion/native/audio scope separate; continuous playback unverified|
|16. Lagrange|passed · 0|passed · 0|Tail interim image checkpoint; final handoff pending; EN 17/17; ZH 17/17|Motion/native/audio scope separate; continuous playback unverified|
|17. KKT|passed · 0|needs-review · 1|Tail interim image checkpoint; final handoff pending; EN 13/13; ZH 13/13|Motion/native/audio scope separate; continuous playback unverified|
|18. Implicit|passed · 0|passed · 0|Tail interim image checkpoint; final handoff pending; EN 11/11; ZH 11/11|Motion/native/audio scope separate; continuous playback unverified|
|19. Outro|needs-review · 1|needs-review · 1|Tail interim image checkpoint; final handoff pending; EN 5/5; ZH 5/5|Motion/native/audio scope separate; continuous playback unverified|

Runtime completion does not establish visual review, and endpoint images do not establish animation/transition, speech timing/listening/sync or continuous playback. The JSON includes exact record/PNG/proof/source hashes, raw warnings and known source-fingerprint differences. Current source disk snapshots are distinct from proof of historical worker imports. Active motion/native jobs may supersede their records.

Evidence: [first five](evidence/ai4-first-five-endpoint-review/README.md), [mid-head](evidence/ai4-mid-head-endpoints/README.md), [theory](evidence/ai4-theory-endpoint-review/README.md), [numeric data](evidence/ai4-data-source-validation/README.md). The new fixed-tangent supplement is under `/workspace/runtime/ai4-derivative-tangent-repair/endpoint-review`; tail interim evidence is `/workspace/runtime/ai4-tail-endpoint-review/endpoint-review-checkpoint-10cases.json`. Neither local path is presented as published final approval.

The immutable earlier first-five package remains historical. The new Derivative supplement supersedes its moving-secant demonstration in the four changed English/Chinese endpoint states. The separate Gradient contour-seam lead was resolved as expected finite-window clipping, with zero missing interior contour segments. The wider-viewport polish and non-causal shared exact-zero helper case were not adopted in this source batch.
