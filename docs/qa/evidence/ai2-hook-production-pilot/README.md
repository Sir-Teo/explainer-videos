# Part 2 Hook EN: original full 1080p30 silent pilot

This is the **pre-mask baseline**, rendered from Hook source `eba5f33461813b36c7044ef7aa99d9f98860c9db66173594197e409e8449d3cd`. The render completed and selected-frame review found a minor existing timeline defect. Root subsequently applied source `06587b3781f0cd7dc71d1e75fcacd771975b7c251f87a35032df8fe8096c7a29`; this baseline does not validate that repair. Repair evidence must remain separately versioned.

The original movie SHA256 is `2921773c921ca1e29fc3eec668ab2ba3a8c787fbd6eb000e22a2a5f500cd7956`. It is 1920×1080, nominal 30fps, 127.532031 seconds, with 3,826 video frames. All frames decoded successfully. Worker runtime was 639.24 seconds; the guarded process took 654.45 seconds (about 10m54s), with nice 15 observed and one numeric/encoder thread requested. Disk stayed above 4.82 GiB during rendering and 4.60 GiB during extraction; neither guard stopped and no new OOM kill occurred. Resource readings include concurrent root jobs, so they are not attributed solely to the pilot.

| Actual visual coverage | Count |
|---|---:|
| Selected encoded movie times, maximum gap 1 second | 246 |
| Unique images viewed chronologically in 22 sheets | 175 |
| Exact-PNG duplicate selected times | 71 |
| Encoded frames additionally viewed individually at native size | 9 |
| Raw worker captures viewed individually at native size | 15 |
| Source frames not visually inspected | 3,580 |

All selected PNGs are native 1920×1080, while sheets scale their tiles. The complete map distinguishes actual sheet views, exact duplicates and individual native followups. No 480p visual inheritance is used. Continuous perceptual playback, narration/listening/synchronization, and target-editor playback remain unverified. This one case does not approve Part 2 or predict full-series render cost.

The green 1971 STRIPS stem crosses the 1970 year-label zero, confirmed in encoded native frames at 39.566341s and 55.699674s. The 1980 event stem also enters its year-label box near an inter-glyph gap. See [early timeline](timeline-1970-stem-encoded-1080.png) and [complete timeline](timeline-complete-encoded-1080.png). The [opening score](opening-score-encoded-1080.png), method boxes, 31-part map and [objectives](objectives-encoded-1080.png) were clear in the native held states checked. A dense map/objectives crossfade briefly overlaps text near 100.032s; this is recorded as an optional design-polish candidate, with a clear held objective state.

Decoded PTS are strictly increasing. Of 3,825 intervals, 3,821 are 512 ticks (33.333333ms) and four are 507 ticks (33.0078125ms), at time base 1/15360. Maximum cadence jitter is 0.325521ms; average frame rate is `4897280/163241` (about 30.000306fps). These differences are an editor-compatibility lead, not demonstrated playback failure. The original stream metadata and full decoded timestamps are preserved; no transcode was performed.

An AAC 48kHz stereo placeholder stream exists, lasting 126.165333s. The original private wrapper incorrectly asserted that no audio stream would exist, after the worker had passed with zero automated QA warnings. Its exit 1, executed code/hash and original result remain preserved. Separate metadata reconciliation records the actual streams without rerendering; a corrected private wrapper is also preserved but was not executed for this baseline. `render.log` retains both this failed postcondition and the encoder's unused `shortest`/`metadata` mux-option warning. Neither is silently relabeled as a successful wrapper run or a demonstrated movie failure.

`manifest.json` records actual packaged bytes and hashes, including compressed and decoded hashes for gzip files. The main report, every selected-time/PNG mapping, native-view receipts, temporal gaps, source/tool/wrapper provenance, full decode, timestamps, resource samples and archive receipt are included. Four supporting PNGs are exact decoded movie frames. Movies, all extracted frames and most sheets remain in the cloud workspace under `renders/qa/production-motion-1080/`; immutable initial movie/source/record copies are under `archive-initial/`. Their omission here bounds repository size and does not expand the recorded review scope.

The independent process-environment read `/proc/516361/environ` was OS-denied (EACCES); it was not retried or bypassed. Requested thread limits are established by preserved launch/code, and nice 15 was independently observed. This probe limitation did not block the pilot. No producer/data/global table/canonical 480p/CI/CD changes were made by the pilot owner.
