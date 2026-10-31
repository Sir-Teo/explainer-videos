# Part 1 foundations: dense motion review

All six selected-time appearance reviews completed; one shared P2 q/z label collision confirmed in both Entropy languages; no additional concrete defect found in Prefix/Huffman. Not production sign-off.

Cloud-only review of existing 854x480, 15 fps silent movies. No source changes, compute jobs, model inference, new Manim renders, commits or pushes were performed by this reviewer.

Branch `qa/ai-series-cloud-20261031`, HEAD at completion `c73844a472fc083bf003eaa6e40d677190cbf015`. Movie/source/input/tool hashes, per-page inspection timestamps and frame-by-frame coverage mappings are in `ai1-foundations-motion-review.json`.

| Case | Decoded frames | Selected appearances | Directly inspected | Exact PNG duplicate coverage | Unreviewed selected | Movie duration |
|---|---:|---:|---:|---:|---:|---:|
| en/Entropy | 3927 | 617 | 568 | 49 | 0 | 261.797s |
| zh/Entropy | 4205 | 615 | 481 | 134 | 0 | 280.330s |
| en/Prefix | 3456 | 512 | 401 | 111 | 0 | 230.400s |
| zh/Prefix | 3672 | 533 | 419 | 114 | 0 | 244.800s |
| en/Huffman | 2964 | 395 | 296 | 99 | 0 | 197.600s |
| zh/Huffman | 3287 | 420 | 293 | 127 | 0 | 219.133s |

The fixed audit tool `qa_motion.py` SHA256 `1d0cee16ad098360ceb70f9cbc513bbce334ea107e90982ace3a7fd3df73595e` decoded complete files using RGB transition detection, bounded gaps at 1 s (floating point epsilon aside), plus onset/midpoint/end extras. Every distinct selected appearance was inspected in chronological order on contact sheets; only exact PNG byte hashes justify duplicate reuse. The JSON distinguishes directly viewed selected indices from exact duplicate coverage.

## Confirmed finding

- **F-ENT-01 (P2), both languages:** q and z labels collide above adjacent rare surprise slivers in `s04_entropy.py:53`. EN native frame 523 at 34.866s; ZH native frame 559 at 37.266s. Bounds measured from captured scene data intersect: z x=[5.440099,5.554162], y=[1.069419,1.221763]; q x=[5.427688,5.551906], y=[0.865392,1.079454]. Separate rare-symbol callouts or show one label while preserving measured bars. Reported to parent; not edited here.

Native before evidence:

- `ai1-foundations-motion-evidence/en/Entropy/native-followups/0000523_000034.866s.png`
- `ai1-foundations-motion-evidence/zh/Entropy/native-followups/0000559_000037.266s.png`

A preliminary apparent global text-corruption lead at EN Entropy 21.4s was rejected after native image/pixel comparison; it is not a supported defect.

## Regression observations

- Prefix EN/ZH decoder paths, tree/interval Kraft construction, converse example, McMillan count proof, growth plot and conclusion entrance/final hold covered. The previously repaired Chinese conclusion is below-left and clear of graph log-axis label; native followups retained for EN 222.466s and ZH 236.200s.
- Huffman EN/ZH entropy lower bound, rounded code overlays, merge branches/tree/code table, swap argument, deepest-sibling diagrams, induction split/morph and theorem/measurement result rows covered. No additional confirmed visual defect.

## Provenance and limits

- All six capture fingerprints report `current_source_and_inputs=false` in the temporal audit. They are evidence about the exact hashed movies, not current-source production approval. Whole-part source fingerprints can be invalidated by unrelated edits.
- Chinese Huffman original capture status is `needs-review` with `source-changed-during-render`; warning retained. Five other original capture statuses were `passed`, which does not override the later stale fingerprint.
- Relevant scene source hashes at review initialization and completion are recorded separately. Completion source snapshots are labeled as such. Current input byte hashes are recorded alongside whether size/mtime match the capture record; this does not retrospectively establish cryptographic provenance of old renders.
- Every selected image, original reviewed sheet, unique representative sheet, audit record and movie hash was rechecked at completion. Immutable copies of all six reviewed movies and audit result JSONs, native followups, and completion source snapshots are retained under `ai1-foundations-motion-evidence/{lang}/{Scene}/`.
- Complete-file decode is automated. Visual review is selected-time image review with at most 1 s gaps and transition extras; unsampled frames and continuous perceptual playback remain unverified.
- These silent movies do not establish narration/listening/synchronization QA. Final-resolution render/typography, player/responsive behavior and post-fix movies are unreviewed here.
