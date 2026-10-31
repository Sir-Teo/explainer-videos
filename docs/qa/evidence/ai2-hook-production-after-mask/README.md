# Hook EN: after-mask 1080p30 selected-frame regression

The year-label repair is visually verified in the recorded selected images. The 1970 zero is clear of the green 1971 STRIPS stem; the 1980 date box is protected. Neighboring event labels, Deep Blue Indicate peak, winter bands and axis entrance remain readable. No additional geometry defect was observed.

| Exact native movie evidence | Before | After |
|---|---|---|
| 39.566341s, 1970 label |[Original](../ai2-hook-production-pilot/timeline-1970-stem-encoded-1080.png)|[Clear](timeline-1970-clear-encoded-1080.png)|
| 55.699674s, complete timeline |[Original](../ai2-hook-production-pilot/timeline-complete-encoded-1080.png)|[Clear](timeline-complete-clear-encoded-1080.png)|

Before source SHA256: `eba5f33461813b36c7044ef7aa99d9f98860c9db66173594197e409e8449d3cd`; movie `2921773c921ca1e29fc3eec668ab2ba3a8c787fbd6eb000e22a2a5f500cd7956`. After source: `06587b3781f0cd7dc71d1e75fcacd771975b7c251f87a35032df8fe8096c7a29`; movie `c966e2f624258bd1dffe3c3e85fa701276ecf2d70ecd28c0926eaf434cab39d9`. The new movie lives in a separately versioned output; the baseline audio-assertion failure and artifacts remain untouched.

All 246 selected times are accounted for: 179 exact-PNG inherited baseline views and 67 changed times, represented by 59 new images actually viewed chronologically across 8 sheets plus 8 exact duplicates. Eight encoded frames were also viewed individually at native 1920×1080, including entrance, first affected hold, 1980 reveal, Deep Blue Indicate and final timeline holds. Sheets scale their native image tiles. The maximum selected-time gap is 1 second. **3,580 source frames remain visually unreviewed; continuous playback, listening/synchronization and target-editor approval remain unverified.**

All 3,826 frames decoded successfully. Video remains 1920×1080, nominal 30/1, average 4897280/163241, duration 127.532031s. Decoded PTS strictly increase: 3,821 intervals of 512 ticks and 4 of 507 ticks at 1/15360 timebase; maximum cadence jitter 0.325521ms. AAC 48kHz stereo placeholders remain, 126.165333s. Original movie, metadata and timestamps are preserved; no transcode. Tiny cadence variation and unused mux-option warnings are compatibility leads, not demonstrated playback failures.

The worker remains **needs-review**, with its original `source-changed-during-render` warning and process exit 1. The corrected wrapper completed stream inspection and all postconditions. Hook source 06587b37, manifest, render tools and wrapper hashes stayed unchanged. Root supplied an exact shared Chinese-caption delta: one added Part 3 outer-product rank caption at 19:23 UTC, existing entries unchanged. Its before/after table hashes and receipt are packaged. This explains the conservative aggregate warning for the unrelated EN Hook render; it does not refresh the fingerprint. A later LowRank caption addition happened after encoding and cannot explain the earlier warning. Source-specific geometry approval is kept separate from aggregate freshness.

The guarded render took 576.28 seconds; worker+checks 569.28 seconds. Native extraction took 249.15 seconds while other root jobs ran. Nice 15 and all five numeric-thread variables 1 are recorded inside the executed wrapper; encoder threads requested 1. Disk stayed≥4.26GiB during rendering and≥4.16GiB during extraction, with no guard stop/new OOM. Resource samples are global and cannot be attributed solely to this case.

`review.json.gz` and `selected-comparison-map.json.gz` retain exact before/after hashes, all 246 time mappings,actual sheet/native views and gaps. Full decoded timestamps, stream metadata, resources, source/wrapper snapshots and warning receipts are included. `manifest.json` hashes actual compressed repository bytes and decoded contents. Movies, all frames and most sheets stay in the cloud under `renders/qa/production-motion-1080-after-year-mask/`; the original baseline proof is in the adjacent pilot directory. No giant movies are packaged.

Only one after-mask EN Hook production movie was rendered. No producer/data/global caption/source/STATUS/CI/CD edits or commits were made by this agent. Root owns bilingual 480p/native endpoint regression and publication. The optional dense map→objectives crossfade polish candidate is unchanged; its held reading state remains clear.

The exact repaired silent1080p30 movie is saved in Library as `libfile_c99fc4a4ffc0819184863822fd859ec4`,version0,2,912,593bytes. MovieSHA c966e2f624258bd1dffe3c3e85fa701276ecf2d70ecd28c0926eaf434cab39d9; source06587b37. Returned version attribute is applied locally. Native player progression of this new artifact remains pending; this is not a narrated file.
