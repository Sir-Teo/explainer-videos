# Part5 native1080 endpoint review

All **299 native1920×1080 endpoint images** across the authorized **17 cases** were inspected on **80 chronological pages** at960×540 per image, with **42 separately inspected original1920×1080 followups**. These are new native captures, not inferences from the earlier480p evidence. No new corrective typography/geometry defect was found in this scope.

| Case | Native PNGs | Pages viewed | Original-size checks | Raw result |
|---|---:|---:|---:|---|
| en/Hook | 13 | 4 | 3 | passed |
| zh/Hook | 17 | 5 | 3 | passed |
| en/Bell | 19 | 5 | 2 | needs-review |
| zh/Bell | 22 | 6 | 2 | passed |
| en/Gauss | 18 | 5 | 2 | passed |
| zh/Gauss | 18 | 5 | 2 | passed |
| en/Likelihood | 16 | 4 | 2 | passed |
| zh/Likelihood | 16 | 4 | 2 | passed |
| en/Fisher | 19 | 5 | 2 | passed |
| zh/Fisher | 19 | 5 | 2 | passed |
| en/Decoding | 19 | 5 | 3 | passed |
| zh/Decoding | 21 | 6 | 3 | passed |
| en/Markov | 16 | 4 | 3 | passed |
| zh/Markov | 16 | 4 | 3 | passed |
| zh/Bayes | 16 | 4 | 2 | passed |
| zh/MaxEnt | 16 | 4 | 3 | passed |
| zh/Tails | 18 | 5 | 3 | passed |

The unchanged private wrapper ran serially at nice15 with one numeric thread, cached-only data and a512MiB free-disk guard before each case. The capture queue exited0. Before each capture, exact direct/shared source snapshots and standard endpoint result/text/log identities were preserved. Native raw records, every frame timestamp/SHA256/size, input hashes, page/view receipts and warnings are retained in compressed case ledgers. Source snapshots were identical before/after every case; the shared caption table was c2914a29…. Input byte hashes were taken after each capture with matching captured size/mtime, then rechecked when packaging.

**Raw warning preserved:** EN Bell is needs-review with `source-changed-during-render`, despite unchanged scoped source snapshots; the remaining16 native records passed with no warnings. This review does not silently rewrite that warning or assert an aggregate fingerprint is current solely from matching direct modules.

**Known endpoint-capture limitations preserved:** Markov EN/ZH step1 can retain an old100% q bar/tag after skipped animations; MaxEnt ZH step60 can show uniform old bars beside final lambda/mean text until a later hold. These exact native examples remain in the package. They are excluded from real-motion correctness conclusions; actual silent-motion reviews are separate evidence. No source repair is inferred from these known skipped-updater artifacts.

The original-size examples cover score-field legends, plan rows, convolution/conditional derivations, likelihood hill labels, Fisher benchmark/regularity/residual qualifications, decoding samples/metric definitions/SE disclaimer, detailed balance/mixing bounds, posterior intervals/MAP, inverse temperature, concentration bounds and the first262-versus-all-n≥281 coin-count distinction.

Full native images/pages remain in `/workspace/runtime/ai5-production1080-review/` and separate canonical `renders/qa/production-endpoints-1080/ai5/`. This bounded repository supplement retains all critical original-size PNGs, one actual page per case, complete compressed coverage/provenance and deduplicated source snapshots. It changes no scene, numerical core, producer, data/cache, translation table or CI configuration.

**Limits:** skipped-animation silent endpoints only. This does not approve1080p full motion, continuous perceptual playback, narration/listening/synchronization or assembled reels. It covers only the listed17 cases, not all Part5 chapters.
