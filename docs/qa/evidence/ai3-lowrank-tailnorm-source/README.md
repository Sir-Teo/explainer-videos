# Part 3 LowRank: tail-norm precision source repair

The image caption previously labeled the scalar `7.8646` as “the singular values left out.” The producer correctly computes the Euclidean norm of those values, `sqrt(sum(sigma[k:]**2))`, and the preceding proof correctly uses their squared sum. Both English narration passages and their two Chinese translations now explicitly state that Frobenius error equals the Euclidean norm of omitted singular values. The caption displays both measured `||A-A_8||_F=7.8646` and `sqrt(sum_{i>8} sigma_i^2)=7.8646`.

**Fresh bilingual scene appearance, motion, VO duration and narration synchronization remain pending.** The source/manual checks below are not rendered sign-off. New narration is longer; bookmark order and animation durations are preserved.

## Actual before evidence

[Chinese image caption at 88.266 seconds](zh-LowRank-before-native-02.png) confirms the loose scalar label. [The preceding proof](zh-LowRank-before-native-01.png) shows the correct squared-sum identity. The corresponding [English caption](en-LowRank-before-native-02.png) is also preserved. The remaining native frames document the unchanged square-root-bigram interpretation.

EN LowRank before movie SHA: `f71dd0491ced9cd3d6c56c223cc954181d1a48d7df16f2d500260371dcf78e54`.

The EN/ZH LowRank capture/movie/source copies were individually matched to the completed immutable owner reviews before the source edit. Their compressed complete ledgers preserve all selected timestamps, PNG/page hashes, viewed representatives, warnings and unselected intervals. No LowRank writer was active during that snapshot.

The larger raw 18-case inventory was copied while an unrelated Einsum render could write canonical files. Both Einsum pairs are explicitly marked uncertain and excluded as valid baselines. Matching copied-byte hashes alone cannot establish a consistent render pair or worker import. Other raw copies require their existing owner-specific review provenance; no blanket “18 validated baselines” claim is made. Raw copies were preserved without blind recopy. Only the required LowRank pairs establish this repair's before evidence.

## Source and manual validation

- `s09_lowrank.py` frozen SHA: `8424ebda29b931c5507cd2b505e8911130c220c3df10ae801afd237e81da0fdd`.
- `zh_lines.py` frozen SHA: `16504c1c99cf99a73ecf17af50500cf2cce29c4187b674b0c7b6e23375b8ab70`; exactly the two owned LowRank entries changed relative to before SHA `a487167b7052952ca30ff29028efb76cf204b9ea172d3c2c19f17f866fbdc38e`.
- Existing `test_ai3_narration_review.py`: **10 tests passed**, 11.009 seconds. Compilation, diff checks and AST preservation checks passed. No exact-wording unit test was added.
- A standalone `[3,4]` omitted-value example gives norm `5`, distinct from sum `7`, reproducing why the qualification matters without production imports or computation.
- Actual Tex caption construction gives EN width `6.0521` and ZH width `5.9667` world units. Both bounds have bottom `-3.45`, top `-2.9643`, leaving the requested margins. This is a caption geometry check, not a video render.
- AST checks permit only the caption expression and two narration arguments to differ. All bookmarks, data access, animations and other geometry remain identical.

The strings-only caption handoff is retained, alongside full changed EN expressions, before/after source snapshots, geometry code/logs, integration-test log and source patch. The parent owns the global caption-table merge and subsequent renders. Current later source/table changes are not silently substituted for these frozen copies.

[manifest.json](manifest.json) hashes every payload and its uncompressed source. Absolute runtime paths are historical provenance. No model/data changes, production imports/loaders, downloads, source rendering, STATUS edits, commits or pushes were performed by this packaging task.
