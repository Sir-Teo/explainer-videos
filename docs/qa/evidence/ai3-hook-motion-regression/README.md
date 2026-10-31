# Part 3 Hook motion regression

The repaired English and Chinese Hook previews have completed full-span **selected-time** visual review. The overview labels now remain visible during legend entry; outgoing overview labels fade before the animal-focus zoom, and the fixed source footer stays readable. No new defect was found in the inspected repaired output. The original defect records remain unchanged in this package and the separate `../ai3-motion-repair-source/` history.

| Exact artifact | Duration | Automatically decoded frames | Selected times | Actual image review |
| --- | ---: | ---: | ---: | --- |
| Original EN | 146.200 s | 2,193 | 356 | 302 unique images on 38 native-size pages; 54 exact PNG duplicates |
| Repaired EN | 146.200 s | 2,193 | 356 | 40 new unique images on 5 pages; 303 exact PNG matches inherited from the original actual review; 13 new exact duplicates |
| Repaired ZH | 165.867 s | 2,488 | 374 | 308 unique images on 39 native-size pages; 66 exact PNG duplicates |

Every selected time maps to an actual image view or an exact PNG SHA-256 match to an inspected representative. Native follow-ups include both repaired transition defects, the complete Chinese milestone timeline and its six-item agenda. The native before/after pairs are `en-blink-{before,after}.png` at source frame 448 / 29.867 s and `en-footer-{before,after}.png` at source frame 846 / 56.400 s. Chinese follow-ups are named `zh-*-after.png`. These are exact 854×480 extracted images, without resizing or retouching.

The original scene SHA is `2cc150ba66e921c64279c1d8a5965836c5971f947d55defb83a69a9a7aa7eae1`. Both repaired captures use scene SHA `ef357b016949f41b3a5383891534634d83dfc84518bd53b228f82e87baef5a3a`. Exact movie SHA-256 values:

- Original EN: `a6d73aafb012437ee615df8a1c3901777e658bbc76bfb79dd5ac7f0c79f83237`.
- Repaired EN: `9bc6d6a636f38a0228ab59024aee93c9c55c9811f37d3faba28a86cbd0319dab`.
- Repaired ZH: `819c28ed8c3a1f09841894f0dbe53d2974a533127b65c5da63533198295b0a7d`.

Both repaired render records retain `needs-review` with `source-changed-during-render`: other Part 3 source edits changed the conservative aggregate fingerprint while these captures ran. The scoped Hook source remained frozen and the recorded measured inputs were current at extraction. This scoped evidence does not convert the automated status into an unqualified pass. Consumed input hashes, original warnings, record hashes and all source snapshot hashes are retained in the compressed ledgers and `manifest.json`.

Temporal extraction used `rgb-max-channel-v2-bounded-gap`, tool SHA `1d0cee16ad098360ceb70f9cbc513bbce334ea107e90982ace3a7fd3df73595e`. It automatically decoded every frame at low-resolution RGB, selected transition extras and unconditional maximum-gap samples, and extracted native images. The largest selected-time gap is 1.0 s in all three audits. Exact settings, selected timestamps, unselected frame gaps and page/frame hashes are preserved.

All `.json.gz` files are deterministic gzip copies of the full original JSON bytes; `manifest.json` records compressed and uncompressed hashes and lengths. The original English full review is the inheritance source for the repaired English regression. Cloud-local movie/page/source paths in the ledgers identify preserved runtime artifacts and are not repository-hosted downloads. This bounded package contains the complete review/provenance ledgers and eight useful native frames, not the full movies or every contact sheet.

This is silent 480p / 15 fps preview QA. Automatically decoding all frames and inspecting selected images does **not** establish continuous perceptual playback, listening, narration synchronization, final production-resolution readability or player/responsive behavior. Unselected frames were not individually visually reviewed; threshold detection and a 1 s maximum gap cannot rule out every short or subtle transient.
