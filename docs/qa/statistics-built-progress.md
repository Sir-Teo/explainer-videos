# Statistics, Built QA progress

Branch: `statistics-built`. Review order is Part 1 through Part 65, with chapters in manifest order.
The branch contains **65 parts and 888 chapters**. All manifests resolve to existing scene files and unique scene names, and dependency fingerprinting completes for every part. The part-by-part receipts below define the scope of review.

## Current checkpoint

All 65 parts have received English scientific source review and focused numerical checks. Parts 1–65 have completed their recorded sampled visual passes. Parts 19–22 are finishing their conservative shared-source refreshes; all other current source fingerprints are reconciled. Part 65's six computation items are reconciled, including the complete 319-row historical Board from all 57 contributing parts.

A [shared World programme-name collision](evidence/world-programmes-20261107/README.md) has been corrected. The [Coverage Board now preserves empirical Monte Carlo uncertainty](evidence/board-mc-20261107/README.md) for correlated intervals within one simulation. Legacy-row values are unchanged. Parts 1–22 retain the visual inspections recorded at their commits; their conservative shared-code fingerprints are being refreshed after the Board correction. Parts 1–19 have completed that latest refresh; remaining parts are being refreshed. Part 23's final receipts include the corrected shared source.

The latest [complete statistics/QA regression](evidence/statistics-final-regression-20261107/README.md) passed 1,138 tests and 10 subtests across 145 files. Its 15 warnings remain visible in the log. Individual evidence folders retain focused scientific checks and numerical input hashes. A subsequent Part 65 cache-load guard passes its 25-check focused regression, including six new dependency-change cases; numerical outputs are unchanged. A subsequent Part 51 curve-clipping repair passes all 14 local checks, including three new tiny-delta and viewport cases. These results do not establish production playback approval.

[Review provenance](evidence/review-provenance-20261107/README.md) now pins inspected thumbnails to exact image hashes under the capture locks. A retrospective comparison covers 607 available current captures; all five obsolete thumbnail differences are reconciled, including a fresh Part 52 inspection.

No part is signed off for bilingual production. The branch has zero narration_zh.json tables and no stats_text_zh.json; full narrated masters and continuous listening/playback remain separate gates. Existing translation warnings remain visible.

## Review checklist per part

1. Read the part's README, compute items and every scene in manifest order; reconcile formulas, numbers, assumptions and historical claims.
2. Run relevant numerical/reference regressions and compute seeded inputs.
3. Capture every English chapter's narration endpoints; inspect the sheets and fix clipping, overlaps, blank narration beats and misleading encodings.
4. Check changed geometry at native 1080p; render representative transitions and any repaired motion.
5. Check actual speech signals/alignment, narrated synchronization and full playback; keep silent estimates distinct from narrated evidence.
6. Supply and verify Chinese narration, numeric templates and on-screen translations before bilingual approval.
7. Save a source/data-keyed receipt, current findings and remaining gates before continuing to the next part.

## Part-by-part status

