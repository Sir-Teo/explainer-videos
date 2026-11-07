# Statistics, Built QA progress

Branch: `statistics-built`. Review order is Part 1 through Part 65, with chapters in manifest order.
The branch contains **65 parts and 888 chapters**. All manifests resolve to existing scene files and unique scene names, and dependency fingerprinting completes for every part. This inventory is not scientific or visual approval of the other parts.

## Current checkpoint

Parts 1–24 have completed chapter-by-chapter English source/visual passes, recorded in their evidence folders and commits. [Part 23](evidence/stats23-polish-20261107/README.md) includes thirteen endpoint captures, twelve native 1080p cases, eleven motion checks and a 333.932-second narrated Cluster preview with nine clean speech checks. Part 26 also has a completed English source/visual pass: fifteen chapter captures, fourteen native and motion checks and an eight-line narrated Hierarchy preview. Part 25 also has a completed English source/visual pass: fifteen chapter captures, fourteen native and motion checks, and a 276.199-second GLMM preview with seven clean speech checks. Parts 27–30 have also completed their English source and visual passes; the table below records later parts separately.

A [shared World programme-name collision](evidence/world-programmes-20261107/README.md) has been corrected. The [Coverage Board now preserves empirical Monte Carlo uncertainty](evidence/board-mc-20261107/README.md) for correlated intervals within one simulation. Legacy-row values are unchanged. Parts 1–22 retain the visual inspections recorded at their commits; their conservative shared-code fingerprints are being refreshed after the Board correction. Parts 1–12 have completed that latest refresh; further parts remain queued. Part 23's final receipts include the corrected shared source.

The earlier broad statistics/QA run passed 645 tests and five subtests. The related Parts 23–27 regression passed 108 tests and five subtests after the latest shared corrections; individual evidence folders retain their focused numerical checks and input hashes. These results do not establish production playback approval.

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
| 13 | `stats13` | 15 | English source/visual pass complete; production gates open |
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
| 37 | `stats37` | 16 | Scientific source corrections and 23 checks complete; visual verification in progress |
| 38 | `stats38` | 14 | English source and sampled visual review complete; 19 checks, 14 endpoint / 13 native / 13 motion sheets; bilingual production gates open |
| 39 | `stats39` | 16 | Scientific source and numerical reconciliation complete; 22 checks pass; visual verification pending |
| 40 | `stats40` | 17 | English scientific source and sampled visual review complete; bilingual/listening/master approval open |
| 41 | `stats41` | 11 | Scientific source corrections complete; visual verification in progress |
| 42 | `stats42` | 12 | Scientific source corrections complete; visual verification in progress |
| 43 | `stats43` | 15 | Scientific source corrections complete; visual verification in progress |
| 44 | `stats44` | 15 | Scientific source corrections and 14 checks complete; visual verification in progress |
| 45 | `stats45` | 15 | Scientific source corrections and 19 checks complete; visual verification in progress |
| 46 | `stats46` | 14 | Scientific source corrections and 20 checks complete; visual verification in progress |
| 47 | `stats47` | 15 | Scientific source corrections and 16 checks complete; visual verification in progress |
| 48 | `stats48` | 14 | Scientific source corrections and 18 checks complete; visual verification in progress |
| 49 | `stats49` | 13 | Scientific source and numerical reconciliation complete; 14 checks pass; visual verification pending |
| 50 | `stats50` | 12 | Scientific source and numerical corrections complete; 17 checks pass; visual verification pending |
| 51 | `stats51` | 12 | Scientific source and numerical reconciliation complete; 17 checks pass; visual verification pending |
| 52 | `stats52` | 13 | Scientific source and numerical reconciliation complete; 19 checks pass; visual verification pending |
| 53 | `stats53` | 13 | Scientific source and numerical reconciliation complete; 21 checks pass; visual verification pending |
| 54 | `stats54` | 12 | Scientific source and numerical reconciliation complete; 23 checks pass; visual verification pending |
| 55 | `stats55` | 8 | Scientific source and numerical reconciliation complete; 21 checks pass; visual verification pending |
| 56 | `stats56` | 12 | Scientific source and numerical reconciliation complete; 18 checks pass; visual verification pending |
| 57 | `stats57` | 12 | Scientific source and numerical reconciliation complete; 20 checks pass; visual verification pending |
| 58 | `stats58` | 16 | Scientific source and numerical reconciliation complete; 23 checks pass; visual verification pending |
| 59 | `stats59` | 12 | Scientific source and numerical reconciliation complete; 23 checks pass; visual verification pending |
| 60 | `stats60` | 13 | Not yet reviewed chapter by chapter |
| 61 | `stats61` | 12 | Not yet reviewed chapter by chapter |
| 62 | `stats62` | 12 | Not yet reviewed chapter by chapter |
| 63 | `stats63` | 14 | Not yet reviewed chapter by chapter |
| 64 | `stats64` | 15 | Not yet reviewed chapter by chapter |
| 65 | `stats65` | 12 | Not yet reviewed chapter by chapter |
