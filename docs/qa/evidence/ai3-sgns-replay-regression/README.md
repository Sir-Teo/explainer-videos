# SGNS replay: original review and rendered repair

The replay now holds each narrated measured snapshot until the next bookmark: **36 → 1,089 → 10,890 updates**. The early lists are described as mixed, with some favouring common function words. The original blanket “commonest words” claim was contradicted by the measured Monday neighbours. Intermediate measured checkpoints remain in the data; the replay omits their unspoken transitions.

| Actual review | Original output | Repaired output |
|---|---|---|
| EN motion | All 437 selected times: 317 unique images viewed on 40 chronological sheets; 120 exact duplicates. Six native follow-ups. | All 437 selected times: 418 exact PNG matches to reviewed original images, 14 newly viewed unique images on two sheets, five within-case duplicates. Three native follow-ups. |
| ZH motion | All 445 selected times: 304 unique images viewed on 38 sheets; 141 exact duplicates. Six native follow-ups. | All 443 selected times: 416 prior exact PNG matches, 21 newly viewed unique images on three sheets, six within-case duplicates. Three native follow-ups. |
| EN endpoints | All 23 native-sized captures viewed. | All 23 accounted: two changed native views and 21 prior exact PNG matches. |
| ZH endpoints | All 22 native-sized captures viewed. | All 22 accounted: two changed native views and 20 prior exact PNG matches. |

Review includes the negative-sampling objective and colour roles, generalized shifted-PMI derivation and empirical-distribution qualifier, observed/free-cell condition, finite-optimization disclaimer, dimension/error panels and omitted points, diagnostic sample/full-cohort distinction, learned neighbours, analogy/purity table, data-dependent counting-wins branch, GloVe card and contextual-vector transition. Displayed measurements agree with the preserved JSON/NPZ. No additional confirmed clipping, collision, incorrect held state or numerical mismatch was found.

| Native comparison | Before | After |
|---|---|---|
| EN early description | [Step 363 shown during the early description](images/en-original-early.png) | [Actual 36-update lists held](images/en-repaired-early.png) |
| EN middle description | [Step 3,630 shown during the 1,089-update description](images/en-original-middle.png) | [Actual 1,089-update lists held](images/en-repaired-middle.png) |
| ZH early description | [Original](images/zh-original-early.png) | [Repaired](images/zh-repaired-early.png) |
| ZH middle description | [Original](images/zh-original-middle.png) | [Repaired](images/zh-repaired-middle.png) |

Combined comparisons: [English](images/en-before-after.png), [Chinese](images/zh-before-after.png). Actual final measured states: [EN](images/en-repaired-final.png), [ZH](images/zh-repaired-final.png). All five newly viewed motion sheets are included; for example [EN checkpoint transition](images/en-changed-sheet-001.png) and [ZH checkpoint transition](images/zh-changed-sheet-001.png).

The actual source-loop fixture reproduces the original scheduling defect and verifies the repair against captured bookmark times. Fresh endpoint and motion narration records then confirm the revised English/Chinese prose, bookmarks `abcd`, unchanged text/duration for the other six blocks, and monotonic word ranges inside each block. In the fresh motion schedule the completed 36-update snapshot holds **4.70 s EN / 5.50 s ZH** before bookmark `c`; the completed 1,089-update snapshot holds **3.84 s EN / 3.63 s ZH** before `d`. The final measured snapshot begins at `d`. Transitions take 0.9 s, with an interpolated progress counter; held snapshot values are measured checkpoints.

The changed English block remains 83 tokens and the same estimated duration. Chinese grows from 136 to 140 tokens, adding **0.93025 s**. These are silent synthesis/token timing estimates, not measured spoken-word timestamps or listening approval. All ten existing Part 3 narration tests passed. Fixtures and logs are preserved as manual QA evidence; no wording-only test file was added to the suite.

Original EN/ZH movies are 214.332357 / 227.265690 s; repaired movies are 214.332357 / 228.198698 s. All frames were decoded. Repaired EN has **2,778 unselected source frames** out of 3,215; repaired ZH has **2,980 unselected frames** out of 3,423. Original EN/ZH have 2,778 / 2,964 unselected frames. The largest selected-time gap is 1.0 s, with exact gaps retained in the ledgers. Sheet tiles are 640 px wide; native follow-ups and endpoints are 854×480. Only exact PNG SHA256 equality permits inherited coverage. This is selected-time visual review, **not continuous playback, audio/listening synchronization, production-resolution or player/responsive QA**.

Original direct scene SHA256: `dc56ada3cfd37d8cbfabcdda082245389ab72a025ae3d86e329fc821c31953e6`.
Repaired direct scene SHA256: `bec79fc8bc271484317b002649960bd40eb3d827eb76cbd7a1cf2948541d1673`.
Repaired EN movie SHA256: `9bcf4449c40f09728464d0952abb20daf0ab1926306febf55dfa83b195dfaf22`.
Repaired ZH movie SHA256: `de4cd782c5be5884ca226b36dd714913ee0ddc20a2ccfe2df62a5ae92150090e`.

All original and repaired movies, records, source snapshots and consumed input hashes were preserved before review. The direct scene, frozen motion-audit tool and all four SGNS/words input byte hashes remained unchanged through completion; input signatures still matched the renders. No computation, training or data write was performed for this repair/review. The scene loop/prose and its local Chinese narration entry were the only repair scope; independent Netflix translation edits in the whole-file snapshot remain attributed separately.

**Recorded warnings remain intact.** Both repaired movies report `passed` with zero warnings. Both repaired endpoint records retain `needs-review` with `source-changed-during-render`. Original EN motion and ZH endpoints retain the same warning; original ZH motion and EN endpoints report passed. All four repaired whole-part fingerprints differ from the source bundle at review completion after concurrent edits. Scoped checks of the frozen direct scene, actual caption/narration output and immutable inputs do not clear those warnings or establish current whole-part approval. See [completion provenance](ledgers/completion-provenance.json.gz).

[manifest.json](manifest.json) authenticates the portable images, gzip ledgers, source snapshots and consumed SGNS numerical data. Complete time-to-view/reuse maps include page SHA256, prior-ledger SHA256, source/movie/tool provenance and unviewed gaps. The package includes representative native evidence and every newly viewed sheet, rather than all original extracted images. Full MP4s remain in the runtime workspace; they are not copied into the repository. Original absolute paths in ledgers may be unavailable outside that workspace. Verify with `sha256sum -c SHA256SUMS`; inspect a ledger with `gzip -dc ledgers/narration-timing-review.json.gz`.

No source/global-caption/STATUS edits, new renders, model/data changes or commits were made during this final regression packaging pass. Root owns the completed renders and publication.
