# Supplemental shared-caption regression after Einsum subtitle

**0 changed translation outputs across the same 2,265 unique strings from all 33 captured Part 1/2 endpoint collections** (17 Part 1, 16 Part 2; 4,550 collected rows plus the current static Logic alpha-renaming supplement).

This independent run compares baseline `b352060` with the latest snapshotted table after adding exactly one Einsum explanatory subtitle. The table delta contains one added English/Chinese entry and no changed or removed entries; `receipt.json` preserves it. Earlier evidence in the parent directory is unchanged.

The actual current `explainer.zh_text.translate` ran in one nice-10 process, with Chinese selected, caches reset per table pass and numerical thread counts limited to one. The captured collection bytes match the previous run. All 33 collection files, their 33 render records and the current table retained their hashes through this run.

The baseline, previous-run current and latest-current output maps all have SHA-256 `c5c51d809b47e418f38d74405a0297f2c0a191d24fe28c2fd552a617145ab6a0`.

- `receipt.json`: bounded result, exact table delta/hashes, original-evidence hashes, execution details and compressed artifact hashes.
- `report.json.gz`: full provenance, source and record hashes, original fingerprints/warnings and comparison limits.
- `used-caption-results.json.gz`: full mapping, baseline/latest outputs and all captured contexts.
- `current-ai_text_zh.json.gz`: exact latest table snapshot. The baseline snapshot remains in the parent directory.
- `comparison.py`: isolated run implementation, with original absolute runtime paths retained.

Raw translator outputs include collected math/symbol candidates marked `needs=false`; that flag is a prose heuristic, not proof of raw model data. Verbatim data_text/Code text bypasses the collector and remains outside coverage. Uncaptured dynamic values and branches remain untested.

This proves table-output equality over the captured key set using the same current translator, not scene/data/narration or production-fingerprint equivalence. It does not approve rendered geometry, playback or audio. Original render warnings are preserved unchanged. No production scene/data/model imports, compute, render, table edit, commit or publication was performed by this supplemental comparison.
