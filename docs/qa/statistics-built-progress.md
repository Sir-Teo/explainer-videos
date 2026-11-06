# Statistics, Built QA progress

Branch: `statistics-built`. Review order is Part 1 through Part 65, with chapters in manifest order.
The branch contains **65 parts and 888 chapters**. All manifests resolve to existing scene files and unique scene names, and dependency fingerprinting completes for every part. This inventory is not scientific or visual approval of the other parts.

## Current checkpoint

Parts 1–3 have received chapter-by-chapter English source reviews and visual repair passes. All 48 current English endpoint captures are free of runtime, clipping and blank-beat warnings. Parts 1 and 2 each have six native 1080p cases; Part 3 has seven. Part 1 has four silent motion checks, and Parts 2 and 3 each have two. Representative narrated previews have six, six and seven clean signal/alignment checks respectively. The combined statistics/QA suite passes 554 tests and five subtests. [Part 1 evidence](evidence/stats1-polish-20261106/README.md) and [Part 2 evidence](evidence/stats2-polish-20261106/README.md), and [Part 3 evidence](evidence/stats3-polish-20261106/README.md).

Parts 4 and 5 have completed their scientific source correction passes. Part 4's final visual checks are in progress, and Part 5's first visual sweep is queued.

No part is signed off for bilingual production. The branch has zero `narration_zh.json` tables and no `stats_text_zh.json`; full narrated masters and continuous listening/playback remain separate gates. Existing translation warnings remain visible.

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
| 4 | `stats4` | 14 | Scientific source corrections complete; visual verification in progress |
| 5 | `stats5` | 16 | Scientific source corrections complete; visual verification pending |
| 6 | `stats6` | 15 | Not yet reviewed chapter by chapter |
| 7 | `stats7` | 13 | Not yet reviewed chapter by chapter |
| 8 | `stats8` | 14 | Not yet reviewed chapter by chapter |
| 9 | `stats9` | 13 | Not yet reviewed chapter by chapter |
| 10 | `stats10` | 14 | Not yet reviewed chapter by chapter |
| 11 | `stats11` | 13 | Not yet reviewed chapter by chapter |
| 12 | `stats12` | 13 | Not yet reviewed chapter by chapter |
| 13 | `stats13` | 15 | Not yet reviewed chapter by chapter |
| 14 | `stats14` | 13 | Not yet reviewed chapter by chapter |
| 15 | `stats15` | 12 | Not yet reviewed chapter by chapter |
| 16 | `stats16` | 13 | Not yet reviewed chapter by chapter |
| 17 | `stats17` | 12 | Not yet reviewed chapter by chapter |
| 18 | `stats18` | 12 | Not yet reviewed chapter by chapter |
| 19 | `stats19` | 12 | Not yet reviewed chapter by chapter |
| 20 | `stats20` | 15 | Not yet reviewed chapter by chapter |
| 21 | `stats21` | 13 | Not yet reviewed chapter by chapter |
| 22 | `stats22` | 15 | Not yet reviewed chapter by chapter |
| 23 | `stats23` | 13 | Not yet reviewed chapter by chapter |
| 24 | `stats24` | 14 | Not yet reviewed chapter by chapter |
| 25 | `stats25` | 15 | Not yet reviewed chapter by chapter |
| 26 | `stats26` | 15 | Not yet reviewed chapter by chapter |
| 27 | `stats27` | 15 | Not yet reviewed chapter by chapter |
| 28 | `stats28` | 13 | Not yet reviewed chapter by chapter |
| 29 | `stats29` | 14 | Not yet reviewed chapter by chapter |
| 30 | `stats30` | 12 | Not yet reviewed chapter by chapter |
| 31 | `stats31` | 12 | Not yet reviewed chapter by chapter |
| 32 | `stats32` | 13 | Not yet reviewed chapter by chapter |
| 33 | `stats33` | 14 | Not yet reviewed chapter by chapter |
| 34 | `stats34` | 13 | Not yet reviewed chapter by chapter |
| 35 | `stats35` | 16 | Not yet reviewed chapter by chapter |
| 36 | `stats36` | 17 | Not yet reviewed chapter by chapter |
| 37 | `stats37` | 16 | Not yet reviewed chapter by chapter |
| 38 | `stats38` | 14 | Not yet reviewed chapter by chapter |
| 39 | `stats39` | 16 | Not yet reviewed chapter by chapter |
| 40 | `stats40` | 17 | Not yet reviewed chapter by chapter |
| 41 | `stats41` | 11 | Not yet reviewed chapter by chapter |
| 42 | `stats42` | 12 | Not yet reviewed chapter by chapter |
| 43 | `stats43` | 15 | Not yet reviewed chapter by chapter |
| 44 | `stats44` | 15 | Not yet reviewed chapter by chapter |
| 45 | `stats45` | 15 | Not yet reviewed chapter by chapter |
| 46 | `stats46` | 14 | Not yet reviewed chapter by chapter |
| 47 | `stats47` | 15 | Not yet reviewed chapter by chapter |
| 48 | `stats48` | 14 | Not yet reviewed chapter by chapter |
| 49 | `stats49` | 13 | Not yet reviewed chapter by chapter |
| 50 | `stats50` | 12 | Not yet reviewed chapter by chapter |
| 51 | `stats51` | 12 | Not yet reviewed chapter by chapter |
| 52 | `stats52` | 13 | Not yet reviewed chapter by chapter |
| 53 | `stats53` | 13 | Not yet reviewed chapter by chapter |
| 54 | `stats54` | 12 | Not yet reviewed chapter by chapter |
| 55 | `stats55` | 8 | Not yet reviewed chapter by chapter |
| 56 | `stats56` | 12 | Not yet reviewed chapter by chapter |
| 57 | `stats57` | 12 | Not yet reviewed chapter by chapter |
| 58 | `stats58` | 16 | Not yet reviewed chapter by chapter |
| 59 | `stats59` | 12 | Not yet reviewed chapter by chapter |
| 60 | `stats60` | 13 | Not yet reviewed chapter by chapter |
| 61 | `stats61` | 12 | Not yet reviewed chapter by chapter |
| 62 | `stats62` | 12 | Not yet reviewed chapter by chapter |
| 63 | `stats63` | 14 | Not yet reviewed chapter by chapter |
| 64 | `stats64` | 15 | Not yet reviewed chapter by chapter |
| 65 | `stats65` | 12 | Not yet reviewed chapter by chapter |
