# SVD ladder-copy reveal audit

Both current EN and ZH silent movies show transient doubled mathematical glyphs in all four copy reveals. The retained prior row remains in place while the animated source copy offsets across it; this obscures tokens over consecutive15fpsframes. A clean single transform could be acceptable, but this simultaneous retained-row ink overlap fails the stated readability criterion. Dark target previews alone are not the reason for failure.

All304encodedframes in eight declared conservative windows were directly inspected chronologically on38sheets, with eight actual native854×480followups. Each window includes pre-event margin, the0.6s row-movement stage, the full1.2s copy stage and settling context. No frames are skipped inside windows. Other intervals are out of scope.

Source: `cd3b22f6f86ad33a548983025d490e53c322c5479803d0cb5292f8e3ab74dd10`. ENmovie: `59090e74b89b7dc10c8e0d85cafb6cd17bd7917f5a0e645a55bba13cc0fc59d0`; ZHmovie: `e43b06c38430defdd5b918d0bdf91ca57512d802e0414d09d913b63432898f6e`. Identities match the final source case map exactly.

| Language | Copy row | Native witness frame | Seconds |
|---|---:|---:|---:|
|en|2|631|42.066667|
|en|3|711|47.400000|
|en|4|838|55.866667|
|en|5|893|59.533333|
|zh|2|688|45.866667|
|zh|3|797|53.133333|
|zh|4|931|62.066667|
|zh|5|977|65.133333|

Recommendation: use a bounded scene-local non-transform reveal for these four copies, preserving equations, timing, data, narration and the shared helper. This is a recommendation only; this audit changed no source. Fresh bilingual motion regression would be needed after any change.

This is15fps480p scoped evidence, not4K appearance approval, full-scene continuous playback, or listening/audio approval.
