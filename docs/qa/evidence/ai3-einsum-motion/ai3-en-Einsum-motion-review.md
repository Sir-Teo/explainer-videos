# Part3 English Einsum: selected-time motion review

Completed 2026-10-31T18:21:36.803958+00:00. No visual defect found in the reviewed selected frames. This is a selected-time preview review, not continuous playback or audio sign-off.

- Movie: /workspace/explainer-videos/renders/qa/series/ai3/en/Einsum_motion/media/videos/480p15/Einsum.mp4
- Movie SHA256: `bd287224d65ec684ec5628444f0d5d590994bdb17c81514263eefb66637ff897`
- Duration: 159.333s; 854×480, 15fps; 2,390 decoded frames.
- 390 selected times accounted for:382 frame images actually displayed on 48 chronological sheets,8 exact-PNG duplicate times mapped to previous actual views (sheet 37 omitted only for byte identity). All 49 sheet hashes and every selected-time mapping retained in JSON.
- Six additional native-size follow-ups:27.067,61.533,86.064,126.731,152.598,158.131s.
- Largest selected time gap 1.0s; 2,000 intervening source frames unviewed, with exact gap ledger.
- Frozen motion extractor SHA256:`1d0cee16ad098360ceb70f9cbc513bbce334ea107e90982ace3a7fd3df73595e`. Single case ran at nice 10 with 1 numerical thread; no production render/compute/model or source edits.

## Observations

- 0–32s, Introduction and tensors: Viewed title/timeline and tensor reveals; axes, two shape lines, grid offsets and labels fit. Native follow-up at27.067s.
- 32–68s, Summation convention: Row/column/output cell highlights match matrix indices; kept/summed index colors agree with equations and code. Native follow-up61.533s.
- 68–89s, Six operations: All six operation rows and gradual ghost-to-full reveal fit; notation and descriptions legible. Native follow-up86.064s.
- 89–128s, Attention contractions and costs: Four contractions including corrected outputbqd, cache-matched805/805/2416million bars, long label and footer fit. Native126.731s. Individual bar growth is staggered; final lengths match1:1:3.
- 128–159.333333s, Matrix-chain comparison and exit: Input and intermediate shapes,40m/.8m costs and50x narrative arithmetic agree with immutable data. Optimized path beginsB,C. Selected reveals/hold/exit show no overlap/clipping. Native152.598s and158.131s.

## Provenance and limits

The original movie, render record, cache JSON and direct scene source were copied before review into `/workspace/runtime/ai3-en-Einsum-original/`, with byte counts and SHA256s. All four preserved and current canonical files still match at completion. Direct scene source SHA256 `0ee08694317f73f1a5a9ab486f387bfbac30d038c44a2a63f16bcf82c0e65ff1` matches commit 4a208 exactly.

The render record remains `needs-review` with `source-changed-during-render`, fingerprint `4d660cd10b555641162f66a262561ca74b08b35685aa167d29516fb6f5f2c1f9`. Broad source/input provenance approval is not inferred from the unchanged direct scene. The full record and immutable data hashes remain in the JSON/preservation manifest.

Continuous-speed playback, audio/listening/synchronization, final production resolution, Chinese motion and player/responsive behavior remain untested by this review.

JSON evidence: `/workspace/runtime/ai3-en-Einsum-motion-review.json`.
Audit: `/workspace/explainer-videos/renders/qa/temporal/ai3-en-Einsum-dense-final/result.json`.
