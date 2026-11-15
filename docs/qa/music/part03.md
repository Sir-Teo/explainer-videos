# Part 3 — The Spectrum

Review date: 15 November 2026. Base: `22f8a08a`. This is source and sampled-preview QA.
Final narrated production is not approved by this record.

## Changes

- Show all 59 harmonic positions needed for thirty odd tones in the opening spectrum. Replace the single
  breathing triangular string with an ideal modal evolution, and disclose slow motion and exaggerated motion.
- State the steady-state linear/time-invariant assumption for the resonator demonstration. Scope sine-only
  projection to the odd, zero-mean square; general periodic waves also need cosines/phases and possibly DC.
  Bring the first projection diagram in earlier, before the multiplication reveal.
- Scope the click's flat spectrum to an ideal infinitely short impulse. Align DFT and leakage stems to their
  integer frequency bins. Present the 0.15-second worked example as a bin-spacing criterion, with actual
  resolution depending on the window, relative levels and noise.
- Describe the clarinet exercise as an ideal stopped-pipe approximation. Distinguish full complex spectra from
  magnitude spectra, and qualify phase insensitivity to resolved steady partials; onsets can also matter.
- Label the displayed waveform envelope accurately and disclose that the drawn STFT window is widened.
- Use cosines for the leakage illustration so its 5.5-cycle endpoint jump actually exists. Keep window response
  curves within their plotting bounds and fit the window comparison's labels inside the frame.
- Define Gabor's uncertainties as normalized Fourier energy standard deviations. Remove the universal claim
  that no measurement can distinguish nearby frequencies sooner than 1/delta-f. State the estimator/window
  distinction consistently in the frontier and recap. Qualify finite sharp-edge bandwidths as sampled estimates;
  ideal abrupt edges have divergent rms bandwidth.
- Correct the 5-to-120-ms quiz duration ratio to twenty-four. Give the two-window comparison common axis
  directions, fit all four burst panels, and scope the drum/organ examples without denying their pitch/onset.
- Correct Q as frequency divided by bin width, rather than the reciprocal. Qualify the uses of constant-Q and
  related wavelet representations, and fit the concluding captions to the frame.
- Replace unrelated random noise traces with samples from the actual clip at the playhead's time. Distinguish
  per-hertz density slopes from integrated octave-band power. Use the clip's sample rate explicitly.
- Keep the reversal example's sound origin clear: it is computed, not a recording. Align the notes and recap
  with the corrected scientific scope.

## Verification and local evidence

All fourteen numerical items were generated. `compute.py` and numerical sound payloads are unchanged.
The lab ran (`python -m videos.music.labs 3`).

- `python -m pytest -q tests/music/test_music3.py tests/music/test_fourier.py tests/music/test_audio.py`:
  **30 passed**, one `audioop` deprecation warning. Log: `/workspace/scratch/music3-final-tests.log`.
- All thirteen chapters rendered as silent-narration 480p15 previews, with 48-sample sheets under
  `renders/qa/music3/`. Chapters were visually sampled in sequence, followed by rerenders and checks of
  repaired sections. Nine additional target frames were inspected in `/workspace/scratch/music3-targets.png`.
  The first noise render caught a missing sample-rate symbol in the new trace path; the corrected `c.sr`
  path rendered successfully. This is sampled visual review, not continuous human playback.
- Native 1920×1080 stills of the uncertainty law and window comparison were rendered and inspected in
  `/workspace/scratch/music3-native/images/music3_native/`. They establish those static layouts only.
- Source-based narrated estimate: 33.8 minutes including 1.8 minutes of listening, not final runtime.

- `python tools/qa_sound.py music3`: **13 scenes, zero failures**; log:
  `/workspace/scratch/music3-final-sound.log`.
- `tools/dead_air.py`, with the same chapter-local cue adapter used for Parts 1–2: **13 scenes,
  15 listening windows, zero failures** at 4 fps. No blank/sparse runs ≥1.5 seconds or still-listening runs
  ≥2.5 seconds were reported. Logs: `renders/qa/music3/<Scene>_dead_air.log`; adapter and results:
  `/workspace/scratch/music3_check_previews.py`, `music3-motion-results.json`.

Source/movie/cue hashes and measured durations are in `renders/qa/music3/source-receipt.json`.
The silent-narration previews total 41.65 minutes; this is not a final narrated runtime.

## Production gates still open

Regenerate changed narration, check pronunciation and continuous listening/playback, measure
final sound/picture alignment, and verify whole-episode native motion, joins and mastering. No publication.
