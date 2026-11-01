# Part3 Outro: smooth trail and marker coupling

An actual motion defect was confirmed in both original silent480p movies: the marker lags far behind the trail drawing front, then catches up late. The final position is correct. Every encoded frame in the full three-second descent plus boundary buffers was inspected: EN source1697–1745 /113.133333–116.333333s and ZH source1870–1918 /124.666667–127.866667s. That is98 native854×480 frames on14 chronological sheets plus two individual native followups, with no frame skips inside the scoped windows. This is scoped per-frame image review, not continuous perceptual playback/listening or a new whole-scene approval.

Actual native examples: [English before, source1716 /114.400000s](en-before-front-lag.png), [Chinese before, source1889 /125.933333s](zh-before-front-lag.png). The white trail already extends toward the field center while the marker remains on the upper-left part of that curve.

The implemented local helper uses one immutable copy of the full original smooth cubic trail and one UpdateFromAlphaFunc animated family containing the visible path and marker. At the already-eased alpha it reveals exactly Create's curve-index prefix, then places the marker at that prefix's endpoint. This deliberately retains the old trail reveal/pacing; marker timing changes to match it. It does not switch the trail to arc-length speed, resample cubic controls or use the separate polyline-only Quadratic helper.

Exact AST comparison restores the entire original module after removing the helper and undoing the single play replacement. Cubic geometry recipe, all other source, data/VO/bookmarks, default smooth easing and3.0s duration remain unchanged. Both path and marker are included in Cairo's moving family.

Four actual-Manim tests pass: all45 encoded animation-progress samples plus exact endpoints and201-point reverse sweep match original Create control arrays exactly; marker stays at the same prefix endpoint; style/full geometry survive; Cairo classifies both objects as moving; and an immutable-copy-only MoveAlongPath still differs by more than1world unit on this actual smooth path. Tests execute only AST-extracted local geometry/helper code and Manim interpolation, with no scene/default-load/model/producer/render execution. Source compilation and scoped diff-whitespace checks also pass.

**Fresh bilingual render regression remains pending at this source freeze.** No repaired-output visual approval is implied. The earlier before-probe report and unexecuted proposal are historical snapshots; this README/source-freeze receipt records the later implementation separately without rewriting those observations.

Before source SHA: `4e1d29200637256128acf72ecffd0f02caaf6733a4222808dd0b32bf82981ed7`.
Frozen repaired source SHA: `e874a8da48693ea2c9ec75584e044d090a6bd9a39c8f0c193c1d245101a8ca24`.
Original movies are preserved byte-for-byte under `/workspace/runtime/ai3-outro-path-front-probe/before/`: EN `f99b2a8263bd613e741d0ed8f61c1ac9601732593445d0fbef874acc48682881`, ZH `56124f7e0155fd8cb5f581d6613184de64d30d3cce7392aade37d325ed3b9667`.

`before-review.json.gz` contains every scoped frame/time/hash and actual viewed-page mapping, original movie/record/source identities and exact extraction command. All98 PNGs and14 sheets remain in that runtime probe directory. `source-freeze.json.gz`, the exact before/after sources, production patch and test/log snapshots preserve the repair receipt. `manifest.json` hashes all package members other than itself. Original broader Outro and Part4 review packages remain untouched. No shared helper, future-part source, caption table, data cache or Library file changed.
