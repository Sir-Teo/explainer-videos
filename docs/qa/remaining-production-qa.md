# Remaining narration and production QA

This queue stays open while sequential source/data/selected-frame reviews advance through the series. Parts1and2
are **not fully production-approved**. Their selected-frame visual passes are complete; that does not close the items below.

| Part | Narrated renders | Listening / continuous perception | Production resolution / player |
|---|---|---|---|
| 1,17scenes×2languages | One English Information169.57s movie; six real speech blocks. Remaining33cases pending | No actual listening approval. OriginalInformation native cloud playback had timed screenshots; current margin-corrected version has selected-frame review. | InformationEN1080p checked; broad remaining final-resolution checks pending |
| 2,16scenes×2languages | All32narrated cases pending; current movies use silent timing placeholders | No listening approval. OriginalLogicEN native playback had timed screenshots; current teaching-caption version has selected-frame review. | All32 preview movies480p15; English Hook also has a reviewed silent1080p motion pilot. Knowledge has41 bilingual native1080p endpoints. Broader production motion pending |
| 3,19scenes×2languages | All 38 narrated cases pending; all 38 endpoint and silent-motion runtime cases exist, with current repaired selected-frame review tracked separately | EinsumEN native cloud playback with timed screenshots; no listening or continuous perceptual approval | Silent previews 480p15; selected native endpoints checked; broad production checks pending |
| 4–31 | Pending; follow per-part manifests and current source | Pending | Pending |

The next narration queue begins with Part1 in manifest order, retaining the completed InformationEnglish cache.
Part2 then follows its16chapter manifest, both languages. Source/data and visual work may progress while these explicit
narration/perceptual gaps remain open; no sampled-frame result is promoted to full playback or audio approval.

Current capability bottleneck: this executor has4CPU quota/16GiB RAM and noGPU. The existing authorized Qwen
CPUFP32 path generated126seconds of new speech in approximately47minutes while renders were active (about22×
real time in that observed workload). Serial CPU chunking fixed a real memory/OOM failure, but does not make full-series
narration fast. The tested service is stopped to free memory for single-owner numerical/model work. No paid service,
new credential, or unvalidated model/precision change has been substituted. A tiny BF16GEMM benchmark is not a measured
full-TTS speed/quality result. Opportunistic bounded narration should resume only when it does not disrupt numerical work.

There is no dependable continuous video/audio perception input in this executor. Dot's native cloud desktop can play
files and supply timed screenshot inspection, which is recorded precisely; it supplies no audio-listening claim.
Actual remaining sync, pronunciation, subjective pacing, end-to-end listening and continuous perceptual review require
that capability or explicit human review. Existing signal/timing/ASR checks are supporting evidence only.

Minor optional polish queue: check provenance-footer insets consistently at final resolution (Logic preview showed18px
in a1364px display); Knowledge boundary anchors and caption clearance are now repaired and verified in both languages, including native1080p endpoints. Remaining footer inset polish is optional.

No web-player application source is tracked in this repository. Responsive behavior of an external hosting player is outside this checkout; native exported-file playback remains a separate, applicable check. The QA HTML reports are evidence viewers, not the educational video product.

Full-part concatenation and chapter-join continuity, production subtitle/metadata muxing, final loudness normalization and whole-part pacing remain pending even where individual silent chapters have selected-frame coverage.
