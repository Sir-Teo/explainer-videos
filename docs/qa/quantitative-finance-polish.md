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
| 6 | Visual pass complete; full production-voice listening pending |
| 7 | Visual pass complete; full production-voice listening pending |
| 8 | Visual pass complete; full production-voice listening pending |
| 9 | Visual pass complete; full production-voice listening pending |
| 10 | Visual pass complete; full production-voice listening pending |
| 11 | Visual pass complete; full production-voice listening pending |
| 12 | In progress: scientific, narration and visual QA |
| 13–43 | Pending; do not infer approval from historical build notes |

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

The completed visual passes for later parts are recorded below; the queue above
shows the current status.


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

### Part 6 continuation: visual and motion repairs

The current review has reached the later chapters. Actual selected-frame and
motion inspection found and repaired a HAC question covering the formula column,
a sparse roadmap reveal, empty camera-reset intervals, the Chinese event-study
statistic falling below the frame, an overflowing Chinese Bayesian error readout,
and an SNR prompt covering its axis label. The DML expansion is split into readable
score and remainder lines. DML axes now become residual axes as the cloud moves.
The RD and DML scatterplots and both confidence-region examples show their full
plotted values rather than moving observations onto the viewing-window edges.

The Euler Monte Carlo histogram now uses a fixed full-sample denominator while
samples appear, and its scale includes its actual 0.082 peak instead of capping it
at 0.04. Event-time paths use a range containing all 40 displayed paths; narration
distinguishes the final mean path from the sequential day-zero readout. DiD states
that its illustrated target averages cells with not-yet-treated controls. IVX and
the local-to-unity limit state their assumptions; the SNR discussion drops the
unsupported half-century precision claim. All computation sources and experiment
history remain unchanged.

Seven focused checks pass, including a new fixed-denominator partial-reveal
regression; the preceding 239-test House/inference run remains recorded above.
The actual English narrated opening is 191.53 seconds (480p15, Kokoro af_heart),
with five speech blocks, matching the captured opening narration. Its blank/sparse
scan finds no intervals of at least 1.5 seconds. Its 32-frame sheet was visually
reviewed. All five English and five Chinese opening speech samples pass waveform
and alignment checks; all four English MLE speech samples pass too. Those checks
do not certify pronunciation or continuous listening.

Bilingual frame and English motion acceptance remain in progress. Some interim
translation warnings arose when a worker imported source before an edit and then
checked translations after that edit; those receipts are not accepted as final.
The final source-fingerprint/input gate must be satisfied after the repairs finish.

The out-of-sample population gain example holds **risk aversion** fixed, rather
than holding portfolio volatility fixed. Its formula follows from weights
`mu/(gamma*sigma^2)` and `(mu+x)/(gamma*sigma_epsilon^2)`. In the shown stylized
case the expected-return gain is 10.1101%, while expected conditional variance
also increases by that proportion. The English/Chinese narration and caption
now make this distinction. This is a closed-form teaching check, with no new
market experiment, strategy registration or hold-out access.

The DML lesson now explicitly conditions a causal interpretation on no unobserved
confounding and a valid partially linear model. Cross-fitting supplies neither
assumption. Its displayed expansion separates the second-order bias remainder
from other `o_p(1)` terms, while retaining the corrected treatment-error-squared
term and the faster-than-quarter-rate condition. This change requires fresh
bilingual frame and narration captures before final acceptance.

### Part 6 continuation: research chapter and exercises

All 21 English chapters now have an initial render. The research chapter exposed
21 missing Chinese text entries, a derivation footer below the frame, and an
empty narrated opening to its question cards. Its initial repaired English pass
has 17 selected states and zero warnings. The derivation now retains three rows,
the density scale includes the simulated peaks, and the larger question cards
and centered final prompt have dedicated space. Multivariate inference is framed
as requiring additional conditions, rather than claiming no joint theory exists.
The revised Chinese chapter and final-source regressions are still running.

The exercises now provide the covariance ratio needed for the numerical
Stambaugh calculation, state independence and expected risk for James–Stein, and
use within-month sums of squares for the possibly unbalanced panel. The arithmetic
in the notes uses `1 + 3*0.91 = 3.73`. The remaining recap and qualifying-exercise
captions are translated. Negative DiD weights receive a color flash without
changing their magnitudes; the last sparse Euler reveal is shortened. Its GMM
p-value is labelled nominal/asymptotic. Bootstrap coverage is reported as the
observed result rather than assigning all residual undercoverage to block length.

