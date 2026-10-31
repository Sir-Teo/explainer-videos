# Part 3 Matrices and Eigen: bilingual motion regression

All four final silent preview movies pass the selected-time visual regression. The repaired quarter turns preserve scale, the Eigen heading stays readable through the moving grid, and the Matrices rank/null-space captions remain protected. No further concrete defect was found in the reviewed selections.

| Final case | Decoded source frames | Selected times covered | Newly viewed unique frames | Exact PNG inheritance | Changed pages | Native followups | Render warnings |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| EN Matrices | 1,976 | 299 | 60 | 221 | 8 | 4 | 0 |
| EN Eigen | 2,421 | 340 | 54 | 226 | 7 | 5 | 0 |
| ZH Matrices | 1,989 | 293 | 63 | 209 | 8 | 4 | 0 |
| ZH Eigen | 2,760 | 361 | 10 | 277 | 2 | 5 | 0 |

Across the four movies, 9,146 frames were automatically decoded, and 1,293 selected timestamps were visually covered: 187 newly inspected unique images on 25 pages, plus 933 unique images inherited only through exact full-PNG SHA equality to an earlier actually viewed representative. Eighteen native followups were inspected. Every selected timestamp is accounted for; the maximum selected gap is one second. These counts do not assert continuous perceptual viewing of every source frame.

## Actual visual evidence

- [Eigen native before/after](en-eigen-before-after.png): the fixed matrix heading is protected where the old moving white axis crossed it; the known rotation preserves the circle's scale.
- [Matrices native before/after](en-matrices-before-after.png): quarter-turn geometry and protected rank/null-space explanation.
- [Chinese caption before/after at 114.533 seconds](zh-matrices-caption-before-after.png): the red null-space line previously crossed the caption's opening characters; its final mask preserves the characters.
- [Chinese composition-heading native crop](zh-matrices-heading-native-crop-no-defect.png): close inspection at 52.133 seconds finds no glyph occlusion. Grid lines reach the existing background mask edge, while the text remains readable. This was checked and is not an additional repair request.
- [Zero-sign correction evidence](en-matrices-zero-sign-retraction-native.png): the original native at 81.399674 seconds shows **det = +0.00**. An initial negative-zero claim was a reviewer sign misread and was retracted. No determinant-formatting repair is claimed.

The additional numbered final-native PNGs preserve all eighteen native followups. Side-by-side images use actual native PNGs, with labels outside the image content.

## Exact provenance

Final Matrices module SHA: `ddc663f7dddd7d9377b269a4aff97268316f944b3d3a532867f968962ee25e47`.

Final Eigen module SHA: `5f83069e33e325b05874f5b9c9a507bd5b06d5f2b10fa2ab7c2ee4bd86278fd0`.

| Final movie | SHA-256 |
| --- | --- |
| EN Matrices | `a4f4c8d78a61ede8f94fd45ba7a135f686562ad746dcc5d0232876791aa195d6` |
| EN Eigen | `a30c8c6c91b04b6cd3c3a3a73463caae54ff6371930cdc21d8ad3cca519bb37d` |
| ZH Matrices | `0a91c45415b27ba454521fa90fd83ffb6e2268ec7f51782258ca34ec7d00230a` |
| ZH Eigen | `851a46486dc8278affaa21b3bb8842f5cc93535683b5a3f67af53b86af105cbf` |

Final render fingerprint: `138a87a47d0fd2dfb3be01795bc4678cd2afb28c878618761ab9a9eb70fd685e`. Direct scene modules and movie bytes were independently hash-matched to the parent's explicit frozen render handoff. All four final records report passed with zero warnings. Later unrelated edits can stale the whole-part fingerprint; this package does not replace those future warnings with a claim that all repository source is current.

The four render input inventories are empty: these two scene modules construct their numerical examples locally. No external cached model/data-file hash is asserted. The manifest records exact current scene/movie hashes and shared-file hashes at packaging, separately from authenticated final render provenance. A current shared-file hash alone does not prove what a historical worker imported.

The **original Chinese Eigen baseline imported source remains uncertain** because its worker reported a source change during rendering. Candidate source `09b46dec…` and the current source-at-review were not proof of that worker's actual import. The complete original warning and source-linkage caution are retained. Exact-PNG baseline inheritance authenticates image identity to actually viewed images, independently of that uncertain source linkage. The fresh final frozen movie closes current appearance without rewriting the baseline provenance.

## Complete ledgers and limits

The deterministic gzip files contain the complete four scoped baseline reviews and audits, all four final review ledgers/audits/render records, confirmed provenance, source snapshots, and review/extraction scripts. Every selected timestamp, frame PNG SHA, page SHA and view checkpoint, exact inheritance mapping, native receipt, unextracted source-frame gap, and warning is retained. [manifest.json](manifest.json) hashes every payload and its uncompressed source. Absolute runtime paths are historical provenance, not portable file links. PNG pages and full movies remain runtime artifacts; their hashes and the complete coverage receipts are preserved here.

Frozen extraction tool SHA: `1d0cee16ad098360ceb70f9cbc513bbce334ea107e90982ace3a7fd3df73595e`. It streams full-file RGB decoding and selects transition extras plus a maximum one-second gap. Inheritance uses identical full PNG bytes, never perceptual similarity, source equivalence, translation equivalence, or a matching crop.

This is selected-frame visual QA of silent 854×480, 15 fps previews. Unselected frames were not individually perceived, and brief or subthreshold defects can fall between selections. Continuous perceptual playback, listening/narration synchronization, production-resolution readability, and player/responsive behavior remain unverified. No production compute, model/data mutation, render, commit, or push was performed by the reviewer. This evidence package changes only its new directory.
