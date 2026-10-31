# Part 1 head endpoint visual review

Reviewed all eight head chapters in English and Chinese: **16 contact sheets containing 381 sampled endpoint images**, plus **26 individual 854×480 frames**. These were actual `view_image` inspections. This is sampled endpoint review, not continuous playback, intermediate-animation, speech/listening, narration synchronization, or final-resolution approval.

Two concrete defects were reported promptly and corrected by root:

- **Probability, EN/ZH:** the fixed-width magnified column's `P(A)=P(t)=0.072` brace lacked a width-scale cue. Fresh frames now show **“width magnified” / “宽度已放大”** above that column. The cue stays clear of the title, formula, and neighboring symbols.
- **Prefix, Chinese:** the final McMillan why-note `可解码：A_m≤2^m` crowded the chart's upper-left y-tick/log-scale area. Fresh English and Chinese frames place the note below-left of the inequality, clear of the graph.

I inspected all four refreshed sheets (**91 endpoint-image observations**, substantially repeating earlier frames) and four native fix frames from immutable copies captured under shared chapter locks. Their source/data provenance was current at fingerprint `a3b80ce4acb50a631be6be6f23cb1bf432e0ef923e839b119d296d0d22fc4a40`. The exact snapshots, original filenames, SHA-256 values, and result records are in `/workspace/runtime/ai1-head-visual-review.json`, under each `post_fix_refresh`; pixels are retained in `/workspace/runtime/ai1-head-visual-evidence/refresh/`.

No further static visual defect was identified in the inspected samples:

| Chapter | What was actually inspected |
|---|---|
| Hook | Every sheet tile; native timeline, 31-part series map, and scoreboard in both languages. Date/model labels and columns fit. Dim future rows are intentional emphasis. Hook records carried an earlier fingerprint and source-change warning, so this is historical layout evidence. |
| Probability | Every sheet tile; native conditional-probability mosaic in both languages and final Chinese interval ladder. Formula, conditional brace and alphabet labels are legible; revised width cues verified separately as above. |
| Surprise | Every sheet tile; native English curve-label and final skyline views and Chinese final skyline. Equation box, surprise values, words/bars, total and legend remain separated. |
| Entropy | Every sheet tile; native final conditional-entropy diagram in each language. Formula, conditional-area caption, unconditional reference line and q-arrow remain readable. New redundancy wording exists in the captured English/translated Chinese narration paragraph; it is narration-only, so it was checked as text rather than claimed visible or heard. |
| Prefix | Every sheet tile; native final comparison proof/chart. Trees, Kraft area accounting and canonical code table fit. Refreshed final proof/why-note placement verified in both languages. |
| Huffman | Every sheet tile; native exchange/sibling demonstration in each language. Long bit strings, probability values, swap formula and rare-sibling labels are readable and separated. |
| Typical | Every sheet tile; native English coding-rate panel and Chinese definition, cardinality ladder and coding-rate panel. Apparent thumbnail truncation was checked at native size and was not actual clipping. Schematic/example disclosures remain visible. |
| CrossEntropy | Every sheet tile; native final loss and KL panels in both languages. The corrected autoregressive-pretraining headline fits. Shared density scales, mu/sigma/KL readouts, source/model colors, objective labels and below-plot captions remain clear. |

Provenance is deliberately explicit. Primary sheets were inspected at the earlier frozen source state (all except Hook passed the current fingerprint/data check then). Root changed the global fingerprint while applying the two visual fixes. Later views of unchanged scenes therefore remain labeled earlier-source evidence; they are not silently promoted to current. A Chinese CrossEntropy metadata snapshot overlapped the worker's result-before-sheet write interval; its sheet and two native frames were subsequently copied under a shared chapter lock and inspected again. That stable reconciliation adds one repeated 24-frame sheet and two native views, with its own recorded hash/provenance.

The JSON records each original asset path and exact filename, sheet/result SHA-256 hashes, captured fingerprints, data-current checks, explicit native-frame lists, review findings, byte-change detection, and the fresh immutable fix/reconciliation assets. Native-frame hashes from the initial pass were read at metadata-finalization time rather than before viewing, and are labeled accordingly; the four fixed cases have stronger pre-view immutable snapshots.

Remaining: current-source preflight refresh for other head records after the global fingerprint change, full silent/narrated playback, listening/sync checks, and final-resolution review belong to root's broader QA. No unresolved visual defect is asserted in the endpoint images I inspected. No repository source, cache, render process, commit, or push was modified/launched by this reviewer.
