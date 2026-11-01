# Part4 history-qualified silent previews

Both English and Chinese nineteen-chapter previews pass full technical validation and the scoped chapter-join regression. The Gradient history wording is corrected. The previous assemblies remain preserved as dated baselines.

| Preview | Duration | Video frames decoded | AAC frames decoded | Subtitle cues |
|---|---:|---:|---:|---:|
| English | 54:27.356 | 49,010 | 153,165 | 966 |
| Chinese | 57:58.820 | 52,182 | 163,077 | 959 |

These are **silent 854×480, 15fps QA previews** with nineteen embedded chapters and soft subtitles from captured estimated narration timings. Complete decoded PCM is digitally zero. They do not establish real narration, listening, synchronization or4K production approval.

Only the two Gradient clips changed. The other36 movie, result, narration-sidecar, duration and scene-source identities exactly match the reviewed baseline. All46 consumed data/expected-absence identities remain unchanged. The current38-case map is `33071a12…`; every movie/result/byte count/order entry hard-matches the frozen inputs. Original source and sparse-frame warnings are preserved; assembly does not relabel old records.

Every final video and AAC frame decoded successfully. Video/audio frame PTS strictly increases, packet DTS is monotonic, expected video frame sums and nineteen chapter boundaries agree, embedded subtitles roundtrip with exact text and millisecond timing, and all1,925 cues stay within their chapters. Both full-stream PCM decodes confirm silence. Full timestamp and command ledgers are retained.

All36 joins are accounted for. The four joins around Gradient were freshly reviewed:74 distinct PNGs on10actual sheets and8native context images cover76selected times, with2exact duplicates. The other32joins (608times and32native pairs) inherit only exactPNG identity from the actually reviewed baseline. No join regression was observed. This is selected-window review, not continuous viewing of the full programs.

Only the final Gradient narration paragraph changed per language, retaining its bookmarks. The English program is0.8s shorter and the Chinese program0.2s shorter; all downstream chapters/subtitles were regenerated. Every unchanged chapter retains exact cue text and local cue timing. The independent Gradient chapter image gate is accepted in `Gradient-acceptance.json`.

English movie SHA256: `bda4603fef4a06b72d06182b550c4688c8e2661d128ee391899cdcfbf8532782` (31,319,908bytes). Chinese SHA256: `322c81224ea983f72c3e01ce6daa9a16e173e036713bcc1bfbc901158a9c6dd0` (32,065,039bytes).

The parent confirmed source publication at `c16a525da73107d6aa8332b942cb5c206dc8107e`. All34 frozen observed source files exactly match that commit tree, including Gradient`10bac018…` and local Chinese narration`ec04b2f4…`. This establishes byte equivalence to published source; it does not prove historical interpreter imports. See `publication-receipt.json`. The parent's421-test suite receipt is external integration evidence, separate from these actual assembly checks.

`summary.json`, `input-freeze.json`, `canonical-crosscheck.json`, `subtitle-delta-check.json` and each language's validation/join receipts preserve exact coverage and identities. Build-time pending fields remain as historical records, resolved by the later acceptance/publication receipts. No rendering, producer/model computation, source/cache/data mutation, local execution, commit, merge, deployment or full-assembly Library upload was performed by this assembly task.

This bounded durable package includes full compressed timing/provenance ledgers, ten freshly viewed delta sheets and eight native context images. Full MP4s, normalized intermediates and raw numerical caches are excluded. Exact final cloud paths and SHA256s remain in receipts.

The baseline join proof is preserved in [the baseline assembly package](../ai4-silent-baseline-assembly/README.md); its current manifest SHA is `51257710a980495ac3b12d0e362eae46f199845185e6c335f9edaab02476910f`. Original raw Markdown hard breaks were losslessly gzip-archived there. The baseline runtime1013-file manifest remains unchanged at `54e414e421e9c31c013f3fab49af5913b07fadd4b093efccf15fd9f378dd6034`.

The independent refreshed chapter proof is in [Gradient history regression](../ai4-gradient-history-regression/README.md). Its scope is separate from this assembly delta. `manifest.json` binds every packaged file to exact original bytes; compressed records preserve all warnings and historical pending fields rather than rewriting them.
