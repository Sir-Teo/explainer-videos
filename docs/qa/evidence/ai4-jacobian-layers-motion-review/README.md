# Part 4 Jacobian and Layers selected-motion review

All selected chronological images were actually reviewed for both chapters in English and Chinese. No confirmed visual/motion defect was observed in this scoped review. No source, global caption, data, render, TTS or shared review-ledger changes were made. This directory is an evidence package only.

|Case|Decoded frames|Selected times|Unique PNGs viewed on sheets|Exact duplicate times|Actual pages|Native follow-ups|
|---|---:|---:|---:|---:|---:|---:|
|en-Jacobian|2,032|265|191|74|24|4|
|en-Layers|2,335|346|259|87|33|4|
|zh-Jacobian|2,273|276|184|92|23|4|
|zh-Layers|2,476|351|259|92|33|4|

Total: 9,116 source frames decoded/analyzed; 1,238 selected timestamps covered by 893 unique-within-case image views and 345 within-case exact PNG duplicates; 871 globally distinct image hashes were viewed;22 cross-case repeated images were viewed again. 113 chronological pages actually viewed; 16 additional native 854×480 follow-ups. The native follow-ups use already selected frames and do not increase selected-frame coverage. **7,878 source frames were not individually visually inspected.**

Selection used frozen `tools/qa_motion.py` with `--dense 0.5 --max-gap 1` (actual argv in each freeze receipt), detected motion onsets/boundaries/midpoints, static midpoints and gap filling. Largest selected-time gap is 1 s subject only to floating-point rounding at approximately 1e−14 s; motion detector thresholds and all unextracted frame gaps remain in each temporal audit. Every selected timestamp has a page/hash proof or an exact PNG-identity link to its actually viewed image. These are selected images across the full movies, not continuous perceptual playback.

Jacobian coverage includes card/fades, nonlinear plane warp, lens and shrinking source neighborhood, tangent-grid convergence, disk clipping and legend, Jacobian partial-derivative definition, m-output/n-input braces, square/parallelogram area 0.95, ordered chain product and dimensions, all five depth gains/reveal transitions, seed-extrema bands, log-norm axes and upper-bound/not-equality/not-every-direction qualifiers. Native follow-ups cover early/final lenses, area/chain and final depth panels in both languages. No lens escape, persistent label collision, clipped graph extreme or incorrect chain order was observed.

Layers coverage includes every derivative-ladder copy/morph/underline transition, XᵀG and GWᵀ matrix order/colors, full-Jacobian/storage/VJP cost panel, softmax quotient-rule transitions, signed 5×5 matrix/key, row-zero/PSD theory, actual signed rounded eigenvalues and VJP reveal; layer-norm formula/two-correction transitions, signed 6×6 matrix/key, eigenvalue reveals and epsilon/learned-scale qualifiers. Native follow-ups cover the cost panel, softmax before/after VJP and final layer norm in both languages. Formula-copy overlap during the intended morph resolves into separate rows; no persistent collision was observed.

The actual Chinese cost caption visibly reads “乘积 XᵀG：共4.8×10⁹次标量乘、加运算”. Read-only checks of frozen outputs give T=1,024, d=768: 2,415,919,104 scalar multiplications and 2,413,559,808 additions if a length-T dot product uses T−1 additions; sum 4,829,478,912. The producer uses the conventional 2Td(4d)=4,831,838,208 two-operations-per-MAC estimate. Both round to 4.8×10⁹; the caption is a scalar multiply/add count, not 4.8 billion fused multiply-add operations. Frozen library gaps/eigenvalues and epsilon/σ³ are retained in `receipts/frozen-data-checks.json.gz`; no producer/cache-loader/model import or production computation was used.

Exact movie identities:

- en-Jacobian: `e0b64ac1910e691610210675f4fd95bcabfa5f452801ee390b70b307fe685085`, 1,603,250 bytes; source `4c832fd112087eb637da46c7fc4d41a7f5a8b49c3767f73600eb8398dab56783`.
- en-Layers: `085d554e54175592e23aba1642d7d278d5d7623a550b95512a127630d65102c0`, 1,198,333 bytes; source `33fa551df06f79aeb6c6cfb883d9b1b97fcc1b3139c541ed525c90c25b4fd3cc`.
- zh-Jacobian: `25e7b9137048e7184ef26e5ea50ff72229ff2a526e88ddd87f4c5754ca24d59d`, 1,682,706 bytes; source `4c832fd112087eb637da46c7fc4d41a7f5a8b49c3767f73600eb8398dab56783`.
- zh-Layers: `771ae08dc0ef9ea6ee700d0b8cc361c3bdb4b02bcab394fcb689b48383bffc65`, 1,236,357 bytes; source `33fa551df06f79aeb6c6cfb883d9b1b97fcc1b3139c541ed525c90c25b4fd3cc`.

Both direct scene sources, local Chinese table, shared caption table, common module and audit tool still matched their frozen review hashes at final check. Shared caption-table SHA256: `20229b679782e6b183a87b809cd2124dbb48950de7179b5be22fb3f04013a182`. Every consumed raw input hash is recorded and was rechecked unchanged. Later frozen hashes bind the review artifacts/current scoped files; they do not independently prove historical renderer imports.

Raw EN Layers runtime status remains `needs-review` with `source-changed-during-render`; the other three raw records say `passed`. All four audit broad source/input freshness flags are `false` and remain retained. No warning or freshness flag is upgraded by this visual result; it applies to the exact preserved movie and image hashes.

**Unverified:** continuous perceptual playback, listening/pronunciation, synthesized narration and speech/animation synchronization, player/browser/responsive behavior and full 1080p motion. These silent movies use estimated narration timing. Separate 1080p endpoint reviews are outside this assignment. Brief/subtle defects between selected times can remain. No new bugs were confirmed, so no source repair is proposed by this batch.

Each `cases/` directory retains the actual 113 review pages and 16 native follow-ups across all four cases plus compressed audit/actual-review/freeze receipts. `provenance-index.json` maps original frozen files to deduplicated gzip blobs for exact raw records, source, tables, tool and data; full MP4s are excluded. `retained-origins.json` preserves original→retained hash mappings and gzip roundtrips; `file-checksums.json` verifies the package.