Audio QA now records the actual language-dependent voice. Mandarin Kokoro uses
`zf_001`; its within-sentence character times are estimated, and passing their
monotonicity checks does not establish word-level forced alignment or listening
approval. The earlier signal-check scope remains unchanged.

### Part 6 continuation: final motion and display audit

The complete first motion pass exposed a two-second near-empty first-row reveal
in the research chapter; the refreshed OLS motion exposed the same issue after
its camera reset. Their first equations now write in 0.4 seconds, and the research
transition is shorter. The review then checked the remaining display clamps
against the actual cached observations, rather than accepting plausible-looking
endpoints.

The OLS/FWL pane now includes every raw and residual point, and its axis labels
change when the observations become residuals. The Stambaugh pane includes all
900 displayed draws at every shown sample length and states that its centre uses
all 4,000 draws. Fama--MacBeth's moving cross-section omits observations outside
its stated plot window and intersects the actual fitted line with that window;
it no longer moves points or line endpoints onto the borders. Its three-cloud
decomposition pane includes the complete clouds and month means.

The IV histograms had density peaks as high as 12.15 capped at 6; their shared
scale now extends to 13 and preserves the full peaks. The bootstrap histogram's
reveal uses the final sample size as its denominator, includes the negative
draws, and has room for the final 4.15 peak. The out-of-sample slope band includes
its full interval, and the DML nuisance-error pane includes its 4.614 maximum.
These are display changes to existing cached results. The computations, data
manifest, registrations, sealed envelope and track record remain unchanged.

The deterministic bounds audit is saved in
`renders/qa/quant6/display_audit.json`. All 109 narration entries remain covered
in Chinese, and the final narration estimate is 63.1 minutes. Seven additional
English research speech samples pass waveform/token-time checks. The refreshed
bilingual and motion receipt gates are still running at this checkpoint.

### Part 6: completed visual pass

All 21 English and 21 Chinese narration-beat checks and all 21 English silent
motion checks pass against source fingerprint
`5722809185048e1f436d9ec506a54749ab517aa4d42f972f59dac9b266a18658`,
with current input signatures and zero automated warnings. Every chapter's
bilingual contact sheets and all 21 forty-frame playback sheets were visually
reviewed. Changed sheets were rechecked, including the final unit-root reveal;
all silent clips have zero blank/sparse holds of at least 1.5 seconds.

The [compact evidence record](quant6-polish-evidence.json) records the 63 receipt
hashes, computed-input hashes, test logs, protocol checks and audio sample scope.
All 37 compute items were restored normally from checksum-verified public inputs.
The 239-test House/inference run and subsequent seven focused display/inference
checks pass. All 109 narration source entries have Chinese coverage, and the
speech estimate is 63.1 minutes. The computation file, data manifest, envelope
and track record are unchanged from the Part 6 checkpoint; the cumulative trial
count remains 296, with no additional trial or hold-out opening in this pass.

All 16 English speech samples (Hook, MLE and Research) and five Mandarin opening
samples pass waveform/token-time checks using the current narration. The actual
English narrated opening is 191.53 seconds and has no blank/sparse hold of at
least 1.5 seconds; its 32-frame sheet was reviewed. Mandarin uses Kokoro `zf_001`
with estimated character times. These checks do not certify pronunciation or
continuous listening. Full production-voice listening and synchronization remain
pending, as for the preceding completed visual passes.

Local review artifacts (git-ignored):

- `renders/quant6_polished_silent.mp4`: English 480p15 preview, approximately
  71.7 minutes, with 21 embedded chapters and English subtitles; `.srt` and
  `.chapters.txt` files sit alongside it.
- `media/quant6/narrated_qa/videos/s01_hook/480p15/Hook.mp4`: actual narrated
  English opening.
- `renders/qa/series/quant6/{en,zh}/`: chapter receipts, images, text captures,
  speech reports and English silent clips.


## Part 7: Time Series and Volatility — completed visual pass

