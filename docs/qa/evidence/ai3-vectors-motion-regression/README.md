# Part 3 Vectors: bilingual motion regression

The three-entry coordinate column previously touched/clipped the upper frame edge during its reveal. The repaired source applies the same safe-top treatment already used by the longer column. Native before/after frames below show the defect and the resulting approximately 18-pixel margin. The final English and Chinese render records both report `passed` with zero warnings.

| Artifact | Duration | Automatically decoded frames | Selected times | Actual visual coverage |
| --- | ---: | ---: | ---: | --- |
| English before | 198.797 s | 2,982 | 509 | 446 unique images on 56 native-size pages; 63 exact duplicate times; 5 native follow-ups |
| English final | 198.797 s | 2,982 | 511 | 5 changed unique images on 1 page; 506 exact PNG matches to reviewed before images; 1 native follow-up |
| Chinese final | 198.997 s | 2,985 | 489 | 367 unique images on 46 native-size pages; 71 exact full-PNG matches to reviewed English images; 51 Chinese duplicate times; 8 native follow-ups |

English before movie SHA: `50e865cca677571f4309874cc953a0504839c0af26b427133773dfcf7610bf5c`.

English final movie SHA: `7eaa69faf100fa3f3fae19e07542ae74f338de1e5b9ef18e5ae02253146fedc2`.

Chinese final movie SHA: `87567350c94d4de8b392fd878c5e5118840a2cab139a0a1fd76054377369ba10`.

Before scene SHA: `12a3d60bd8741c5b68b5690d66413ee980bb7b995b183d2d07b6846ba23d992a`. Final shared scene SHA: `110a369b78476c6d4a302e9ff61dfbb5fe5e569a74e0843d2c249cc1eb5cb62e`.

## Native visual evidence

- [English column before](en-before-frame-250.png), [English column after](en-after-frame-251.png), [Chinese column after](zh-after-frame-219.png): every number and bracket endpoint fits after repair.
- [English parallel equality](en-before-frame-1944.png), [English antiparallel equality](en-before-frame-1983.png), [Chinese parallel equality](zh-after-frame-1998.png), [Chinese antiparallel equality](zh-after-antiparallel-136.000s.png): both directions show the parabola touching zero within the symmetric domain, including the negative tick. The English final equality frames inherit coverage only through exact full-PNG matches in its ledger.
- [English raw scores](en-before-frame-2825.png), [English probabilities](en-before-frame-2944.png), [Chinese raw scores](zh-after-frame-2838.png), [Chinese probabilities](zh-after-frame-2951.png): negative raw values remain labeled above a disclosed common floor near −96.49; green softmax probabilities explicitly use the true zero baseline.

No additional defect was found in the reviewed final content. The formula-copy animations briefly cross their own explanatory rows during movement and settle into readable rows; these actual observations are retained in the page ledgers.

## Reproducible coverage and limits

The gzip files preserve exact complete JSON review ledgers, plans, render records, temporal audits and the English PNG inheritance catalog. They include every selected timestamp, native PNG SHA, page SHA and observation, exact inherited provenance, unselected source-frame gaps, data hashes and extraction-time source checks. `manifest.json` hashes each payload and its uncompressed source; gzip timestamps are deterministic. Runtime absolute paths are historical provenance, not portable links.

Frozen tool SHA: `1d0cee16ad098360ceb70f9cbc513bbce334ea107e90982ace3a7fd3df73595e`, algorithm `rgb-max-channel-v2-bounded-gap`. All source frames were automatically decoded at low-resolution RGB. Selected native frames use adaptive transition extras and an unconditional maximum one-second gap, subject to timestamp/floating-point quantization. The extra Chinese antiparallel views use explicitly recorded FFmpeg requested seek times, quantized to the 15 fps source; no exact frame-index claim is made for those views.

Cross-language inheritance requires identical full PNG bytes. It does not assume translated text, source equivalence, approximate appearance or cropped similarity. New Chinese content was actually inspected in temporal order; every reused English identity links to its original reviewed receipt.

This is selected-frame visual QA of silent 854×480, 15 fps previews. Unselected frames were not individually perceived. Short or subthreshold defects can fall between selections. Continuous perceptual playback, listening/narration alignment, production-resolution readability and player/responsive behavior remain unverified by this package. Extraction-time current-source/input checks are scoped to their recorded instants, not a claim about future repository edits.
