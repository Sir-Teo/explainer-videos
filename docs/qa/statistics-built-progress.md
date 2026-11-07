# Statistics, Built QA progress

Branch: `statistics-built`. Review order is Part 1 through Part 65, with chapters in manifest order.
The branch contains **65 parts and 888 chapters**. All manifests resolve to existing scene files and unique scene names, and dependency fingerprinting completes for every part. This inventory is not scientific or visual approval of the other parts.

## Current checkpoint

All 65 parts have received English scientific source review and focused numerical checks. Parts 1–55 and 58–62 have completed their recorded sampled visual passes. The remaining visual checks are running, including fresh source-matched renders after the layout repairs. Part 65's six computation items are reconciled, including the complete 319-row historical Board from all 57 contributing parts.

A [shared World programme-name collision](evidence/world-programmes-20261107/README.md) has been corrected. The [Coverage Board now preserves empirical Monte Carlo uncertainty](evidence/board-mc-20261107/README.md) for correlated intervals within one simulation. Legacy-row values are unchanged. Parts 1–22 retain the visual inspections recorded at their commits; their conservative shared-code fingerprints are being refreshed after the Board correction. Parts 1–13 have completed that latest refresh; further parts remain queued. Part 23's final receipts include the corrected shared source.

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
| 1 | `stats1` | 16 | English source/visual pass complete; production gates open |
| 2 | `stats2` | 16 | English source/visual pass complete; production gates open |
| 3 | `stats3` | 16 | English source/visual pass complete; production gates open |
| 4 | `stats4` | 14 | English source/visual pass complete; production gates open |
| 5 | `stats5` | 16 | English source/visual pass complete; production gates open |
| 6 | `stats6` | 15 | English source/visual pass complete; production gates open |
| 7 | `stats7` | 13 | English source/visual pass complete; production gates open |
| 8 | `stats8` | 14 | English source/visual pass complete; production gates open |
| 9 | `stats9` | 13 | English source/visual pass complete; production gates open |
| 10 | `stats10` | 14 | English source/visual pass complete; production gates open |
| 11 | `stats11` | 13 | English source/visual pass complete; production gates open |
| 12 | `stats12` | 13 | English source/visual pass complete; production gates open |
| 13 | `stats13` | 15 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 14 | `stats14` | 13 | English source/visual pass complete; production gates open |
| 15 | `stats15` | 12 | English source/visual pass complete; production gates open |
| 16 | `stats16` | 13 | English source/visual pass complete; production gates open |
| 17 | `stats17` | 12 | English source/visual pass complete; production gates open |
| 18 | `stats18` | 12 | English source/visual pass complete; production gates open |
| 19 | `stats19` | 12 | English source/visual pass complete; production gates open |
| 20 | `stats20` | 15 | English source/visual pass complete; production gates open |
| 21 | `stats21` | 13 | English source/visual pass complete; production gates open |
| 22 | `stats22` | 15 | English source/visual pass complete; production gates open |
| 23 | `stats23` | 13 | English source/visual pass complete; production gates open |
| 24 | `stats24` | 14 | English source/visual pass complete; production gates open |
| 25 | `stats25` | 15 | English source/visual pass complete; production gates open |
| 26 | `stats26` | 15 | English source/visual pass complete; production gates open |
| 27 | `stats27` | 15 | English source and visual review complete; bilingual/listening/master gates open |
| 28 | `stats28` | 13 | English source and visual review complete; bilingual/listening/master gates open |
| 29 | `stats29` | 14 | English source and visual review complete; bilingual/listening/master gates open |
| 30 | `stats30` | 12 | English source and visual review complete; bilingual/listening/master gates open |
| 31 | `stats31` | 12 | English source and visual review complete; bilingual/listening/master gates open |
| 32 | `stats32` | 13 | English source and visual review complete; bilingual/listening/master gates open |
| 33 | `stats33` | 14 | English source and visual review complete; bilingual/listening/master gates open |
| 34 | `stats34` | 13 | English source and sampled visual review complete; 16 checks, 13 endpoint / 12 native / 12 motion sheets; bilingual production gates open |
| 35 | `stats35` | 16 | English source and sampled visual review complete; 20 checks, 16 endpoint / 15 native / 15 motion sheets; bilingual production gates open |
| 36 | `stats36` | 17 | English source and visual review complete; bilingual/listening/master gates open |
| 37 | `stats37` | 16 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 38 | `stats38` | 14 | English source and sampled visual review complete; 19 checks, 14 endpoint / 13 native / 13 motion sheets; bilingual production gates open |
| 39 | `stats39` | 16 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 40 | `stats40` | 17 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 41 | `stats41` | 11 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 42 | `stats42` | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 43 | `stats43` | 15 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 44 | `stats44` | 15 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 45 | `stats45` | 15 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 46 | `stats46` | 14 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 47 | `stats47` | 15 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 48 | `stats48` | 14 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 49 | `stats49` | 13 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 50 | `stats50` | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 51 | `stats51` | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 52 | `stats52` | 13 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 53 | `stats53` | 13 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 54 | `stats54` | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 55 | `stats55` | 8 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 56 | `stats56` | 12 | Scientific source and numerical reconciliation complete; 18 checks pass; visual verification pending |
| 57 | `stats57` | 12 | Scientific source and numerical reconciliation complete; 20 checks pass; visual verification pending |
| 58 | `stats58` | 16 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 59 | `stats59` | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 60 | `stats60` | 13 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 61 | `stats61` | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 62 | `stats62` | 12 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 63 | `stats63` | 14 | English scientific source reviewed; 20 checks pass; sampled visual review pending; bilingual/listening/master approval open |
| 64 | `stats64` | 15 | English scientific source reviewed; 23 checks pass; sampled visual review pending; bilingual/listening/master approval open |
| 65 | `stats65` | 12 | English scientific source and all numerics reviewed; 25 checks pass; 319 historical Board rows reconciled; sampled visual review pending |