The scientific pass aligns the English explanation, Chinese narration, captions,
and worked solutions. The Dickey–Fuller derivation now includes the fitted
constant used by its simulation. Wold, Ljung–Box, GARCH stationarity, stochastic
volatility, realized-variance limits, QLIKE and forecast-comparison results state
the assumptions needed for their conclusions. DCC's multistep expectation keeps
the normalized correlation matrix inside the recursion; its persistence half-life
is identified as a linearized summary.

The evaluation chapters distinguish the neural training and validation dates from
the classical fit dates, label the 2020 comparison as retrospective, and explain
fixed seed averaging and later entrants. The foundation example is identified as
a token-embedding MLP illustration. The quoted foundation-model comparison was
checked against Brini's Table 6, and HARNet authorship against the DOI metadata.
The nested-forecast chapter includes a worked DM/CW calculation and explains why
its adjusted standard error must normally be estimated separately.

The visual pass restores Kalman density curves in the correct data coordinates,
expands ranges to include the observed crisis values and coefficient paths, uses
one probability scale throughout the foundation replay, and removes contaminated
histogram edge bins. Chinese question cards fit their side panels. House API rows
remain readable. The opening objectives, first ADF equation, first smoother row, and forecast-comparison opening
appear promptly; fresh playback scans and the narrated opening have no blank
or sparse holds of 1.5 seconds or longer.

All 30 existing compute items were restored from the public data without changing
`quant7/compute.py`, the data manifest, trial registry, or track record. The
as-of-Part-7 counter is 307. This pass added no market trials and opened no sealed
holdout. The raw global registry count is not used as this part's trial count.

Validation: all 63 receipts are current with matching input signatures and zero
automated warnings: 21 English narration-beat checks, 21 Chinese checks, and 21
English silent playback checks. All endpoint sheets and all 40-frame playback
sheets were visually reviewed, including the refreshed repaired scenes. The House
and inference checks passed 236 tests; seven expected dependency/mock-data
warnings are recorded separately from visual QA. Chinese narration coverage is
156/156 source lines, and the narration estimate is 57.2 minutes.

Actual Kokoro samples cover Hook, Garch and Research in English and Hook in
Chinese: 29 lines pass waveform and token-time checks. These checks do not certify
pronunciation or continuous listening; Mandarin within-sentence character times
remain estimates. Full production-voice listening remains pending.

The [compact evidence record](quant7-polish-evidence.json) retains source/input
hashes, all 63 receipts, manual-review hashes, paper checks, tests, speech reports,
and preview hashes. Local git-ignored artifacts are:

- `renders/quant7_polished_silent.mp4`: 69:23, 480p15, 21 embedded chapters
  and English soft subtitles, plus its `.srt` and chapter list.
- `media/quant7/narrated_qa/videos/s01_hook/480p15/Hook.mp4`: the actual English
  opening, 199.9 seconds, with its current narration
  capture and a clean dead-air scan.

Part 8 is next in the sequential pass.


## Part 8: Decisions and Control — completed visual pass

The English explanation, Chinese narration, captions and notes now distinguish
exact results, numerical approximations, simulated scores and retrospective
historical illustrations. The coin's exact log growth at a 40% stake is negative;
the capped finite-horizon game has a different objective from long-run log growth.
Kelly dominance is stated for distinct fixed fractions with a strict growth gap.
Utility, dynamic programming, verification, viscosity convergence, martingale
pricing, stopping and secretary results include their required assumptions. The
perpetual-put smooth-fit slope comparison and discounted variational inequality
are corrected. The finite-horizon monthly cost solver is distinguished from the
continuous singular-control theory and its small-cost asymptotic formula.

PPO's displayed reward includes the simulator's gross-return floor. Its policy
gradient separates the true advantage from the learned TD estimate, and clipping
is identified as a surrogate objective. The cached shortfall is labelled as a
continuous-growth proxy at the mean action, rather than a full policy evaluation.
The five restored seeds are all retained; runtime-dependent results are reported
from that restoration. The funding example is a ratio call spread. The mean-field
iteration is identified as a damped best-response fixed point.

The research chapter distinguishes expected CE across estimation samples from
unconditional expected utility, an analytic known-variance oracle from estimated-
variance simulations, and a negative CE score from an expected monetary loss.
It includes the worked shrinkage answer. Volatility targeting discloses its
full-sample normalization and ordinary OLS reference errors. The drawdown formula
was checked against the primary mathematical source; its nominal weekly
illustration is distinguished from the continuous discounted-wealth theorem.
Unverified fund return figures were removed and book claims remain attributed.

