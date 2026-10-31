# Entropy q/z repair regression

Entropy q/z callout collision resolved in both languages; all new selected PNG content inspected and all remaining selected content inherited only by exact PNG SHA from completed baseline. No new confirmed visual defect.

| Language | Decoded frames | Selected appearances | Exact baseline inheritance | Newly inspected representatives | Exact duplicates of new views | Unreviewed selected |
|---|---:|---:|---:|---:|---:|---:|
| en | 3927 | 617 | 587 | 29 | 1 | 0 |
| zh | 4205 | 615 | 587 | 23 | 5 | 0 |

All seven changed-content sheets were inspected in source-time order (EN 4, ZH 3), including labels appearing, area note, steady holds and outgoing fades. Native 854x480 followups confirm q/z are distinct and each leader points back to the corresponding narrow bar. No new clipping or collision observed.

The captured q bounding box is x=[5.147687602,5.271906352], y=[0.865391527,1.079454027]. The z box is x=[5.720099286,5.834161786], y=[1.069419025,1.221762775]. Horizontal clearance is **0.448192933 world units** in both languages, so the bounding boxes are disjoint despite the overlapping vertical ranges. Both endpoint captures in each language confirm the same bounds.

Source comparison against the preserved pre-fix s04 module shows only the q/z horizontal offsets and leader-line addition. The area/sliver geometry expressions are unchanged. All six data-cache input files retain their exact baseline SHA256 hashes.

Before/after native evidence (original movie time differs slightly between ZH before/after; hashes tie each frame to its movie):

- EN: `ai1-entropy-repair-evidence/en/before-native.png` (34.866s) → `ai1-entropy-repair-evidence/en/after-native.png` (34.866s).
- ZH: `ai1-entropy-repair-evidence/zh/before-native.png` (37.266s) → `ai1-entropy-repair-evidence/zh/after-native.png` (35.266s).

New movies and temporal audit/capture snapshots are frozen under `ai1-entropy-repair-evidence/{en,zh}/`. The JSON preserves complete time-to-coverage mappings, representative links, bounds, hashes, original capture fingerprints and exact baseline-report SHA.

Both original new captures report `passed`, zero warnings. The frozen bounded-gap audit tool SHA256 is `1d0cee16ad098360ceb70f9cbc513bbce334ea107e90982ace3a7fd3df73595e`; largest selected-time gap is 1 s (floating-point epsilon aside).

- en movie SHA256 `b6a58a72dc670aa47c2da4574706687e0b2a7ab8fe561424282dcb4624d7e8df`; audit current_source_and_inputs=`true`.
- zh movie SHA256 `babb289d429bee0398b7dfb35b554f099413133b72d7b553761bb975611b6f1f`; audit current_source_and_inputs=`true`.

Continuous perceptual playback, unsampled frames, narration/listening/sync and final-resolution sign-off remain unverified. No repo source edits, compute jobs, Manim renders, commits or pushes performed by this reviewer.
