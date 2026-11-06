# Quant, Built: sequential polish and QA

Source branch: `quantitative-finance`, starting at `20b4e7e0`.
Working branch: `polish/quantitative-finance`.
The pass was rebased onto `11c5c9d4` to preserve the concurrent Part 31 work and
shared axis-label fix; final checks use that updated base.

Finish one part before advancing. For each part, review the scientific explanation,
inspect narration-beat frames in English and Chinese, fix the layouts, and review
silent animation playback and its dead-air scan. Silent playback estimates speech
timing; narrated production masters need a separate listening and synchronization
pass. A successful render is not, by itself, visual approval.

## Queue

| Parts | Status in this pass |
| --- | --- |
| 1 | Visual pass complete; full production-voice listening pending |
| 2–43 | Pending; do not infer approval from historical build notes |

## Part 1: The Fair Game

Changes:

- The opening reaches the four-chart experiment sooner. The simulated paths are
  described accurately as compounded Gaussian log returns.
- The answer removes the distractor charts and gives the real chart and its
  explanation separate space. The historical path fan leaves room for its readout.
- A new animated probability tree shows why a martingale can rise 90% of the time:
  gains of 1 with probability 0.9 balance losses of 9 with probability 0.1.
- Low autocorrelation is distinguished from a martingale property. The research
  chapter states the symmetry and regularity conditions for its robust inference.
- The tail-chart narration matches its six-sigma view. Finite variance is described
  as supported by evidence; the README distinguishes fourth-moment consistency
  from the eighth-moment requirement for finite estimator variance.
- The no-trade theorem states its allocation, prior and rationality assumptions.
- Optional stopping states a bounded stopping time, matching the simulation's
  200-toss deadline; almost-sure eventual stopping is explicitly distinguished.
- Related Chinese narration and captions are updated with the English content.
- The research chapter's 33 missing Chinese captions and the two qualifying-exam
  questions are translated. A worked variance-ratio example reveals both statistics
  after a pause. Its inset and derivation appear in separate beats.
- Narration starts with content already appearing, and the sparse table opening is
  filled with its first data row and explanatory note. Crisis-card borders and the
  Gaussian tail curve stay inside their intended bounds; Chinese notes wrap inside
  their side panels.
- The QA runner initializes each worker's language and silent speech backend before
  importing `explainer`; previously English initialization could break Chinese TeX,
  start speech synthesis during a silent run, and omit text collection.

Evidence is generated under `renders/qa/series/quant1/{en,zh}/` (git-ignored).
Each chapter has `result.json`, narration-beat images and `sheet.png`; motion
chapters have a movie, `motion_sheet.png` and `dead_air.log`.
Read the fingerprint and input signatures in each record before treating it as
current after a source change.

Reproduce from the repository root with a configured Manim/TeX environment:

```bash
python -m videos.quant.quant1.compute
python tools/qa_series.py quant1 --cached-only --resume --timeout 1200
python tools/qa_series.py quant1 --lang zh --cached-only --resume --timeout 1200
python tools/qa_series.py quant1 --motion --cached-only --resume --timeout 1800
python tools/zh_lines.py quant1 --todo
python tools/lecture_length.py quant1 --floor 50
```

Validation: all 19 English and 19 Chinese narration-beat frame checks pass,
and all 19 English silent playback checks pass, with zero automated warnings.
Their contact sheets were visually reviewed. All 100 narration source lines have
Chinese coverage. The narration estimate is 57.8 minutes; the silent preview,
including animation and pauses, is 67:14. Eleven focused geometry, initialization
and financial-statistics tests pass.

The [compact evidence record](quant1-polish-evidence.json) captures the current
source fingerprint, 57 scene receipts and three audio sample reports. All 21
sampled English lines (Hook, Walk and Research) pass signal and alignment checks.
Kokoro emitted word-count/tokenization warnings on some technical Research lines;
these remain a listening lead, and do not certify pronunciation. The actual
148-second narrated Hook sample has no blank or sparse-screen dead air. Full
production-voice listening and synchronization remain pending. Chinese coverage
here is narration-beat frame QA, rather than whole-part narrated playback.

Local review artifacts (git-ignored):

- `renders/quant1_polished_silent.mp4`: English 480p15 preview, 19 embedded chapters
  and English subtitles; `.srt` and `.chapters.txt` sit alongside it.
- `media/quant1/narrated_qa/videos/s01_hook/480p15/Hook.mp4`: actual narrated English
  opening sample.

Part 2 is next in the sequential visual pass. Parts 2–43 have not been approved
by this pass.
