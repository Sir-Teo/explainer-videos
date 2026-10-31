# Spectra: frozen endpoint and selected-frame review

No concrete visual defect was found in this assigned EN/ZH artifact review. All 31 native 854×480 endpoint images and both endpoint contact sheets were inspected. Both silent motion jobs reported `passed` with zero automated warnings; runtime completion is separate from this visual review.

| Motion case | Duration | Decoded frames | Selected times | Unique images inspected | Exact PNG duplicate times | Chronological sheets inspected | Native followups | Unviewed source frames |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| EN | 154.8s | 2,322 | 310 | 223 | 87 | 28 | 8 | 2,012 |
| ZH | 176.0s | 2,640 | 317 | 218 | 99 | 28 | 8 | 2,323 |

Every selected time is mapped to an actually inspected representative image or an exactly byte-identical PNG representative. In total, 627 selected times account for 441 unique inspected images and 186 exact duplicates. All 56 chronological sheets and 16 native encoded followups were actually viewed. The selected-time gap is at most one second within floating-point tolerance. **4,335 decoded source frames were not individually visually reviewed.** This is not continuous playback or listening/synchronization approval.

The review checked the single 768×3072 random-reference qualification, finite-sample MP-edge caveat, strict-above counts, log-density axis units, GPT-2 trained/shuffled comparison, tail-fit limitations, and 30-matrix novels fresh/trained comparison. Frozen cached values match the 62 strict-above readout, 8.7 maximum/edge ratio, 46 of 48 tail fits within the descriptive comparison band, and selected MLE/two-sided KS calculation. Small footnotes were checked at native 480p. Ten narration blocks were read as text only.

## Provenance and scope

Direct scene source SHA256 `571d273685a004e9440e5d669517b9edda2ccfd1c82b0b4d4e880d664719a053` is independently anchored to commit `4a20866abd5d8b5edbf3fd600b0d9474748b790b`, plus the parent's unchanged-direct-source attestation. Original render fingerprint: `a1ea477a61f43792541a6894683ebe0ddb372f3c12e386d3d73f8b7b84c1b000`. Later broad aggregate source differs after unrelated source/shared-caption edits. The initial strict association assertion failed before image viewing and is retained; the later source snapshot is **not** represented as import-time source bytes. Original render statuses and warning fields remain unchanged.

Movies and render records were frozen under the chapter locks after completion. MP input bytes and signatures match between endpoint and motion snapshots. The `.npz` is absent by design for this JSON-only item. The archived movie has no adjacent standard result for the extraction tool's automatic provenance; explicit SHA-bound movie/record association is retained in `motion-freeze.json.gz`. Fresh seed-0, same-config model construction was traced in source; equality to an original saved initial checkpoint was not tested.

`*-selected-frame-review-map.json.gz` contains complete selected-time/PNG hashes, duplicate mappings, actual page hashes and native followups. `*-temporal-audit.json.gz` retains the automatic selection and unextracted-frame gaps. `endpoint-review.json.gz` and `freeze-receipt.json.gz` retain all endpoint image hashes/dimensions, source snapshot ledger and qualification history. `motion-review.json.gz` contains the per-case checklist and exact frozen movie hashes. The four PNG examples below are supporting evidence, not substitutes for the full mapped coverage.

- [EN shuffled transition](en-trained-shuffled-transition-480.png)
- [EN novels comparison](en-novels-trained-fresh-480.png)
- [ZH strict-edge readout](zh-strict-edge-readout-480.png)
- [ZH descriptive tail fits](zh-descriptive-tail-fits-480.png)

No production 1080p motion, final export, player/responsive, primary-source history verification or audio listening was performed. No producer/model loads, training, downloads, renders, numerical cache changes or scene changes were made by this reviewer. The MP cache copy is retained as numerical evidence only; this review does not establish uniform provenance for all 17 Part 3 cache items.

Gzip members preserve exact uncompressed source bytes. `manifest.json` records actual compressed-file hashes/sizes and uncompressed hashes/sizes; paths inside frozen records refer to the cloud workspace at capture time. Full movies, all extracted PNGs and sheets remain in that workspace and are omitted from this bounded package.
