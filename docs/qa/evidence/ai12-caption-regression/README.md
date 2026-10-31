# Shared-caption regression: Parts 1 and 2

**0 changed translation outputs across 2,265 unique strings** from all 33 captured English endpoint collections: 17 Part 1 and 16 Part 2 scenes. The set includes 4,550 collected rows and one supplementary current Logic alpha-renaming caption, absent from those collections.

The actual current `explainer.zh_text.translate` compared the shared table at `b35206038c127933bc1fc6f74d35b647a01c7389` with the snapshotted working-tree table after the Part 3 additions. Each pass reset `_TABLE` and `_BY_NUMBERS` and selected Chinese. One nice-10 process ran with numerical thread counts limited to one; no production scene, data or model modules were imported and no compute or render was performed.

Both output-map SHA-256 values are `c5c51d809b47e418f38d74405a0297f2c0a191d24fe28c2fd552a617145ab6a0`. All 33 captured text files, their 33 render records, and the current table still matched their recorded content hashes after comparison.

- `report.json.gz`: exact comparison report, collection/record/source/table hashes, original render fingerprints and warnings, execution details, and limits.
- `used-caption-results.json.gz`: full English-to-baseline/current-output mapping and every captured context.
- `baseline-ai_text_zh.json.gz` and `current-ai_text_zh.json.gz`: exact compared table snapshots.
- `comparison.py`: original comparison implementation; its absolute runtime paths document the run and need adaptation for replay elsewhere.
- `manifest.json`: compressed and uncompressed artifact hashes.

Raw translator output was compared for every collected string, including `needs=false` math or symbol candidates. The `needs` flag is an English-prose heuristic, not evidence that text is raw model data. Verbatim `data_text`/Code text bypasses this collector and is outside this sample.

This establishes shared-table output equality only for this captured key set and the one static supplement, using the same current translator implementation for both passes. It does **not** establish scene/data/narration equivalence, fresh production-fingerprint equivalence, rendered geometry, playback or audio approval. Uncaptured dynamic values and branches remain outside coverage. Historical render warnings remain in the report unchanged; this result does not clear them. Source hashes describe bytes observed at comparison time, not code proven to have been imported by historical render workers.
