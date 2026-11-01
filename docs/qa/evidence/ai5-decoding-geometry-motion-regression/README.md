# Part 5 Decoding: bilingual geometry regression

Both repaired visual issues are clear in the final English and Chinese preview artifacts: the entropy unit follows the number with a readable gap, including 13.5; the cumulative-distribution path faithfully joins the actual CDF points without overshoot or decreasing ringing. No new defect was observed in the reviewed scope.

| Language | Duration (s) | File frames decoded | Selected times | Unique PNGs actually viewed | Exact duplicate coverage | Viewed chronological pages |
|---|---:|---:|---:|---:|---:|---:|
| EN | 208.466667 | 3,127 | 485 | 353 | 132 | 45 |
| ZH | 222.8 | 3,342 | 500 | 364 | 136 | 46 |

Every selected time maps to an actually viewed unique representative by exact PNG SHA-256. All 91 chronological sheets were viewed at 640×360 per tile from 854×480 previews; 12 critical movie frames were additionally viewed individually at native size. The frozen `qa_motion.py` audit used explicit `--dense .25 --max-gap 1`: maximum selected-time gap is 1.0 second in each case, with no unavoidable source gaps. All file frames were decoded algorithmically. The 5,484 unsampled encoded frames were not visually inspected; their exact frame-index/time runs are retained in the compressed ledgers. This is complete review of the selected chronology, not continuous perceptual playback.

The 40 endpoint states comprise 12 changed states actually viewed before/after on six unscaled paired pages and 28 exact PNG matches to the previously completed baseline review. Four repaired endpoints were also viewed individually at native size. Narration records, endpoint durations and input signatures are identical before/after. Previous buggy artifact records remain immutable in the baseline package.

Native checks also covered the 10.5-digit-width transition, the 13.5 peak, CDF reveal and nucleus threshold peak, four-family chart/readouts at diversity 0.85, corrected Chinese greedy 0.54 / 35% / 4-token caption, and final sample rows. Top-k is the descriptive minimum among all four supported interpolations at the requested diversity. The mean SE 0.05 caption explicitly excludes passage SD/CI. Headline NLL is character-weighted; the mean SE concerns unweighted prompt setting means and is not uncertainty for that weighted headline. Generated English continuations remain intentionally untranslated in the Chinese lesson.

All four final endpoint/motion runtime records passed with zero warnings; their raw bytes/logs are retained compressed. This preserves runtime outcomes separately from manual visual findings. Exact source, movie, table, tool, result and input hashes are in `freeze.json`, `report.json` and the full ledgers. Closing checks confirmed source/movie/input/result bytes unchanged. The source repair is bound to `be8c9b419ea61ecc004d275ccbef276db838bec0a29f57801c8f4db52c63e693` and caption table `6220e391fe7c9bf714f5ad363b6ae8eeff3815b84f901ae5b1e5a5ec1ff9b231`.

Evidence includes six native paired before/after pages, critical individual native PNGs, complete time-to-view maps with page/frame hashes, raw render records/logs, provenance and the exact frozen analysis tool/source. Full movies and all selected frames remain in the cloud runtime/render paths recorded by the ledgers; no movies are committed here.

Continuous viewing, audio/listening/narration synchronization, final production resolution/frame rate and unsampled encoded frames remain unverified. No models, production experiments, renderers or scene construction were invoked by this review. Existing source/tests and factual repairs are documented separately in [source proof](../ai5-decoding-geometry-source/) and [baseline endpoints](../ai5-decoding-outro-endpoint-review/); this receipt adds actual final visual evidence only.
