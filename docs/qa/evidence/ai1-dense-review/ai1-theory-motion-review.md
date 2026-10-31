# Part 1 theory motion review

Completed: 2026-10-31T14:38:09.727962+00:00

Reviewed six existing silent 480p15 movies: Typical, CrossEntropy and Arithmetic in English and Chinese. Every original selected time has an inspected contact-sheet tile or a byte-identical native PNG match to an inspected representative. This is selected-frame review, not continuous perceptual playback.

| Case | Duration | Frames decoded automatically | Selected times covered | Unique PNG representatives | Times covered only by exact duplicates |
| --- | ---: | ---: | ---: | ---: | ---: |
| en/Typical | 240.266s | 3604 | 499/499 | 371 | 90 |
| zh/Typical | 254.533s | 3818 | 523/523 | 396 | 127 |
| en/CrossEntropy | 252.865s | 3793 | 531/531 | 396 | 135 |
| zh/CrossEntropy | 257.599s | 3864 | 557/557 | 411 | 146 |
| en/Arithmetic | 290.663s | 4360 | 569/569 | 416 | 153 |
| zh/Arithmetic | 299.263s | 4489 | 585/585 | 436 | 149 |

Actual review: 164 original/unique contact pages, plus 3 local risk-follow-up pages. The original schedule contains 3264 selected times, with gaps of at most one second (floating-point error below 2e-15) and extra transition/onset/midpoint/end frames. 2426 unique native PNG representatives were inspected chronologically, plus repeated source-frame tiles and 12 native follow-ups. Only exact SHA256 image equality was used for duplicate mapping.

The Chinese Arithmetic pulse follow-up inspected every one of 47 source frames from 239.730 to 242.797 seconds, including 42 source times outside the original selected schedule. This exposed a brief collision whose peak the original schedule missed. Short unsampled defects elsewhere can therefore remain.

## Findings

1. **Rounded cross-entropy equalities, both languages (minor).** Examples show `4.84 = 4.08 + 0.75` and `4.75 = 4.07 + 0.69`. Separately rounded values differ by 0.01 when summed. Use an approximate sign on numeric examples; preserve the exact symbolic identity. Source at inspection: `videos/ai/ai1/s08_cross_entropy.py:145–146`. EN native evidence: 72.533s, frame 1088. Chinese contact evidence: 71.600s, frame 1074.
2. **Arithmetic final bitstring pulse collides with its label, both languages (medium).** The `Indicate` animation enlarges the bitstring leftwards over the fixed `sent:`/`发送:` label. Use `scale_factor=1.0` or a safely grouped pulse. Source at inspection: `videos/ai/ai1/s09_arithmetic.py:512`. EN native evidence: 236.063s, frame 3541. Chinese native evidence: 242.197s, frame 3633, in the additional all-frame window.
3. **Rare-symbol emphasis obscures its tiny interval (optional clarity refinement).** The whole c-partition row flashes solid red, hiding partition contrast while explaining its 0.8% probability. Consider emphasizing the selected sliver and probability readout, or an outline. Settled geometry is correct. EN evidence: 85.333s, frame 1280; Chinese: 87.733s, frame 1316. Source at inspection: `s09_arithmetic.py:209`.

All findings were reported to the parent. This reviewer made no source changes. Fixes and targeted regression remain with the parent.

## Actual visual coverage

- **Typical:** histogram concentration, changing sample sizes and live readouts, AEP definition/proof ladder, toy count/probability bars, block-code explanation, rate curve, explicitly schematic nested areas and fades. No concrete clipping or collision found. The initially empty data axes accompany callback narration; this was not classified as a blank-screen defect.
- **CrossEntropy:** codeword/probability table, true/swapped comparison bars, CE derivation, Gibbs/Jensen proof, equality and MI card, autoregressive loss/nats callout, and forward/reverse Gaussian KL movement. The shared normalized scale, target shading, objectives and readouts fit. Rounded numeric examples are reported above.
- **Arithmetic:** whole-bit motivation, scrolling interval ladder, binary endpoint readouts, dyadic containment/overhead proof, reverse decoder, integer renormalization/waiting bits, reciprocal model/compressor arrows, new complete-prefix normalization note and final fades. Native follow-ups confirm the note, arrows and long equations fit in both languages. The pulse collision is reported above.

## Provenance and evidence

- Detailed report: `/workspace/runtime/ai1-theory-motion-review.json`.
- Actual views ledger: `/workspace/runtime/ai1-theory-motion-views.json`. It records page SHA256, time ranges, every represented source-frame PNG and native follow-ups.
- Per-case audit: `renders/qa/temporal/ai1-{en|zh}-{Typical|CrossEntropy|Arithmetic}-dense-final/result.json`. These preserve exact movie/tool hashes, selection settings, motion intervals and unsampled frame gaps.
- Exact duplicate mappings: each case’s `unique-review/index.json`.
- Additional pulse evidence: `renders/qa/temporal/ai1-zh-Arithmetic-dense-final/native-pulse-followup/index.json`.
- Frozen tool SHA256: `1d0cee16ad098360ceb70f9cbc513bbce334ea107e90982ace3a7fd3df73595e`.
- Capture fingerprint: `85926ba513a624bac1a38eb8a9455b82c5978b8e1ef01f3f87f667ba21f18caf`. Whole-part fingerprints are currently stale. English Arithmetic explicitly reports a source change during rendering. The movies are identified by bytes; no claim is made that these renders match current source. All recorded capture input signatures still match their size/mtime observations at review, and current input hashes are retained in JSON.

## Remaining limits

- Continuous perceptual video playback is unavailable and unverified. Automated whole-file RGB decoding is not manual playback.
- The movies are silent. Listening and actual narrated audio/animation synchronization are unverified; proxy narration timestamps do not establish audio sync.
- Manual review covers only listed representative frames, exact duplicates and the extra 47-frame window. It does not cover every decoded frame elsewhere.
- Most tiles are 480px wide; the first 16 original English Typical pages used 640px tiles. Native follow-ups use 854×480. Final production-resolution readability still needs production review.
- Current-source rerenders and regression of the reported fixes are pending with the parent.
- This reviewer did not render scenes, recompute data, edit repository source, commit or push.
