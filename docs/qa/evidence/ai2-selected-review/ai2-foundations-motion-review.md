# Part 2 foundations: selected-frame visual review

Completed 2026-10-31T16:32:11.583613+00:00. Hook, Turing, Search and AStar in English and Chinese have all selected appearances covered. The final Hook report supersedes its separately retained baseline.

Current eight movies: 23,832 frames automatically decoded; 3,149 selected appearances mapped (2,041 directly inspected, 877 exact PNG duplicates of inspected representatives, 231 inherited by exact PNG SHA from completed baseline). All selected time gaps are at most one second. 258 chronological pages directly reviewed across these reports.

| Case | Decoded | Selected | Direct | Exact duplicate | Exact baseline | Original capture |
|---|---:|---:|---:|---:|---:|---|
| en/AStar | 3425 | 486 | 357 | 129 | 0 | needs-review |
| en/Hook | 1910 | 272 | 40 | 1 | 231 | passed |
| en/Search | 2658 | 327 | 225 | 102 | 0 | passed |
| en/Turing | 3378 | 471 | 328 | 143 | 0 | needs-review |
| zh/AStar | 3336 | 479 | 358 | 121 | 0 | passed |
| zh/Hook | 2169 | 282 | 196 | 86 | 0 | passed |
| zh/Search | 3007 | 342 | 212 | 130 | 0 | passed |
| zh/Turing | 3949 | 490 | 325 | 165 | 0 | needs-review |

The missing 1997 DeepBlue label was caused by concurrent reveal and emphasis on the same initially invisible label. Hook now sequences the label reveal and emphasis inside the original one-second interval. The local roadmap is 12.5% larger (scale 0.8 to 0.9), preserving semantic colors. Both final silent language movies verify the repaired label through reveal/hold and the enlarged roadmap without clipping. No additional concrete visual defects were found in the six assigned Turing/Search/AStar movies.

Hook before/after evidence and native follow-ups: [ai2-hook-repair-review.json](/workspace/runtime/ai2-hook-repair-review.json) and [ai2-hook-repair-review.md](/workspace/runtime/ai2-hook-repair-review.md).
Frozen original baseline: /workspace/runtime/ai2-foundations-motion-evidence/completed-baseline-review.json.

The JSON preserves every selected time, PNG hash, directly viewed page hash/time range, representative mapping, movie/source/tool/input provenance and original capture warning. EN Turing, ZH Turing and EN AStar retain source-changed-during-render warnings. The audit’s whole-part current-source flag remains recorded as captured; this report does not turn warnings into a clean production pass.

Limitations:

- Silent 854x480 render review using chronological selected frames with maximum one-second gaps and additional transition samples; not continuous perceptual playback.
- All source frames were automatically decoded at 320x180 for RGB transition analysis; that does not establish direct visual inspection of every frame.
- Only byte-identical selected PNGs inherit a viewed representative; exact times and mappings are preserved in frame_coverage.
- No listening, narration alignment, full-resolution render or responsive-player verification by this agent.
- Original source-changed-during-render warnings remain for EN Turing, ZH Turing and EN AStar. Whole-part audit current_source_and_inputs remains as captured; matching scene-source hashes are narrower evidence and do not erase warnings.
