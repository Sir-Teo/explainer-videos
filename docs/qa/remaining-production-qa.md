# Remaining narration and production QA

This queue stays open while sequential source/data/selected-frame reviews advance through the series. Parts1and2
are **not fully production-approved**. Their selected-frame visual passes are complete; that does not close the items below.

| Part | Narrated renders | Listening / continuous perception | Production resolution / player |
|---|---|---|---|
| 1,17scenes×2languages | One English Information169.57s movie; six real speech blocks. Remaining33cases pending | No actual listening approval. OriginalInformation native cloud playback had timed screenshots; current margin-corrected version has selected-frame review. | InformationEN1080p checked; broad remaining final-resolution and responsive-player checks pending |
| 2,16scenes×2languages | All32narrated cases pending; current movies use silent timing placeholders | No listening approval. OriginalLogicEN native playback had timed screenshots; current teaching-caption version has selected-frame review. | All current full movies480p15; Knowledge has41 bilingual native1080p endpoints, not full1080p motion. Broader production resolution and responsive behavior pending |
| 3,19scenes×2languages | All narrated cases pending; first nine data-ready scenes have bilingual endpoint review and silent motion review underway | EinsumEN native cloud playback with timed screenshots; no listening or continuous perceptual approval | Silent previews480p15; production checks pending |
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
