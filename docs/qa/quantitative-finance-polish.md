# Quant, Built: sequential polish and QA

Source branch: `quantitative-finance`, starting at `20b4e7e0`.
Part 1 branch: `polish/quantitative-finance`; Part 2 branch: `polish/quant2`;
Part 3 branch: `polish/quant3`; Part 4 branch: `polish/quant4`;
Part 5 branch: `polish/quant5`.
The pass was rebased onto `11c5c9d4` to preserve the concurrent Part 31 work and
shared axis-label fix; final checks use that updated base.

Finish one part before advancing. For each part, review the scientific explanation,
inspect narration-beat frames in English and Chinese, fix the layouts, and review
silent animation playback and its dead-air scan. Silent playback estimates speech
timing; narrated production masters need a separate listening and synchronization
pass. A successful render is not, by itself, visual approval.

Delivery workflow: continue directly on `quantitative-finance`. Commit and push completed parts to that branch; do not create additional pull requests. Parts 1–5 below retain their original review-branch history.

## Queue

| Parts | Status in this pass |
| --- | --- |
| 1 | Visual pass complete; full production-voice listening pending |
| 2 | Visual pass complete; full production-voice listening pending |
| 3 | Visual pass complete; full production-voice listening pending |
| 4 | Visual pass complete; full production-voice listening pending |
| 5 | Visual pass complete; full production-voice listening pending |
| 6 | In progress: econometrics audit and bilingual layout checks |
| 7–43 | Pending; do not infer approval from historical build notes |

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

The completed visual passes for Parts 2–4 are recorded below. Parts 5–43 remain pending.


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
sample. Part 4’s visual pass is recorded below.

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


## Part 4: Martingales and Measure

Visual pass complete on `polish/quant4`, stacked on Part 3:

- Correct the bounded betting confidence sequence: avoid candidate-specific clipping,
  use predictable one-sided stakes, split the error budget and bracket continuous
  means outward from the numerical grid. State its constant conditional-mean model.
- Preserve the original registration and add `btc_mean_confseq_bounded_v2` as one
  corrective trial. All previous registrations, sealed dataset hashes and hold-out
  opening records remain unchanged; the Part 4 trial counter becomes 232.
- Restore the optional-stopping histogram's missing +1 atom and left-overflow mass,
  using the full sample's mean rather than the displayed histogram's truncated mean.
- Map ONS replay checkpoints to completed days: show the full sampled curve through
  day 9,981 and its first crossing on day 2,542. The registered simulation is unchanged.
- Include the final observation in the drift-history replay, so its final 9.5% estimate
  matches the summary. Distinguish Gaussian credible bands from confidence sequences.
- Identify estimated market drift and residuals as diagnostics requiring calibration;
  state integrability, boundedness and stopping-time conditions for the theorems.
- Correct the LIL envelope statement, Gaussian proof scope and observation times;
  add a staged, worked boundary comparison. Correct the frontier's 21-day review
  schedule and known-variance z tests; average full seed FDPs without clipping them.
- Qualify stable-law moments, likelihood-search convergence, calendar comparisons,
  bold play, historical casino figures and the pricing-measure illustrations.
- Give questions and legends separate space, switch the singular-measure title when
  its model changes, and show context before the exit-time derivation begins.
- Update Chinese narration and captions. Speed plain Chinese wrapping with monotone
  prefix search while preserving the original greedy line breaks and TeX fallback.

Validation: all 21 English and 21 Chinese narration-beat frame checks pass, as do
all 21 English silent playback checks, with zero automated warnings. Every receipt
matches the final source fingerprint and input signatures. Narration-beat contact
sheets and sampled playback frames were visually reviewed, with focused rechecks
of changed layouts and transitions. Fifteen focused numerical, envelope, martingale
and wrapping tests pass; six actual Chinese TeX layouts match the original greedy
wrapping oracle. Chinese narration covers 150/150 source lines; the narration
estimate is 63.6 minutes. All 23 sampled English lines (Hook, House and Research)
pass signal and alignment checks. The actual 163-second narrated opening matches
the final narration and has zero blank or sparse-screen intervals of at least 1.5s.

The [compact evidence record](quant4-polish-evidence.json) captures source and input
hashes, all scene receipts, review scope and current speech reports. Signal and
alignment checks do not certify pronunciation; technical speech warnings remain
listening leads. Full production-voice listening and synchronization remain pending.
Chinese coverage is narration-beat frame QA rather than whole-part narrated playback.

