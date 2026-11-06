# Quant, Built: sequential polish and QA

Source branch: `quantitative-finance`, starting at `20b4e7e0`.
Part 1 branch: `polish/quantitative-finance`; Part 2 branch: `polish/quant2`;
Part 3 branch: `polish/quant3`.
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
| 2 | Visual pass complete; full production-voice listening pending |
| 3 | Visual pass complete; full production-voice listening pending |
| 4–43 | Pending; do not infer approval from historical build notes |

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

The completed visual passes for Parts 2 and 3 are recorded below. Parts 4–43 remain pending.


## Part 2: The Machinery of Markets

Visual pass complete on `polish/quant2`, stacked on the Part 1 review branch:

- Replace a simulated sample's distinct-value count with the full 251 possible
  annual breach counts; compute exact rejection probability over the full support.
- Fix Kupiec's all-breaches endpoint (`0 log 0`) and add boundary regression tests.
- Add a magnified breach cluster and worked count/independence comparison after
  the research pause, with explicit dates so transition counts are unambiguous.
- State execution, venue-priority, carry-pricing and reflection-model assumptions.
- Distinguish simulated hourly-close account deficits from actual exchange losses,
  and full-sample constant volatility from a forecast available at the time.
- Match spoken return-smoothing weights to the model and shorten the opening.
- Keep the hedge valley within valid correlations, and convert simple price limits
  to log-return bounds before clipping the price-limit simulation.
- Keep content visible during the bond-price explanation and research transitions.
- Separate small waterfall-layer callouts, stage the liquidation prediction after
  its derivation, and remove empty camera-reset time between 3D and 2D material.
- Keep replay children matched across checkpoints and extend the right regression
  fit across its full data range.
- State the smoothing assumptions and allow for partial fills at price limits.
  Describe EWMA as improved but still oversized; its historical independence
  statistic still rejects.
- Trim repeated introductions and recap narration to keep the expanded lecture
  within the syllabus's 55–65-minute target.

Validation: all 21 English and 21 Chinese narration-beat frame checks pass, and all
21 English silent playback checks pass, with zero automated warnings. Their contact
sheets were visually reviewed. All 124 narration source lines have Chinese coverage;
six focused funding and numerical-example tests pass. The narration estimate is
64.8 minutes, within the syllabus's 55–65-minute target.

The [compact evidence record](quant2-polish-evidence.json) captures the final source
fingerprint, data hashes, 63 scene receipts and three speech reports. All 22 sampled
English lines (Hook, Margin and Research) pass signal and alignment checks. The
actual 128-second narrated Hook sample matches the final narration and has no blank
or sparse-screen dead air. These checks do not certify pronunciation; full
production-voice listening and synchronization remain pending. Chinese coverage is
narration-beat frame QA rather than whole-part narrated playback.

Local review artifacts (git-ignored): `renders/quant2_polished_silent.mp4`, an English
480p15 preview (75:49 including animation and pauses) with 21 embedded chapters and
English subtitles, plus its `.srt` and
`.chapters.txt`; and `media/quant2/narrated_qa/videos/s01_hook/480p15/Hook.mp4`, the
actual narrated English opening sample. Part 3’s visual pass is recorded below.

Reproduce Part 2 from the repository root (refresh the two changed cache items):

```bash
python -m videos.quant.quant2.compute backtest_theory limits --force
python -m videos.quant.quant2.compute
python tools/qa_series.py quant2 --cached-only --resume --timeout 1200
python tools/qa_series.py quant2 --lang zh --cached-only --resume --timeout 1200
python tools/qa_series.py quant2 --motion --cached-only --resume --timeout 1800
python tools/zh_lines.py quant2 --todo
python tools/lecture_length.py quant2 --floor 50
EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart python tools/qa_audio.py quant2 --only Hook Margin Research
```

## Part 3: Value, Accounting and the Firm

Visual pass complete on `polish/quant3`, stacked on Part 2:

- Distinguish the annual-change Shiller illustration from the formal variance bound,
  and state its constant discount rate and terminal-price assumptions.
- Replace the claim that Ohlson's multiple diverges at persistence one with its
  finite `1/r` limit, and explain the equal-persistence limit.
- Add a staged answer and contribution bar for the Ohlson exercise. Show the EDGAR
  slope marker and its implied multiple rather than silently omitting them.
- State the descriptive nature of the pooled filing regressions, and qualify causal
  claims from Treasury-yield regressions and payout timelines.
- Distinguish duration's local −33% approximation from the exact −25% finite change.
- Correct the equity/debt surface description, the day-0–1 earnings-event labels,
  and the treatment of net buybacks in aggregate and per-share valuation.
- Explain that negative takeover probabilities expose an inconsistent fallback
  assumption; physical probabilities require a risk-premium assumption.
- Correct the SEC's 2009–2011 XBRL phase-in and remove empty 3D camera resets.
- Keep as-of animation children stable so text is not copied into newly added dots.
- Show present value outside the duration chart's 60-year window, label surface
  display caps, and keep the takeover-model interpretation inside its panel.
- Correct ASC 842 operating leases: EBITDA stays 100; including lease debt gives
  EV/EBITDA 13.5 and debt/EBITDA 4.5. A rent add-back to EBITDA 120 is a separate
  analyst adjustment. Checked against ASU 2016-02, paragraph 842-20-25-6.
- Update the corresponding Chinese narration and captions.

Validation: all 21 English and 21 Chinese narration-beat frame checks pass, as do
all 21 English silent playback checks, with zero automated warnings. Every receipt
matches the final source fingerprint and input signatures. Narration-beat contact
sheets and sampled playback frames were visually reviewed, with focused rechecks
of the changed layouts and transitions. All 22 compute items were regenerated
against the frozen data checksums without changing registered forecast code or
the sealed envelope. Twelve focused valuation/accounting tests pass; Chinese
narration covers 129/129 lines; the narration estimate is 64.6 minutes.

The [compact evidence record](quant3-polish-evidence.json) captures the final source
fingerprint, input hashes, 63 scene receipts, visual-review scope and three speech
reports. All 19 sampled English lines (Hook, Duration and Research) pass signal and
alignment checks against current receipts. The actual 199-second narrated opening
matches the final narration and has no blank or sparse-screen warnings. Full
production-voice listening and synchronization remain pending; these checks do not
certify pronunciation. Chinese coverage is narration-beat frame QA rather than
whole-part narrated playback.

Local review artifacts (git-ignored): `renders/quant3_polished_silent.mp4`, an English
480p15 preview (75:58 including animation and pauses) with 21 embedded chapters
and English subtitles; its `.srt` and `.chapters.txt`; and
`media/quant3/narrated_qa/videos/s01_hook/480p15/Hook.mp4`, the narrated opening
sample. Part 4 is next in the sequential visual pass.

```bash
SEC_USER_AGENT='explainer-videos research bot' python -m videos.quant.quant3.compute
python tools/qa_series.py quant3 --cached-only --resume --timeout 1200
python tools/qa_series.py quant3 --lang zh --cached-only --resume --timeout 1200
python tools/qa_series.py quant3 --motion --cached-only --resume --timeout 1800
python -m pytest tests/test_quant3_valuation_examples.py tests/test_quant_house.py -k 'quant3_valuation_examples or part3 or valuation_closed or modigliani or fundamentals_store' -q
python tools/zh_lines.py quant3 --todo
python tools/lecture_length.py quant3 --floor 50
EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart python tools/qa_audio.py quant3 --only Hook Duration Research
```
