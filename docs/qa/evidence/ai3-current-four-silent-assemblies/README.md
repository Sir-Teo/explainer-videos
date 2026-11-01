# Part 3 current silent assemblies: SVD and Outro replacements

New English and Chinese silent preview reels were assembled from the separate current 38-case map, incorporating SVD source `291bba0e…` and Outro source `e874a8da…`. The old reels and bundles remain byte-for-byte unchanged. The existing stitch-only build workflow was used through a private output adapter with scene rendering hard-forbidden, one FFmpeg input/output/filter thread and low scheduler priority. No numerical/model computation, production source edit, local rendering/transport or Library upload occurred.

| Reel | Duration | Video frames | Subtitle cues | New MP4 SHA256 |
|---|---:|---:|---:|---|
| en | 3281.809979 s | 49,227 | 990 | `c472adc44341fee6fcf7dcb7c278e59cbb451838babf57a0c27d93cc19d76cb1` |
| zh | 3469.088542 s | 52,036 | 1,039 | `d7cb13f96070b9d4b8867247df485bfadcb6cd917932d342892d39d986ba62b8` |

All 101,263 video frames and both complete AAC streams decoded without errors. Decoded video/audio PTS strictly increase; packet DTS are nondecreasing per stream. Both full stereo 16-bit PCM decodes contain zero nonzero bytes, confirming digital silence. All 19 localized chapters per reel, normalized/source frame counts, marker timing, soft-subtitle text/millisecond roundtrip and every cue's chapter boundary pass. The first video PTS remains 0.021029 s; no zero-offset claim is made.

All 38 narration sidecars—including raw/translated text, utterance starts/durations and word timestamps—are byte-identical to their historical counterparts. Both SRT files and chapter lists, embedded chapter timing/title structures, full durations/frame counts and first/last video PTS exactly match the old reels. Every original clip/result/sidecar/direct-module hash and all 34 consumed numerical payload/expected-absence identities were frozen before and checked again after assembly. Source observations are snapshots, not historical import proof. Five original chapter warning cases remain raw in the receipts.

All **36 joins** are covered at **684 selected timestamps**, including every frame within ±0.4 s and additional ±0.6/0.8/1.0 s context. Every new join PNG exactly matches an authenticated image in the prior actually viewed join ledger. All **72 native before/after context appearances** likewise inherit exact PNG matches to prior individual native views. **No novel join image or new direct image view is claimed.** The full old actual-view proof and hashes accompany each new mapping in `join-regression.json.gz`; no visual approval is inferred from a decoded frame alone.

The complete frozen input map, raw chapter results/narration sidecars, build commands, source observations, full video/audio frame and packet-time ledgers, cue checks, exact join mappings and post-integrity checks are retained here in compressed form. `summary.json` records the new reel identities and runtime locations. Full movies and duplicate join PNGs stay outside Git. Historical proof images remain in [the original assembly evidence](../ai3-final-assembly-review/README.md); chapter repair evidence remains in [SVD](../ai3-svd-reveal-motion-regression/README.md) and [Outro](../ai3-outro-trail-motion-regression/README.md).

**Limits:** these are silent 854×480 at 15 fps previews with estimated narration/subtitle timing. Actual speech, pronunciation, listening, production loudness, spoken synchronization, uninterrupted full-reel perceptual viewing, native 1080p/4K motion and player/responsive overlays remain unverified. Frames outside the selected join windows were automatically decoded but not newly visually reviewed in this assembly pass. This is cloud QA, with no transport handoff or external publication implied.

The raw `join-selection.json.gz` retains its extractor-time pending view fields. The separate completed `join-regression.json.gz` is authoritative for exact inheritance and all accounted-for join times; the original extraction plan was not rewritten as an actual-view receipt.
