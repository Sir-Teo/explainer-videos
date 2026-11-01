# Part 5 selected endpoint regression

**Accepted for the reviewed endpoint states.** All 93 fresh states are accounted for: 77 PNGs are byte-identical to previously viewed baseline states; all 16 changed images were actually inspected at native 854×480. No new endpoint defect was observed. This is not full motion or audio approval.

| Case | Captured states | Exact PNG inheritance | Changed states viewed native |
| --- | ---: | ---: | ---: |
| EN Brownian | 11 | 7 | 4 |
| EN MonteCarlo | 19 | 17 | 2 |
| EN ScoreFn | 16 | 14 | 2 |
| ZH Brownian | 12 | 8 | 4 |
| ZH MonteCarlo | 19 | 17 | 2 |
| ZH ScoreFn | 16 | 14 | 2 |

MonteCarlo now uses a clearly labelled 2.6–3.7 vertical window and outward triangle markers for estimates outside it. The data line has no fabricated flat caps. The final 3.158 readout, rare-hit cohorts and ESS panels remain unchanged. ScoreFn shows a straight score line cropped at the viewport; its ES smoothed-objective star and diagnostics remain unchanged. Brownian retains the raw extreme path values in the expanded local range and explicitly labels the mean/± across-path standard deviation in English and Chinese.

| Critical comparison | Before | After |
| --- | --- | --- |
| EN MonteCarlo | [before](images/051286d8716a704fcde9059414e8ec020dbdac273f71a5efc8af06d447a0d98a.png) | [after](images/14ce973a86bae9da637f226f1737fe86b8842bfb81da039a25bf7ba304e68ff7.png) |
| ZH MonteCarlo | [before](images/5934f0d023b962753475abc8c1cf745a7ad43187535956eb041a9fda05c05b16.png) | [after](images/dc7b11d3b8d7f002e7d84073fb5300eab8becd4c43bbf50519d238f7d241010a.png) |
| EN ScoreFn | [before](images/03c2110df93ca72f4af5929d68698a08379ec1437ba77a6d8aeb168d9a9e5792.png) | [after](images/ce43784ad6525fbe54345d62be9d8c787a30dddd3785edd69af2e602ae95ea7e.png) |
| ZH ScoreFn | [before](images/3fe29dcdbb9f60218e4eea8c661273ce5880454945267498d2cc1ad97b16c5ab.png) | [after](images/20161fc24b3c5e0cdaa4341d90cf09786cd65764b60547f7ee81072e33e8ede5.png) |
| EN Brownian | [before](images/69fcb3c56b2c9edeaf1456b8cda0c1dfcd85f5c9cf1628610a6c0ae7605a30a6.png) | [after](images/6379318406aa8a321d5746bbcee85b126a3c5282ff0fbeebea83629be7942220.png) |
| ZH Brownian | [before](images/f9134ac54d7b5bd0b4f732fb38f7258208108711ba21bf77e75a657e2bf6557e.png) | [after](images/06ff9f620e0aff678fe503356a1b62881efb5d0af73ecc19ce986ba1d64ec1c2.png) |

Every fresh PNG is retained losslessly and deduplicated by SHA. `comparison.json.gz` maps all 93 before/after PNG and decoded RGB identities to actual baseline-view receipts. All 77 inherited images match both PNG bytes and RGB pixels; there are no RGB-only substitutions. Sixteen unchanged native followups inherit exact native-view evidence, in addition to the 16 newly viewed native states. The original eight-case baseline covers 130 states at 427×240 sheet-tile scale and 32 native followups. Historical MCMC baseline views remain historical; this package does not claim a fresh current-fingerprint MCMC review.

The six fresh raw runtime records report passed with zero warnings. Their original visual/full-playback/narrated-playback pending flags are preserved in compressed raw evidence. All narration captures, selected times/reasons, total durations and input signatures match the baseline exactly. Current canonical PNG/record/text/log/sheet bytes, source observations and consumed data bytes were verified unchanged after review. Broad fingerprints differ between baseline and fresh runs and remain explicit; source snapshots are observations, not proof of historical in-memory imports.

`raw/` preserves exact original records, text collections, render logs and freezes as lossless gzip. `sources/` and `source-repair/` preserve before/after code, the private caption proposal, geometry and focused tests. `root-integration/` retains the root-owned 507-test/47.923-second passing receipt and source inventory; the reviewer did not rerun that suite or numerical experiments. `gzip-original-byte-receipts.json` records decoded hashes. No movies or numerical-cache payload copies are included.

Remaining gates: full/dense motion and transition review; continuous perceptual playback; real narration/audio/listening/synchronization; native 1080p/4K; player/responsive behaviour. In particular, the first MonteCarlo 4.000 readout and early triangle entrance are absent from these endpoint captures and still need actual motion verification. No source, pipeline, cache or translation-table changes, renders, commits or uploads were performed during this regression review.