Local review artifacts (git-ignored): `renders/quant4_polished_silent.mp4`, an English
480p15 preview (76:51 including animation and pauses) with 21 embedded chapters
and English subtitles; its `.srt` and `.chapters.txt`; and
`media/quant4/narrated_qa/videos/s01_hook/480p15/Hook.mp4`, the narrated opening sample.
Part 5 is next in the sequential visual pass.

```bash
python -m videos.quant.quant4.compute
python tools/qa_series.py quant4 --cached-only --resume --timeout 1500
python tools/qa_series.py quant4 --lang zh --cached-only --resume --timeout 1800
python tools/qa_series.py quant4 --motion --cached-only --resume --timeout 1800
python -m pytest tests/test_quant4_betting_cs.py tests/test_quant4_firstpassage_display.py tests/test_quant_house.py -k 'quant4 or martingale_tools or envelope_seals or trial_counter' -q
python -m pytest tests/test_quant_house.py::test_martingale_part4_expansion -q
EXPLAINER_TTS=silent python -m pytest tests/test_plain_cjk_wrap.py -q
python tools/zh_lines.py quant4 --todo
python tools/lecture_length.py quant4 --floor 50
EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart python tools/qa_audio.py quant4 --only Hook House Research
```


## Part 5: Stochastic Calculus

Completed on `polish/quant5`, stacked on Part 4.

- Clarify the stopping hedge's mean shortfall and cash account; mark wealth between rebalances while preserving every cached rebalance value.
- Normalize density displays by the full Monte Carlo sample, including weighted Girsanov paths; preserve probability mass outside the visible range.
- State conditions for integration, martingale representation, measure changes, simulation orders and asymptotic variance intervals. Correct the time-midpoint limit, fractional-Brownian normalization and helix's initial-offset term.
- Treat monthly-average CIR fitting as transition pseudo-likelihood, thresholded returns as outliers, Hawkes p-values as nominal in-sample diagnostics and the neural SDE's 2020 split as research testing.
- Add a worked realized-variance interval, reveal quiz answers after questions, translate the revised English content and captions, and fix the local boxed pause helper.
- Clear the opening's strike/price labels, Chinese source credits and proof/table layouts; shorten sparse equation reveals and the three 3D reset transitions.

All 42 compute items were generated; corrected density displays were regenerated. All 63 current checks pass with zero automated warnings: 21 English narration-beat frame checks, 21 Chinese frame checks and 21 English silent playback renders. All 21 chapters were visually reviewed in each mode through contact sheets and sampled playback frames, with focused rechecks of changed text, plots and transitions. This is not a complete real-time viewing of both narrated productions.

Eight focused tests pass. Chinese source coverage is 122/122 and the narration estimate is 64.9 minutes. Eighteen CPU speech samples (Hook 5, Representation 4, Research 9) pass waveform and alignment checks. The actual narrated opening lasts 138.267 seconds, matches the current narration and has no blank or sparse-screen hold of at least 1.5 seconds. Full production-voice listening and synchronization remain pending; signal checks do not certify pronunciation.

The four registered computation function sources and the complete registration, seal and opening history match the Part 4 base. The cumulative Part 5 trial count remains 236; no additional trial or hold-out opening was introduced. The density window contains simulated mass 0.9945 versus analytic 0.994566, with L1 discrepancy about 0.038.

The [compact evidence record](quant5-polish-evidence.json) records source and input hashes, all 63 receipts, visual scope, current speech reports and the narrated opening. Local artifacts remain git-ignored: `renders/quant5_polished_silent.mp4` (76:13, 480p15, 21 embedded chapters, English subtitles, H.264/AAC/mov_text), its `.srt` and chapter list, and `media/quant5/narrated_qa/videos/s01_hook/480p15/Hook.mp4`. Part 6 is next in the sequential visual pass.

```bash
python -m videos.quant.quant5.compute
python tools/qa_series.py quant5 --cached-only --resume --timeout 1800
python tools/qa_series.py quant5 --lang zh --cached-only --resume --timeout 1800
python tools/qa_series.py quant5 --motion --cached-only --resume --timeout 1800
EXPLAINER_TTS=silent python -m pytest tests/test_quant5_density_display.py tests/test_quant5_marked_hedge.py tests/test_quant_house.py -k 'quant5 or simulation_library or neural_sde_generator or envelope_seals or trial_counter' -q
python tools/zh_lines.py quant5 --todo
python tools/lecture_length.py quant5 --floor 50
EXPLAINER_TTS=kokoro EXPLAINER_VOICE=af_heart python tools/qa_audio.py quant5 --only Hook Representation Research
```

## Part 6: Financial Econometrics

