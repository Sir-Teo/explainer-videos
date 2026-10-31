# Part 1 cross-entropy and arithmetic repair review

Completed: 2026-10-31T14:59:29.122490+00:00

All three reported issues are resolved in the reviewed English and Chinese movies. No new defect was observed in this regression scope.

| Case | Selected times covered | Exact baseline inheritance | Changed times | Changed unique images inspected |
| --- | ---: | ---: | ---: | ---: |
| en/CrossEntropy | 531/531 | 488 | 43 | 33 |
| en/Arithmetic | 576/576 | 562 | 14 | 14 |
| zh/CrossEntropy | 557/557 | 512 | 45 | 37 |
| zh/Arithmetic | 594/594 | 580 | 14 | 13 |

The audit decoded 16506 frames automatically. All 2258 selected times are covered: 2142 inherit only byte-identical PNG evidence from actually inspected baseline images; 116 changed times map to 97 newly inspected unique native PNGs on 8 sheets. Full mappings preserve every selected frame, timestamp, SHA256 and evidence page.

Additional targeted inspection covered all 125 consecutive source frames in four repair windows on 10 sheets, plus 6 native follow-ups.

## Verified behavior

- Rounded cross-entropy examples use `≈` in both languages; the exact symbolic `H(p,q) = H(p) + D_KL(p||q)` remains unchanged. Native text is readable and separated.
- Final arithmetic codeword transform, pulse and hold retain a clear gap to `sent:`/`发送:` throughout the checked source frames. The original overlap is absent at its previously failing timestamps.
- Rare-c emphasis colors only the tiny selected cell and its probability readout. Other bins and labels remain visible, preserving the probability geometry.

## Consecutive-frame risk windows

| Case | Window | First/last source time | Source frames inspected |
| --- | --- | --- | ---: |
| en/Arithmetic | sent-pulse | 235.063–237.196s | 33 |
| en/Arithmetic | rare-cell | 84.533–86.200s | 26 |
| zh/Arithmetic | sent-pulse | 240.863–243.197s | 36 |
| zh/Arithmetic | rare-cell | 86.866–88.800s | 30 |

## Provenance and evidence

- Detailed report and full mappings: `/workspace/runtime/ai1-theory-repair-review.json`.
- Actual view ledger: `/workspace/runtime/ai1-theory-repair-views.json`.
- Distinct repaired audit folders: `renders/qa/temporal/ai1-{en|zh}-{CrossEntropy|Arithmetic}-repaired-final`.
- Changed-image pages: each folder’s `changed-review/`; consecutive risk windows: `all-frame-sent-pulse/` and `all-frame-rare-cell/`.
- All four render records report `passed` with no warnings. Source/input provenance was current when each audit ran and was checked again at final review. Fingerprint: `c7679c4a581f8f795949b96b25c745441a6c16012ca24d0a9de18b096272d8b8`.
- Audit tool SHA256: `1d0cee16ad098360ceb70f9cbc513bbce334ea107e90982ace3a7fd3df73595e`. Exact movie, render-record, audit, page and input hashes are retained in JSON.
- Preserved before movies in `renders/qa/ai1-final-layout-batch/before/{lang}/{Scene}/movie.mp4` match the exact movie hashes from the baseline review.

## Limits

- Continuous perceptual playback remains unavailable and unverified.
- These are silent proxy-narration movies; actual audio listening and narrated synchronization remain unverified.
- Manual whole-movie coverage is the listed selected-frame schedule (at most1second gaps), with inherited evidence only on exact native PNG byte equality. Other unsampled frames are not manually reviewed.
- Only the four local risk windows receive every-source-frame inspection. Production-resolution readability requires production review.
- No scene rendering, recomputation, repository source edits, commits or pushes were performed by this reviewer.
