# Part 3 current chapter artifact map

Observed 2026-11-01T01:16:40.639154+00:00. This [current 38-case map](ai3-current-source-case-map.json) selects the reviewed English and Chinese SVD and Outro replacements. The [historical map at commit 927fba66](ai3-final-source-case-map.json) remains byte-for-byte intact (SHA `7cca99a8ce8a27f460fdd85ad273ace41ac757f1cd99abbdd04e51ad190d59b6`). Its commit, caption-table and import identity fields remain historical.

All 34 unreplaced movie, direct scene-module and raw result bytes still match their historical rows at this observation. All four replacement movie, module and result hashes match their closed scoped visual receipts. Raw statuses, warning lists and render fingerprints are preserved: 33 passed, five need review, and five retain warnings. These byte checks and visual gates do not establish broad aggregate-source freshness or historical worker imports.

| Replacement | Source repair | Current review cohort | Direct images | Exact prior image inheritance |
|---|---|---:|---:|---:|
| EN Outro | `6b86ee8b` | 344 | 60 | 284 |
| EN SVD | `7c47c11e` | 338 | 72 | 266 |
| ZH Outro | `6b86ee8b` | 372 | 60 | 312 |
| ZH SVD | `7c47c11e` | 356 | 72 | 284 |

SVD source `291bba0e…` is linked to its [source freeze and exact AST comparison](evidence/ai3-svd-reveal-motion-regression/freeze.json) and [bilingual encoded-window, selected-cohort and endpoint proof](evidence/ai3-svd-reveal-motion-regression/README.md). Its repair commit is `7c47c11e3802390141c9551ac376ebe4ddf31e0e`.

Outro source `e874a8da…` is linked to [four actual-Manim tests and source/before proof](evidence/ai3-outro-path-front-repair/README.md) and [every repaired descent frame plus baseline-cohort visual regression](evidence/ai3-outro-trail-motion-regression/README.md). Its repair commit is `6b86ee8b8c1a9a080c90b8d7f4d78880dcf724e0`. Both replacement module hashes match the exact inventory of the [421-test frozen source run](evidence/integrated-outro-gradient-20261101/receipt.json), which passed with unchanged before/after source inventories. That historical source test run is separate from rendered visual proof and audio approval.

The current review cohort totals **15,014 time appearances** from 101,263 automatically decoded frames; **86,249 encoded frames remain individually unseen**. Exact derivation: 14,729 − (227 + 250 + 310 + 338) + (338 + 356 + 344 + 372). This retains the other 34 case review scopes and substitutes the four expanded repair cohorts. It is not a new uniform or every-frame full-series viewing run.

This update adds no native 1080p motion, listening, pronunciation, synchronization, player/responsive or continuous perceptual playback approval. The original 695 native 1080p endpoint images and original 19-chapter/36-join assembly reviews remain historical. No new assembly or Library upload was performed; replacement assemblies require a separate parent-owned operation and review.