In progress directly on `quantitative-finance`. Preserve all seven legacy registered computations and record one retrospective inference correction separately. The corrected Shanken covariance avoids counting the factor variance twice; the GRS statistic uses consistent divisor-T covariances. Three independent checks cover the zero-premium limit, residual-variance inflation, and the single-asset identity with the squared intercept t-statistic. Together with the econometrics and protocol checks, seven focused tests pass. The cumulative Part 6 trial count is 296; all previous registrations, seals and openings are preserved, with no new hold-out opening.

The source and visuals are still being revised. The original 36 compute items and the corrective inference item are available; full bilingual frame, playback, speech and narrated QA remain pending.

The current checkpoint updates the opening, OLS, HAC, clustering, Fama–MacBeth and out-of-sample lessons in English and Chinese. The opening hides the sixth estimate until the prediction prompt. Dependence and identification assumptions are explicit, and the overlap example's factor-of-h variance result is restricted to its stated mean-estimation setting. The two-pass display uses the separately registered corrected inference item.

The out-of-sample illustration is labelled as a chronological refit on revised historical data. Its legacy CT column is omitted because the legacy implementation selected a sign using the full sample. The population excess-return investment formula is taught separately from the empirical real log total-return forecast scores, with a staged stylized example and quiz answer. Its 11 English endpoint frames passed with zero geometry warnings and were visually reviewed; this is a partial layout check, not completed Part 6 QA.

Checkpoint validation: seven focused tests pass; all 109 Chinese source entries are covered; the seven original registered compute functions and every prior experiment record are preserved. Remaining chapter corrections and the complete bilingual, motion and narrated checks are still pending. Continue committing and pushing directly to `quantitative-finance`; do not create another PR.

### Part 6 continuation: MLE confidence-region animation

The MLE sample-size demonstration now redraws the grey independent-score sandwich
region along with the gold and pink regions. All three divide covariance by the
same sample multiplier, use the same plotting window, and clear their redraw
updaters at the end. The question has a separate answer bookmark in both languages.
The caption distinguishes the original-sample SE readouts from the hypothetical
larger-sample regions. Narration states the stationary-process assumption behind
inverse-T scaling and the regularity/identification assumptions behind a
pseudo-true quasi-likelihood target; robust uncertainty does not establish model fit.

Validation: four tests pass (the three existing inference checks plus a regression
exercising the scene's actual Manim redraw constructors at 25 sample multipliers,
including 1, 2 and 4). The fixture uses synthetic positive-definite covariance
matrices and checks every curve control point relative to the unchanged estimate;
it is not production-data visual acceptance. Chinese narration coverage remains
109/109. No registered computation or experiment record changed.

**Current environment blocker:** this resumed workspace has no `.cache/quant6/`
payloads. English and Chinese `qa_series.py quant6 --only MLE --cached-only`
checks both report `missing-data: quant6/mle`, with zero frames evaluated. Previous
workspace caches, receipts and movies were not restored. No synthetic fixture was
substituted for a production cache, and no experiment was rerun. Restore the
original Part 6 computation inputs before completing bilingual layout, motion,
speech and narrated QA. Part 6 remains in progress; Part 7 has not started.

### Part 6 continuation: inputs restored and statistical teaching corrections

The public-data sources reproduced all 37 Part 6 cache items with their normal
checksum checks enabled. The tracked data manifest and experiment ledger are
unchanged, as is `compute.py`; no additional hold-out was opened. This resolves
the preceding workspace-input blocker. The executor's bundled TeX tools are
available after sourcing `/workspace/environment/activate.sh`.

This pass corrects full-sample histogram normalization and leaves out-of-window
observations outside the plot, including the research chapter's stored histogram.
It fixes the MLE trail's final endpoint and expands the scale axis to show the
complete baseline HAC ellipse. It distinguishes fixed circular bootstrap blocks
from geometric block lengths, negative treatment-effect weights from nonnegative
Bacon comparison weights, and conditional posterior bead positions from averaged
posterior estimates. The DML expansion includes the squared treatment-model error;
all higher-moment Sharpe variance terms divide by T. Likelihood, GMM, James–Stein,
placebo, multiple-testing and Sharpe interpretations now state their assumptions.
The associated Chinese narration, captions and lesson notes are updated.

Validation: 239 focused/House tests pass, including full-sample histogram mass and
actual MLE redraw geometry regressions. Chinese narration source coverage is
109/109. Initial bilingual Hook and English OLS/MLE selected-frame inspections
were completed; MLE's displayed clipping was found in that review and repaired.
The complete bilingual final-source frame and silent-motion passes are running;
this checkpoint does not claim full visual or production-voice acceptance.
