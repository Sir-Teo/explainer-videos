# Rank-qualified Einsum: rendered regression

No visual defect was found in the reviewed preview samples. English and Chinese now show and narrate **rank at most one**, preserving the zero-input case. The six-operation table, index-identity subtitle and reveals remain readable and aligned.

| Case | Actual coverage |
|---|---|
| EN motion | 402 selected times: 66 unique new images viewed on nine chronological sheets, five exact within-case duplicates, 331 exact PNG matches to the prior reviewed `def7543b…` movie. Two native follow-ups. |
| ZH motion | 407 selected times: 65 unique new images viewed on nine chronological sheets, four exact within-case duplicates, 338 prior exact-PNG matches. Two native follow-ups. |
| EN endpoints | All 23 captures: five changed native views and 18 prior exact-PNG views. |
| ZH endpoints | All 24 captures: five changed native views and 19 prior exact-PNG views. |

Both silent movies are 854×480 at 15fps, about 160.07s EN and 159.40s ZH. All 2,401 EN and 2,391 ZH source frames were decoded. **1,999 EN and 1,984 ZH intervening frames were not visually inspected.** Maximum selected-time gaps are 1.0s; exact gaps and every time-to-review/reuse mapping remain in the ledgers. Reuse requires exact PNG SHA256, not perceptual similarity.

| Native comparison | Before | After |
|---|---|---|
| EN completed table | [Before](images/en-endpoint-before.png) | [After](images/en-endpoint-after.png) |
| ZH completed table | [Before](images/zh-endpoint-before.png) | [After](images/zh-endpoint-after.png) |
| New movie, outer-product reveal | — | [EN](images/en-motion-outer-reveal.png), [ZH](images/zh-motion-outer-reveal.png) |
| New movie, all six operations | — | [EN](images/en-motion-all-six.png), [ZH](images/zh-motion-all-six.png) |

Representative newly viewed motion sheets: [EN reveal](images/en-changed-sheet-003.png), [EN exit](images/en-changed-sheet-007.png), [ZH reveal](images/zh-changed-sheet-003.png), [ZH exit](images/zh-changed-sheet-007.png). The complete 18-page view ledger is compressed; this bounded package includes representative page PNGs rather than every extracted image.

Actual narration records contain the qualified EN/ZH text. All six blocks were checked in all four records: the other five blocks retain their text, translated clean text matches capture, and recorded word-time ranges remain monotonic and inside their blocks. The changed block grows by **0.740708s EN / 0.465125s ZH**. Bookmarks remain `abcdef`; `a/b` retain their token indices and `c–f` move by two tokens. Production token-index logic reconstructs in-range bookmark times. These are **silent synthesis timing estimates**, not measured spoken timestamps or listening/synchronization approval.

The direct scene source remains frozen at SHA256 `4cf32fd13a907723f2478104b8be2de7dd38df693fa330558edb15d1716ed23e`. Its bytes, the audit tool and consumed numerical JSON remained unchanged through this review; all four recorded input signatures still matched at completion. Exact new caption/narration content is verified in preserved output.

**Aggregate provenance limits remain explicit.** EN motion retains `needs-review` and `source-changed-during-render`; the other three records report `passed` without warnings. All four whole-part fingerprints differ from the completion-time source after concurrent edits. Scoped visual/content checks do not clear the EN warning or establish a current whole-part source bundle. The [completion ledger](ledgers/completion-provenance.json.gz) records each fingerprint and input check without relabeling runtime outcomes.

Fresh EN movie SHA256: `5c0c27de2dd25f0ea8a363860c99125d9532dd97d17bec30b10299953ded554b`.
Fresh ZH movie SHA256: `359b168c7e2ef8cdb1042af8e3b577b45378e0adc3db29b0a69a4024ecd73b9d`.
Both movies, records, native captures and source/input snapshots were copied before auditing. Movies remain in the runtime workspace and are not copied into this repository package. [manifest.json](manifest.json) authenticates the included native images and original-byte gzip ledgers; original absolute paths may be unavailable outside that workspace. Verify portable files with `sha256sum -c SHA256SUMS`; inspect a ledger with `gzip -dc ledgers/narration-timing-review.json.gz`.

The earlier [legend-polish package](../ai3-einsum-polish-regression/README.md) and native Library artifact remain unchanged historical evidence. This review does not update/upload Library content. Continuous playback, narrated listening/audio sync, production resolution and player/responsive behavior remain unverified. No scene/source/global-caption/data/model edits, renders, STATUS changes or commits were made by this regression review.
