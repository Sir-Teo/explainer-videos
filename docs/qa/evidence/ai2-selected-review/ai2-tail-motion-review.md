# Part 2 tail motion review checkpoint

This is selected-time review of silent 854×480/15fps preview movies. Selections span each full timeline with at most one second between selections and additional motion boundaries. It is not continuous playback, narration/listening/synchronization, or production-resolution approval. Exact PNG duplicates may reuse an earlier actual view; the JSON retains the complete mapping and all unselected frame gaps.

| Case | Status | Selected times covered | Actually viewed sheets | Exact duplicate times | Native views |
|---|---|---:|---:|---:|---:|
| en-SAT | selected-time-review-complete | 533/533 | 66 | 8 | 1 |
| en-Knowledge | selected-time-review-complete | 429/429 | 52 | 16 | 0 |
| en-Eliza | before-selected-review-complete; EN-repair-after-regression-passed | 388/388 | 46 | 24 | 1 |
| en-Winters | before-selected-review-complete; EN-repair-after-regression-passed | 412/412 | 49 | 24 | 1 |
| en-Survives | selected-time-review-complete | 462/462 | 56 | 16 | 0 |
| en-Outro | all-selected-times-accounted-for; continuous-playback/audio-unverified | 303/303 | 38 | 0 | 2 |
| zh-SAT | review-reassigned-to-qa_integrity | 0/pending | 0 | 0 | 0 |
| zh-Knowledge | review-reassigned-to-qa_integrity | 0/pending | 0 | 0 | 0 |
| zh-Eliza | review-reassigned-to-motion_theory | 0/pending | 0 | 0 | 0 |
| zh-Winters | review-reassigned-to-motion_theory | 0/pending | 0 | 0 | 0 |
| zh-Survives | all-selected-times-accounted-for; continuous-playback/audio-unverified | 510/510 | 58 | 48 | 0 |
| zh-Outro | all-selected-times-accounted-for; continuous-playback/audio-unverified | 328/328 | 40 | 8 | 2 |

EN Eliza after repair: all 389 selected times accounted for: 56 times on 7 newly viewed sheets plus 333 exact PNG matches to before frames already actually viewed; native 65.6s confirms the three-line historical reply and full page fit. Separate after audit/report: `/workspace/runtime/ai2-eliza-after-review.json`. No full original before MP4 was copied before canonical replacement; before source, selected PNGs/sheets, native frame and audit/hash map remain.

Winters original MP4 was saved by root at `/workspace/runtime/ai2-winters-original-preservation`; parent-reported SHA matches the original ledger SHA. EN regression passed for all 417 selected times: 24 actually shown in sheets 49–51 and 393 exact PNG matches to actually reviewed before frames. Native 192.065s confirms measured coordinates remain fixed. Report: `/workspace/runtime/ai2-winters-after-review.json`.

ZH SAT/Knowledge are reassigned to qa_integrity; ZH Eliza/Winters to motion_theory. Their results live in separate reports. ZH Eliza extraction was completed and handed off with zero visual views by this reviewer.

## Findings and repairs

- E01 ELIZA: the original 1966 differing reply was compressed to a single tiny line. Repaired in s13_eliza.py using raw-data-safe word wrapping at 17pt; actual raw-data/whitespace checks pass. EN after selected/native validation passes; ZH delegated. Before native frame: `renders/qa/temporal/ai2-en-Eliza-dense-final/frames/0000983_000065.533s.png`.
- W01 Winters: default Indicate scaled the measured cumulative curve beyond 0–100% while axes and threshold dots remained fixed. Repaired in s14_winters.py with scale_factor=1.0. Actual Manim interpolation geometry check passes. EN rendered regression passes; ZH is delegated. Before native frame: `renders/qa/temporal/ai2-en-Winters-dense-final/frames/0002881_000192.065s.png`.

No other definite new visual defect confirmed in completed selected-frame reviews. Detailed section observations/checklists and provenance remain in the JSON. No production data computations or render jobs launched by this reviewer.