The visual pass expands chart ranges, removes artificial boundary plateaus,
discloses omitted points and histogram edge bins, uses common histogram scales,
and repairs Chinese cost panels. House rows show callable APIs at readable sizes;
the sizing pipeline is explicitly a combination of separate illustrative rules.
Timeline labels, the historical growth curve and first derivation rows appear
promptly during narration.

All 46 existing compute items were restored normally. The compute source, data
manifest, trial registry and track record are unchanged from the Part 7 completion
commit. The as-of-Part-8 counter is 310; this pass added no market trials and
opened no sealed holdout. Twelve existing control tests pass, with one recorded
dependency deprecation warning.

Validation: all 66 receipts match the final source and input signatures and have
zero automated warnings: 22 English narration-beat checks, 22 Chinese checks and
22 English silent playback checks. All endpoint sheets and all 40-frame playback
sheets were visually reviewed. Chinese narration covers 125/125 source lines;
the narration estimate is 65.6 minutes. Actual Kokoro samples cover Hook,
Samuelson and Research in English and Hook in Chinese: 28 lines pass waveform
and token-time checks. Those checks do not certify pronunciation or continuous
listening; Mandarin character times remain estimates. Full production-voice
listening and synchronization remain pending.

The [compact evidence record](quant8-polish-evidence.json) retains the source,
input and review hashes, 66 receipts, analytical and primary-source checks, tests,
speech reports and preview hashes. Local git-ignored artifacts are:

- `renders/quant8_polished_silent.mp4`: 74:37, 480p15,
  22 embedded chapters and English soft subtitles, plus its subtitle and chapter files.
- `media/quant8/narrated_qa/videos/s01_hook/480p15/Hook.mp4`: the actual English
  opening, 247.3 seconds, matching the current narration
  capture and with its recorded dead-air scan.

Part 9’s completed visual pass is recorded below.


## Part 9: No Arbitrage — completed visual pass

Repeated introductions and explanations were shortened bilingually to meet the
lecture length target. The English explanation, Mandarin narration and captions now state the assumptions
behind pricing, replication and numerical bounds. The boundary state-price vector
is (0, 0, 1); a weak separating plane at an endpoint does not rule out arbitrage.
Incomplete-market extensions are explicitly selected, and closed hedge limits are
distinguished from prices under strictly positive measures. Continuous-time claims
distinguish local martingales, supermartingales and true pricing expectations.

The Bitcoin example separates its $8,597 undiscounted forward value from its
approximately $8,479 spot-dollar present value under the stated discount choices.
The density reconstruction discloses its interpolation and extrapolation model,
weighted RMSE, endpoint requirements and invalid positive-part spline diagnostic.
The historical density ratio is an illustration with limited identification.

Martingale transport uses normalized finite marginals. Finite LP certificates,
interpolated hedge violations, non-nested grid sensitivity and raw entropic
iterates are distinguished. The square-payoff hedge includes its dynamic term.
All three neural seeds and their optimizer overshoots are retained; raw costs and
weighted mean shortfalls do not certify a bound. Method attribution and the
referenced papers’ publication status were checked against primary sources.

The fractional-price chapter distinguishes a log-increment score from
self-financing wealth, an iid risk reference from a theorem, and retrospective
signal direction from prospective evidence. Its final worked answer is visible.
The doubling example discloses its finite clock, unhit paths, schematic barrier
endpoints and omitted display tails. Chart ranges, camera cleanup, opening rows,
Chinese panels and callable API labels were repaired and visually checked.

All 28 existing compute items were restored normally. The compute source, pricing
algorithms, data manifest, trial registry and track record are unchanged from the
Part 8 completion commit; one neural-result docstring was corrected. Nine existing
tests pass, with one dependency deprecation warning. The counter remains 310;
this pass added no market trials and opened no sealed holdout.

Validation: all 63 receipts match the final source and input signatures, with zero
automated warnings: 21 English endpoint checks, 21 Mandarin checks and 21 English
silent playback checks. All endpoint sheets and all forty-frame motion sheets
were visually reviewed. Chinese coverage is 143/143 source lines and spliced
sentences. The source narration estimate is 64.4 minutes at the calibrated 168 words per minute.
The silent backend allocates 73.0 minutes to its speech timing; its preview includes
additional animation and pauses.