| Part | Video | Chapters | Review status |
|---|---|---:|---|
| 1 | [stats1](evidence/stats1-polish-20261106/README.md) | 16 | English source/visual pass complete; production gates open |
| 2 | [stats2](evidence/stats2-polish-20261106/README.md) | 16 | English source/visual pass complete; production gates open |
| 3 | [stats3](evidence/stats3-polish-20261106/README.md) | 16 | English source/visual pass complete; production gates open |
| 4 | [stats4](evidence/stats4-polish-20261106/README.md) | 14 | English source/visual pass complete; production gates open |
| 5 | [stats5](evidence/stats5-polish-20261106/README.md) | 16 | English source/visual pass complete; production gates open |
| 6 | [stats6](evidence/stats6-polish-20261106/README.md) | 15 | English source/visual pass complete; production gates open |
| 7 | [stats7](evidence/stats7-polish-20261106/README.md) | 13 | English source/visual pass complete; production gates open |
| 8 | [stats8](evidence/stats8-polish-20261106/README.md) | 14 | English source/visual pass complete; production gates open |
| 9 | [stats9](evidence/stats9-polish-20261107/README.md) | 13 | English source/visual pass complete; production gates open |
| 10 | [stats10](evidence/stats10-polish-20261107/README.md) | 14 | English source/visual pass complete; production gates open |
| 11 | [stats11](evidence/stats11-polish-20261107/README.md) | 13 | English source/visual pass complete; production gates open |
| 12 | [stats12](evidence/stats12-polish-20261107/README.md) | 13 | English source/visual pass complete; production gates open |
| 13 | [stats13](evidence/stats13-polish-20261107/README.md) | 15 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 14 | [stats14](evidence/stats14-polish-20261107/README.md) | 13 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 15 | [stats15](evidence/stats15-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 16 | [stats16](evidence/stats16-polish-20261107/README.md) | 13 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 17 | [stats17](evidence/stats17-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 18 | [stats18](evidence/stats18-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 19 | `stats19` | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 20 | [stats20](evidence/stats20-polish-20261107/README.md) | 15 | English source/visual pass complete; production gates open |
| 21 | [stats21](evidence/stats21-polish-20261107/README.md) | 13 | English source/visual pass complete; production gates open |
| 22 | [stats22](evidence/stats22-polish-20261107/README.md) | 15 | English source/visual pass complete; production gates open |
| 23 | [stats23](evidence/stats23-polish-20261107/README.md) | 13 | English source/visual pass complete; production gates open |
| 24 | [stats24](evidence/stats24-polish-20261107/README.md) | 14 | English source/visual pass complete; production gates open |
| 25 | [stats25](evidence/stats25-polish-20261107/README.md) | 15 | English source/visual pass complete; production gates open |
| 26 | [stats26](evidence/stats26-polish-20261107/README.md) | 15 | English source/visual pass complete; production gates open |
| 27 | [stats27](evidence/stats27-polish-20261107/README.md) | 15 | English source and visual review complete; bilingual/listening/master gates open |
| 28 | [stats28](evidence/stats28-polish-20261107/README.md) | 13 | English source and visual review complete; bilingual/listening/master gates open |
| 29 | [stats29](evidence/stats29-polish-20261107/README.md) | 14 | English source and visual review complete; bilingual/listening/master gates open |
| 30 | [stats30](evidence/stats30-polish-20261107/README.md) | 12 | English source and visual review complete; bilingual/listening/master gates open |
| 31 | [stats31](evidence/stats31-polish-20261107/README.md) | 12 | English source and visual review complete; bilingual/listening/master gates open |
| 32 | [stats32](evidence/stats32-polish-20261107/README.md) | 13 | English source and visual review complete; bilingual/listening/master gates open |
| 33 | [stats33](evidence/stats33-polish-20261107/README.md) | 14 | English source and visual review complete; bilingual/listening/master gates open |
| 34 | [stats34](evidence/stats34-polish-20261107/README.md) | 13 | English source and sampled visual review complete; 16 checks, 13 endpoint / 12 native / 12 motion sheets; bilingual production gates open |
| 35 | [stats35](evidence/stats35-polish-20261107/README.md) | 16 | English source and sampled visual review complete; 20 checks, 16 endpoint / 15 native / 15 motion sheets; bilingual production gates open |
| 36 | [stats36](evidence/stats36-polish-20261107/README.md) | 17 | English source and visual review complete; bilingual/listening/master gates open |
| 37 | [stats37](evidence/stats37-polish-20261107/README.md) | 16 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 38 | [stats38](evidence/stats38-polish-20261107/README.md) | 14 | English source and sampled visual review complete; 19 checks, 14 endpoint / 13 native / 13 motion sheets; bilingual production gates open |
| 39 | [stats39](evidence/stats39-polish-20261107/README.md) | 16 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 40 | [stats40](evidence/stats40-polish-20261107/README.md) | 17 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 41 | [stats41](evidence/stats41-polish-20261107/README.md) | 11 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 42 | [stats42](evidence/stats42-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 43 | [stats43](evidence/stats43-polish-20261107/README.md) | 15 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 44 | [stats44](evidence/stats44-polish-20261107/README.md) | 15 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 45 | [stats45](evidence/stats45-polish-20261107/README.md) | 15 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 46 | [stats46](evidence/stats46-polish-20261107/README.md) | 14 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 47 | [stats47](evidence/stats47-polish-20261107/README.md) | 15 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 48 | [stats48](evidence/stats48-polish-20261107/README.md) | 14 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 49 | [stats49](evidence/stats49-polish-20261107/README.md) | 13 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 50 | [stats50](evidence/stats50-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 51 | [stats51](evidence/stats51-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 52 | [stats52](evidence/stats52-polish-20261107/README.md) | 13 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 53 | [stats53](evidence/stats53-polish-20261107/README.md) | 13 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 54 | [stats54](evidence/stats54-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 55 | [stats55](evidence/stats55-polish-20261107/README.md) | 8 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 56 | [stats56](evidence/stats56-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 57 | [stats57](evidence/stats57-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 58 | [stats58](evidence/stats58-polish-20261107/README.md) | 16 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 59 | [stats59](evidence/stats59-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 60 | [stats60](evidence/stats60-polish-20261107/README.md) | 13 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 61 | [stats61](evidence/stats61-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 62 | [stats62](evidence/stats62-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 63 | [stats63](evidence/stats63-polish-20261107/README.md) | 14 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 64 | [stats64](evidence/stats64-polish-20261107/README.md) | 15 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 65 | [stats65](evidence/stats65-polish-20261107/README.md) | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