Actual Kokoro samples cover Hook, Continuous and Research in English and Hook in
Mandarin: 30 lines pass signal and token-time checks. Technical-line word-count
warnings remain a listening lead. These checks do not certify pronunciation;
Mandarin character times are estimates. Full production-voice listening and
synchronization remain pending.

The [compact evidence record](quant9-polish-evidence.json) retains the final source,
input and review hashes, receipts, derivation checks, primary-source checks, tests
and speech reports. Local git-ignored review artifacts are:

- `renders/quant9_polished_silent.mp4`: 76:07, 480p15, with 21 embedded chapters,
  English soft subtitles and companion subtitle and chapter files.
- `media/quant9/narrated_qa/videos/s01_hook/480p15/Hook.mp4`: the actual English
  opening, 107.4 seconds, matching the final narration
  and accompanied by its reviewed contact sheet and dead-air scan.

Part 10’s completed visual pass is recorded below.


## Part 10: Black–Scholes–Merton — completed visual pass

The derivation, examples, Mandarin narration and captions now distinguish model
assumptions from empirical observations. The Bitcoin experiment is a hypothetical
dollar call priced with a DVOL proxy, with retrospective window selection,
overlapping windows and timing limitations. The plots align forward realized
volatility to the window start. Their bootstrap envelope is pointwise, and the
ordinary standard errors do not establish independence or executable returns.

The hedge argument uses self-financing gains, rather than the differential of an
option-minus-stock position without its cash account. Robust hedging states its
continuous-diffusion, volatility-bound and admissibility assumptions. Discrete
errors are leading martingale differences; the jump expression separates the exact
nonlinear remainder from its quadratic approximation. The dashed jump-risk proxy
is not a proved variance floor for the simulated Merton model. Tree consistency,
heat-kernel display scaling, cost conventions and American-exercise assumptions
are explicit.

Quote inversion uses a Surface IV reconstructed from a mark price and then
repriced: numerical round-trip precision is distinct from market accuracy. Coin
premiums, forward Black values, spot-dollar present values and discount conventions
are separated. The Surface score is weighted RMSE and its calendar check is sampled.
All recorded solver and neural overshoots remain visible; invalid Newton display
points and diagnostic sentinels are disclosed. The neural replay retains five seeds
and is a teaching example, with no claimed replication or runtime benchmark of the
2026 preprints. Primary-source checks support the attributed paper and industry
claims.

Histograms preserve their full recorded ranges and use common count scales. The
3D comparison bars stay fixed in screen space, and the dense lattice settles into
a steady view after a short orbit. Comparison axes and baseline table rows appear
during their explanations, with references separated from long labels. The 1987
replay matches pre-return states, stock weights and the October-end date to cached
observations, and holds its event states at the corresponding narration cues. The
research chapter states its asymptotic conditions, discloses hindsight volatility
and pooled band tuning, and shows the worked answer after its pause. Missing
Mandarin captions and a decimal-template ambiguity are repaired.

All 26 compute items were restored normally. The compute source, pricing algorithms,
data manifest, trial registry and track record are unchanged from the Part 9
completion commit. Thirteen existing tests pass, with one dependency deprecation
warning. The as-of-Part-10 counter remains 310; this pass added no market trials and opened no
sealed holdout.

Validation: all 66 receipts match the final source and input signatures, with zero
automated warnings: 22 English endpoint checks, 22 Mandarin checks and 22 English
silent playback checks. All endpoint sheets and all forty-frame motion sheets were
visually reviewed, with native-frame checks of repaired formulas and transitions.
Chinese coverage is 131/131 source lines and spliced sentences. The narration
estimate is 61.3 minutes.

Actual Kokoro samples cover Hook, WrongVol, Research and Frontier in English and
Hook and Frontier in Mandarin: 33 lines pass signal and token-time checks.
Technical-line warnings remain a listening lead. These checks do not certify
pronunciation; Mandarin character times are estimates. Full production-voice
listening and synchronization remain pending.

The [compact evidence record](quant10-polish-evidence.json) retains source, input
and review hashes, receipts, derivation and primary-source checks, tests and speech
reports. Local git-ignored review artifacts are:

- `renders/quant10_polished_silent.mp4`: 70:56, 480p15, with 22 embedded chapters,
  English soft subtitles and companion subtitle and chapter files.
- `media/quant10/narrated_qa/videos/s01_hook/480p15/Hook.mp4`: the actual English
  opening, 146.7 seconds, matching the final narration,
  with its reviewed contact sheet and dead-air scan.

Part 11’s completed visual pass is recorded below.


## Part 11: Trading Options — completed visual pass

The examples distinguish hypothetical model P&L, observational option marks and
executable trades. The HAR forecast includes later entry-day variance; the weekly
Surface reconstructs IV from marks pooled through noon. Neither example establishes
an implementable forecasting edge. Disjoint windows need not be independent, and
existing code registrations do not establish registration before calculation.
All 66 out-of-sample predictions and all five bootstrap refits remain visible;
the refit range is descriptive. Kelly's quadratic uses the second moment, while
the overlapping-sample bankruptcy wall does not bound unseen losses.

Short-dated ticket returns treat each trade record as one unit, ignoring reported
amount. Their hypothetical buyer returns are distinct from the sellers’ own P&L.
Greek derivations state their model and finite-step assumptions. The 25-delta call
and put signs, local RR/BF interpretation, continuous log-contract weights,
American cash-dividend exercise tie and same-expiry put-spread liability bound are
corrected or qualified. Markouts use signed dollar-converted values, with changing
horizon cohorts; their change does not identify informed traders. The fixed
24-client Glosten–Milgrom replay ends at belief 0.5, with quotes recomputed at
0.35/0.65. Full recorded inventory, hedge-loss and pinning ranges are retained.
Fixed-rule versus learner evaluation cohorts are explicit, and only kappa=1 has
three replay seeds. Synthetic Black–Scholes hedge marks on Heston paths are
identified as such.

The research derivation fixes a martingale measure and hedge before the
mean-variance approximation. Its finite empirical exponential tilt is distinct
from optimizing hedge strategies or proving a population exponential moment.
A worked answer compares dollar and IV cross-impact. Initial research cards,
baseline curves and near-money table rows appear during their explanations.
Camera orbits settle after at most eight seconds, and duplicate post-camera
fade-outs are removed. Two small formula reveals reach their explanatory notes
sooner; the gamma surface labels its scale and display cap. Missing Mandarin captions and
narration are repaired. Regulatory histories distinguish allegations, judgments,
market-value losses and principal losses; OCC totals include futures and COR3M
pre-launch history is backcast.

All 29 original compute items are cached. Two descriptive caches initially enumerated partial raw-date folders while dependency
restoration was incomplete. Flow and short-dated-option caches were quarantined
and restored normally from the unchanged 100 frozen dates, with both repairs
recorded separately. The full flow sample contains 524,281 trades. No force or data-refresh option was used. Compute and
pricing sources, the manifest, trial registry and track record remain unchanged
from the Part 10 completion commit. Twelve existing tests pass. The as-of-Part-11
counter remains 312 (chapter 7: 311); the global registry remains 23,562. This pass
added no market trials and opened no sealed holdout.

Validation: 63 current receipts, all with zero automated warnings: 21 English
endpoint checks, 21 Mandarin checks and 21 English silent playback checks.
Every endpoint sheet and forty-frame motion sheet was visually inspected, with
review hashes bound to the final artifacts. Chinese coverage is
145/145 source lines and spliced sentences; the source narration estimate is
64.9 minutes. Actual Kokoro
samples cover Hook, MarketMaker, Research, Frontier and India in English and Hook,
Frontier and India in Mandarin: 46 lines pass signal and token-time checks. These checks
do not certify pronunciation; full production-voice listening and synchronization
remain pending.

The [compact evidence record](quant11-polish-evidence.json) retains source, input,
receipt and manual-review hashes, source checks, cache repair, tests and speech
reports. Local git-ignored review artifacts are:

- `renders/quant11_polished_silent.mp4`: 76:59, 480p15, with 21 embedded chapters,
  English soft subtitles and companion subtitle and chapter files.
- `media/quant11/narrated_qa/videos/s01_hook/480p15/Hook.mp4`: the actual English
  opening, 190.9 seconds, with its reviewed contact
  sheet and dead-air scan.

Part 12 is next in the sequential pass.
